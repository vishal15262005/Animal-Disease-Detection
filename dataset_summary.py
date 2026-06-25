import os
from fpdf import FPDF

def generate_dataset_summary():
    try:
        # Get base directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Dataset paths - updated to project root directory
        cow_healthy_path = os.path.join(base_path, 'dataset', 'cow', 'healthy')
        cow_lsd_path = os.path.join(base_path, 'dataset', 'cow', 'lsd')
        dog_healthy_path = os.path.join(base_path, 'dataset', 'dog', 'healthy')
        dog_fungal_path = os.path.join(base_path, 'dataset', 'dog', 'fungal_infection')
        dog_allergy_path = os.path.join(base_path, 'dataset', 'dog', 'hypersensitivity_allergy')

        print("Checking paths:")
        print(f"Cow healthy: {cow_healthy_path}")
        print(f"Cow LSD: {cow_lsd_path}")
        print(f"Dog healthy: {dog_healthy_path}")
        print(f"Dog fungal: {dog_fungal_path}")
        print(f"Dog allergy: {dog_allergy_path}")

        # Count images in each category
        cow_healthy_count = len([f for f in os.listdir(cow_healthy_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        cow_lsd_count = len([f for f in os.listdir(cow_lsd_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        dog_healthy_count = len([f for f in os.listdir(dog_healthy_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        dog_fungal_count = len([f for f in os.listdir(dog_fungal_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
        dog_allergy_count = len([f for f in os.listdir(dog_allergy_path) if f.endswith(('.jpg', '.jpeg', '.png'))])

        # Success rates (example rates - update with actual rates)
        success_rates = {
            'cow': {
                'healthy': 92.5,
                'lsd': 89.8,
                'overall': 91.2
            },
            'dog': {
                'healthy': 94.2,
                'fungal': 88.7,
                'allergy': 87.5,
                'overall': 90.1
            }
        }

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'VetCare AI Dataset Summary', 0, 1, 'C')
        pdf.ln(10)

        # Cow Dataset Summary
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Cow Disease Dataset', 0, 1, 'L')
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Total Images: {cow_healthy_count + cow_lsd_count}', 0, 1, 'L')
        pdf.cell(0, 10, f'Healthy Images: {cow_healthy_count}', 0, 1, 'L')
        pdf.cell(0, 10, f'LSD Images: {cow_lsd_count}', 0, 1, 'L')
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Success Rates:', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'• Healthy Detection: {success_rates["cow"]["healthy"]}%', 0, 1, 'L')
        pdf.cell(0, 10, f'• LSD Detection: {success_rates["cow"]["lsd"]}%', 0, 1, 'L')
        pdf.cell(0, 10, f'• Overall Accuracy: {success_rates["cow"]["overall"]}%', 0, 1, 'L')
        
        pdf.ln(10)

        # Dog Dataset Summary
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Dog Disease Dataset', 0, 1, 'L')
        
        pdf.set_font('Arial', '', 12)
        total_dog = dog_healthy_count + dog_fungal_count + dog_allergy_count
        pdf.cell(0, 10, f'Total Images: {total_dog}', 0, 1, 'L')
        pdf.cell(0, 10, f'Healthy Images: {dog_healthy_count}', 0, 1, 'L')
        pdf.cell(0, 10, f'Fungal Infection Images: {dog_fungal_count}', 0, 1, 'L')
        pdf.cell(0, 10, f'Hypersensitivity/Allergy Images: {dog_allergy_count}', 0, 1, 'L')
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Success Rates:', 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'• Healthy Detection: {success_rates["dog"]["healthy"]}%', 0, 1, 'L')
        pdf.cell(0, 10, f'• Fungal Infection Detection: {success_rates["dog"]["fungal"]}%', 0, 1, 'L')
        pdf.cell(0, 10, f'• Hypersensitivity Detection: {success_rates["dog"]["allergy"]}%', 0, 1, 'L')
        pdf.cell(0, 10, f'• Overall Accuracy: {success_rates["dog"]["overall"]}%', 0, 1, 'L')

        # Save PDF
        output_file = 'dataset_summary.pdf'
        pdf.output(output_file)
        print(f"\nDataset summary PDF generated successfully: {output_file}")

    except Exception as e:
        print(f"Error generating dataset summary: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")

if __name__ == "__main__":
    generate_dataset_summary()