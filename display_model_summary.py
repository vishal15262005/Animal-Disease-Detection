import tensorflow as tf
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

BATCH_SIZE = 32
IMAGE_SIZE = (224, 224)

def display_model_summary():
    try:
        # Get base directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Define model paths
        cow_model_path = os.path.join(base_path, 'models', 'trained', 'cow_model.h5')
        dog_model_path = os.path.join(base_path, 'models', 'trained', 'dog_model.h5')

        print("\n" + "="*50)
        print("ORIGINAL MODEL SUMMARY")
        print("="*50)

        # Load and display Cow Model summary
        print("\nCOW MODEL ARCHITECTURE:")
        print("-"*30)
        cow_model = tf.keras.models.load_model(cow_model_path)
        cow_model.summary()

        print("\n" + "="*50)

        # Load and display Dog Model summary
        print("\nDOG MODEL ARCHITECTURE:")
        print("-"*30)
        dog_model = tf.keras.models.load_model(dog_model_path)
        dog_model.summary()

    except FileNotFoundError as e:
        print(f"\nError: Model file not found.")
        print(f"Please ensure the model files exist at:")
        print(f"Cow Model: {cow_model_path}")
        print(f"Dog Model: {dog_model_path}")
    except Exception as e:
        print(f"\nError displaying model summary: {str(e)}")

def evaluate_model_accuracy(model, directory, image_size, batch_size):
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    
    val_gen = datagen.flow_from_directory(
        directory,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    loss, accuracy = model.evaluate(val_gen, verbose=1)
    return accuracy

if __name__ == "__main__":
    display_model_summary()
    
    # Cow Model Accuracy
    cow_model = tf.keras.models.load_model('models/trained/cow_model.h5')
    cow_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    cow_val_gen = cow_datagen.flow_from_directory(
        'dataset/cow',
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    loss, accuracy = cow_model.evaluate(cow_val_gen, verbose=1)
    print(f"Cow Model Validation Accuracy: {accuracy:.4f}")

    # Dog Model Accuracy
    dog_model = tf.keras.models.load_model('models/trained/dog_model.h5')
    dog_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    dog_val_gen = dog_datagen.flow_from_directory(
        'dataset/dog',
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    loss, accuracy = dog_model.evaluate(dog_val_gen, verbose=1)
    print(f"Dog Model Validation Accuracy: {accuracy:.4f}")