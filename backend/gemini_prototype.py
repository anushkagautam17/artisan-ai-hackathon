import os

def read_prompt(file_path):
    """Read prompt template from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"✓ Successfully read: {file_path}")
            return file.read()
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
        return "FILE_NOT_FOUND"
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return "ERROR"

def simulate_chatgpt_listing(description, image_details):
    """Simulate ChatGPT response for product listing"""
    # Get the absolute path to the prompt file
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    listing_path = os.path.join(project_root, 'prompts', 'listing.txt')
    
    prompt_template = read_prompt(listing_path)
    
    # If we couldn't read the prompt file, use a default prompt
    if prompt_template in ["FILE_NOT_FOUND", "ERROR"]:
        prompt_template = """You are a helpful seller assistant specializing in handmade artisan products. 
Input: short description + image details. 
Output in this exact format:
- Title: [create a compelling title under 8 words]
- Bullet 1: [first key feature, concise]
- Bullet 2: [second key feature, concise]
- Bullet 3: [third key feature, concise]
- Bullet 4: [fourth key feature, concise]
- Price: [suggested price range in INR, format as "₹X - ₹Y"]"""
    
    full_prompt = f"{prompt_template}\n\nDescription: {description}\nImage details: {image_details}"
    
    print("=== Simulated ChatGPT Response for Listing ===")
    print("Prompt sent to ChatGPT:")
    print(full_prompt)
    print("\n--- Simulated Response ---")
    
    # Simulated response based on your listing.txt format
    simulated_response = """
- Title: Unique Handmade Artisan Product
- Bullet 1: Crafted with premium quality materials
- Bullet 2: Eco-friendly and sustainable design
- Bullet 3: Perfect for gifting or personal use
- Bullet 4: Adds charm to any space
- Price: ₹500 - ₹1500
"""
    
    print(simulated_response)
    return simulated_response

def simulate_chatgpt_social(title, features):
    """Simulate ChatGPT response for social media content"""
    # Get the absolute path to the prompt file
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    social_path = os.path.join(project_root, 'prompts', 'social.txt')
    
    prompt_template = read_prompt(social_path)
    
    # If we couldn't read the prompt file, use a default prompt
    if prompt_template in ["FILE_NOT_FOUND", "ERROR"]:
        prompt_template = """You are a social media marketing expert for handmade artisan products.
Input: product title and features.
Output in this exact format:
- Caption: [engaging 1-2 sentence description for social media]
- Hashtags: [5-7 relevant hashtags including #Handmade #LocalArtisan]"""
    
    full_prompt = f"{prompt_template}\n\nTitle: {title}\nFeatures: {features}"
    
    print("=== Simulated ChatGPT Response for Social ===")
    print("Prompt sent to ChatGPT:")
    print(full_prompt)
    print("\n--- Simulated Response ---")
    
    # Simulated response
    simulated_response = """
- Caption: Discover this unique handmade artisan product crafted with premium materials. Perfect for gifting or adding charm to your space!
- Hashtags: #Handmade #ArtisanCraft #Sustainable #LocalArtisan #HomeDecor #EcoFriendly #UniqueGifts
"""
    
    print(simulated_response)
    return simulated_response

if __name__ == "__main__":
    print("=== Starting Gemini Prototype Simulation ===")
    
    # Test with sample data
    description = "Handwoven bamboo basket with leather handles, traditional pattern"
    image_details = "Natural bamboo color, cylindrical shape, 12 inches height, leather straps"
    
    # Simulate listing response
    listing_response = simulate_chatgpt_listing(description, image_details)
    
    # Extract title and features from the simulated response for social media
    lines = [line.strip() for line in listing_response.strip().split('\n') if line.strip()]
    title = lines[0].replace('- Title: ', '').strip() if lines else "Unknown Product"
    
    # Extract bullets (lines that start with "- Bullet")
    features = []
    for line in lines:
        if line.startswith('- Bullet'):
            features.append(line)
    features_text = '\n'.join(features) if features else "No features extracted"
    
    # Simulate social media response
    social_response = simulate_chatgpt_social(title, features_text)
    
    # Save example outputs to files WITH UTF-8 ENCODING
    with open('example_listing_output.txt', 'w', encoding='utf-8') as f:
        f.write("Input Description: " + description + "\n")
        f.write("Input Image Details: " + image_details + "\n")
        f.write("Output:\n" + listing_response)
        
    with open('example_social_output.txt', 'w', encoding='utf-8') as f:
        f.write("Input Title: " + title + "\n")
        f.write("Input Features: " + features_text + "\n")
        f.write("Output:\n" + social_response)
        
    print("\n✓ Example outputs saved to:")
    print("  - example_listing_output.txt")
    print("  - example_social_output.txt")
    print("=== Simulation Complete ===")