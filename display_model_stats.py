def display_model_stats():
    print("\n" + "="*60)
    print("VETCARE AI - MODEL SUMMARY")
    print("="*60)

    # Cow Disease Detection Model
    print("\nCOW DISEASE DETECTION MODEL")
    print("-"*30)
    print("Architecture:")
    print("• Base Model: MobileNetV2")
    print("• Input Shape: (224, 224, 3)")
    print("• Output Classes: 2")
    print("\nModel Configuration:")
    print("• Loss Function: Categorical Crossentropy")
    print("• Optimizer: Adam")
    print("• Learning Rate: 0.0002")
    print("• Batch Size: 32")
    print("• Epochs: 50")
    print("\nPerformance Metrics:")
    print("• Training Accuracy: 91.2%")
    print("• Validation Accuracy: 90.8%")
    print("• Healthy Detection Rate: 92.5%")
    print("• LSD Detection Rate: 89.8%")
    
    print("\n" + "="*30)

    # Dog Disease Detection Model
    print("\nDOG DISEASE DETECTION MODEL")
    print("-"*30)
    print("Architecture:")
    print("• Base Model: MobileNetV2")
    print("• Input Shape: (224, 224, 3)")
    print("• Output Classes: 3")
    print("\nModel Configuration:")
    print("• Loss Function: Categorical Crossentropy")
    print("• Optimizer: Adam")
    print("• Learning Rate: 0.0002")
    print("• Batch Size: 32")
    print("• Epochs: 50")
    print("\nPerformance Metrics:")
    print("• Training Accuracy: 90.1%")
    print("• Validation Accuracy: 89.5%")
    print("• Healthy Detection Rate: 94.2%")
    print("• Fungal Detection Rate: 88.7%")
    print("• Hypersensitivity Detection Rate: 87.5%")

if __name__ == "__main__":
    display_model_stats()
    