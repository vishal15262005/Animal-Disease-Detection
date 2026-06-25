document.addEventListener('DOMContentLoaded', function() {
    // Initialize counters
    const cowCounter = new CountUp('cowCount', 0, 1000);
    const dogCounter = new CountUp('dogCount', 0, 800);
    const accuracyCounter = new CountUp('accuracyCount', 0, 90);
    
    // Start counters when in view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                cowCounter.start();
                dogCounter.start();
                accuracyCounter.start();
            }
        });
    });
    
    observer.observe(document.querySelector('.stats'));

    // Slideshow functionality
    const slideshow = document.getElementById('slideshow');
    const slides = slideshow.getElementsByClassName('slideshow-image');
    let currentSlide = 0;

    function nextSlide() {
        // Remove active class from current slide
        slides[currentSlide].classList.remove('active');
        // Move to next slide
        currentSlide = (currentSlide + 1) % slides.length;
        // Add active class to new slide
        slides[currentSlide].classList.add('active');
    }

    // Start slideshow
    if (slides.length > 0) {
        // Make sure first slide is visible
        slides[0].classList.add('active');
        // Change slide every 5 seconds
        setInterval(nextSlide, 5000);
    }
});

function selectAnimal(type) {
    document.getElementById('animal-type').value = type;
    document.getElementById('upload-section').scrollIntoView({ behavior: 'smooth' });
}

document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('image-upload');
    const animalType = document.getElementById('animal-type').value;
    
    formData.append('file', fileInput.files[0]);
    formData.append('animal_type', animalType);
    
    try {
        const submitButton = e.target.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Analyzing...';
        
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        function handleDiseaseDetection(result) {
            const previewSection = document.getElementById('preview');
            const resultSection = document.getElementById('result');
            const warningDiv = document.getElementById('disease-warning');
            const predictionText = document.getElementById('prediction-text');
            const confidenceText = document.getElementById('confidence-text');
            const diseaseInfo = document.getElementById('disease-info');
            
            // Reset classes and content
            previewSection.classList.remove('disease-detected');
            resultSection.classList.remove('disease-detected');
            warningDiv.classList.remove('visible');
            diseaseInfo.innerHTML = '';
            
            // Check if disease is detected
            const isDiseaseDetected = result.prediction.toLowerCase() !== 'healthy';
            
            if (isDiseaseDetected) {
                previewSection.classList.add('disease-detected');
                resultSection.classList.add('disease-detected');
                warningDiv.classList.add('visible');
                predictionText.style.color = '#d32f2f';
                
                // Add disease information based on the prediction
                const diseaseDetails = getDiseaseInformation(result.prediction);
                diseaseInfo.innerHTML = `
                    <div class="disease-details">
                        <h3>About ${result.prediction}</h3>
                        <div class="info-section">
                            <h4>Description</h4>
                            <p>${diseaseDetails.description}</p>
                        </div>
                        <div class="info-section">
                            <h4>Stages</h4>
                            <ul>
                                ${diseaseDetails.stages.map(stage => `<li>${stage}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="info-section">
                            <h4>Treatment Recommendations</h4>
                            <ul>
                                ${diseaseDetails.treatment.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            } else {
                predictionText.style.color = '#4CAF50';
                // Add precautions for healthy animals
                diseaseInfo.innerHTML = `
                    <div class="precautions-details">
                        <h3>Preventive Care Tips</h3>
                        <ul>
                            ${getPreventiveCare().map(tip => `<li>${tip}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            // Update result text
            predictionText.textContent = `Disease: ${result.prediction}`;
            confidenceText.textContent = `Confidence: ${(result.confidence * 100).toFixed(2)}%`;
        }

        if (result.error) {
            alert(result.error);
            return;
        }
        
        document.getElementById('preview-img').src = canvas.toDataURL('image/jpeg');
        // or URL.createObjectURL(file) for file upload
        document.getElementById('preview').classList.add('active');
        
        handleDiseaseDetection(result);
        document.getElementById('result').classList.remove('hidden');
        
        submitButton.disabled = false;
        submitButton.textContent = 'Detect Disease';
    } catch (error) {
        console.error('Error:', error);
        alert('Error processing image');
    }
});

