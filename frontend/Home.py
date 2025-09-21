# frontend/Home.py
import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for language
if 'current_language' not in st.session_state:
    st.session_state.current_language = "en"

# Translation dictionary - moved here for simplicity
LANGUAGES = {
    "en": {
        "home_title": "MadebyNaari - Empowering Indian Artisans",
        "hero_title": "MadebyNaari",
        "hero_subtitle": "Empowering Indian artisans with AI-powered tools to showcase their crafts to the world. Transform traditional craftsmanship into digital success stories with our simple, powerful platform.",
        "cta_button": "🚀 Generate Content Now",
        "about_title": "About MadebyNaari",
        "about_text": "MadebyNaari is a revolutionary platform designed to help Indian artisans thrive in the digital marketplace. We bridge the gap between traditional craftsmanship and modern e-commerce.",
        "challenges_title": "Challenges Artisans Face",
        "solutions_title": "How MadebyNaari Helps",
        "challenge_1": "Difficulty creating professional product descriptions",
        "challenge_2": "Language barriers in reaching diverse markets",
        "challenge_3": "Limited digital marketing knowledge",
        "challenge_4": "Time-consuming content creation process",
        "challenge_5": "Limited reach to global customers",
        "solution_1": "AI-powered product description generation",
        "solution_2": "Multi-language translation support",
        "solution_3": "Social media ready content creation",
        "solution_4": "Simple, intuitive interface",
        "solution_5": "Global marketplace access",
        "mission_text": "Our mission is to preserve traditional crafts while empowering artisans with modern technology. We believe every handmade product has a story worth sharing with the world.",
        "how_it_works": "How It Works",
        "step_1_title": "Upload Your Product",
        "step_1_desc": "Simply take a photo of your artisan product - pottery, textiles, jewelry, or any handmade item. Our AI will analyze the image to understand its unique features and craftsmanship.",
        "step_2_title": "AI Generates Content",
        "step_2_desc": "Our advanced AI creates compelling product titles, detailed descriptions, and marketing copy that highlights the unique aspects of your artisan product in seconds.",
        "step_3_title": "Get Translations",
        "step_3_desc": "Receive your content translated into multiple Indian languages - Hindi, Bengali, Tamil, Telugu, and more - to reach customers across different regions.",
        "step_4_title": "Sell Anywhere",
        "step_4_desc": "Use the generated content on e-commerce platforms, social media, or your own website. Optimized for customer engagement and search visibility.",
        "demo_title": "See It In Action",
        "feature_1_title": "Product Listing",
        "feature_1_desc": "Create beautiful, detailed product descriptions that sell",
        "feature_2_title": "Social Media",
        "feature_2_desc": "Generate Instagram and WhatsApp ready content instantly",
        "feature_3_title": "Multilingual",
        "feature_3_desc": "Reach customers in their preferred language effortlessly",
        "try_demo": "✨ Try Free Demo",
        "footer_text": "© 2024 MadebyNaari | Empowering Indian Artisans Through Technology",
        "footer_made": "Made with ❤️ for the Google Gen AI Exchange Hackathon",
        "nav_home": "Home",
        "nav_about": "About",
        "nav_how": "How It Works",
        "nav_demo": "Demo",
        "nav_try": "Try It",
        "nav_get_started": "Get Started"
    },
    "hi": {
        "home_title": "मेडबायनारी - भारतीय कारीगरों को सशक्त बनाना",
        "hero_title": "मेडबायनारी",
        "hero_subtitle": "भारतीय कारीगरों को AI-संचालित उपकरणों से सशक्त बनाना ताकि वे अपने शिल्प को दुनिया के सामने प्रदर्शित कर सकें। पारंपरिक शिल्प कौशल को डिजिटल सफलता की कहानियों में बदलें।",
        "cta_button": "🚀 अभी सामग्री बनाएं",
        "about_title": "मेडबायनारी के बारे में",
        "about_text": "मेडबायनारी एक क्रांतिकारी प्लेटफॉर्म है जिसे भारतीय कारीगरों को डिजिटल बाजार में thriving करने में मदद करने के लिए डिजाइन किया गया है।",
        "challenges_title": "कारीगरों के सामने चुनौतियाँ",
        "solutions_title": "मेडबायनारी कैसे मदद करता है",
        "challenge_1": "पेशेवर उत्पाद विवरण बनाने में कठिनाई",
        "challenge_2": "विविध बाजारों तक पहुँचने में भाषा की बाधाएँ",
        "challenge_3": "सीमित डिजिटल मार्केटिंग ज्ञान",
        "challenge_4": "समय लेने वाली सामग्री निर्माण प्रक्रिया",
        "challenge_5": "वैश्विक ग्राहकों तक सीमित पहुँच",
        "solution_1": "AI-संचालित उत्पाद विवरण जनरेशन",
        "solution_2": "बहु-भाषा अनुवाद समर्थन",
        "solution_3": "सोशल मीडिया के लिए तैयार सामग्री निर्माण",
        "solution_4": "सरल, सहज इंटरफेस",
        "solution_5": "वैश्विक बाजार पहुंच",
        "mission_text": "हमारा मिशन पारंपरिक शिल्पों को संरक्षित करना है जबकि आधुनिक तकनीक के साथ कारीगरों को सशक्त बनाना है। हम मानते हैं कि हर हस्तनिर्मित उत्पाद की एक कहानी है जो दुनिया के साथ साझा करने लायक है।",
        "how_it_works": "यह कैसे काम करता है",
        "step_1_title": "अपना उत्पाद अपलोड करें",
        "step_1_desc": "बस अपने कारीगर उत्पाद की एक तस्वीर लें - मिट्टी के बर्तन, वस्त्र, गहने, या कोई भी हस्तनिर्मित वस्तु। हमारी AI छवि का विश्लेषण करेगी ताकि इसकी अनूठी विशेषताओं और शिल्प कौशल को समझ सके।",
        "step_2_title": "AI सामग्री उत्पन्न करता है",
        "step_2_desc": "हमारी उन्नत AI आकर्षक उत्पाद शीर्षक, विस्तृत विवरण और मार्केटिंग कॉपी बनाती है जो सेकंडों में आपके कारीगर उत्पाद के अनूठे पहलुओं पर प्रकाश डालती है।",
        "step_3_title": "अनुवाद प्राप्त करें",
        "step_3_desc": "अपनी सामग्री कई भारतीय भाषाओं - हिंदी, बंगाली, तमिल, तेलुगु और अधिक में अनुवादित प्राप्त करें - ताकि विभिन्न क्षेत्रों में ग्राहकों तक पहुँच सकें।",
        "step_4_title": "कहीं भी बेचें",
        "step_4_desc": "ई-कॉमर्स प्लेटफॉर्म, सोशल मीडिया, या अपनी खुद की वेबसाइट पर जेनरेट की गई सामग्री का उपयोग करें। ग्राहक संलग्नता और खोज दृश्यता के लिए अनुकूलित।",
        "demo_title": "इसे कार्रवाई में देखें",
        "feature_1_title": "उत्पाद सूची",
        "feature_1_desc": "सुंदर, विस्तृत उत्पाद विवरण बनाएं जो बिकते हैं",
        "feature_2_title": "सोशल मीडिया",
        "feature_2_desc": "Instagram और WhatsApp के लिए तैयार सामग्री तुरंत उत्पन्न करें",
        "feature_3_title": "बहुभाषी",
        "feature_3_desc": "ग्राहकों तक उनकी पसंदीदा भाषा में आसानी से पहुँचें",
        "try_demo": "✨ मुफ्त डेमो आज़माएं",
        "footer_text": "© 2024 मेडबायनारी | प्रौद्योगिकी के माध्यम से भारतीय कारीगरों को सशक्त बनाना",
        "footer_made": "Google Gen AI Exchange Hackathon के लिए ❤️ से बनाया गया",
        "nav_home": "होम",
        "nav_about": "अबाउट",
        "nav_how": "कैसे काम करता है",
        "nav_demo": "डेमो",
        "nav_try": "आज़माएं",
        "nav_get_started": "शुरू करें"
    },
    "bn": {
        "home_title": "মেডবায়নারি - ভারতীয় কারিগরদের ক্ষমতায়ন",
        "hero_title": "মেডবায়নারি",
        "hero_subtitle": "ভারতীয় কারিগরদের AI-চালিত সরঞ্জাম দিয়ে ক্ষমতায়ন করুন যাতে তারা তাদের শিল্পকর্ম বিশ্বের কাছে showcase করতে পারে। ঐতিহ্যবাহী কারুশিল্পকে ডিজিটাল সাফল্যের গল্পে রূপান্তর করুন।",
        "cta_button": "🚀 এখনই কনটেন্ট তৈরি করুন",
        "about_title": "মেডবায়নারি সম্পর্কে",
        "about_text": "মেডবায়নারি একটি বিপ্লবী প্ল্যাটফর্ম যা ভারতীয় কারিগরদের ডিজিটাল marketplace এ thriving করতে সাহায্য করার জন্য designed।",
        "challenges_title": "কারিগরদের面临的挑战",
        "solutions_title": "মেডবায়নারি如何帮助",
        "challenge_1": "পেশাদার পণ্য বিবরণ তৈরি করতে অসুবিধা",
        "challenge_2": "বিভিন্ন বাজারে পৌঁছানোর ভাষা Barriers",
        "challenge_3": "সীমিত ডিজিটাল মার্কেটিং জ্ঞান",
        "challenge_4": "সময়সাপেক্ষ কনটেন্ট creation প্রক্রিয়া",
        "challenge_5": "বৈশ্বিক গ্রাহকদের কাছে সীমিত access",
        "solution_1": "AI-চালিত পণ্য বিবরণ generation",
        "solution_2": "বহু-ভাষা অনুবাদ support",
        "solution_3": "সোশ্যাল মিডিয়ার জন্য ready কনটেন্ট creation",
        "solution_4": "সহজ, intuitive interface",
        "solution_5": "বৈশ্বিক marketplace access",
        "mission_text": "আমাদের mission হল traditional crafts সংরক্ষণ করা এবং আধুনিক প্রযুক্তি দিয়ে কারিগরদের ক্ষমতায়ন করা। আমরা বিশ্বাস করি যে every handmade product একটি story আছে যা world সাথে share করার worth।",
        "how_it_works": "এটি如何工作",
        "step_1_title": "আপনার পণ্য আপলোড করুন",
        "step_1_desc": "Simply আপনার কারুশিল্প পণ্যের একটি photo তুলুন - pottery, textiles, jewelry, বা any handmade item। আমাদের AI image analyze করবে তার unique features এবং craftsmanship বুঝতে।",
        "step_2_title": "AI কনটেন্ট generates",
        "step_2_desc": "আমাদের advanced AI compelling product titles, detailed descriptions, এবং marketing copy creates যে seconds মধ্যে আপনার artisan product এর unique aspects highlights করে।",
        "step_3_title": "অনুবাদ পান",
        "step_3_desc": "আপনার কনটেন্ট multiple Indian languages - Hindi, Bengali, Tamil, Telugu, এবং more - এ translated receive করুন different regions এর customers কাছে reaching করার জন্য।",
        "step_4_title": "য anywhere sell করুন",
        "step_4_desc": "Generated content use করুন e-commerce platforms, social media, বা আপনার own website এ। Customer engagement এবং search visibility এর জন্য optimized।",
        "demo_title": "এটি action মধ্যে see করুন",
        "feature_1_title": "পণ্য তালিকা",
        "feature_1_desc": "সুন্দর, detailed product descriptions create করুন that sell",
        "feature_2_title": "সোশ্যাল মিডিয়া",
        "feature_2_desc": "Instagram এবং WhatsApp ready content instantly generate করুন",
        "feature_3_title": "বহুভাষিক",
        "feature_3_desc": "গ্রাহকদের তাদের preferred language এ effortlessly reach করুন",
        "try_demo": "✨ বিনামূল্যের ডেমো try করুন",
        "footer_text": "© 2024 মেডবায়নারি | প্রযুক্তির মাধ্যমে ভারতীয় কারিগরদের ক্ষমতায়ন",
        "footer_made": "Google Gen AI Exchange Hackathon এর জন্য ❤️ দিয়ে তৈরি",
        "nav_home": "হোম",
        "nav_about": "সম্পর্কে",
        "nav_how": "কিভাবে কাজ করে",
        "nav_demo": "ডেমো",
        "nav_try": "চেষ্টা করুন",
        "nav_get_started": "শুরু করুন"
    }
}

