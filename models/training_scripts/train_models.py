import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras import Model
import os
from fpdf import FPDF

# Create directories if they don't exist
os.makedirs('models/trained', exist_ok=True)

def create_model(num_classes):
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze the base model
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)  # Add dropout to prevent overfitting
    x = Dense(128, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    return model

# Data augmentation and preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

# Training parameters
BATCH_SIZE = 32
EPOCHS = 30
IMAGE_SIZE = (224, 224)

# Train cow model
print("Training cow model...")
cow_model = create_model(num_classes=2)

# Prepare cow datasets
cow_train_generator = train_datagen.flow_from_directory(
    'dataset/cow',
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

cow_validation_generator = train_datagen.flow_from_directory(
    'dataset/cow',
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Compile cow model
cow_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train cow model with callbacks
cow_callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=0.00001
    )
]

cow_history = cow_model.fit(
    cow_train_generator,
    steps_per_epoch=cow_train_generator.samples // BATCH_SIZE,
    validation_data=cow_validation_generator,
    validation_steps=cow_validation_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=cow_callbacks,
    verbose=1  # This prints accuracy & loss per epoch
)

# Save cow model
cow_model.save('models/trained/cow_model.h5')
print("Cow model trained and saved!")

# Train dog model
print("\nTraining dog model...")
dog_model = create_model(num_classes=3)

# Prepare dog datasets
dog_train_generator = train_datagen.flow_from_directory(
    'dataset/dog',
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

dog_validation_generator = train_datagen.flow_from_directory(
    'dataset/dog',
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Compile dog model
dog_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train dog model with callbacks
dog_callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=0.00001
    )
]

dog_history = dog_model.fit(
    dog_train_generator,
    steps_per_epoch=dog_train_generator.samples // BATCH_SIZE,
    validation_data=dog_validation_generator,
    validation_steps=dog_validation_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=dog_callbacks,
    verbose=1  # This prints accuracy & loss per epoch
)

# Save dog model
dog_model.save('models/trained/dog_model.h5')
print("Dog model trained and saved!")

# Print final training and validation metrics for cow model
print("Cow Model Training Complete")
print("Final Training Accuracy:", cow_history.history['accuracy'][-1])
print("Final Training Loss:", cow_history.history['loss'][-1])
print("Final Validation Accuracy:", cow_history.history['val_accuracy'][-1])
print("Final Validation Loss:", cow_history.history['val_loss'][-1])
print("Final Cow Model Training Accuracy:", cow_history.history['accuracy'][-1])
print("Final Cow Model Training Loss:", cow_history.history['loss'][-1])
print("Final Cow Model Validation Accuracy:", cow_history.history['val_accuracy'][-1])
print("Final Cow Model Validation Loss:", cow_history.history['val_loss'][-1])

# Print final training and validation metrics for dog model
print("\nDog Model Training Complete")
print("Final Training Accuracy:", dog_history.history['accuracy'][-1])
print("Final Training Loss:", dog_history.history['loss'][-1])
print("Final Validation Accuracy:", dog_history.history['val_accuracy'][-1])
print("Final Validation Loss:", dog_history.history['val_loss'][-1])
print("Final Dog Model Training Accuracy:", dog_history.history['accuracy'][-1])
print("Final Dog Model Training Loss:", dog_history.history['loss'][-1])
print("Final Dog Model Validation Accuracy:", dog_history.history['val_accuracy'][-1])
print("Final Dog Model Validation Loss:", dog_history.history['val_loss'][-1])

# Print all training and validation accuracies for cow model
print("All Training Accuracies:", cow_history.history['accuracy'])
print("All Validation Accuracies:", cow_history.history['val_accuracy'])

def generate_accuracy_pdf(cow_train_acc, cow_val_acc, dog_train_acc, dog_val_acc):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'VetCare AI Model Accuracy Report', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Cow Disease Detection Model', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Final Training Accuracy: {cow_train_acc:.2%}', 0, 1, 'L')
    pdf.cell(0, 10, f'Final Validation Accuracy: {cow_val_acc:.2%}', 0, 1, 'L')
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Dog Disease Detection Model', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Final Training Accuracy: {dog_train_acc:.2%}', 0, 1, 'L')
    pdf.cell(0, 10, f'Final Validation Accuracy: {dog_val_acc:.2%}', 0, 1, 'L')

    pdf.ln(20)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'This report was generated automatically by VetCare AI.', 0, 1, 'C')

    output_file = 'model_accuracy_report.pdf'
    pdf.output(output_file)
    print(f"\nPDF generated successfully: {output_file}")

if __name__ == "__main__":
    # Replace these with your actual results from train_models.py output
    cow_train_acc = 0.912  # Example: 91.2%
    cow_val_acc = 0.908    # Example: 90.8%
    dog_train_acc = 0.901  # Example: 90.1%
    dog_val_acc = 0.895    # Example: 89.5%
    generate_accuracy_pdf(cow_train_acc, cow_val_acc, dog_train_acc, dog_val_acc)