function getDiseaseInformation(disease) {
    const diseaseInfo = {
        'lsd': {
            description: 'Lumpy Skin Disease (LSD) is a viral disease affecting cattle, characterized by nodules on the skin and internal organs.',
            stages: [
                'Initial fever and enlarged lymph nodes',
                'Development of firm, round nodules on skin',
                'Lesions may become necrotic',
                'Secondary bacterial infections possible'
            ],
            treatment: [
                'Isolate affected animals immediately',
                'Provide supportive care and good nutrition',
                'Administer antibiotics for secondary infections',
                'Implement fly control measures',
                'Contact veterinarian for specific treatment plan'
            ]
        },
        'fungal_infection': {
            description: 'A skin condition in dogs caused by various types of fungi, leading to irritation and hair loss.',
            stages: [
                'Initial redness and irritation',
                'Hair loss in affected areas',
                'Development of circular lesions',
                'Possible secondary bacterial infection'
            ],
            treatment: [
                'Apply prescribed antifungal medications',
                'Keep affected areas clean and dry',
                'Regular bathing with medicated shampoo',
                'Monitor for spreading of infection',
                'Complete full course of treatment'
            ]
        },
        'hypersensitivity_allergy': {
            description: 'An overreaction of the immune system to environmental allergens, causing skin irritation in dogs.',
            stages: [
                'Initial itching and discomfort',
                'Redness and inflammation',
                'Development of hot spots',
                'Chronic skin changes if untreated'
            ],
            treatment: [
                'Identify and avoid allergen triggers',
                'Use prescribed antihistamines or steroids',
                'Regular bathing with hypoallergenic shampoo',
                'Dietary modifications if recommended',
                'Consider immunotherapy for severe cases'
            ]
        }
    };
    
    return diseaseInfo[disease.toLowerCase()] || {};
}

function getPreventiveCare() {
    return [
        'Schedule regular veterinary check-ups',
        'Maintain proper vaccination schedule',
        'Practice good hygiene and grooming',
        'Provide balanced nutrition',
        'Ensure clean living environment',
        'Monitor for any changes in behavior or appearance',
        'Implement proper parasite control',
        'Maintain regular exercise routine'
    ];
}

function generatePDF(result) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Add header
    doc.setFontSize(22);
    doc.setTextColor(76, 175, 80);
    doc.text("Animal Disease Detection Report", 105, 20, { align: "center" });
    
    // Add date and time
    doc.setFontSize(12);
    doc.setTextColor(100);
    const date = new Date().toLocaleString();
    doc.text(`Generated on: ${date}`, 20, 30);
    
    // Add detection results
    doc.setFontSize(16);
    doc.setTextColor(0);
    doc.text("Detection Results", 20, 45);
    
    doc.setFontSize(14);
    doc.text(`Disease: ${result.prediction}`, 20, 55);
    doc.text(`Confidence: ${(result.confidence * 100).toFixed(2)}%`, 20, 65);
    
    // Add disease information if disease detected
    if (result.prediction.toLowerCase() !== 'healthy') {
        const diseaseInfo = getDiseaseInfo(result.prediction);
        
        doc.setFontSize(16);
        doc.text("Disease Information", 20, 85);
        
        doc.setFontSize(14);
        doc.text("Description:", 20, 95);
        const descLines = doc.splitTextToSize(diseaseInfo.description, 170);
        doc.text(descLines, 20, 105);
        
        doc.text("Stages:", 20, 125);
        let yPos = 135;
        diseaseInfo.stages.forEach(stage => {
            doc.text(`• ${stage}`, 25, yPos);
            yPos += 10;
        });
        
        doc.text("Treatment Recommendations:", 20, yPos + 10);
        yPos += 20;
        diseaseInfo.treatment.forEach(treatment => {
            doc.text(`• ${treatment}`, 25, yPos);
            yPos += 10;
        });
    } else {
        // Add preventive care tips for healthy animals
        doc.setFontSize(16);
        doc.text("Preventive Care Recommendations", 20, 85);
        
        doc.setFontSize(14);
        let yPos = 95;
        getPreventiveCare().forEach(tip => {
            doc.text(`• ${tip}`, 25, yPos);
            yPos += 10;
        });
    }
    
    // Add footer
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text("This report was generated automatically by the Animal Disease Detection System", 105, 280, { align: "center" });
    
    // Save the PDF
    const filename = `disease-detection-report-${new Date().toISOString().slice(0,10)}.pdf`;
    doc.save(filename);
}

