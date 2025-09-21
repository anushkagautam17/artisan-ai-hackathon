import streamlit as st
import re

# Set page configuration
st.set_page_config(
    page_title="Streamlit Requirements Troubleshooter",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #1F77B4;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #F0F2F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FFF3CD;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #FFC107;
    }
    .success-box {
        background-color: #D4EDDA;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #28A745;
    }
    .error-box {
        background-color: #F8D7DA;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #DC3545;
    }
    .code-block {
        background-color: #2D2D2D;
        color: #F8F9FA;
        padding: 1rem;
        border-radius: 0.5rem;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
    }
    .step-number {
        background-color: #FF4B4B;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.5rem;
    }
    .tab-container {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<div class="main-header">🔍 Streamlit Requirements Troubleshooter</div>', unsafe_allow_html=True)
st.markdown("""
Follow this step-by-step guide to identify and fix issues with your requirements.txt file that are preventing your Streamlit app from deploying.
""")

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Step-by-step troubleshooting guide
steps = [
    {
        "title": "Check Requirements File Basics",
        "content": """
        Let's start with the basics. Make sure your requirements.txt:
        1. Is named exactly 'requirements.txt' (case matters)
        2. Is in the root directory of your repository
        3. Uses proper syntax (one package per line)
        4. Doesn't have any empty lines or comments that might cause issues
        """,
        "action": """
        # Example of a good requirements.txt
        streamlit>=1.22.0
        pandas>=1.5.0
        numpy>=1.24.0
        
        # Example of a bad requirements.txt
        streamlit  # Missing version specifier
        pandas==1.5.0 numpy==1.24.0  # Multiple packages on one line
        """
    },
    {
        "title": "Validate Package Names",
        "content": """
        Some package names might be different on PyPI than what you expect.
        For example, 'python-dotenv' is the package name but you import it as 'dotenv'.
        
        Common naming mismatches:
        - Import name: dotenv → Package name: python-dotenv
        - Import name: yaml → Package name: PyYAML
        - Import name: sklearn → Package name: scikit-learn
        - Import name: cv2 → Package name: opencv-python
        """,
        "action": """
        # Correct package names
        python-dotenv>=0.19.0
        PyYAML>=6.0
        scikit-learn>=1.0.0
        opencv-python>=4.5.0
        """
    },
    {
        "title": "Check Python Version Compatibility",
        "content": """
        Streamlit Cloud uses a specific Python version (currently 3.7+).
        Some packages might not be compatible. Check if your packages support Python 3.7.
        
        You can check package compatibility on PyPI:
        1. Visit https://pypi.org/
        2. Search for your package
        3. Check the "Requires" section for Python version requirements
        """,
        "action": """
        # If you need to specify Python version, add to requirements.txt
        # (Note: This is a comment, not actual syntax)
        
        # Requires Python 3.7+
        ; python_requires='>=3.7'
        
        # Or use environment markers (advanced)
        package-name ; python_version >= '3.7'
        """
    },
    {
        "title": "Identify Platform-Specific Packages",
        "content": """
        Some packages have platform-specific dependencies that won't work on Streamlit's Linux environment.
        Common examples include packages that require:
        - Windows-specific DLLs
        - macOS-specific frameworks
        - System libraries not available in the Streamlit environment
        
        Problematic packages often include:
        - pywin32 (Windows only)
        - pyaudio (may need system dependencies)
        -某些系统级库
        """,
        "action": """
        # Replace platform-specific packages with alternatives:
        
        # Instead of pywin32 (Windows only)
        # Use cross-platform alternatives for your use case
        
        # For audio processing, consider:
        soundfile>=0.10.0
        librosa>=0.9.0
        
        # For system operations, consider platform-independent alternatives
        psutil>=5.9.0  # Cross-platform process utilities
        """
    },
    {
        "title": "Check for Dependency Conflicts",
        "content": """
        Even if your direct dependencies seem compatible, their sub-dependencies might conflict.
        This is one of the most common issues with Python packaging.
        
        Common conflict scenarios:
        - Package A requires numpy>=1.20.0
        - Package B requires numpy<1.20.0
        - Result: Conflict that pip cannot resolve
        """,
        "action": """
        # Strategies to resolve conflicts:
        
        1. Pin specific versions for all packages:
        numpy==1.24.0
        pandas==1.5.0
        
        2. Use compatible version ranges:
        numpy>=1.20.0,<2.0.0
        
        3. Remove unnecessary packages to simplify dependencies
        
        4. Test with a minimal requirements.txt first:
        streamlit>=1.22.0
        # Then add packages one by one
        """
    }
]

# Display current step
if st.session_state.current_step < len(steps):
    step = steps[st.session_state.current_step]
    st.markdown(f'<div class="info-box"><h3>Step {st.session_state.current_step + 1}: {step["title"]}</h3>{step["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown("**Example:**")
    st.code(step["action"], language="plaintext")

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.session_state.current_step > 0:
        if st.button("◀ Previous Step"):
            st.session_state.current_step -= 1
            st.rerun()
with col2:
    if st.session_state.current_step < len(steps) - 1:
        if st.button("Next Step ▶"):
            st.session_state.current_step += 1
            st.rerun()
with col3:
    if st.button("🔄 Reset Steps"):
        st.session_state.current_step = 0
        st.rerun()

# Input section
st.markdown("---")
st.markdown('<div class="sub-header">📝 Analyze Your Requirements.txt</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Paste Content", "Upload File"])

requirements_content = ""

with tab1:
    requirements_content = st.text_area("Paste your requirements.txt content here", height=200,
                                      placeholder="streamlit>=1.22.0\npandas>=1.5.0\nnumpy>=1.24.0")

with tab2:
    uploaded_file = st.file_uploader("Or upload your requirements.txt file", type=['txt'])
    if uploaded_file is not None:
        requirements_content = uploaded_file.getvalue().decode("utf-8")
        st.text_area("Uploaded file content", requirements_content, height=200)

# Analysis button
if st.button("Analyze My Requirements", type="primary"):
    st.session_state.analysis_done = True
else:
    st.session_state.analysis_done = False

if st.session_state.analysis_done and requirements_content:
    st.markdown("---")
    st.markdown('<div class="sub-header">📊 Analysis Results</div>', unsafe_allow_html=True)
    
    # Perform analysis
    issues_found = []
    suggestions = []
    
    lines = requirements_content.split('\n')
    packages = []
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Check for multiple packages on one line
        if len(line.split()) > 1 and not any(op in line for op in ['==', '>=', '<=', '~=']):
            issues_found.append(f"Line {line_num}: Multiple packages on one line")
            suggestions.append(f"Split into separate lines: '{line}'")
            continue
            
        # Extract package name
        if '==' in line:
            pkg_name = line.split('==')[0].strip()
        elif '>=' in line:
            pkg_name = line.split('>=')[0].strip()
        elif '<=' in line:
            pkg_name = line.split('<=')[0].strip()
        elif '~=' in line:
            pkg_name = line.split('~=')[0].strip()
        else:
            pkg_name = line.strip()
            issues_found.append(f"Line {line_num}: No version specified for '{pkg_name}'")
            suggestions.append(f"Add version specifier: '{pkg_name}>=0.0.0'")
            
        packages.append(pkg_name)
        
        # Check for known problematic packages
        problematic_packages = {
            'pywin32': 'Windows-only package, will not work on Streamlit Cloud',
            'pyaudio': 'May require system dependencies not available on Streamlit Cloud',
            'opencv-python': 'Consider using opencv-python-headless instead',
            'tensorflow-gpu': 'Use tensorflow instead for cloud deployment',
        }
        
        if pkg_name in problematic_packages:
            issues_found.append(f"Line {line_num}: Potentially problematic package '{pkg_name}'")
            suggestions.append(problematic_packages[pkg_name])
    
    # Display results
    if issues_found:
        st.markdown('<div class="warning-box"><strong>⚠️ Issues Found:</strong></div>', unsafe_allow_html=True)
        for issue in issues_found:
            st.markdown(f"- {issue}")
        
        st.markdown('<div class="info-box"><strong>💡 Suggestions:</strong></div>', unsafe_allow_html=True)
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")
    else:
        st.markdown('<div class="success-box">No obvious issues found in your requirements.txt structure.</div>', unsafe_allow_html=True)
        st.markdown("""
        If you're still having deployment issues, try:
        1. Creating a minimal requirements.txt with just streamlit
        2. Deploying with only that file
        3. Adding packages back one by one to find the problematic one
        """)
    
    # Generate a fixed requirements.txt
    st.markdown('<div class="sub-header">📝 Generate a Clean requirements.txt</div>', unsafe_allow_html=True)
    
    fixed_content = "# Cleaned requirements.txt\n"
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].strip()
        
        # Skip problematic packages
        if pkg_name in problematic_packages:
            fixed_content += f"# {line}  # Removed: {problematic_packages[pkg_name]}\n"
        else:
            # Add version if missing
            if not any(op in line for op in ['==', '>=', '<=', '~=']):
                fixed_content += f"{line}>=0.0.0  # Added version specifier\n"
            else:
                fixed_content += line + "\n"
    
    st.text_area("Recommended requirements.txt", fixed_content, height=200)
    
    st.download_button(
        label="Download Clean requirements.txt",
        data=fixed_content,
        file_name="requirements_clean.txt",
        mime="text/plain"
    )

# Minimal requirements template
st.markdown("---")
st.markdown('<div class="sub-header">📋 Minimal Requirements Template</div>', unsafe_allow_html=True)

minimal_requirements = """# Start with just Streamlit
streamlit>=1.22.0

# Add packages one by one after confirming deployment works
# pandas>=1.5.0
# numpy>=1.24.0
# plotly>=5.10.0
"""

st.code(minimal_requirements, language="plaintext")

if st.button("Copy Minimal Template"):
    st.code(minimal_requirements, language="plaintext")
    st.success("Copy this code to your requirements.txt")

# Footer
st.markdown("---")
st.markdown("""
**Need more help?**
- [Streamlit Community Forums](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Packaging User Guide](https://packaging.python.org/)
""")