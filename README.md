<div align="center">

# Farm & Co

### AI-Powered Livestock & Pet Disease Detection Platform

*Empowering Farmers with Artificial Intelligence for Early Disease Detection, Better Animal Healthcare, and Sustainable Agriculture.*

</div>

---

## About the Project

Farm & Co is an AI-powered web application that enables the early detection of diseases in livestock and pets using Deep Learning and Computer Vision. The platform allows users to upload or capture an image of an animal, after which a trained **MobileNetV2-based Convolutional Neural Network (CNN)** analyzes the image and predicts potential diseases in their early stages.

Beyond disease detection, Farm & Co provides health recommendations, veterinary support, livestock insurance information, and multilingual accessibility, making quality animal healthcare more accessible to both rural and urban communities.

---

## Problem Statement

Livestock diseases such as **Lumpy Skin Disease (LSD)** and other infectious conditions often remain unnoticed during their early stages due to:

* Limited access to veterinary professionals
* Delayed diagnosis and treatment
* Lack of awareness among livestock owners
* Reduced productivity and milk yield
* Significant financial losses for farmers

Early identification is essential to reduce disease spread, improve animal welfare, and protect farmers' livelihoods.

---

## Our Solution

Farm & Co provides an intelligent AI-driven disease detection system that enables users to upload or capture images of livestock and pets from any device.

The uploaded image undergoes preprocessing and is analyzed using a **MobileNetV2-based CNN model**, which automatically extracts visual features such as lesions, swelling, discoloration, and texture abnormalities. Based on these features, the model predicts the disease at an early stage and provides healthcare recommendations for timely intervention.

The platform also offers veterinary assistance, multilingual accessibility, and direct access to livestock insurance resources.

---

## Key Features

* AI-powered disease detection using Deep Learning
* Early-stage disease prediction through image analysis
* MobileNetV2-based CNN architecture
* Veterinary appointment support
* Animal healthcare recommendations
* Livestock insurance information with direct links
* Multilingual support (English, Tamil, Hindi)
* Responsive design compatible with mobile, tablet, and desktop devices
* Optimized for low-bandwidth environments

---

## System Workflow

```text
User Uploads or Captures Animal Image
                │
                ▼
      Image Preprocessing
      • Resize (224 × 224)
      • Normalization
                │
                ▼
      MobileNetV2 (CNN Model)
      • Feature Extraction
      • Disease Classification
                │
                ▼
        Softmax Prediction
                │
                ▼
      Prediction Results
      • Disease Name
      • Confidence Score
      • Health Recommendations
      • Veterinary Support
      • Insurance Information
```

---

## Technology Stack

### Artificial Intelligence

* TensorFlow
* Keras
* Convolutional Neural Networks (CNN)
* MobileNetV2
* Transfer Learning

### Backend

* Python
* Flask

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Image Processing

* OpenCV
* NumPy
* Pillow

---

## Why MobileNetV2?

* Lightweight and optimized CNN architecture
* High classification accuracy
* Fast inference with low computational cost
* Suitable for deployment on web and mobile platforms
* Efficient feature extraction through transfer learning

---

## Core Modules

### Disease Detection

AI-based image classification for livestock and pet diseases.

### Health Recommendations

Personalized guidance based on the detected disease.

### Veterinary Support

Connects users with veterinary consultation services.

### Livestock Insurance

Provides information and direct links to livestock insurance schemes.

### Multilingual Support

Available in English, Tamil, and Hindi to improve accessibility.

---

## Sustainable Development Goals

Farm & Co contributes to the following United Nations Sustainable Development Goals:

* **SDG 2 – Zero Hunger**
* **SDG 3 – Good Health and Well-being**

---

## Future Enhancements

* Support for additional livestock and pet diseases
* Offline AI inference for remote farming regions
* IoT-based livestock health monitoring
* Cloud-based health records
* Advanced analytics dashboard
* Government veterinary service integration

---

## Repository Structure

```text
Farm-and-Co/
│── app.py
│── model/
│── static/
│── templates/
│── dataset/
│── requirements.txt
│── README.md
```

---

## Installation

```bash
git clone https://github.com/your-username/Farm-and-Co.git

cd Farm-and-Co

pip install -r requirements.txt

python app.py
```

---

## Vision

To build an intelligent digital healthcare ecosystem for livestock and pets by enabling early disease detection, improving veterinary accessibility, supporting livestock insurance awareness, and empowering farmers through Artificial Intelligence.

---

<div align="center">

**Developed with Artificial Intelligence to Improve Animal Healthcare and Sustainable Agriculture**

</div>
