# frontend/app.py
import sys
import os
<<<<<<< HEAD

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from PIL import Image
import io
import base64
import time
import json
import random
from backend.services.listing import generate_listing
=======
>>>>>>> 13dbf0ddc2d78fe6ddcc130b043ce08e27332612

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
from PIL import Image
from backend.services.listing import generate_listing

<<<<<<< HEAD
# Set page configuration
st.set_page_config(
    page_title="MadebyNari - AI Assistant for Artisans",
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
    
    .secondary-btn {
        background-color: #FF6B6B !important;
    }
    
    .secondary-btn:hover {
        background-color: #FF8E8E !important;
    }
    
    /* Card styling */
    .card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .card-title {
        color: #6a11cb;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        color: #6a11cb;
        margin-bottom: 0.5rem;
        font-family: 'Playfair Display', serif;
    }
    
    .header p {
        color: #5F6368;
    }
    
    /* Language buttons */
    .lang-btn {
        padding: 0.5rem 1rem;
        background-color: white;
        border: 1px solid #DADCE0;
        border-radius: 20px;
        margin: 0 0.5rem 0.5rem 0;
        font-size: 0.9rem;
        cursor: pointer;
    }
    
    .lang-btn.active {
        background-color: #6a11cb;
        color: white;
        border-color: #6a11cb;
    }
    
    /* Mobile preview styling */
    .mobile-preview {
        width: 350px;
        border: 2px solid #ddd;
        border-radius: 20px;
        padding: 20px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .mobile-header {
        text-align: center;
        color: #333;
        font-size: 16px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    
    .mobile-image {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    
    .mobile-title {
        color: #222;
        margin-bottom: 10px;
        font-size: 18px;
        font-weight: bold;
    }
    
    .mobile-description {
        color: #555;
        font-size: 14px;
        line-height: 1.4;
        margin-bottom: 15px;
    }
    
    .mobile-price {
        color: #e67e22;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 15px;
    }
    
    .mobile-button {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        width: 100%;
        cursor: pointer;
        font-weight: bold;
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
        
        .mobile-preview {
            width: 300px;
            padding: 15px;
        }
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #6a11cb;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    /* Error message styling */
    .error-message {
        background-color: #ffebee;
        color: #c62828;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #c62828;
        margin: 15px 0;
    }
    
    .warning-message {
        background-color: #fff8e1;
        color: #f57c00;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f57c00;
        margin: 15px 0;
    }
    
    /* Toast notification */
    .toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #333;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: fadeIn 0.3s, fadeOut 0.3s 2.7s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    /* Translation tabs */
    .translation-tabs {
        display: flex;
        border-bottom: 1px solid #ddd;
        margin-bottom: 15px;
    }
    
    .tab {
        padding: 10px 20px;
        cursor: pointer;
        border-bottom: 3px solid transparent;
    }
    
    .tab.active {
        border-bottom: 3px solid #6a11cb;
        color: #6a11cb;
        font-weight: 500;
    }
    
    /* Copy button styling */
    .copy-btn {
        background-color: #34A853;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.9rem;
        margin-top: 10px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    
    .copy-btn:hover {
        background-color: #2E8B47;
    }
    
    /* Login/Signup section */
    .auth-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .auth-tabs {
        display: flex;
        margin-bottom: 20px;
        border-radius: 5px;
        overflow: hidden;
        border: 1px solid #ddd;
    }
    
    .auth-tab {
        flex: 1;
        padding: 10px;
        text-align: center;
        background-color: #f9f9f9;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .auth-tab.active {
        background-color: #6a11cb;
        color: white;
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
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #6a11cb;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sample data for demo
SAMPLE_PRODUCTS = {
    "Select a sample product": {"image": None, "description": ""},
    "Blue Pottery Vase": {
        "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cG90dGVyeXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
        "description": "Handmade blue pottery vase with traditional Indian patterns, crafted by skilled artisans."
    },
    "Handloom Saree": {
        "image": "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c2FyZWV8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
        "description": "Authentic handloom silk saree with intricate zari work and traditional designs."
    },
    "Terracotta Jewelry": {
        "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVycmFjb3R0YSUyMGpld2Vscnl8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
        "description": "Handcrafted terracotta jewelry with ethnic patterns and eco-friendly colors."
    }
}

# Initialize session state for fallback functionality
def init_session_state():
    if 'selected_lang' not in st.session_state:
        st.session_state.selected_lang = 'en'
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = None
    if 'image_uploaded' not in st.session_state:
        st.session_state.image_uploaded = False
    if 'last_successful_result' not in st.session_state:
        st.session_state.last_successful_result = None
    if 'backend_status' not in st.session_state:
        st.session_state.backend_status = "unknown"  # unknown, up, down
    if 'mobile_preview' not in st.session_state:
        st.session_state.mobile_preview = False
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'en'
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'
    if 'user_type' not in st.session_state:
        st.session_state.user_type = 'buyer'
    if 'demo_description' not in st.session_state:
        st.session_state.demo_description = ""

# Function to convert image to base64 for HTML display
def image_to_base64(image):
    try:
        if hasattr(image, 'read'):
            image.seek(0)
            img_bytes = image.read()
            return base64.b64encode(img_bytes).decode()
        else:
            # If it's already a bytes object
            return base64.b64encode(image).decode()
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return ""

# Function to show toast notification
def show_toast(message):
    st.markdown(f"""
    <div class="toast">
        {message}
    </div>
    """, unsafe_allow_html=True)
    # Use a small delay to allow the toast to be visible
    time.sleep(0.1)

# Function to format the backend response for the frontend
def format_backend_response(result):
    """Convert the backend response to the frontend format"""
    formatted = {
        "title": result.get("title", ""),
        "description": result.get("description", ""),
        "caption": result.get("vision", {}).get("caption", ""),
        "hashtags": "#" + " #".join(result.get("vision", {}).get("keywords", [])),
        "price_suggestion": result.get("suggested_price", ""),
        "bullet_points": result.get("bullets", []),
        "translations": {
            "hi": {
                "title": result.get("title", ""),
                "description": result.get("description", ""),
                "caption": result.get("vision", {}).get("caption", ""),
                "hashtags": "#" + " #".join(result.get("vision", {}).get("keywords", [])),
                "price_suggestion": result.get("suggested_price", ""),
                "bullet_points": result.get("bullets", [])
            }
        }
    }
    return formatted

# Login/Signup Section
def show_auth_section():
    st.markdown("""
    <div class="auth-container">
        <h2 style="text-align: center; color: #6a11cb; margin-bottom: 20px;">Login / Sign Up</h2>
        
        <div class="auth-tabs">
            <div class="auth-tab %s" onclick="setAuthTab('login')">Login</div>
            <div class="auth-tab %s" onclick="setAuthTab('signup')">Sign Up</div>
        </div>
    """ % (
        "active" if st.session_state.auth_tab == 'login' else "",
        "active" if st.session_state.auth_tab == 'signup' else ""
    ), unsafe_allow_html=True)
    
    if st.session_state.auth_tab == 'login':
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Email", key="login_email")
        with col2:
            st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            st.success("Login successful!")
            
    else:  # Sign up
        # User type selection
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <label class="form-label">I want to sign up as:</label>
            <div class="auth-tabs">
                <div class="auth-tab %s" onclick="setUserType('buyer')">Buyer</div>
                <div class="auth-tab %s" onclick="setUserType('seller')">Seller</div>
            </div>
        </div>
        """ % (
            "active" if st.session_state.user_type == 'buyer' else "",
            "active" if st.session_state.user_type == 'seller' else ""
        ), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", key="signup_name")
            st.text_input("Email", key="signup_email")
        with col2:
            st.text_input("Phone Number", key="signup_phone")
            st.text_input("State", key="signup_state")
        
        if st.session_state.user_type == 'seller':
            st.date_input("Date of Birth", key="signup_dob")
        
        st.text_input("Password", type="password", key="signup_password")
        st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        if st.button("Create Account", key="signup_btn"):
            st.success("Account created successfully!")
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Initialize session state
    init_session_state()
    
    # Add navigation to homepage
    st.sidebar.markdown("[← Back to Homepage](/)")
    
    # Header section
    st.markdown("""
    <div class="header">
        <h1>MadebyNari 🎨</h1>
        <p>Empowering local artisans with AI-powered tools to market their craft</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show login/signup section
    show_auth_section()
    
    # Create tabs for different functionalities
    tabs = st.tabs(["Product Listing", "Social Media", "Translation"])
    
    with tabs[0]:
        st.header("Product Listing — Upload image + short description")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Description input
            description = st.text_area(
                "Short description (what is the product, materials, any context):",
                value=st.session_state.get('demo_description', ''),
                height=140,
                help="Describe your product in your own words"
            )
            
            # File uploader
            image_file = st.file_uploader(
                "Upload product image (required for dynamic analysis)", 
                type=["png", "jpg", "jpeg"]
            )
            
            # Model selection
            model_choice = st.selectbox(
                "LLM model (OpenAI)", 
                ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"], 
                index=0
            )
            
            # Generate button
            if st.button("Generate Dynamic Listing"):
                if not description:
                    st.error("Please add a short description.")
                elif not image_file:
                    st.error("Please upload an image for dynamic analysis.")
                else:
                    with st.spinner("Analyzing image and generating listing..."):
                        try:
                            # Read image bytes
                            image_bytes = image_file.read()
                            
                            # Call the backend service
                            result = generate_listing(description, image_bytes, model=model_choice)
                            
                            # Format the result for frontend display
                            formatted_result = format_backend_response(result)
                            
                            # Store the result
                            st.session_state.generated_content = formatted_result
                            st.session_state.last_successful_result = formatted_result
                            st.session_state.image_uploaded = True
                            
                            # Display the results
                            st.subheader(result.get("title", ""))
                            
                            # Bullet points
                            st.markdown("**Key Features**")
                            for bullet in result.get("bullets", []):
                                st.write(f"- {bullet}")
                            
                            # Price information
                            col_price1, col_price2 = st.columns(2)
                            with col_price1:
                                st.markdown("**Price from model**")
                                st.write(result.get("price", "N/A"))
                            with col_price2:
                                st.markdown("**Suggested price**")
                                st.write(result.get("suggested_price", "N/A"))
                            
                            # Origin information
                            st.markdown("**Origin hint**")
                            st.write(result.get("origin_hint", "No specific origin detected"))
                            
                            # Vision analysis
                            st.markdown("**Vision analysis**")
                            st.write(result.get("vision", {}).get("caption", ""))
                            
                            # Keywords
                            st.markdown("**Keywords**")
                            st.write(", ".join(result.get("vision", {}).get("keywords", [])))
                            
                            # Dominant color
                            st.markdown("**Dominant color**")
                            st.write(result.get("vision", {}).get("dominant_color", ""))
                            
                            # Recommendations
                            st.markdown("**Artisan recommendations**")
                            for rec in result.get("recommendations", []):
                                st.write(f"- {rec}")
                                
                            # Image fix suggestions
                            st.markdown("**Image improvement suggestions**")
                            for fix in result.get("image_fix_suggestions", []):
                                st.write(f"- {fix}")
                                
                            # Debug information
                            if st.checkbox("Show raw model output (for debugging)"):
                                st.code(result.get("_raw_model_output", ""), language="json")
                                st.code(result.get("_raw_recommendations_output", ""))
                                
                        except Exception as e:
                            st.error(f"Error generating listing: {str(e)}")
                            st.info("Please check that the backend service is running properly.")
        
        with col2:
            st.info("""
            **Tips:**
            - Provide a concise description mentioning material if possible.
            - High-quality, well-lit photos produce better captions and recommendations.
            """)
            
            if st.button("Example test data"):
                st.session_state.demo_description = "Handmade blue pottery vase, floral motifs, glossy finish."
                st.rerun()
                
            # Show image preview if uploaded
            if image_file is not None:
                st.image(Image.open(image_file), caption="Uploaded Image", use_column_width=True)
    
    with tabs[1]:
        st.header("Social Media Generator")
        st.write("Generate social media content from your product listings")
        
        if st.session_state.generated_content:
            st.subheader("Social Media Content")
            st.text_area("Caption", st.session_state.generated_content.get("caption", ""), height=100)
            st.text_area("Hashtags", st.session_state.generated_content.get("hashtags", ""), height=60)
            
            if st.button("Copy Social Content"):
                show_toast("Social content copied to clipboard!")
        else:
            st.info("Generate a product listing first to see social media content here.")
    
    with tabs[2]:
        st.header("Multilingual Translation")
        st.write("Translate your product content into multiple languages")
        
        if st.session_state.generated_content:
            # Language selection
            languages = ["Hindi", "Bengali", "Tamil", "Telugu", "Gujarati", "Marathi"]
            selected_languages = st.multiselect(
                "Select languages for translation",
                options=languages,
                default=["Hindi", "Bengali", "Tamil"]
            )
            
            # Display translations
            for lang in selected_languages:
                with st.expander(f"{lang} Translation"):
                    # For demo purposes, we'll just show the English content
                    # In a real implementation, you would call a translation API
                    st.write("**Title:**", st.session_state.generated_content.get("title", ""))
                    st.write("**Description:**", st.session_state.generated_content.get("description", ""))
                    st.write("**Caption:**", st.session_state.generated_content.get("caption", ""))
                    
                    if st.button(f"Copy {lang} Translation", key=f"copy_{lang}"):
                        show_toast(f"{lang} translation copied to clipboard!")
        else:
            st.info("Generate a product listing first to see translations here.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #5F6368;">
        <p>MadebyNari - Empowering Indian Artisans with AI</p>
        <p>Built with ❤️ for Google Gen AI Exchange Hackathon</p>
    </div>
    """, unsafe_allow_html=True)

# JavaScript for authentication tabs
auth_js = """
<script>
function setAuthTab(tab) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {auth_tab: tab}
    }, '*');
}

function setUserType(type) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {user_type: type}
    }, '*');
}
</script>
"""

st.components.v1.html(auth_js, height=0)

if __name__ == "__main__":
    main()
=======
st.set_page_config(page_title="Artisan AI — Dynamic MVP", layout="centered")
st.title("Artisan AI — Dynamic Product Listing (MVP → dynamic)")

tabs = st.tabs(["Product Listing", "Social (MVP)", "Translation (MVP)"])

with tabs[0]:
    st.header("Product Listing — Upload image + short description")
    col1, col2 = st.columns([2,1])
    with col1:
        description = st.text_area("Short description (what is the product, materials, any context):", height=140)
        image_file = st.file_uploader("Upload product image (required for dynamic analysis)", type=["png","jpg","jpeg"])
        model_choice = st.selectbox("LLM model (OpenAI)", ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"], index=0)
        if st.button("Generate Dynamic Listing"):
            if not description:
                st.error("Please add a short description.")
            elif not image_file:
                st.error("Please upload an image for dynamic analysis.")
            else:
                with st.spinner("Analyzing image and generating listing..."):
                    image_bytes = image_file.read()
                    result = generate_listing(description, image_bytes, model=model_choice)
                    # display
                    st.subheader(result.get("title",""))
                    st.markdown("**Bullets**")
                    for b in result.get("bullets", []):
                        st.write("- " + b)
                    st.markdown("**Price from model**")
                    st.write(result.get("price"))
                    st.markdown("**Price (heuristic suggestion)**")
                    st.write(result.get("suggested_price"))
                    st.markdown("**Origin hint**")
                    st.write(result.get("origin_hint") or "No specific origin detected")
                    st.markdown("**Vision caption (what image model saw)**")
                    st.write(result.get("vision", {}).get("caption",""))
                    st.markdown("**Vision keywords**")
                    st.write(", ".join(result.get("vision", {}).get("keywords", [])))
                    st.markdown("**Dominant color**")
                    st.write(result.get("vision", {}).get("dominant_color",""))
                    st.markdown("**Artisan recommendations (how to increase value)**")
                    for r in result.get("recommendations", []):
                        st.write("- " + r)
                    st.markdown("**Image fix suggestions (what to improve in image/product)**")
                    for f in result.get("image_fix_suggestions", []):
                        st.write("- " + f)
                    if st.checkbox("Show raw model output (for debugging)"):
                        st.code(result.get("_raw_model_output",""), language="json")
                        st.code(result.get("_raw_recommendations_output",""))

    with col2:
        st.info("Tips:\n- Provide a concise description mentioning material if possible.\n- High-quality, well-lit photos produce better captions and recommendations.")
        if st.button("Example test data"):
            st.session_state['demo_description'] = "Handmade blue pottery vase, floral motifs, glossy finish."
            st.experimental_rerun()

with tabs[1]:
    st.header("Social Media Generator (MVP)")
    st.write("Use your existing social flow (this tab is placeholder)")

with tabs[2]:
    st.header("Multilingual Translation (MVP)")
    st.write("Use your existing translate flow (this tab is placeholder)")

>>>>>>> 3487404 (Updated project with latest fixes and API changes)
