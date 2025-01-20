import streamlit as st
import requests
from PIL import Image
import io
from huggingface_hub import InferenceClient
import time

# API details for image captioning - using a faster model
API_URL_CAPTION = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers_caption = {"Authorization": "Bearer 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"}


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


# Define the client for the text-to-image generation model
client = InferenceClient(
    model="stabilityai/stable-diffusion-xl-base-1.0",  # Using a faster model
    token="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"
)

st.set_page_config(
    page_title="AI Vision Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;800;900&display=swap');

    .main {
        background: linear-gradient(135deg, #1a1c2c 0%, #4b1248 50%, #1a1c2c 100%);
        padding: 2rem;
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

    /* Sub-headers */
    .section-header {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 1.5rem 0;
        padding: 10px 0;
    }

    /* Processing indicator */
    .processing-text {
        color: #4ECDC4 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-align: center;
        margin: 1rem 0;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    /* Enhanced form elements */
    .stSelectbox > div > div > div {
        font-weight: bold !important;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
    }

    .stButton > button {
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 0.8rem 2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Header with enhanced boldness
st.markdown('<h1 class="mega-header">🎨 AI Vision Studio</h1>', unsafe_allow_html=True)

option = st.selectbox(
    "Choose Your Creative Tool",
    ("Image Captioning", "Text-to-Image Generation"),
)

if option == "Image Captioning":
    st.markdown('<h2 class="section-header">📸 Image Captioning</h2>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload your image", type=["jpg", "png"])

    if st.button("Generate Caption"):
        if uploaded_image is not None:
            with st.spinner("Processing..."):
                start_time = time.time()
                image = uploaded_image.read()
                img = optimize_image(image)
                st.image(img, caption="Uploaded Image", use_column_width=True)

                caption_response = query_caption(image)
                if caption_response:
                    caption = caption_response[0]['generated_text']
                    st.success(f"Caption: {caption}")
                    st.write(f"Processing time: {time.time() - start_time:.2f} seconds")

elif option == "Text-to-Image Generation":
    st.markdown('<h2 class="section-header">🎨 Text-to-Image Generation</h2>', unsafe_allow_html=True)
    text_input = st.text_input("Describe your image:", placeholder="Enter your description...")

    if st.button("Generate Image"):
        if text_input:
            with st.spinner("Creating your image..."):
                start_time = time.time()
                try:
                    generated_image = client.text_to_image(
                        text_input,
                        negative_prompt="blurry, bad quality, distorted",
                        num_inference_steps=30,  # Reduced for faster generation
                        guidance_scale=7.5
                    )
                    st.image(generated_image, caption="Generated Image", use_column_width=True)
                    st.write(f"Generation time: {time.time() - start_time:.2f} seconds")

                    # Save image
                    img_bytes = io.BytesIO()
                    generated_image.save(img_bytes, format='PNG')
                    st.download_button(
                        label="Download Image",
                        data=img_bytes.getvalue(),
                        file_name="generated_image.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error("Failed to generate image. Please try again.")

st.markdown("---")
st.markdown("Made with ❤️ by AI Vision Studio")