let currentLang = localStorage.getItem('preferred-language') || 'en';

function toggleLanguageMenu() {
    const menu = document.getElementById('languageMenu');
    menu.classList.toggle('show');
}

function updateNewsTickerContent(newsItems) {
    const tickerContent = document.querySelector('.ticker-content');
    if (tickerContent) {
        tickerContent.innerHTML = newsItems.map(item => 
            `<span class="ticker-item">${item}</span>`
        ).join('');
    }
}

function changeLanguage(lang) {
    const t = window.translations[lang];
    
    try {
        // Update hero section
        document.getElementById('mainTitle').textContent = t.title;
        document.getElementById('mainSubtitle').textContent = t.subtitle;
        document.getElementById('mainDescription').textContent = t.subtext;

        // Update buttons
        const ctaButtons = document.querySelectorAll('.cta-buttons .cta-button');
        ctaButtons[0].textContent = t.detectCow;
        ctaButtons[1].textContent = t.detectDog;
        
        // Update news ticker
        updateNewsTickerContent(t.newsItems);
        
        // Update vet section
        const vetTitle = document.querySelector('.vet-section .section-title');
        if (vetTitle) vetTitle.textContent = t.bookVet;
        
        const vetDesc = document.querySelector('.vet-section p');
        if (vetDesc) vetDesc.textContent = t.vetDesc;
        
        const bookBtn = document.querySelector('.vet-cta');
        if (bookBtn) bookBtn.textContent = t.bookBtn;
        
        // Update video section
        const videoTitle = document.querySelector('.video-section .section-title');
        if (videoTitle) videoTitle.textContent = t.educationTitle;
        
        // Update video titles
        const videoTitles = document.querySelectorAll('.video-card h3');
        if (videoTitles && videoTitles.length >= 3) {
            videoTitles[0].textContent = t.videoTitles.cowPrevention;
            videoTitles[1].textContent = t.videoTitles.dogSkinCare;
            videoTitles[2].textContent = t.videoTitles.animalHealth;
        }
        
        // Update Analytics section
        document.querySelector('.analytics-section .section-title').textContent = t.analytics.title;
        document.querySelector('.analytics-section .section-subtitle').textContent = t.analytics.subtitle;
        document.querySelector('.analytics-cta').innerHTML = t.analytics.buttonText;
        
        // Update How to Use section
        const howToUseSection = document.querySelector('.how-to-use-section');
        if (howToUseSection) {
            howToUseSection.querySelector('.section-title').textContent = t.howToUse.title;
            howToUseSection.querySelector('.section-subtitle').textContent = t.howToUse.subtitle;

            // Update step cards
            const stepCards = howToUseSection.querySelectorAll('.step-card');
            stepCards.forEach((card, index) => {
                const stepData = t.howToUse.steps[index];
                card.querySelector('h3').textContent = stepData.title;
                card.querySelector('p').textContent = stepData.description;
                
                // Update features
                const features = card.querySelector('.step-features');
                features.innerHTML = stepData.features
                    .map(feature => `<span>✓ ${feature}</span>`)
                    .join('');
            });
        }

        // Save preference
        localStorage.setItem('preferred-language', lang);
        document.querySelector('.current-lang').textContent = lang.toUpperCase();
    } catch (error) {
        console.error('Error updating language:', error);
    }
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferred-language') || 'en';
    changeLanguage(savedLang);
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    const menu = document.getElementById('languageMenu');
    const btn = document.querySelector('.settings-btn');
    if (menu && !menu.contains(e.target) && !btn.contains(e.target)) {
        menu.classList.remove('show');
    }
});

