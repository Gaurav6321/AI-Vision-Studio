import streamlit as st
import requests
from PIL import Image, ImageOps, ImageFilter
import io
from huggingface_hub import InferenceClient
import time
import random
import base64
from streamlit_lottie import st_lottie
import json
import streamlit.components.v1 as components

# API details for image captioning - using a faster model
API_URL_CAPTION = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers_caption = {"Authorization": "Bearer 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"}

# Define the client for the text-to-image generation model
client = InferenceClient(
    model="stabilityai/stable-diffusion-xl-base-1.0",  # Using a faster model
    token="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"
)

# Custom CSS with animations and dark theme
def load_css():
    return """
    <style>
    /* Dark theme with gradient background */
    .stApp {
        background: linear-gradient(45deg, #1a1a2e, #16213e, #1a1a2e);
        color: #e0e0e0;
    }

    /* Bold Header Styling */
    .mega-header {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 900 !important;
        font-size: 4rem !important;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text !important;
        color: transparent !important;
        text-shadow: 0 2px 10px rgba(255, 107, 107, 0.3);
        letter-spacing: 2px;
        margin: 2rem 0;
        padding: 20px;
        -webkit-text-stroke: 2px rgba(255, 255, 255, 0.1);
    }

    /* Section headers with glow effect */
    .section-header {
        color: #4ecdc4;
        text-shadow: 0 0 10px rgba(78, 205, 196, 0.5);
        font-size: 2em;
        margin-bottom: 1em;
    }

    /* Card-like containers */
    .stButton button {
        background: linear-gradient(45deg, #2e2e4e, #1f1f3f);
        color: #e0e0e0;
        border: 1px solid #4ecdc4;
        border-radius: 10px;
        padding: 0.5em 1em;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3);
    }

    /* Custom file uploader */
    .stFileUploader {
        background: rgba(30, 30, 50, 0.5);
        padding: 2em;
        border-radius: 15px;
        border: 2px dashed #4ecdc4;
    }

    /* Animated progress bars */
    .stProgress > div > div {
        background-color: #4ecdc4;
        transition: width 0.3s ease;
    }

    /* Custom select box */
    .stSelectbox {
        background: rgba(30, 30, 50, 0.5);
        border-radius: 10px;
    }

    /* Animations */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Image container with hover effect */
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        transition: transform 0.3s ease;
    }

    .image-container:hover {
        transform: scale(1.02);
    }
    </style>
    """

# Enhanced Creative AI Agent
class CreativeAgent:
    def __init__(self):
        self.art_styles = [
            "realistic", "impressionist", "abstract", "surreal",
            "minimalist", "fantasy", "sci-fi", "vintage", "cyberpunk",
            "steampunk", "watercolor", "oil painting", "digital art"
        ]
        self.mood_modifiers = [
            "dreamy", "dramatic", "peaceful", "energetic",
            "mysterious", "whimsical", "elegant", "bold",
            "ethereal", "nostalgic", "futuristic", "melancholic"
        ]
        self.composition_elements = [
            "foreground emphasis", "rule of thirds", "symmetrical",
            "dynamic angle", "birds eye view", "close-up", "panoramic",
            "dutch angle", "leading lines", "framing", "golden ratio"
        ]
        self.time_of_day = [
            "golden hour", "blue hour", "sunset", "sunrise",
            "midnight", "noon", "twilight", "dawn"
        ]
        self.weather_effects = [
            "foggy", "rainy", "sunny", "stormy",
            "snowy", "cloudy", "misty", "clear"
        ]

    def enhance_prompt(self, base_prompt):
        """Enhanced prompt generation with more elements"""
        style = random.choice(self.art_styles)
        mood = random.choice(self.mood_modifiers)
        composition = random.choice(self.composition_elements)
        time = random.choice(self.time_of_day)
        weather = random.choice(self.weather_effects)

        enhanced_prompt = (
            f"{base_prompt}, {style} style, {mood} atmosphere, "
            f"{composition}, {time}, {weather} conditions, "
            "highly detailed, professional photography, "
            "8k resolution, artistic composition, masterpiece"
        )
        return enhanced_prompt, {
            "style": style,
            "mood": mood,
            "composition": composition,
            "time": time,
            "weather": weather
        }

    def suggest_variations(self, base_prompt):
        """Generate more diverse creative variations"""
        variations = []
        for _ in range(4):
            style = random.choice(self.art_styles)
            mood = random.choice(self.mood_modifiers)
            time = random.choice(self.time_of_day)
            variations.append({
                "prompt": f"{base_prompt} in {style} style with {mood} mood during {time}",
                "style": style,
                "mood": mood,
                "time": time
            })
        return variations

    def analyze_caption(self, caption):
        """Generate creative suggestions based on image caption"""
        suggestions = [
            f"Try reimagining this scene in {random.choice(self.art_styles)} style",
            f"Consider the mood: How about making it more {random.choice(self.mood_modifiers)}?",
            f"Experiment with timing: Visualize this during {random.choice(self.time_of_day)}",
            f"Add atmosphere with {random.choice(self.weather_effects)} conditions",
            f"Play with composition using {random.choice(self.composition_elements)}"
        ]
        return suggestions

# Optimize image processing
def optimize_image(image, max_size=(512, 512)):
    img = Image.open(io.BytesIO(image))
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img

def query_caption(image):
    try:
        response = requests.post(API_URL_CAPTION, headers=headers_caption, data=image, timeout=10)
        return response.json()
    except:
        st.error("Caption generation failed. Please try again.")
        return None

