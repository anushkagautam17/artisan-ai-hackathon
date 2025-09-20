# frontend/app.py
import sys
import os

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

# Mock response data for demonstration (fallback)
MOCK_RESPONSE = {
    "title": "Handmade Blue Pottery Vase with Traditional Indian Patterns",
    "description": "This exquisite handmade blue pottery vase features traditional Indian patterns, meticulously crafted by skilled artisans. Each piece is unique, showcasing the rich cultural heritage of Indian pottery. Perfect for home decoration or as a special gift, this vase adds an elegant touch to any space.",
    "caption": "Discover the beauty of traditional Indian craftsmanship with this handmade blue pottery vase! Each piece tells a story of cultural heritage and artisan skill. Perfect addition to your home decor or as a unique gift. 🏺✨",
    "hashtags": "#HandmadePottery #IndianArtisans #BluePottery #TraditionalCraft #ArtisanMade #HomeDecor #SupportArtisans #MadeInIndia #CraftHeritage #PotteryLover",
    "price_suggestion": "₹1,499",
    "bullet_points": [
        "Handmade by skilled artisans",
        "Traditional design patterns",
        "Eco-friendly materials",
        "Perfect for home decoration"
    ],
    "translations": {
        "hi": {
            "title": "हस्तनिर्मित नीला मिट्टी का फूलदान पारंपरिक भारतीय नमूनों के साथ",
            "description": "यह उत्कृष्ट हस्तनिर्मित नीला मिट्टी का फूलदान पारंपरिक भारतीय नमूनों से सुशोभित है, जिसे कुशल कारीगरों द्वारा सावधानीपूर्वक तैयार किया गया है। प्रत्येक टुकड़ा अनूठा है, जो भारतीय मिट्टी के बर्तनों की समृद्ध सांस्कृतिक विरासत को प्रदर्शित करता है।",
            "caption": "पारंपरिक भारतीय शिल्प कौशल की सुंदरता की खोज इस हस्तनिर्मित नीले मिट्टी के फूलदान के साथ करें! प्रत्येक टुकड़ा सांस्कृतिक विरासत और कारीगर कौशल की कहानी कहता है।",
            "hashtags": "#हस्तनिर्मितमिट्टीकेबर्तन #भारतीयकारीगर #नीलामिट्टीकेबर्तन #पारंपरिकशिल्प #कारीगरनिर्मित #घरकीसजावट #कारीगरोंकासमर्थन #भारतमेंनिर्मित #शिल्पविरासत #मिट्टीकेबर्तनप्रेमी",
            "price_suggestion": "₹1,499",
            "bullet_points": [
                "कुशल कारीगरों द्वारा हस्तनिर्मित",
                "पारंपरिक डिजाइन पैटर्न",
                "पर्यावरण के अनुकूल सामग्री",
                "घर की सजावट के लिए बिल्कुल सही"
            ]
        },
        "bn": {
            "title": "প্রথাগত ভারতীয় নকশা সহ হস্তনির্মিত নীল মৃৎশিল্পের ফুলদানি",
            "description": "এই অত্যুৎকৃষ্ট হস্তনির্মিত নীল মৃৎশিল্পের ফুলদানিটি প্রথাগত ভারতীয় নকশায় সজ্জিত, যা দক্ষ কারিগরদের দ্বারা সযত্নে তৈরি করা হয়েছে। প্রতিটি টুকরা অনন্য, যা ভারতীয় মৃৎশিল্পের সমৃদ্ধ সাংস্কৃতিক heritage প্রদর্শন করে।",
            "caption": "এই হस्तনির্মিত নীল মৃৎশিল্পের ফুলদানির সাথে প্রথাগত ভারতীয় কারুশিল্পের সৌন্দর্য আবিষ্কার করুন! প্রতিটি টুকরা সাংস্কৃতিক heritage এবং কারিগর দক্ষতার গল্প বলে।",
            "hashtags": "#হস্তনির্মিতমৃৎশিল্প #ভারতীয়কারিগর #নীলমৃৎশিল্প #প্রথাগতশিল্প #কারিগরনির্মিত #হোমডেকর #কারিগরসমর্থন #ভারততৈরি #শিল্পঐতিহ্য #মৃৎশিল্পপ্রেমী",
            "price_suggestion": "₹1,499",
            "bullet_points": [
                "দক্ষ কারিগরদের দ্বারা হস্তনির্মিত",
                "প্রথাগত নকশা প্যাটার্ন",
                "পরিবেশ বান্ধব উপকরণ",
                "বাড়ির সাজসজ্জার জন্য উপযুক্ত"
            ]
        },
        "ta": {
            "title": "பாரம்பரிய இந்திய வடிவங்களுடன் கைவினை நீல மட்பாண்ட குவளை",
            "description": "இந்த அருமையான கைவினை நீல மட்பாண்ட குவளை பாரம்பரிய இந்திய வடிவங்களுடன் அலங்கரிக்கப்பட்டுள்ளது, இது திறமையான கைவினைஞர்களால் கவனமாக crafted உருவாக்கப்பட்டது. ஒவ்வொரு துண்டும் தனித்துவமானது, இந்திய மட்பாண்டங்களின் பண்பட்ட கலாச்சார மரபைக் காட்டுகிறது.",
            "caption": "இந்த கைவினை நீல மட்பாண்ட குவளையுடன் பாரம்பரிய இந்திய கைவினைத்திறனின் அழகைக் கண்டறியவும்! ஒவ்வொரு துண்டும் கலாச்சார மரபு மற்றும் கைவினை திறன்களின் கதையைச் சொல்கிறது.",
            "hashtags": "#கைவினைமட்பாண்டம் #இந்தியகைவினைஞர்கள் #நீலமட்பாண்டம் #பாரம்பரியகைவினை #கைவினைஞர்நிர்மாணித்தது #வீட்டஅலங்காரம் #கைவினைஞர்கள்காப்பாற்றுங்கள் #இந்தியாவில்தயாரித்தது #கைவினைமரபு #மட்பாண்டப்பிரியர்",
            "price_suggestion": "₹1,499",
            "bullet_points": [
                "திறமையான கைவினைஞர்களால் கைவினைப் படைப்பு",
                "பாரம்பரிய வடிவமைப்பு வடிவங்கள்",
                "சூழலுக்கு உகந்த பொருட்கள்",
                "வீட்டு அலங்காரத்திற்கு சிறந்தது"
            ]
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
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'en'
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'
    if 'user_type' not in st.session_state:
        st.session_state.user_type = 'buyer'

# Function to check backend status
def check_backend():
    try:
        # Try to connect to backend
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
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
def call_backend_api(image_data, description, target_languages):
    # Check backend status first
    if not check_backend():
        raise ConnectionError("Backend service is unavailable")
    
    try:
        # Prepare the request
        files = {"image": ("image.jpg", image_data, "image/jpeg")}
        data = {
            "description": description,
            "target_languages": target_languages
        }
        
        # Call the backend API
        response = requests.post(
            "http://localhost:8000/generate",
            files=files,
            data=data,
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Backend returned status code {response.status_code}")
            
    except Exception as e:
        # If backend call fails, use mock data
        st.session_state.backend_status = "down"
        raise ConnectionError(f"Failed to connect to backend: {str(e)}")

# Function to show toast notification
def show_toast(message):
    st.markdown(f"""
    <div class="toast">
        {message}
    </div>
    """, unsafe_allow_html=True)
    # Use a small delay to allow the toast to be visible
    time.sleep(0.1)

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
        
        # Try sample dropdown
        st.divider()
        st.header("Try Sample")
        sample_option = st.selectbox("Select a sample product", options=list(SAMPLE_PRODUCTS.keys()))
        
        st.divider()
        st.header("Info")
        st.info("""
        MadebyNari helps local artisans create better product listings using AI.
        Upload an image and we'll generate a title, description, and suggested price.
        """)
    
    # If sample product is selected, show the image and description
    if sample_option != "Select a sample product":
        sample = SAMPLE_PRODUCTS[sample_option]
        st.image(sample["image"], caption=sample_option, use_column_width=True)
        product_description = sample["description"]
    else:
        product_description = ""
    
    # File uploader with size warning
    uploaded_file = st.file_uploader(
        "Upload product photo", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of your artisan product (max 5MB recommended)"
    )
    
    # Show image preview if uploaded
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Check file size
        MAX_IMAGE_SIZE_MB = 5
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > MAX_IMAGE_SIZE_MB:
            st.markdown(f"""
            <div class="warning-message">
                ⚠️ Image size ({file_size_mb:.1f}MB) exceeds the recommended limit of {MAX_IMAGE_SIZE_MB}MB. 
                Processing may be slow. Consider resizing your image.
            </div>
            """, unsafe_allow_html=True)
    
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
    st.write("Select target languages for translation:")
    languages = ["Hindi", "Bengali", "Tamil", "Telugu", "Gujarati", "Marathi"]
    lang_codes = {
        "Hindi": "hi", 
        "Bengali": "bn", 
        "Tamil": "ta",
        "Telugu": "te",
        "Gujarati": "gu",
        "Marathi": "mr"
    }
    
    selected_languages = st.multiselect(
        "Languages",
        options=languages,
        default=["Hindi", "Bengali", "Tamil"],
        help="Select languages for translation"
    )
    
    # Convert selected languages to codes
    target_languages = ",".join([lang_codes[lang] for lang in selected_languages])
    
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
                    if uploaded_file:
                        image_data = uploaded_file.getvalue()
                    else:
                        # For sample products, we'll use a placeholder
                        image_data = None
                    
                    # Call backend API
                    result = call_backend_api(image_data, description, target_languages)
                    
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
                        # Use mock data as fallback
                        st.info("Using sample data for demonstration purposes.")
                        st.session_state.generated_content = MOCK_RESPONSE
                        
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
        
        # Create translation tabs
        st.markdown("### Generated Content")
        
        # Create tabs for different languages
        tab_names = ["English"] + selected_languages
        tabs = st.tabs(tab_names)
        
        for i, tab in enumerate(tabs):
            with tab:
                # Determine which language content to show
                if i == 0:  # English tab
                    lang = 'en'
                    content = st.session_state.generated_content
                else:  # Translation tabs
                    lang_name = tab_names[i]
                    lang_code = lang_codes[lang_name]
                    content = st.session_state.generated_content.get('translations', {}).get(lang_code, {})
                
                # Display content in cards
                # Product Title
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📝 Product Title</div>
                    <p>{content.get('title', 'No title generated')}</p>
                    <button class="copy-btn" onclick="navigator.clipboard.writeText('{content.get('title', '')}')">📋 Copy</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Product Description
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📄 Product Description</div>
                    <p>{content.get('description', 'No description generated')}</p>
                    <button class="copy-btn" onclick="navigator.clipboard.writeText('{content.get('description', '')}')">📋 Copy</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Social Media Caption
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">💬 Social Media Caption</div>
                    <p>{content.get('caption', 'No caption generated')}</p>
                    <button class="copy-btn" onclick="navigator.clipboard.writeText('{content.get('caption', '')}')">📋 Copy</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Hashtags
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">#️⃣ Hashtags</div>
                    <p>{content.get('hashtags', 'No hashtags generated')}</p>
                    <button class="copy-btn" onclick="navigator.clipboard.writeText('{content.get('hashtags', '')}')">📋 Copy</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Price suggestion and bullet points (only for English)
                if lang == 'en':
                    # Price Suggestion
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-title">💰 Price Suggestion</div>
                        <p>{content.get('price_suggestion', 'No price suggestion')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Bullet Points
                    bullet_points = content.get('bullet_points', [])
                    if bullet_points:
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-title">📌 Key Features</div>
                            <ul>
                                {"".join([f"<li>{point}</li>" for point in bullet_points])}
                            </ul>
                            <button class="copy-btn" onclick="navigator.clipboard.writeText('{"\\n".join(bullet_points)}')">📋 Copy All</button>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Mobile preview
        if st.session_state.mobile_preview and uploaded_file:
            st.markdown("### 📱 Mobile Preview")
            st.markdown(f"""
            <div class="mobile-preview">
                <div class="mobile-header">Artisan Marketplace</div>
                <img src="data:image/jpeg;base64,{image_to_base64(uploaded_file)}" class="mobile-image" />
                <div class="mobile-title">{st.session_state.generated_content.get('title', 'Product Title')}</div>
                <div class="mobile-description">{st.session_state.generated_content.get('description', 'No description generated')}</div>
                <div class="mobile-price">{st.session_state.generated_content.get('price_suggestion', '$35.00')}</div>
                <button class="mobile-button">Add to Cart</button>
            </div>
            """, unsafe_allow_html=True)
        
        # Copy all content functionality
        st.markdown("### 📋 Copy All Content")
        copy_text = f"{st.session_state.generated_content.get('title', '')}\n\n{st.session_state.generated_content.get('description', '')}\n\n{st.session_state.generated_content.get('caption', '')}\n\n{st.session_state.generated_content.get('hashtags', '')}"
        st.text_area("Copy all content", copy_text, height=200, key="copy_area")
        
        if st.button("Copy to Clipboard", key="copy_btn"):
            # This will show a toast notification
            show_toast("Content copied to clipboard!")
    
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

components.html(auth_js, height=0)

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
