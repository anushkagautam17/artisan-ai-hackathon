# frontend/app.py
import sys
import os
import streamlit as st
from PIL import Image
import base64
import time
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="MadebyNaari - AI Assistant for Artisans",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-friendly design and styling
st.markdown("""
<style>
    /* Main styles */
    .main {
        padding: 2rem 1rem;
    }
    
    .stButton button {
        width: 100%;
        background-color: #6a11cb;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .stButton button:hover {
        background-color: #2575fc;
        color: white;
    }
    
    /* Card styling */
    .card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #6a11cb;
    }
    
    .social-card {
        border-left: 4px solid #FF6B6B;
    }
    
    .translation-card {
        border-left: 4px solid #4CAF50;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        color: #6a11cb;
        margin-bottom: 0.5rem;
    }
    
    /* Feature badges */
    .feature-badge {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main {
            padding: 1rem 0.5rem;
        }
        
        .header h1 {
            font-size: 1.75rem;
        }
        
        .card {
            padding: 1rem;
        }
    }
    
    /* Status indicators */
    .status-connected {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #2e7d32;
        margin: 10px 0;
    }
    
    .status-disconnected {
        background-color: #ffebee;
        color: #c62828;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #c62828;
        margin: 10px 0;
    }
    
    /* Platform badges */
    .platform-badge {
        display: inline-block;
        background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .whatsapp-badge {
        background: linear-gradient(45deg, #25D366, #128C7E);
    }
    
    /* Language buttons */
    .lang-btn {
        padding: 0.5rem 1rem;
        background-color: white;
        border: 2px solid #6a11cb;
        border-radius: 25px;
        margin: 0 0.5rem 0.5rem 0;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .lang-btn.active {
        background-color: #6a11cb;
        color: white;
    }
    
    .lang-btn:hover {
        background-color: #2575fc;
        color: white;
        border-color: #2575fc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = None
    if 'image_uploaded' not in st.session_state:
        st.session_state.image_uploaded = False
    if 'demo_description' not in st.session_state:
        st.session_state.demo_description = ""
    if 'backend_status' not in st.session_state:
        st.session_state.backend_status = "unknown"
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "en"
    if 'social_content' not in st.session_state:
        st.session_state.social_content = None
    if 'selected_platform' not in st.session_state:
        st.session_state.selected_platform = "instagram"
    if 'page' not in st.session_state:
        st.session_state.page = "home"

# Function to check backend connection
def check_backend_connection():
    """Check if backend is available"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, {"error": f"Backend returned status {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Cannot connect to backend: {e}"}

# Function to call backend API
def call_backend_api(description, image_file=None, target_lang="en", endpoint="generate"):
    """Call the backend API for different functionalities"""
    try:
        backend_url = f"http://localhost:8000/{endpoint}"
        
        files = {}
        data = {"description": description, "target_lang": target_lang}
        
        if image_file and endpoint == "generate":
            files = {"image": (image_file.name, image_file.getvalue(), image_file.type)}
        
        response = requests.post(backend_url, files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return None

# Function to generate social media content
def generate_social_media_content(product_data, platform="instagram"):
    """Generate platform-specific social media content"""
    title = product_data.get("title", "")
    description = product_data.get("description", "")
    bullets = product_data.get("bullets", [])
    price = product_data.get("price", "")
    origin = product_data.get("origin_hint", "Handcrafted in India")
    
    if platform == "instagram":
        caption = f"✨ {title} ✨\n\n"
        caption += f"{description}\n\n"
        
        caption += "🌟 **Key Features:**\n"
        for i, bullet in enumerate(bullets[:4], 1):
            caption += f"{i}️⃣ {bullet}\n"
        
        caption += f"\n💰 **Price:** {price}\n"
        caption += f"📍 **Origin:** {origin}\n\n"
        
        caption += "🎯 **Perfect For:**\n"
        caption += "• Home decoration 🏠\n"
        caption += "• Gift giving 🎁\n"
        caption += "• Cultural enthusiasts 🪷\n\n"
        
        caption += "#Handmade #Artisan #SupportLocal #IndianCraft #Handcrafted #MadeInIndia #Sustainable #EthicalFashion #LocalArtisans #CraftRevival"
        
        return caption
        
    elif platform == "whatsapp":
        message = f"*{title}*\n\n"
        message += f"{description}\n\n"
        
        message += "*🌟 Key Features:*\n"
        for bullet in bullets[:4]:
            message += f"• {bullet}\n"
        
        message += f"\n*💰 Price:* {price}\n"
        message += f"*📍 Origin:* {origin}\n\n"
        
        message += "*🎯 Perfect For:*\n"
        message += "• Home decoration 🏠\n"
        message += "• Gift giving 🎁\n"
        message += "• Cultural enthusiasts 🪷\n\n"
        
        message += "_#Handmade #Artisan #SupportLocal_"
        
        return message
    
    return ""

# Function to translate content via backend
def translate_content_via_api(text, target_lang):
    """Call backend for translation"""
    if target_lang == "en":
        return text
    
    try:
        # This endpoint should be implemented in your backend
        response = requests.post(
            "http://localhost:8000/translate",
            json={"text": text, "target_lang": target_lang},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("translated_text", text)
    except:
        pass
    
    # Fallback mock translations
    mock_translations = {
        "hi": {
            "Handcrafted Blue Pottery Vase": "हस्तनिर्मित नीला मिट्टी का फूलदान",
            "Beautiful handmade blue pottery vase": "सुंदर हस्तनिर्मित नीला मिट्टी का फूलदान",
            "Perfect for home decor or as a gift": "घर की सजावट या उपहार के लिए आदर्श",
            "₹1,200 - ₹1,500": "₹1,200 - ₹1,500"
        },
        "bn": {
            "Handcrafted Blue Pottery Vase": "হস্তনির্মিত নীল মৃৎশিল্পের ফুলদানি",
            "Beautiful handmade blue pottery vase": "সুন্দর হস্তনির্মিত নীল মৃৎশিল্পের ফুলদানি", 
            "Perfect for home decor or as a gift": "বাড়ির সাজসজ্জা বা উপহারের জন্য উপযুক্ত",
            "₹1,200 - ₹1,500": "₹1,200 - ₹1,500"
        }
    }
    
    return mock_translations.get(target_lang, {}).get(text, text)

# Mock function for fallback
def mock_generate_listing(description, image_bytes=None):
    return {
        "title": "Handcrafted Blue Pottery Vase",
        "description": "Beautiful handmade blue pottery vase with traditional floral motifs and glossy finish. Perfect for home decor or as a gift.",
        "price": "₹1,200 - ₹1,500",
        "suggested_price": "₹1,350",
        "bullets": [
            "Handcrafted by skilled artisans using traditional techniques",
            "Made from high-quality clay with eco-friendly glaze",
            "Unique floral patterns inspired by traditional Indian art",
            "Perfect for home decoration or as a thoughtful gift"
        ],
        "origin_hint": "Rajasthan, India - known for blue pottery",
        "vision": {
            "caption": "A blue ceramic vase with floral patterns on a wooden table",
            "keywords": ["blue", "vase", "pottery", "floral", "handmade", "ceramic"],
            "dominant_color": "Blue"
        },
        "recommendations": [
            "Include more lighting to showcase the glaze better",
            "Add a photo with a common object for scale (like a coin or hand)",
            "Show the vase from multiple angles"
        ],
        "image_fix_suggestions": [
            "Use natural light to reduce shadows",
            "Capture the intricate details up close"
        ]
    }

# About section function
def about_section():
    st.header("About MadebyNaari")
    st.write("""
    MadebyNaari is a revolutionary platform designed to empower women artisans across India 
    to thrive in the digital marketplace. We bridge the gap between traditional craftsmanship 
    and modern e-commerce while specifically addressing the unique challenges faced by women 
    in artisan communities.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Challenges Women Artisans Face")
        st.markdown("""
        - Difficulty creating professional product descriptions
        - Language barriers in reaching diverse markets
        - Limited digital marketing knowledge
        - Time-consuming content creation process
        - Limited reach to global customers
        - Additional societal barriers to market access
        """)
    
    with col2:
        st.subheader("How MadebyNaari Helps")
        st.markdown("""
        - AI-powered product description generation
        - Multi-language translation support
        - Social media ready content creation
        - Simple, intuitive interface designed for all skill levels
        - Global marketplace access specifically for women artisans
        - Community support and networking opportunities
        """)
    
    st.info("""
    *"Our mission is to preserve traditional crafts while empowering women artisans with modern technology. 
    We believe every handmade product tells a story, and every woman artisan deserves the opportunity 
    to share hers with the world."*
    """)

def home_page():
    """Main home page content"""
    # Header section
    st.markdown("""
    <div class="header">
        <h1>MadebyNaari 🎨</h1>
        <p>Empowering local artisans with AI-powered tools to market their craft</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Backend status
    connected, status = check_backend_connection()
    if connected:
        st.markdown('<div class="status-connected">✅ Connected to AI backend</div>', unsafe_allow_html=True)
        st.session_state.backend_status = "connected"
    else:
        st.markdown(f"""
        <div class="status-disconnected">
            ⚠️ Backend not connected. Using demo mode. 
            <br>Make sure backend is running: <code>cd backend && uvicorn main:app --reload</code>
            <br>Error: {status.get('error', 'Unknown error')}
        </div>
        """, unsafe_allow_html=True)
        st.session_state.backend_status = "disconnected"
    
    # Create tabs for each feature
    tab1, tab2, tab3 = st.tabs([
        "🏪 Product Listing", 
        "📱 Social Media", 
        "🌍 Multilingual"
    ])
    
    # TAB 1: PRODUCT LISTING
    with tab1:
        st.markdown('<span class="feature-badge">AI Marketplace Ready</span>', unsafe_allow_html=True)
        st.header("Create Perfect Product Listings")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            description = st.text_area(
                "Describe your product:",
                value=st.session_state.get('demo_description', ''),
                height=100,
                placeholder="Handmade blue pottery vase with traditional patterns...",
                help="Be specific about materials, craftsmanship, and unique features"
            )
            
            image_file = st.file_uploader(
                "Upload product photo", 
                type=["png", "jpg", "jpeg"],
                help="Clear, well-lit photos work best for AI analysis"
            )
            
            if st.button("✨ Generate Listing", type="primary"):
                if not description:
                    st.error("Please describe your product first")
                else:
                    with st.spinner("🧠 AI is creating your perfect listing..."):
                        # Try to call real backend API
                        result = call_backend_api(description, image_file)
                        
                        if result is None:
                            # Fallback to mock data
                            st.warning("Using demo data - connect backend for AI-powered results")
                            result = mock_generate_listing(description)
                        
                        st.session_state.generated_content = result
                        st.rerun()
        
        with col2:
            st.info("""
            **💡 Pro Tips:**
            - Mention materials (clay, silk, wood, etc.)
            - Describe craftsmanship techniques
            - Include size/dimensions if possible
            - Highlight unique cultural elements
            """)
            
            if st.button("📋 Load Example"):
                st.session_state.demo_description = "Handmade blue pottery vase, floral motifs, glossy finish, 12-inch height, traditional Rajasthani art"
                st.rerun()
                
            if image_file:
                st.image(Image.open(image_file), caption="Your Product", use_container_width=True)
        
        # Display generated content
        if st.session_state.generated_content:
            content = st.session_state.generated_content
            
            st.markdown("---")
            st.subheader("🎯 Generated Product Listing")
            
            # Title and Description
            st.markdown(f"**{content.get('title', '')}**")
            st.write(content.get('description', ''))
            
            # Features
            st.markdown("**🌟 Key Features:**")
            for bullet in content.get('bullets', []):
                st.write(f"• {bullet}")
            
            # Pricing
            col_price1, col_price2 = st.columns(2)
            with col_price1:
                st.metric("💰 Price Range", content.get('price', ''))
            with col_price2:
                st.metric("💎 Suggested Price", content.get('suggested_price', ''))
            
            # Additional info
            if content.get('origin_hint'):
                st.info(f"**📍 Origin:** {content.get('origin_hint')}")
            
            if content.get('recommendations'):
                with st.expander("💡 AI Recommendations"):
                    for rec in content.get('recommendations', []):
                        st.write(f"• {rec}")
    
    # TAB 2: SOCIAL MEDIA
    with tab2:
        st.markdown('<span class="feature-badge">Auto Social Posts</span>', unsafe_allow_html=True)
        st.header("Social Media Content Generator")
        
        if not st.session_state.generated_content:
            st.info("👆 Generate a product listing first to create social media content")
        else:
            st.success("Ready to create social media posts!")
            
            # Platform selection
            platform = st.radio("Choose platform:", ["Instagram", "WhatsApp"], 
                               horizontal=True, key="platform_selector")
            
            st.session_state.selected_platform = platform.lower()
            
            # Generate platform-specific content
            social_content = generate_social_media_content(
                st.session_state.generated_content, 
                st.session_state.selected_platform
            )
            
            st.session_state.social_content = social_content
            
            # Display platform badge
            if st.session_state.selected_platform == "instagram":
                st.markdown('<span class="platform-badge">Instagram</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="platform-badge whatsapp-badge">WhatsApp</span>', unsafe_allow_html=True)
            
            # Display content
            st.text_area(
                f"{platform} Content:", 
                social_content,
                height=250 if st.session_state.selected_platform == "instagram" else 200,
                help="Copy this content for your social media posts"
            )
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy to Clipboard", key="copy_btn"):
                    st.success("Content copied! Ready to paste on social media")
            with col2:
                if st.button("🔄 Regenerate", key="regenerate_btn"):
                    with st.spinner("Creating fresh content..."):
                        new_content = generate_social_media_content(
                            st.session_state.generated_content, 
                            st.session_state.selected_platform
                        )
                        st.session_state.social_content = new_content
                        st.rerun()
            
            # Platform tips
            with st.expander(f"💡 {platform} Best Practices"):
                if platform == "Instagram":
                    st.write("""
                    - Use high-quality images/videos
                    - Post during peak hours (7-9 PM)
                    - Use 5-10 relevant hashtags
                    - Engage with comments quickly
                    - Use Instagram Stories for behind-the-scenes
                    """)
                else:
                    st.write("""
                    - Personalize messages for customers
                    - Share clear product photos
                    - Include pricing and availability
                    - Respond promptly to inquiries
                    - Use WhatsApp Business features
                    """)
    
    # TAB 3: MULTILINGUAL
    with tab3:
        st.markdown('<span class="feature-badge">Vernacular Translations</span>', unsafe_allow_html=True)
        st.header("Multilingual Support")
        
        if not st.session_state.generated_content:
            st.info("👆 Generate a product listing first to see translations")
        else:
            # Language selection
            st.write("Select language for translation:")
            
            languages = [
                ("English", "en"), ("Hindi", "hi"), 
                ("Bengali", "bn"), ("Tamil", "ta"), ("Telugu", "te")
            ]
            
            # Create interactive language buttons
            cols = st.columns(5)
            for i, (lang_name, lang_code) in enumerate(languages):
                with cols[i]:
                    is_active = st.session_state.selected_language == lang_code
                    button_style = "primary" if is_active else "secondary"
                    if st.button(lang_name, key=f"lang_{lang_code}", type=button_style):
                        st.session_state.selected_language = lang_code
                        st.rerun()
            
            # Display translated content
            current_lang = st.session_state.selected_language
            st.markdown(f"**Showing content in: {[name for name, code in languages if code == current_lang][0]}**")
            
            content = st.session_state.generated_content
            
            if current_lang == "en":
                # Show original English content
                translated_title = content.get("title", "")
                translated_desc = content.get("description", "")
                translated_price = content.get("price", "")
            else:
                # Show translated content
                with st.spinner(f"Translating to {current_lang}..."):
                    translated_title = translate_content_via_api(content.get("title", ""), current_lang)
                    translated_desc = translate_content_via_api(content.get("description", ""), current_lang)
                    translated_price = translate_content_via_api(content.get("price", ""), current_lang)
            
            st.markdown(f"**{translated_title}**")
            st.write(translated_desc)
            st.info(f"**Price:** {translated_price}")
            
            # Translation status
            if current_lang != "en":
                st.warning("⚠️ Using demo translations. Connect backend for real AI translations!")

def main():
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("MadebyNaari 🎨")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio("Navigate to:", ["Home", "About", "Generator"])
    
    # Connection status in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Connection Status")
    
    if st.sidebar.button("Check Backend Connection"):
        with st.sidebar:
            with st.spinner("Checking connection..."):
                connected, status = check_backend_connection()
                if connected:
                    st.success("✅ Backend connected successfully!")
                    st.json(status)
                else:
                    st.error("❌ Backend connection failed")
                    st.error(status.get("error", "Unknown error"))
    
    # Page routing
    if page == "Home":
        home_page()
    elif page == "About":
        about_section()
    elif page == "Generator":
        st.switch_page("pages/generator.py")

if __name__ == "__main__":
    main()