# Main application
def main():
    st.set_page_config(
        page_title="Enhanced AI Vision Studio",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load custom CSS
    st.markdown(load_css(), unsafe_allow_html=True)

    # Initialize session state
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []

    # Header with animation
    st.markdown('<h1 class="mega-header">🎨 Enhanced AI Vision Studio</h1>', unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.markdown("### 🎮 Settings")
        image_quality = st.slider("Image Quality", 1, 100, 85)
        enable_effects = st.checkbox("Enable Image Effects", True)
        st.markdown("### 🎨 Style Preferences")
        preferred_style = st.multiselect(
            "Preferred Styles",
            options=CreativeAgent().art_styles,
            default=["realistic", "fantasy"]
        )

    # Main content
    option = st.selectbox(
        "Choose Your Creative Tool",
        ("🎨 Text-to-Image Generation", "📸 Image Captioning", "🤖 Creative Assistant", "🖼️ Gallery")
    )

    if option == "🎨 Text-to-Image Generation":
        text_to_image_tab()
    elif option == "📸 Image Captioning":
        image_captioning_tab()
    elif option == "🤖 Creative Assistant":
        creative_assistant_tab()
    else:
        gallery_tab()

def text_to_image_tab():
    st.markdown('<h2 class="section-header">🎨 Text-to-Image Generation</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form("generation_form"):
            text_input = st.text_area(
                "Describe your image:",
                placeholder="Enter your detailed description...",
                height=100
            )
            use_enhancement = st.checkbox("Use AI Enhancement", value=True)
            submitted = st.form_submit_button("Generate Image")

            if submitted:
                with st.spinner("🎨 Creating your masterpiece..."):
                    generate_image(text_input, use_enhancement)

    with col2:
        st.markdown("### 💡 Tips")
        st.info(
            "For better results:\n"
            "- Be specific in your description\n"
            "- Include details about lighting and mood\n"
            "- Mention the style you prefer"
        )

def image_captioning_tab():
    st.markdown('<h2 class="section-header">📸 Image Captioning</h2>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"],
        help="Max file size: 5MB"
    )

    if uploaded_file is not None:
        try:
            image_bytes = uploaded_file.read()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Uploaded Image")
                img = optimize_image(image_bytes)
                if img:
                    st.image(img, use_column_width=True)

            if st.button("Generate Caption", key="caption_btn"):
                with st.spinner("🔍 Analyzing image..."):
                    start_time = time.time()
                    caption_response = query_caption(image_bytes)

                    if caption_response:
                        caption = caption_response[0]['generated_text']
                        with col2:
                            st.markdown("#### Generated Caption")
                            st.success(caption)
                            st.download_button(
                                label="📝 Download Caption",
                                data=caption,
                                file_name="image_caption.txt",
                                mime="text/plain"
                            )

                            creative_agent = CreativeAgent()
                            suggestions = creative_agent.analyze_caption(caption)

                            with st.expander("💡 Creative Suggestions"):
                                for suggestion in suggestions:
                                    st.write(f"- {suggestion}")

                            st.write(f"⏱️ Processing time: {time.time() - start_time:.2f}s")
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

def creative_assistant_tab():
    st.markdown('<h2 class="section-header">🤖 Creative Assistant</h2>', unsafe_allow_html=True)

    prompt_input = st.text_input(
        "Enter your base prompt:",
        placeholder="Describe your artistic vision..."
    )

    if prompt_input:
        creative_agent = CreativeAgent()
        variations = creative_agent.suggest_variations(prompt_input)

        st.markdown("### ✨ Prompt Variations")
        cols = st.columns(2)

        for idx, variation in enumerate(variations):
            with cols[idx % 2]:
                with st.container(border=True):
                    st.markdown(f"""
                        <div style='padding: 1em; border-radius: 10px; margin-bottom: 1em;'>
                            <p style='font-size: 1.1em;'>{variation['prompt']}</p>
                            <div style='display: flex; gap: 1em; margin-top: 0.5em;'>
                                <span class='badge'>{variation['style']}</span>
                                <span class='badge'>{variation['mood']}</span>
                                <span class='badge'>{variation['time']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"Generate This Variation", key=f"var_{idx}"):
                        with st.spinner("Generating variation..."):
                            generate_image(variation['prompt'], True)

def gallery_tab():
    st.markdown('<h2 class="section-header">🖼️ Gallery</h2>', unsafe_allow_html=True)

    if st.session_state.generated_images:
        columns = st.columns(3)
        for idx, img in enumerate(st.session_state.generated_images):
            with columns[idx % 3]:
                with st.container(border=True):
                    st.image(img, use_column_width=True)
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    st.download_button(
                        label="📥 Download",
                        data=img_bytes.getvalue(),
                        file_name=f"creation_{idx + 1}.png",
                        mime="image/png",
                        key=f"dl_{idx}"
                    )
    else:
        st.info("Generate some images to see them in your gallery!")

def generate_image(prompt, use_enhancement=True):
    try:
        creative_agent = CreativeAgent()
        if use_enhancement:
            enhanced_prompt, elements = creative_agent.enhance_prompt(prompt)
            with st.expander("🎨 Enhanced Elements"):
                st.json(elements)
            prompt_to_use = enhanced_prompt
        else:
            prompt_to_use = prompt

        image = client.text_to_image(
            prompt_to_use,
            negative_prompt="blurry, bad quality, distorted, ugly, deformed",
            num_inference_steps=50,
            guidance_scale=7.5
        )

        # Add to gallery
        st.session_state.generated_images.append(image)

        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Generated Image", use_column_width=True)
        with col2:
            st.success("🎉 Image generated successfully!")
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            st.download_button(
                label="📥 Download Image",
                data=img_bytes.getvalue(),
                file_name=f"creation_{len(st.session_state.generated_images)}.png",
                mime="image/png"
            )

    except Exception as e:
        st.error(f"Failed to generate image: {str(e)}")

if __name__ == "__main__":
    main()
