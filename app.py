import os
import io
import uuid
from datetime import datetime
from PIL import Image
from tensorflow import keras
import tensorflow as tf
import numpy as np
from flask import Flask, render_template, request, jsonify, url_for
import requests
from groq import Groq

# Suppress TensorFlow warnings
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Initialize Flask app
app = Flask(__name__)

# ── Firebase Setup (Firestore only - free Spark plan) ──
firebase_db = None
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    firebase_cred = credentials.Certificate('firebase-service-account.json')
    firebase_admin.initialize_app(firebase_cred)
    firebase_db = firestore.client()
    print("Firebase Firestore initialized successfully")
except ImportError as ie:
    print(f"Firebase import error: {ie}")
    print("Firebase Firestore will be disabled. App will continue without it.")
except Exception as e:
    print(f"Firebase init error: {e}")
    print("Firebase Firestore will be disabled.")
    firebase_db = None

def save_image_and_log(image_bytes, animal_type, prediction, confidence, filename):
    """Save image locally in classified folders and log metadata to Firestore"""
    try:
        # Generate unique filename
        ext = os.path.splitext(filename)[1] if '.' in filename else '.jpg'
        unique_name = f"{uuid.uuid4().hex}{ext}"

        # Local path: uploads/cow/healthy/image.jpg
        save_dir = os.path.join('uploads', animal_type, prediction)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, unique_name)

        with open(save_path, 'wb') as f:
            f.write(image_bytes)

        print(f"Image saved locally: {save_path}")

        # Log metadata and counts to Firestore (free tier)
        if firebase_db is not None:
            firebase_db.collection('image_uploads').add({
                'animal_type': animal_type,
                'prediction': prediction,
                'confidence': confidence,
                'filename': unique_name,
                'local_path': save_path,
                'timestamp': datetime.now()
            })

            # Update counts: image_counts/{animal_type}
            count_ref = firebase_db.collection('image_counts').document(animal_type)
            count_doc = count_ref.get()
            if count_doc.exists:
                counts = count_doc.to_dict()
                counts[prediction] = counts.get(prediction, 0) + 1
                counts['total'] = counts.get('total', 0) + 1
                count_ref.update(counts)
            else:
                count_ref.set({prediction: 1, 'total': 1})

            print(f"Metadata logged to Firestore")

        return save_path
    except Exception as e:
        print(f"Save/log error: {e}")
        return None

# Global variables for models
cow_model = None
dog_model = None

def load_models():
    global cow_model, dog_model
    try:
        # Custom objects to handle compatibility
        custom_objects = {
            'DepthwiseConv2D': keras.layers.DepthwiseConv2D
        }
        
        # Load models with custom objects
        cow_model = keras.models.load_model(
            'models/trained/cow_model.h5',
            custom_objects=custom_objects,
            compile=False
        )
        dog_model = keras.models.load_model(
            'models/trained/dog_model.h5',
            custom_objects=custom_objects,
            compile=False
        )
        
        # Compile models with basic settings
        for model in [cow_model, dog_model]:
            if model is not None:
                model.compile(
                    optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy']
                )
        
        print("Models loaded successfully")
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        raise

# Load models when starting the app
load_models()