// Add this function to both detection pages
function updatePageTranslations(lang) {
    const t = window.translations[lang].detection;
    const isDogPage = document.querySelector('.detection-page.dog-theme') !== null;
    const pageTitle = isDogPage ? t.dogTitle : t.cowTitle;
    
    // Update page title and headers
    document.title = pageTitle;
    document.querySelector('.page-title').textContent = pageTitle;
    
    // Update camera section
    document.querySelector('.method-card h2').textContent = t.useCamera;
    document.getElementById('start-camera').textContent = t.turnOnCamera;
    document.getElementById('capture-btn').textContent = t.captureImage;
    
    // Update divider
    document.querySelector('.method-divider span').textContent = t.or;
    
    // Update upload section
    document.querySelector('.method-card:nth-child(3) h2').textContent = t.uploadImage;
    document.querySelector('.upload-btn').textContent = t.chooseFile;
    document.querySelector('.submit-btn').textContent = t.analyzeImage;
    
    // Update preview section
    document.querySelector('.preview-section h3').textContent = t.imagePreview;
    
    // Update result section
    document.querySelector('.result-title').textContent = t.detectionResult;
    document.querySelector('.download-btn').innerHTML = 
        `<span class="download-icon">📥</span>${t.downloadReport}`;
}

// Add event listener for language changes
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferred-language') || 'en';
    updatePageTranslations(savedLang);
});

// Listen for language changes
window.addEventListener('storage', (e) => {
    if (e.key === 'preferred-language') {
        updatePageTranslations(e.newValue);
    }
});

function toggleChat() {
    const chatBody = document.getElementById('chatBody');
    chatBody.classList.toggle('minimized');
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';

    // Show loading message
    const loadingMsg = addMessage("Thinking...", 'bot');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        // Remove loading message
        const messages = document.getElementById('chatMessages');
        if (loadingMsg && loadingMsg.parentNode) {
            messages.removeChild(loadingMsg);
        }
        
        // Always show the response, whether it's an error or success
        if (data.response) {
            addMessage(data.response, 'bot');
        } else if (data.error) {
            addMessage("I'm having technical difficulties. Please try:\n• Asking about cow or dog diseases\n• Symptoms and treatments\n• Booking a vet appointment", 'bot');
        }
    } catch (e) {
        console.error('Chat error:', e);
        const messages = document.getElementById('chatMessages');
        if (loadingMsg && loadingMsg.parentNode) {
            messages.removeChild(loadingMsg);
        }
        addMessage("Connection error. Please check your internet and try again.", 'bot');
    }
}

function addMessage(text, sender) {
    const messages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
    return messageDiv; // Return the element so we can remove it later
}

// Remove the old callGeminiAPI function - not needed anymore

// Mobile Format Toggle Function
function toggleMobileFormat() {
    const body = document.body;
    const modeText = document.querySelector('.mode-text');
    const newMode = body.classList.contains('mobile-format') ? 'desktop' : 'mobile';
    
    // Update all open pages
    if (newMode === 'mobile') {
        body.classList.add('mobile-format');
        if (modeText) modeText.textContent = 'Desktop Mode';
    } else {
        body.classList.remove('mobile-format');
        if (modeText) modeText.textContent = 'Mobile Mode';
    }
    
    // Save preference
    localStorage.setItem('viewMode', newMode);
    
    // Trigger storage event for other open pages
    window.dispatchEvent(new StorageEvent('storage', {
        key: 'viewMode',
        newValue: newMode
    }));
}

// Check saved view mode on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedMode = localStorage.getItem('viewMode');
    const body = document.body;
    const modeText = document.querySelector('.mode-text');
    
    if (savedMode === 'mobile') {
        body.classList.add('mobile-format');
        if (modeText) modeText.textContent = 'Desktop Mode';
    }
});

// Listen for storage changes to sync mobile format across tabs
window.addEventListener('storage', (e) => {
    if (e.key === 'viewMode') {
        const body = document.body;
        const modeText = document.querySelector('.mode-text');
        
        if (e.newValue === 'mobile') {
            body.classList.add('mobile-format');
            if (modeText) modeText.textContent = 'Desktop Mode';
        } else if (e.newValue === 'desktop') {
            body.classList.remove('mobile-format');
            if (modeText) modeText.textContent = 'Mobile Mode';
        }
    }
});

function toggleSettings() {
    const menu = document.getElementById('settingsMenu');
    menu.classList.toggle('show');
}

function toggleLanguageOptions() {
    const langMenu = document.getElementById('languageMenu');
    langMenu.classList.toggle('show');
}

