# frontend/Home.py
import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import base64
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="MadebyNari - Empowering Indian Artisans",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
    }
    
    .navbar {
        background-color: white;
        padding: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
        width: 100%;
    }
    
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .logo {
        font-size: 1.8rem;
        font-weight: 700;
        color: #6a11cb;
        font-family: 'Playfair Display', serif;
    }
    
    .nav-menu {
        display: flex;
        list-style: none;
        align-items: center;
    }
    
    .nav-item {
        margin-left: 30px;
    }
    
    .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .nav-link:hover {
        color: #6a11cb;
    }
    
    .login-btn {
        background-color: #6a11cb;
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 500;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .login-btn:hover {
        background-color: #2575fc;
        color: white;
        text-decoration: none;
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(106,17,203,0.1) 0%, rgba(37,117,252,0.1) 100%);
        padding: 80px 0;
        text-align: center;
        margin-bottom: 40px;
        border-radius: 10px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: #333;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        margin-bottom: 30px;
        color: #666;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .cta-button {
        background-color: #FF6B6B;
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-button:hover {
        background-color: #FF8E8E;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        color: white;
        text-decoration: none;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin: 60px 0 40px 0;
        color: #333;
        font-family: 'Playfair Display', serif;
    }
    
    .about-section {
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
        padding: 60px 40px;
        border-radius: 15px;
        margin: 40px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .about-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 30px;
        color: #6a11cb;
        text-align: center;
        font-family: 'Playfair Display', serif;
    }
    
    .problem-solution-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        margin-top: 40px;
    }
    
    .problem-box, .solution-box {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    .problem-title, .solution-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: #333;
        display: flex;
        align-items: center;
    }
    
    .problem-list, .solution-list {
        list-style: none;
        padding: 0;
    }
    
    .problem-list li, .solution-list li {
        margin-bottom: 15px;
        padding-left: 30px;
        position: relative;
    }
    
    .problem-list li:before {
        content: "❌";
        position: absolute;
        left: 0;
        color: #ff6b6b;
    }
    
    .solution-list li:before {
        content: "✅";
        position: absolute;
        left: 0;
        color: #4caf50;
    }
    
    .mission-statement {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-top: 40px;
        font-style: italic;
        font-size: 1.2rem;
    }
    
    .footer {
        background-color: #f8f9fa;
        padding: 40px 0;
        margin-top: 60px;
        text-align: center;
        color: #666;
    }
    
    .image-slider {
        margin: 40px 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .slider-image {
        width: 100%;
        height: 400px;
        object-fit: cover;
    }
    
    .login-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    
    .modal-content {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        width: 90%;
        max-width: 500px;
        max-height: 90vh;
        overflow-y: auto;
    }
    
    .form-title {
        text-align: center;
        margin-bottom: 20px;
        color: #6a11cb;
    }
    
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-label {
        display: block;
        margin-bottom: 5px;
        font-weight: 500;
    }
    
    .form-input {
        width: 100%;
        padding: 10px 15px;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 1rem;
    }
    
    .form-submit {
        background-color: #6a11cb;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .form-submit:hover {
        background-color: #2575fc;
    }
    
    .user-type-selector {
        display: flex;
        margin-bottom: 20px;
        border-radius: 5px;
        overflow: hidden;
        border: 1px solid #ddd;
    }
    
    .user-type-btn {
        flex: 1;
        padding: 10px;
        text-align: center;
        background-color: #f9f9f9;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .user-type-btn.active {
        background-color: #6a11cb;
        color: white;
    }
    
    .close-modal {
        position: absolute;
        top: 10px;
        right: 10px;
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .nav-menu {
            display: none;
        }
        
        .problem-solution-grid {
            grid-template-columns: 1fr;
        }
        
        .mobile-menu-btn {
            display: block;
        }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for modal functionality
modal_js = """
<script>
function openLoginModal() {
    document.getElementById('loginModal').style.display = 'flex';
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function setUserType(type) {
    document.querySelectorAll('.user-type-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-type="${type}"]`).classList.add('active');
    document.getElementById('userType').value = type;
}

// Close modal if clicked outside
window.onclick = function(event) {
    const modal = document.getElementById('loginModal');
    if (event.target === modal) {
        closeLoginModal();
    }
}
</script>
"""

# Add JavaScript to page
components.html(modal_js, height=0)

# Navigation Bar
st.markdown("""
<div class="navbar">
    <div class="nav-container">
        <div class="logo">MadebyNari</div>
        <ul class="nav-menu">
            <li class="nav-item"><a href="#" class="nav-link">Home</a></li>
            <li class="nav-item"><a href="#about" class="nav-link">About</a></li>
            <li class="nav-item"><a href="#how-it-works" class="nav-link">How It Works</a></li>
            <li class="nav-item"><a href="#demo" class="nav-link">Demo</a></li>
            <li class="nav-item"><a href="/app" class="nav-link">Try It</a></li>
            <li class="nav-item"><a href="#" class="login-btn" onclick="openLoginModal()">Login / Sign Up</a></li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section with Logo and Tagline
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">MadebyNari</h1>
    <p class="hero-subtitle">Empowering Indian artisans with AI-powered tools to showcase their crafts to the world. 
    We help transform traditional craftsmanship into digital success stories.</p>
    <a href="/app" class="cta-button">👉 Generate Content Now</a>
</div>
""", unsafe_allow_html=True)

# Image Slider (using sample images)
st.markdown("""
<div class="image-slider">
    <img src="https://images.unsplash.com/photo-1605000797499-95a51c5269ae?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" class="slider-image" alt="Artisan Products">
</div>
""", unsafe_allow_html=True)

# About MadebyNari Section
st.markdown("""
<div class="about-section" id="about">
    <h2 class="about-title">About MadebyNari</h2>
    <p style="text-align: center; font-size: 1.2rem; line-height: 1.6; margin-bottom: 40px;">
        MadebyNari is a tool created to enable Indian artisans to make online product demonstration easy and worldwide.
    </p>
    
    <div class="problem-solution-grid">
        <div class="problem-box">
            <h3 class="problem-title">The Challenges Artisans Face</h3>
            <ul class="problem-list">
                <li>Crafting professional-sounding product descriptions</li>
                <li>Language translation into many languages</li>
                <li>Marketing their craft on the internet</li>
                <li>Limited digital literacy and technical knowledge</li>
                <li>Difficulty reaching global customers</li>
            </ul>
        </div>
        
        <div class="solution-box">
            <h3 class="solution-title">How MadebyNari Helps</h3>
            <ul class="solution-list">
                <li>Upload a photo of your product</li>
                <li>Instantly generate product titles, captions, and hashtags</li>
                <li>Get translations in English and regional languages</li>
                <li>User-friendly interface requiring no technical knowledge</li>
                <li>Reach global markets with optimized content</li>
            </ul>
        </div>
    </div>
    
    <div class="mission-statement">
        <p>Our purpose is to connect local women creators and markets by providing them with the digital know-how to thrive — without demanding technical or marketing knowledge.</p>
        <p style="margin-top: 20px; font-weight: 600;">✨ Your work, our tech — an alliance for a sustainable artisan economy.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# How It Works Section (from previous implementation)
st.markdown('<h2 class="section-title" id="how-it-works">How It Works</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="how-it-works-container">
    <div class="process-step">
        <div class="step-number">1</div>
        <div class="step-content">
            <h3>Upload Your Product Image</h3>
            <p>Simply upload a clear photo of your artisan product - whether it's pottery, textiles, jewelry, or any handmade item. Our AI will analyze the image to understand its features and craftsmanship.</p>
        </div>
    </div>
    
    <div class="step-divider"></div>
    
    <div class="process-step">
        <div class="step-number">2</div>
        <div class="step-content">
            <h3>AI Generates Compelling Content</h3>
            <p>Our advanced AI analyzes your product and automatically creates engaging titles, detailed descriptions, and persuasive marketing copy that highlights the unique aspects of your artisan product.</p>
        </div>
    </div>
    
    <div class="step-divider"></div>
    
    <div class="process-step">
        <div class="step-number">3</div>
        <div class="step-content">
            <h3>Get Multilingual Translations</h3>
            <p>Receive your product content translated into multiple Indian languages to help you reach customers across different regions. We currently support Hindi, Bengali, Tamil, Telugu, and more.</p>
        </div>
    </div>
    
    <div class="step-divider"></div>
    
    <div class="process-step">
        <div class="step-number">4</div>
        <div class="step-content">
            <h3>Use Across Platforms</h3>
            <p>Copy and use the generated content on e-commerce platforms like Amazon, Flipkart, or your own website. The content is optimized for search engines and customer engagement.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Login/Signup Modal
st.markdown("""
<div class="login-modal" id="loginModal" style="display: none;">
    <div class="modal-content">
        <button class="close-modal" onclick="closeLoginModal()">×</button>
        <h2 class="form-title">Login / Sign Up</h2>
        
        <input type="hidden" id="userType" value="buyer">
        
        <div class="user-type-selector">
            <div class="user-type-btn active" data-type="buyer" onclick="setUserType('buyer')">As Buyer</div>
            <div class="user-type-btn" data-type="seller" onclick="setUserType('seller')">As Seller</div>
        </div>
        
        <div class="form-group">
            <label class="form-label">Full Name</label>
            <input type="text" class="form-input" placeholder="Enter your full name">
        </div>
        
        <div class="form-group">
            <label class="form-label">Email Address</label>
            <input type="email" class="form-input" placeholder="Enter your email">
        </div>
        
        <div class="form-group">
            <label class="form-label">Phone Number</label>
            <input type="tel" class="form-input" placeholder="Enter your phone number">
        </div>
        
        <div class="form-group">
            <label class="form-label">State</label>
            <input type="text" class="form-input" placeholder="Enter your state">
        </div>
        
        <div class="form-group" id="birthDateField" style="display: none;">
            <label class="form-label">Date of Birth</label>
            <input type="date" class="form-input">
        </div>
        
        <button class="form-submit">Continue</button>
    </div>
</div>
""", unsafe_allow_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2023 MadebyNari | Empowering Indian Artisans</p>
    <p>Team Members: [Your Names Here]</p>
    <p>
        <a href="https://github.com/your-repo" style="color: #6a11cb; text-decoration: none; margin: 0 10px;">GitHub</a> | 
        <a href="https://linkedin.com" style="color: #6a11cb; text-decoration: none; margin: 0 10px;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Additional JavaScript for user type switching
switch_js = """
<script>
function setUserType(type) {
    document.querySelectorAll('.user-type-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-type="${type}"]`).classList.add('active');
    document.getElementById('userType').value = type;
    
    // Show/hide birth date field based on user type
    const birthDateField = document.getElementById('birthDateField');
    if (type === 'seller') {
        birthDateField.style.display = 'block';
    } else {
        birthDateField.style.display = 'none';
    }
}
</script>
"""

components.html(switch_js, height=0)