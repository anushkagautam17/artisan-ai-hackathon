# frontend/Home.py
import streamlit as st
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(
    page_title="Artisan Booster - Empowering Indian Artisans with AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 80px 0;
        color: white;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 40px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        margin-bottom: 30px;
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
    }
    
    .step-card {
        background-color: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .step-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        color: #6a11cb;
    }
    
    .step-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 15px;
        color: #333;
    }
    
    .step-description {
        color: #666;
        line-height: 1.6;
    }
    
    .footer {
        background-color: #f8f9fa;
        padding: 40px 0;
        margin-top: 60px;
        text-align: center;
        color: #666;
    }
    
    .demo-container {
        background-color: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 40px;
    }
    
    .about-section {
        background-color: #f8f9fa;
        padding: 60px 0;
        border-radius: 15px;
        margin: 40px 0;
    }
    
    .navbar {
        background-color: white;
        padding: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
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
    }
    
    .nav-menu {
        display: flex;
        list-style: none;
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
        
        .step-card {
            margin-bottom: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar
st.markdown("""
<div class="navbar">
    <div class="nav-container">
        <div class="logo">Artisan Booster</div>
        <ul class="nav-menu">
            <li class="nav-item"><a href="#" class="nav-link">Home</a></li>
            <li class="nav-item"><a href="#about" class="nav-link">About</a></li>
            <li class="nav-item"><a href="#how-it-works" class="nav-link">How It Works</a></li>
            <li class="nav-item"><a href="#demo" class="nav-link">Demo</a></li>
            <li class="nav-item"><a href="/app" class="nav-link">Try It</a></li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Empowering Indian Artisans with AI</h1>
    <p class="hero-subtitle">Upload artisan product images and instantly generate titles, captions, and translations to reach global customers.</p>
    <a href="/app" class="cta-button">👉 Try It Now</a>
</div>
""", unsafe_allow_html=True)

# How It Works Section
st.markdown('<h2 class="section-title" id="how-it-works">How It Works</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-icon">📸</div>
        <h3 class="step-title">Upload Image</h3>
        <p class="step-description">Upload a picture of your artisan product - pottery, handloom, jewelry, or any handmade item.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-icon">🤖</div>
        <h3 class="step-title">AI Generates Info</h3>
        <p class="step-description">Our AI automatically creates compelling titles, descriptions, and captions for your product.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-icon">🌍</div>
        <h3 class="step-title">Get Translations</h3>
        <p class="step-description">Receive your content translated into multiple languages to reach global customers.</p>
    </div>
    """, unsafe_allow_html=True)

# Demo Section
st.markdown('<h2 class="section-title" id="demo">See It In Action</h2>', unsafe_allow_html=True)
st.markdown("""
<div class="demo-container">
    <p style="text-align: center; margin-bottom: 20px;">See how AI helps artisans showcase their products to a global audience.</p>
    <div style="text-align: center;">
        <img src="https://via.placeholder.com/800x450?text=Artisan+Booster+Demo+Video+or+Screenshot" alt="Demo" style="max-width: 100%; border-radius: 10px;">
    </div>
</div>
""", unsafe_allow_html=True)

# About Section
st.markdown("""
<div class="about-section" id="about">
    <h2 class="section-title">Our Mission</h2>
    <p style="text-align: center; font-size: 1.2rem; max-width: 800px; margin: 0 auto; line-height: 1.6;">
        Our mission is to bridge the gap between artisans and global markets by using AI to make product listings easier, faster, and multilingual. We believe in preserving traditional crafts while empowering artisans with modern technology.
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2023 Artisan Booster | Created for the Hackathon</p>
    <p>Team Members: [Your Names Here]</p>
    <p>
        <a href="https://github.com/your-repo" style="color: #6a11cb; text-decoration: none; margin: 0 10px;">GitHub</a> | 
        <a href="https://linkedin.com" style="color: #6a11cb; text-decoration: none; margin: 0 10px;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)