def preprocess_image(image_bytes):
    try:
        # Convert bytes to image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image
        img = img.resize((224, 224), Image.Resampling.LANCZOS)
        
        # Convert to array
        img_array = np.array(img)
        
        # Normalize pixel values
        img_array = img_array.astype(np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, 0)
        
        # Debug print
        print(f"Processed image shape: {img_array.shape}")
        print(f"Image data range: [{img_array.min()}, {img_array.max()}]")
        
        return img_array
        
    except Exception as e:
        print(f"Error in preprocess_image: {str(e)}")
        print(f"Image bytes length: {len(image_bytes)}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cow_detection')
def cow_detection():
    return render_template('cow_detection.html')

@app.route('/dog_detection')
def dog_detection():
    return render_template('dog_detection.html')

@app.route('/vet_appointment')
def vet_appointment():
    return render_template('vet_appointment.html')

@app.route('/health_analytics')
def health_analytics():
    return render_template('health_analytics.html')

@app.route('/insurance')
def insurance():
    return render_template('insurance.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'})
    
    files = request.files.getlist('files')
    animal_type = request.args.get('animal_type')
    
    if not files or len(files) == 0:
        return jsonify({'error': 'No files selected'})
    
    if len(files) > 5:
        return jsonify({'error': 'Maximum 5 images allowed'})
    
    try:
        all_predictions = []
        
        # Process each image
        for file in files:
            if file.filename == '':
                continue
                
            img_bytes = file.read()
            img_array = preprocess_image(img_bytes)
            
            if img_array is None:
                continue
            
            # Make prediction
            if animal_type == 'cow':
                prediction = cow_model.predict(img_array, verbose=0)
                classes = ['healthy', 'lsd']
            else:  # dog
                prediction = dog_model.predict(img_array, verbose=0)
                classes = ['fungal_infection', 'healthy', 'hypersensitivity_allergy']
            
            pred_class = classes[np.argmax(prediction)]
            confidence = float(np.max(prediction))

            # Save image locally + log metadata to Firestore
            saved_path = save_image_and_log(
                img_bytes, animal_type, pred_class, confidence, file.filename
            )
            
            all_predictions.append({
                'prediction': pred_class,
                'confidence': confidence
            })
        
        if not all_predictions:
            return jsonify({'error': 'Could not process any images'})
        
        # Calculate combined result
        combined_result = calculate_combined_result(all_predictions, animal_type)
        
        return jsonify(combined_result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Error processing images: {str(e)}'})

def calculate_combined_result(predictions, animal_type):
    """Combine results from multiple images"""
    if animal_type == 'cow':
        classes = ['healthy', 'lsd']
    else:
        classes = ['fungal_infection', 'healthy', 'hypersensitivity_allergy']
    
    # Count occurrences of each class
    class_counts = {cls: 0 for cls in classes}
    total_confidence = {cls: 0 for cls in classes}
    
    for pred in predictions:
        class_counts[pred['prediction']] += 1
        total_confidence[pred['prediction']] += pred['confidence']
    
    # Find the most common prediction
    most_common = max(class_counts, key=class_counts.get)
    avg_confidence = total_confidence[most_common] / class_counts[most_common]
    
    return {
        'prediction': most_common,
        'confidence': avg_confidence,
        'total_images': len(predictions),
        'details': predictions,
        'votes': class_counts
    }

@app.route('/chat', methods=['POST'])
def chat():
    """Handle AI chat requests with conversation context."""
    try:
        data = request.get_json(silent=True) or {}
        user_message = (data.get('message') or '').strip()
        history = data.get('history', [])

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Keep only valid role/content pairs from recent history.
        safe_history = []
        if isinstance(history, list):
            for item in history[-12:]:
                if not isinstance(item, dict):
                    continue
                role = item.get('role')
                content = (item.get('content') or '').strip()
                if role in ('user', 'assistant') and content:
                    safe_history.append({'role': role, 'content': content})

        system_prompt = (
            "You are FARM&CO veterinary AI assistant. "
            "Answer any user question helpfully, clearly, and concisely. "
            "For animal-health questions, provide practical guidance for cows and dogs, "
            "note uncertainty when needed, and advise contacting a licensed veterinarian for emergencies."
        )

        llm_messages = [{'role': 'system', 'content': system_prompt}] + safe_history + [
            {'role': 'user', 'content': user_message}
        ]

        print(f"Received chat message: {user_message[:80]}...")

        # Provider 1: Groq (OpenAI-compatible chat completions)
        try:
            groq_api_key = os.getenv('GROQ_API_KEY', '')
            if groq_api_key:
                client = Groq(api_key=groq_api_key)

                chat_completion = client.chat.completions.create(
                    messages=llm_messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=500,
                )

                ai_response = chat_completion.choices[0].message.content
                print("Chat response served by Groq")
                return jsonify({'response': ai_response})
        except Exception as e:
            print(f"Groq API error: {str(e)}")

        # Provider 2: Gemini REST API fallback
        try:
            gemini_api_key = os.getenv('GEMINI_API_KEY', '')
            if gemini_api_key:
                gemini_model = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}"
                    f":generateContent?key={gemini_api_key}"
                )

                # Gemini expects role values: "user" or "model"
                gemini_contents = []
                for msg in llm_messages:
                    if msg['role'] == 'system':
                        continue
                    gemini_contents.append({
                        'role': 'user' if msg['role'] == 'user' else 'model',
                        'parts': [{'text': msg['content']}]
                    })

                payload = {
                    'system_instruction': {
                        'parts': [{'text': system_prompt}]
                    },
                    'contents': gemini_contents,
                    'generationConfig': {
                        'temperature': 0.7,
                        'maxOutputTokens': 500
                    }
                }

                api_response = requests.post(url, json=payload, timeout=30)
                if api_response.ok:
                    response_json = api_response.json()
                    candidates = response_json.get('candidates', [])
                    if candidates:
                        parts = candidates[0].get('content', {}).get('parts', [])
                        ai_response = '\n'.join(
                            p.get('text', '') for p in parts if p.get('text')
                        ).strip()
                        if ai_response:
                            print("Chat response served by Gemini")
                            return jsonify({'response': ai_response})
                else:
                    print(f"Gemini API error: {api_response.status_code} {api_response.text[:200]}")
        except Exception as e:
            print(f"Gemini API error: {str(e)}")

        return jsonify({
            'response': (
                "AI chat is currently unavailable. Please configure `GROQ_API_KEY` or `GEMINI_API_KEY` "
                "in your environment and try again."
            )
        })
            
    except Exception as e:
        print(f"Chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'response': 'I ran into a temporary chat error. Please try again in a moment.'}), 200

@app.route('/test-gemini')
def test_gemini():
    """Test Gemini API connectivity"""
    try:
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDraiHvH_KIAnFJGLH4gP0OS0YlGtmeO1Y')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": "Hello, can you help with animal health?"}]
            }]
        }
        
        response = requests.post(url, json=payload)
        
        return jsonify({
            'status': response.status_code,
            'response': response.json() if response.ok else response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/firebase_stats')
def firebase_stats():
    """Get image upload counts from Firebase"""
    if firebase_db is None:
        return jsonify({'error': 'Firebase not configured'})
    try:
        stats = {}
        docs = firebase_db.collection('image_counts').stream()
        for doc in docs:
            stats[doc.id] = doc.to_dict()
        return jsonify({'counts': stats})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/api/admin/stats')
def admin_stats():
    """API endpoint for admin dashboard data"""
    if firebase_db is None:
        return jsonify({'error': 'Firebase not configured'})
    try:
        # Get image counts
        counts = {}
        count_docs = firebase_db.collection('image_counts').stream()
        for doc in count_docs:
            counts[doc.id] = doc.to_dict()

        # Get recent uploads (last 50)
        recent = []
        uploads = firebase_db.collection('image_uploads').order_by(
            'timestamp', direction=firestore.Query.DESCENDING
        ).limit(50).stream()
        for doc in uploads:
            data = doc.to_dict()
            data['id'] = doc.id
            if 'timestamp' in data and data['timestamp']:
                data['timestamp'] = data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            recent.append(data)

        # Get local upload folder stats
        local_stats = {}
        upload_root = 'uploads'
        if os.path.exists(upload_root):
            for animal in os.listdir(upload_root):
                animal_path = os.path.join(upload_root, animal)
                if os.path.isdir(animal_path):
                    local_stats[animal] = {}
                    for disease in os.listdir(animal_path):
                        disease_path = os.path.join(animal_path, disease)
                        if os.path.isdir(disease_path):
                            local_stats[animal][disease] = len([
                                f for f in os.listdir(disease_path)
                                if os.path.isfile(os.path.join(disease_path, f))
                            ])

        return jsonify({
            'counts': counts,
            'recent_uploads': recent,
            'local_stats': local_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("VetCare AI - Animal Disease Detection System")
    print("="*50)
    print("\nServer starting...")
    print("Access the application at: http://localhost:5000")
    print("Press CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)