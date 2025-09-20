# frontend/app.py
import sys
import os
import streamlit as st
from PIL import Image
import base64
import time

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    
    /* Card styling */
    .card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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

# Mock function for listing generation (since backend might not be working)
def mock_generate_listing(description, image_bytes, model="gpt-3.5-turbo"):
    """Mock function that simulates the backend service"""
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

def main():
    # Initialize session state
    init_session_state()
    
    # Header section
    st.markdown("""
    <div class="header">
        <h1>MadebyNari 🎨</h1>
        <p>Empowering local artisans with AI-powered tools to market their craft</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
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
                "Upload product image", 
                type=["png", "jpg", "jpeg"]
            )
            
            # Generate button
            if st.button("Generate Listing"):
                if not description:
                    st.error("Please add a short description.")
                else:
                    with st.spinner("Generating listing..."):
                        try:
                            # Try to import the actual backend service
                            try:
                                from backend.services.listing import generate_listing
                                if image_file:
                                    image_bytes = image_file.read()
                                    result = generate_listing(description, image_bytes)
                                else:
                                    result = generate_listing(description, None)
                            except ImportError:
                                # Fallback to mock data if backend not available
                                st.warning("Backend service not available. Using demo data.")
                                result = mock_generate_listing(description, None)
                            
                            # Store the result
                            st.session_state.generated_content = result
                            st.session_state.image_uploaded = image_file is not None
                            
                            # Display results
                            st.subheader(result.get("title", ""))
                            
                            st.markdown("**Key Features**")
                            for bullet in result.get("bullets", []):
                                st.write(f"- {bullet}")
                            
                            col_price1, col_price2 = st.columns(2)
                            with col_price1:
                                st.markdown("**Price**")
                                st.write(result.get("price", "N/A"))
                            with col_price2:
                                st.markdown("**Suggested price**")
                                st.write(result.get("suggested_price", "N/A"))
                            
                            if result.get("origin_hint"):
                                st.markdown("**Origin**")
                                st.write(result.get("origin_hint"))
                            
                            if image_file:
                                st.markdown("**Image Analysis**")
                                st.write(result.get("vision", {}).get("caption", ""))
                                
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                            st.info("Please ensure the backend server is running.")
        
        with col2:
            st.info("""
            **Tips:**
            - Provide a concise description mentioning material if possible.
            - High-quality, well-lit photos produce better results.
            """)
            
            if st.button("Load Example"):
                st.session_state.demo_description = "Handmade blue pottery vase, floral motifs, glossy finish."
                st.rerun()
                
            if image_file:
                st.image(Image.open(image_file), caption="Uploaded Image", use_container_width=True)
    
    with tabs[1]:
        st.header("Social Media Generator")
        if st.session_state.generated_content:
            content = st.session_state.generated_content
            st.text_area("Social Media Caption", 
                        f"{content.get('title', '')}\n\n{content.get('description', '')}\n\n#Handmade #Artisan #Craft",
                        height=150)
        else:
            st.info("Generate a product listing first to see social media content.")
    
    with tabs[2]:
        st.header("Multilingual Translation")
        if st.session_state.generated_content:
            st.info("Translation feature would be implemented here with proper backend integration.")
        else:
            st.info("Generate a product listing first to see translations.")

if __name__ == "__main__":
    main()