// Close menus when clicking outside
document.addEventListener('click', (e) => {
    const settingsMenu = document.getElementById('settingsMenu');
    const settingsBtn = document.querySelector('.settings-btn');
    const langMenu = document.getElementById('languageMenu');
    
    if (!settingsBtn.contains(e.target) && !settingsMenu.contains(e.target)) {
        settingsMenu.classList.remove('show');
        langMenu.classList.remove('show');
    }
});

// Voice to text feature for chatbot
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = window.SpeechRecognition ? new window.SpeechRecognition() : null;

const micBtn = document.getElementById('micBtn');
if (recognition && micBtn) {
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    micBtn.addEventListener('click', () => {
        recognition.start();
        micBtn.disabled = true;
        micBtn.innerHTML = '<span>🎤...</span>';
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('userInput').value = transcript;
        micBtn.disabled = false;
        micBtn.innerHTML = '<span>🎤</span>';
    };

    recognition.onerror = () => {
        micBtn.disabled = false;
        micBtn.innerHTML = '<span>🎤</span>';
        alert('Voice recognition error. Please try again.');
    };

    recognition.onend = () => {
        micBtn.disabled = false;
        micBtn.innerHTML = '<span>🎤</span>';
    };
} else if (micBtn) {
    micBtn.style.display = 'none';
}

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = fileInput.files[0];
    const affectedArea = document.getElementById('affected-area').value;
    if (!file) {
        alert('Please select an image file');
        return;
    }

    // Show loading state
    const submitBtn = uploadForm.querySelector('.submit-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing...';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('affected_area', affectedArea);

    try {
        const response = await fetch(`/predict?animal_type=dog`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        function handleDiseaseDetection(result) {
            const previewSection = document.getElementById('preview');
            const resultSection = document.getElementById('result');
            const warningDiv = document.getElementById('disease-warning');
            const predictionText = document.getElementById('prediction-text');
            const confidenceText = document.getElementById('confidence-text');
            const diseaseInfo = document.getElementById('disease-info');
            
            // Reset classes and content
            previewSection.classList.remove('disease-detected');
            resultSection.classList.remove('disease-detected');
            warningDiv.classList.remove('visible');
            diseaseInfo.innerHTML = '';
            
            // Check if disease is detected
            const isDiseaseDetected = result.prediction.toLowerCase() !== 'healthy';
            
            if (isDiseaseDetected) {
                previewSection.classList.add('disease-detected');
                resultSection.classList.add('disease-detected');
                warningDiv.classList.add('visible');
                predictionText.style.color = '#d32f2f';
                
                // Add disease information based on the prediction
                const diseaseDetails = getDiseaseInformation(result.prediction);
                diseaseInfo.innerHTML = `
                    <div class="disease-details">
                        <h3>About ${result.prediction}</h3>
                        <div class="info-section">
                            <h4>Description</h4>
                            <p>${diseaseDetails.description}</p>
                        </div>
                        <div class="info-section">
                            <h4>Stages</h4>
                            <ul>
                                ${diseaseDetails.stages.map(stage => `<li>${stage}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="info-section">
                            <h4>Treatment Recommendations</h4>
                            <ul>
                                ${diseaseDetails.treatment.map(item => `<li>${item}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            } else {
                predictionText.style.color = '#4CAF50';
                // Add precautions for healthy animals
                diseaseInfo.innerHTML = `
                    <div class="precautions-details">
                        <h3>Preventive Care Tips</h3>
                        <ul>
                            ${getPreventiveCare().map(tip => `<li>${tip}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            // Update result text
            predictionText.textContent = `Disease: ${result.prediction}`;
            confidenceText.textContent = `Confidence: ${(result.confidence * 100).toFixed(2)}%`;
        }

        if (result.error) {
            alert(result.error);
            return;
        }
        
        document.getElementById('preview-img').src = canvas.toDataURL('image/jpeg');
        // or URL.createObjectURL(file) for file upload
        document.getElementById('preview').classList.add('active');
        
        handleDiseaseDetection(result);
        document.getElementById('result').classList.remove('hidden');
        
        submitButton.disabled = false;
        submitButton.textContent = 'Detect Disease';
    } catch (error) {
        console.error('Error:', error);
        alert('Error processing image');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Analyze Image';
    }
});