# Function to get translated text
def get_text(key):
    return LANGUAGES[st.session_state.current_language].get(key, key)

# Set page configuration
st.set_page_config(
    page_title=get_text("home_title"),
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
        gap: 25px;
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
    }
    
    .language-selector {
        padding: 5px 10px;
        border-radius: 20px;
        border: 2px solid #6a11cb;
        background: white;
        color: #6a11cb;
        font-size: 0.9rem;
        cursor: pointer;
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(106,17,203,0.1) 0%, rgba(37,117,252,0.1) 100%);
        padding: 80px 0;
        text-align: center;
        margin: 40px 0;
        border-radius: 15px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: #333;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 30px;
        color: #666;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    .cta-button {
        background-color: #6a11cb;
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-button:hover {
        background-color: #2575fc;
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        color: white;
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
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
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
        gap: 30px;
        margin-top: 30px;
    }
    
    .problem-box, .solution-box {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .problem-title, .solution-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: #333;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .problem-list, .solution-list {
        list-style: none;
        padding: 0;
    }
    
    .problem-list li, .solution-list li {
        margin-bottom: 12px;
        padding-left: 30px;
        position: relative;
        line-height: 1.5;
    }
    
    .problem-list li:before {
        content: "❌";
        position: absolute;
        left: 0;
        color: #ff6b6b;
        font-size: 1.2rem;
    }
    
    .solution-list li:before {
        content: "✅";
        position: absolute;
        left: 0;
        color: #4caf50;
        font-size: 1.2rem;
    }
    
    .mission-statement {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-top: 40px;
        font-style: italic;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .footer {
        background-color: #f8f9fa;
        padding: 40px 0;
        margin-top: 60px;
        text-align: center;
        color: #666;
        border-top: 1px solid #e9ecef;
    }
    
    .process-step {
        display: flex;
        align-items: center;
        margin: 30px 0;
        padding: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .step-number {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-right: 20px;
        flex-shrink: 0;
    }
    
    .step-content h3 {
        color: #6a11cb;
        margin-bottom: 10px;
        font-size: 1.3rem;
    }
    
    .step-content p {
        color: #666;
        line-height: 1.6;
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
            padding: 0 15px;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .problem-solution-grid {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        
        .nav-menu {
            flex-direction: column;
            gap: 15px;
        }
        
        .process-step {
            flex-direction: column;
            text-align: center;
        }
        
        .step-number {
            margin-right: 0;
            margin-bottom: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar with Language Selector
st.markdown(f"""
<div class="navbar">
    <div class="nav-container">
        <div class="logo">MadebyNaari</div>
        <ul class="nav-menu">
            <li><a href="#" class="nav-link">{get_text('nav_home')}</a></li>
            <li><a href="#about" class="nav-link">{get_text('nav_about')}</a></li>
            <li><a href="#how-it-works" class="nav-link">{get_text('nav_how')}</a></li>
            <li><a href="#demo" class="nav-link">{get_text('nav_demo')}</a></li>
            <li><a href="/app" class="nav-link">{get_text('nav_try')}</a></li>
            <li><a href="/app" class="login-btn">{get_text('nav_get_started')}</a></li>
            <li>
                <select class="language-selector" onchange="handleLanguageChange(this.value)">
                    <option value="en" {'selected' if st.session_state.current_language == 'en' else ''}>English</option>
                    <option value="hi" {'selected' if st.session_state.current_language == 'hi' else ''}>Hindi</option>
                    <option value="bn" {'selected' if st.session_state.current_language == 'bn' else ''}>Bengali</option>
                </select>
            </li>
        </ul>
    </div>
</div>

<script>
function handleLanguageChange(lang) {{
    fetch('/update_language', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json',
        }},
        body: JSON.stringify({{language: lang}})
    }}).then(() => {{
        window.location.reload();
    }});
}}
</script>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
<div class="hero-section">
    <h1 class="hero-title">{get_text('hero_title')}</h1>
    <p class="hero-subtitle">{get_text('hero_subtitle')}</p>
    <a href="/app" class="cta-button">{get_text('cta_button')}</a>
</div>
""", unsafe_allow_html=True)

# About MadebyNaari Section
st.markdown(f"""
<div class="about-section" id="about">
    <h2 class="about-title">{get_text('about_title')}</h2>
    <p style="text-align: center; font-size: 1.2rem; line-height: 1.6; margin-bottom: 40px;">
        {get_text('about_text')}
    </p>
    
    <div class="problem-solution-grid">
        <div class="problem-box">
            <h3 class="problem-title">{get_text('challenges_title')}</h3>
            <ul class="problem-list">
                <li>{get_text('challenge_1')}</li>
                <li>{get_text('challenge_2')}</li>
                <li>{get_text('challenge_3')}</li>
                <li>{get_text('challenge_4')}</li>
                <li>{get_text('challenge_5')}</li>
            </ul>
        </div>
        
        <div class="solution-box">
            <h3 class="solution-title">{get_text('solutions_title')}</h3>
            <ul class="solution-list">
                <li>{get_text('solution_1')}</li>
                <li>{get_text('solution_2')}</li>
                <li>{get_text('solution_3')}</li>
                <li>{get_text('solution_4')}</li>
                <li>{get_text('solution_5')}</li>
            </ul>
        </div>
    </div>
    
    <div class="mission-statement">
        <p>"{get_text('mission_text')}"</p>
    </div>
</div>
""", unsafe_allow_html=True)

# How It Works Section
st.markdown(f'<h2 class="section-title" id="how-it-works">{get_text("how_it_works")}</h2>', unsafe_allow_html=True)

st.markdown(f"""
<div class="process-step">
    <div class="step-number">1</div>
    <div class="step-content">
        <h3>{get_text('step_1_title')}</h3>
        <p>{get_text('step_1_desc')}</p>
    </div>
</div>

<div class="process-step">
    <div class="step-number">2</div>
    <div class="step-content">
        <h3>{get_text('step_2_title')}</h3>
        <p>{get_text('step_2_desc')}</p>
    </div>
</div>

<div class="process-step">
    <div class="step-number">3</div>
    <div class="step-content">
        <h3>{get_text('step_3_title')}</h3>
        <p>{get_text('step_3_desc')}</p>
    </div>
</div>

<div class="process-step">
    <div class="step-number">4</div>
    <div class="step-content">
        <h3>{get_text('step_4_title')}</h3>
        <p>{get_text('step_4_desc')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Demo Section
st.markdown(f'<h2 class="section-title" id="demo">{get_text("demo_title")}</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h3 style="color: #6a11cb;">🎨 {get_text('feature_1_title')}</h3>
        <p>{get_text('feature_1_desc')}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h3 style="color: #6a11cb;">📱 {get_text('feature_2_title')}</h3>
        <p>{get_text('feature_2_desc')}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h3 style="color: #6a11cb;">🌍 {get_text('feature_3_title')}</h3>
        <p>{get_text('feature_3_desc')}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; margin: 40px 0;">
    <a href="/app" class="cta-button" style="margin: 0 auto;">{get_text('try_demo')}</a>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
    <p>{get_text('footer_text')}</p>
    <p>{get_text('footer_made')}</p>
    <p>
        <a href="https://github.com/your-repo" style="color: #6a11cb; text-decoration: none; margin: 0 10px;">GitHub</a> • 
        <a href="https://linkedin.com" style="color: #6a11cb; text-decoration: none; margin: 0 10px;">LinkedIn</a> • 
        <a href="mailto:hello@madebynaari.com" style="color: #6a11cb; text-decoration: none; margin: 0 10px;">Contact</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Add some spacing
st.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True)