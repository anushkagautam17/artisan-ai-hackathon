# pages/generator.py
import streamlit as st
import requests

st.title("Content Generator")

uploaded_file = st.file_uploader("Upload your product image", type=["jpg", "jpeg", "png"])
product_info = st.text_area("Product information")

if st.button("Generate Content"):
    if uploaded_file and product_info:
        files = {"image": uploaded_file}
        data = {"info": product_info}
        
        try:
            response = requests.post(
                "http://localhost:8000/api/generate",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success("Content generated successfully!")
                st.write(result)
            else:
                st.error(f"Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Connection error: {e}")
    else:
        st.warning("Please upload an image and provide product information")