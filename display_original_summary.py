import tensorflow as tf
import os

def display_dataset_and_model_summary():
    try:
        print("\n" + "="*50)
        print("DATASET SUMMARY")
        print("="*50)

        # Dataset Statistics
        print("\nCOW DATASET:")
        print("-"*30)
        cow_healthy = len(os.listdir('dataset/cow/healthy'))
        cow_lsd = len(os.listdir('dataset/cow/lsd'))
        total_cow = cow_healthy + cow_lsd
        
        print(f"Total Images: {total_cow}")
        print(f"Healthy Images: {cow_healthy}")
        print(f"LSD Images: {cow_lsd}")
        
        print("\nDOG DATASET:")
        print("-"*30)
        dog_healthy = len(os.listdir('dataset/dog/healthy'))
        dog_fungal = len(os.listdir('dataset/dog/fungal_infection'))
        dog_allergy = len(os.listdir('dataset/dog/hypersensitivity_allergy'))
        total_dog = dog_healthy + dog_fungal + dog_allergy
        
        print(f"Total Images: {total_dog}")
        print(f"Healthy Images: {dog_healthy}")
        print(f"Fungal Infection Images: {dog_fungal}")
        print(f"Hypersensitivity/Allergy Images: {dog_allergy}")

        print("\n" + "="*50)
        print("MODEL SUMMARY")
        print("="*50)

        # Load models
        print("\nCOW MODEL:")
        print("-"*30)
        cow_model = tf.keras.models.load_model('models/trained/cow_model.h5')
        cow_model.summary()

        print("\nDOG MODEL:")
        print("-"*30)
        dog_model = tf.keras.models.load_model('models/trained/dog_model.h5')
        dog_model.summary()

    except Exception as e:
        print(f"Error displaying summary: {str(e)}")

if __name__ == "__main__":
    display_dataset_and_model_summary()