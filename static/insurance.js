const eligibilityForm = document.getElementById('eligibilityForm');
const eligibilityResult = document.getElementById('eligibilityResult');

eligibilityForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const type = document.getElementById('animalType').value;
    const age = parseInt(document.getElementById('animalAge').value);
    const health = document.getElementById('healthStatus').value;
    const value = parseFloat(document.getElementById('animalValue').value);

    let eligible = true;
    let reason = [];

    if (health !== 'healthy') {
        eligible = false;
        reason.push('Animal must be healthy');
    }
    if (type === 'cow' && (age < 6 || age > 120)) {
        eligible = false;
        reason.push('Cow age must be 6–120 months');
    }
    if (type === 'dog' && (age < 3 || age > 108)) {
        eligible = false;
        reason.push('Dog age must be 3–108 months');
    }

    if (value < 5000) {
        eligible = false;
        reason.push('Value too low for coverage');
    }

    eligibilityResult.innerHTML = eligible
        ? `✅ <strong>Eligible</strong><br>Suggested Plans: ${type === 'cow' ? 'Govt Livestock Scheme' : 'Private Pet Insurance'}`
        : `❌ <strong>Not Eligible</strong><br>${reason.join(', ')}`;
});

const premiumForm = document.getElementById('premiumForm');
const premiumResult = document.getElementById('premiumResult');

premiumForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const value = parseFloat(document.getElementById('calcValue').value);
    const subsidy = parseFloat(document.getElementById('subsidyRate').value);

    const basePremium = value * 0.03; // 3% of value per year
    const subsidyAmount = basePremium * subsidy;
    const farmerPay = basePremium - subsidyAmount;

    premiumResult.innerHTML = `
        <div>Annual Premium: <strong>₹${basePremium.toFixed(0)}</strong></div>
        <div>Subsidy Applied: <strong>₹${subsidyAmount.toFixed(0)}</strong></div>
        <div>Farmer Pays: <strong>₹${farmerPay.toFixed(0)}/year</strong></div>
        <div>Coverage Amount: <strong>₹${value.toFixed(0)}</strong></div>
    `;
});