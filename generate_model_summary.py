import tensorflow as tf
from fpdf import FPDF
import io
import sys
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)

def generate_model_summary():
    try:
        # Define model paths
        base_path = os.path.dirname(os.path.abspath(__file__))
        cow_model_path = os.path.join(base_path, 'models', 'trained', 'cow_model.h5')
        dog_model_path = os.path.join(base_path, 'models', 'trained', 'dog_model.h5')

        print("Loading models...")
        cow_model = tf.keras.models.load_model(cow_model_path)
        dog_model = tf.keras.models.load_model(dog_model_path)
        
        print("Creating PDF...")
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'VetCare AI Model Architectures', 0, 1, 'C')
        
        # Cow Model Summary
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Cow Disease Detection Model', 0, 1, 'L')
        
        # Model configuration
        pdf.set_font('Arial', '', 10)
        cow_configs = [
            "Input Shape: (224, 224, 3)",
            "Number of Classes: 2 (Healthy, LSD)",
            "Loss Function: Categorical Crossentropy",
            "Optimizer: Adam",
            "Learning Rate: 0.0002",
            "Metrics: Accuracy"
        ]
        
        for config in cow_configs:
            pdf.cell(0, 8, f"- {config}", 0, 1, 'L')
        
        pdf.ln(10)
        
        # Dog Model Summary
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Dog Disease Detection Model', 0, 1, 'L')
        
        pdf.set_font('Arial', '', 10)
        dog_configs = [
            "Input Shape: (224, 224, 3)",
            "Number of Classes: 3 (Healthy, Fungal, Allergy)",
            "Loss Function: Categorical Crossentropy",
            "Optimizer: Adam",
            "Learning Rate: 0.0002",
            "Metrics: Accuracy"
        ]
        
        for config in dog_configs:
            pdf.cell(0, 8, f"- {config}", 0, 1, 'L')
        
        pdf.ln(10)
        
        # Layer-wise architecture
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Model Architectures', 0, 1, 'L')
        
        # Capture model summaries
        stdout = sys.stdout
        summary_cow = io.StringIO()
        summary_dog = io.StringIO()
        
        sys.stdout = summary_cow
        cow_model.summary()
        cow_summary = summary_cow.getvalue()
        
        sys.stdout = summary_dog
        dog_model.summary()
        dog_summary = summary_dog.getvalue()
        
        sys.stdout = stdout
        
        # Add summaries to PDF
        pdf.set_font('Courier', '', 8)
        pdf.multi_cell(0, 4, cow_summary)
        pdf.ln(5)
        pdf.multi_cell(0, 4, dog_summary)
        
        output_file = 'model_summary.pdf'
        pdf.output(output_file)
        print(f"\nPDF generated successfully: {output_file}")

    except Exception as e:
        print(f"Error generating summary: {str(e)}")

if __name__ == "__main__":
    generate_model_summary()