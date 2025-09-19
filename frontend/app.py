import streamlit as st
import requests
from PIL import Image
import io
import base64
import time
import json
import random

# Set page configuration
st.set_page_config(
    page_title="ArtisanAI - Marketplace Assistant",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"  # Changed to expanded for better UX
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
        background-color: #4285F4;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .stButton button:hover {
        background-color: #3367D6;
        color: white;
    }
    
    .secondary-btn {
        background-color: #F4B400 !important;
    }
    
    .secondary-btn:hover {
        background-color: #E4A500 !important;
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
        color: #4285F4;
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
        color: #4285F4;
        margin-bottom: 0.5rem;
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
        background-color: #4285F4;
        color: white;
        border-color: #4285F4;
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
        border-top: 4px solid #4285F4;
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
</style>
""", unsafe_allow_html=True)

# Sample data for demo
SAMPLE_PRODUCTS = {
    "Select a sample product": {"image": None, "description": ""},
    "Blue Pottery Vase": {
        "image": "sample_images/pottery.jpg",
        "description": "Handmade blue pottery vase with traditional Indian patterns, crafted by skilled artisans."
    },
    "Handloom Saree": {
        "image": "sample_images/saree.jpg",
        "description": "Authentic handloom silk saree with intricate zari work and traditional designs."
    },
    "Terracotta Jewelry": {
        "image": "sample_images/jewelry.jpg",
        "description": "Handcrafted terracotta jewelry with ethnic patterns and eco-friendly colors."
    }
}

# Mock response data for demonstration
MOCK_RESPONSE = {
    "title": "Handmade Blue Pottery Vase with Traditional Indian Patterns",
    "description": "This exquisite handmade blue pottery vase features traditional Indian patterns, meticulously crafted by skilled artisans. Each piece is unique, showcasing the rich cultural heritage of Indian pottery. Perfect for home decoration or as a special gift, this vase adds an elegant touch to any space.",
    "caption": "Discover the beauty of traditional Indian craftsmanship with this handmade blue pottery vase! Each piece tells a story of cultural heritage and artisan skill. Perfect addition to your home decor or as a unique gift. 🏺✨",
    "hashtags": "#HandmadePottery #IndianArtisans #BluePottery #TraditionalCraft #ArtisanMade #HomeDecor #SupportArtisans #MadeInIndia #CraftHeritage #PotteryLover",
    "translations": {
        "hi": {
            "title": "हस्तनिर्मित नीला मिट्टी का फूलदान पारंपरिक भारतीय नमूनों के साथ",
            "description": "यह उत्कृष्ट हस्तनिर्मित नीला मिट्टी का फूलदान पारंपरिक भारतीय नमूनों से सुशोभित है, जिसे कुशल कारीगरों द्वारा सावधानीपूर्वक तैयार किया गया है। प्रत्येक टुकड़ा अनूठा है, जो भारतीय मिट्टी के बर्तनों की समृद्ध सांस्कृतिक विरासत को प्रदर्शित करता है।",
            "caption": "पारंपरिक भारतीय शिल्प कौशल की सुंदरता की खोज इस हस्तनिर्मित नीले मिट्टी के फूलदान के साथ करें! प्रत्येक टुकड़ा सांस्कृतिक विरासत और कारीगर कौशल की कहानी कहता है।",
            "hashtags": "#हस्तनिर्मितमिट्टीकेबर्तन #भारतीयकारीगर #नीलामिट्टीकेबर्तन #पारंपरिकशिल्प #कारीगरनिर्मित #घरकीसजावट #कारीगरोंकासमर्थन #भारतमेंनिर्मित #शिल्पविरासत #मिट्टीकेबर्तनप्रेमी"
        },
        "bn": {
            "title": "প্রথাগত ভারতীয় নকশা সহ হস্তনির্মিত নীল মৃৎশিল্পের ফুলদানি",
            "description": "এই অত্যুৎকৃষ্ট হস্তনির্মিত নীল মৃৎশিল্পের ফুলদানিটি প্রথাগত ভারতীয় নকশায় সজ্জিত, যা দক্ষ কারিগরদের দ্বারা সযত্নে তৈরি করা হয়েছে। প্রতিটি টুকরা অনন্য, যা ভারতীয় মৃৎশিল্পের সমৃদ্ধ সাংস্কৃতিক heritage প্রদর্শন করে।",
            "caption": "এই হস্তনির্মিত নীল মৃৎশিল্পের ফুলদানির সাথে প্রথাগত ভারতীয় কারুশিল্পের সৌন্দর্য আবিষ্কার করুন! প্রতিটি টুকরা সাংস্কৃতিক heritage এবং কারিগর দক্ষতার গল্প বলে।",
            "hashtags": "#হস্তনির্মিতমৃৎশিল্প #ভারতীয়কারিগর #নীলমৃৎশিল্প #প্রথাগতশিল্প #কারিগরনির্মিত #হোমডেকর #কারিগরসমর্থন #ভারততৈরি #শিল্পঐতিহ্য #মৃৎশিল্পপ্রেমী"
        },
        "ta": {
            "title": "பாரம்பரிய இந்திய வடிவங்களுடன் கைவினை நீல மட்பாண்ட குவளை",
            "description": "இந்த அருமையான கைவினை நீல மட்பாண்ட குவளை பாரம்பரிய இந்திய வடிவங்களுடன் அலங்கரிக்கப்பட்டுள்ளது, இது திறமையான கைவினைஞர்களால் கவனமாக crafted உருவாக்கப்பட்டது. ஒவ்வொரு துண்டும் தனித்துவமானது, இந்திய மட்பாண்டங்களின் பண்பட்ட கலாச்சார மரபைக் காட்டுகிறது.",
            "caption": "இந்த கைவினை நீல மட்பாண்ட குவளையுடன் பாரம்பரிய இந்திய கைவினைத்திறனின் அழகைக் கண்டறியவும்! ஒவ்வொரு துண்டும் கலாச்சார மரபு மற்றும் கைவினை திறன்களின் கதையைச் சொல்கிறது.",
            "hashtags": "#கைவினைமட்பாண்டம் #இந்தியகைவினைஞர்கள் #நீலமட்பாண்டம் #பாரம்பரியகைவினை #கைவினைஞர்நிர்மாணித்தது #வீட்டஅலங்காரம் #கைவினைஞர்கள்காப்பாற்றுங்கள் #இந்தியாவில்தயாரித்தது #கைவினைமரபு #மட்பாண்டப்பிரியர்"
        }
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

# Function to check backend status (SIMULATED - for demo purposes)
def check_backend():
    try:
        # SIMULATED: 70% chance of success, 30% chance of failure for demo
        if random.random() < 0.7:  # 70% success rate
            st.session_state.backend_status = "up"
            return True
        else:
            st.session_state.backend_status = "down"
            return False
    except:
        st.session_state.backend_status = "down"
        return False

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

# Function to call backend API (with fallback handling)
def call_backend_api(image_data, description, craft_type):
    # Check backend status first (simulated)
    if not check_backend():
        raise ConnectionError("Backend service is unavailable")
    
    # Simulate API processing time
    time.sleep(2)
    
    # Return mock response
    return MOCK_RESPONSE

def main():
    # Initialize session state
    init_session_state()
    
    # Header section
    st.markdown("""
    <div class="header">
        <h1>ArtisanAI 🎨</h1>
        <p>Empowering local artisans with AI-powered tools to market their craft</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings and info
    with st.sidebar:
        st.header("Settings")
        
        # Mobile preview toggle
        st.session_state.mobile_preview = st.checkbox("Enable Mobile Preview", value=False)
        
        # Backend status indicator
        st.divider()
        st.header("System Status")
        if st.session_state.backend_status == "up":
            st.success("✅ Backend: Connected")
        elif st.session_state.backend_status == "down":
            st.error("❌ Backend: Disconnected")
            if st.session_state.last_successful_result:
                st.info("Showing cached results from last successful generation")
        else:
            st.info("🔍 Backend: Checking status...")
        
        st.divider()
        st.header("Info")
        st.info("""
        This tool helps local artisans create better product listings using AI.
        Upload an image and we'll generate a title, description, and suggested price.
        """)
    
    # Sample product selector
    sample_option = st.selectbox("Try a sample product", options=list(SAMPLE_PRODUCTS.keys()))
    
    # File uploader with size warning
    uploaded_file = st.file_uploader(
        "Upload product photo", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of your artisan product (max 5MB recommended)"
    )
    
    # Max image size warning (5MB limit)
    MAX_IMAGE_SIZE_MB = 5
    if uploaded_file is not None:
        # Check file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > MAX_IMAGE_SIZE_MB:
            st.markdown(f"""
            <div class="warning-message">
                ⚠️ Image size ({file_size_mb:.1f}MB) exceeds the recommended limit of {MAX_IMAGE_SIZE_MB}MB. 
                Processing may be slow. Consider resizing your image.
            </div>
            """, unsafe_allow_html=True)
    
    # If sample product is selected, update the description
    product_description = ""
    if sample_option != "Select a sample product":
        product_description = SAMPLE_PRODUCTS[sample_option]["description"]
    
    # Description input
    description = st.text_area(
        "Product description",
        value=product_description,
        height=100,
        help="Describe your product in your own words"
    )
    
    # Craft type selection
    craft_type = st.selectbox(
        "Craft type",
        options=["Pottery", "Handloom & Textiles", "Jewelry", "Woodwork", "Metalwork", "Other"],
        help="Select the category that best describes your craft"
    )
    
    # Language selection
    st.write("Select languages for translation:")
    lang_cols = st.columns(5)
    languages = [("English", "en"), ("Hindi", "hi"), ("Bengali", "bn"), ("Tamil", "ta"), ("Telugu", "te")]
    
    for i, (lang_name, lang_code) in enumerate(languages):
        with lang_cols[i]:
            if st.button(lang_name, key=lang_code):
                st.session_state.selected_lang = lang_code
    
    # Highlight selected language
    st.markdown(f"**Selected language:** {[name for name, code in languages if code == st.session_state.selected_lang][0]}")
    
    # Generate button
    if st.button("Generate Content", type="primary"):
        if not uploaded_file and sample_option == "Select a sample product":
            st.error("Please upload a product image or select a sample product")
        elif not description:
            st.error("Please provide a product description")
        else:
            # Show loading spinner
            with st.spinner("Generating marketing content... This may take a few moments."):
                try:
                    # Prepare image data
                    image_data = uploaded_file.read() if uploaded_file else None
                    
                    # Call backend API
                    result = call_backend_api(image_data, description, craft_type)
                    
                    # Store successful result
                    st.session_state.generated_content = result
                    st.session_state.last_successful_result = result
                    st.session_state.image_uploaded = True if uploaded_file else False
                    st.session_state.backend_status = "up"
                    
                except ConnectionError as e:
                    st.session_state.backend_status = "down"
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Connection Error: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show last successful result if available
                    if st.session_state.last_successful_result:
                        st.info("Showing your last successfully generated content:")
                        st.session_state.generated_content = st.session_state.last_successful_result
                    else:
                        st.error("No previous results available. Please try again when the backend is connected.")
                        st.session_state.generated_content = None
                        
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        ⚠️ An unexpected error occurred: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.generated_content = None
    
    # Display results if content has been generated
    if st.session_state.generated_content:
        st.success("Content generated successfully!")
        
        # Get content for selected language
        lang = st.session_state.selected_lang
        if lang == 'en':
            content = st.session_state.generated_content
        else:
            content = st.session_state.generated_content['translations'].get(lang, {})
            # Fallback to English if translation not available
            if not content:
                content = st.session_state.generated_content
                st.warning(f"Translation not available for {lang}. Showing English content.")
        
        # Display generated content in cards
        st.markdown("### Generated Content")
        
        # Product Title
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📝 Product Title</div>
            <p>{content.get('title', 'No title generated')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Product Description
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📄 Product Description</div>
            <p>{content.get('description', 'No description generated')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Social Media Caption
        st.markdown(f"""
        <div class="card">
            <div class="card-title">💬 Social Media Caption</div>
            <p>{content.get('caption', 'No caption generated')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hashtags
        st.markdown(f"""
        <div class="card">
            <div class="card-title">#️⃣ Hashtags</div>
            <p>{content.get('hashtags', 'No hashtags generated')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mobile preview
        if st.session_state.mobile_preview and st.session_state.image_uploaded and uploaded_file:
            st.markdown("### 📱 Mobile Preview")
            st.markdown(f"""
            <div class="mobile-preview">
                <div class="mobile-header">Artisan Marketplace</div>
                <img src="data:image/png;base64,{image_to_base64(uploaded_file)}" class="mobile-image" />
                <div class="mobile-title">{content.get('title', 'Product Title')}</div>
                <div class="mobile-description">{content.get('description', 'No description generated')}</div>
                <div class="mobile-price">$35.00</div>
                <button class="mobile-button">Add to Cart</button>
            </div>
            """, unsafe_allow_html=True)
        
        # Copy to clipboard functionality
        copy_text = f"{content.get('title', '')}\n\n{content.get('description', '')}\n\n{content.get('caption', '')}\n\n{content.get('hashtags', '')}"
        st.text_area("Copy all content", copy_text, height=200, key="copy_area")
        
        if st.button("Copy to Clipboard", key="copy_btn"):
            st.info("Please manually copy the content from the text area above")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #5F6368;">
        <p>Built with ❤️ for Google Gen AI Exchange Hackathon</p>
        <p>Powered by Google Cloud AI technologies</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()