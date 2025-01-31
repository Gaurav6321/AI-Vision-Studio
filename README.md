# 🎨 AI Vision Studio

AI Vision Studio is a powerful web application that combines state-of-the-art image captioning and text-to-image generation capabilities, built with Streamlit and Hugging Face's inference API.

## ✨ Features

### Image Captioning
- Upload images in JPG or PNG format
- Get accurate AI-generated descriptions of your images
- Fast processing with optimized model performance
- Support for high-resolution images with automatic resizing

### Text-to-Image Generation
- Convert text descriptions into stunning images
- High-quality image generation using Stable Diffusion
- Customizable generation parameters
- One-click image download functionality

## 🚀 Technologies Used

- **Frontend Framework**: Streamlit
- **AI Models**: 
  - BLIP Image Captioning
  - Stable Diffusion XL
- **API Integration**: Hugging Face Inference API
- **Image Processing**: Pillow (PIL)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-vision-studio.git
cd ai-vision-studio
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Hugging Face API token:
   - Create an account on Hugging Face
   - Generate an API token
   - Replace the token in the code with your token

## 📦 Dependencies

```
streamlit
requests
Pillow
huggingface-hub
python-dotenv
```

## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `https://ai-vision-studio.streamlit.app/`

3. Choose between Image Captioning or Text-to-Image Generation

4. For Image Captioning:
   - Upload an image
   - Click "Generate Caption"
   - View the AI-generated description

5. For Text-to-Image Generation:
   - Enter your text description
   - Click "Generate Image"
   - Download the generated image

## 🎨 UI Features

- Modern gradient background
- Glass morphism design elements
- Responsive layout
- User-friendly interface
- Progress indicators
- Download capabilities
- Error handling with user feedback

## ⚡ Performance

- Optimized image processing
- Fast model inference
- Efficient memory management
- Progress tracking
- Error handling and recovery

## 🔒 Security

- API key protection
- Input validation
- Secure file handling
- Error message sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for providing the AI models
- Streamlit for the amazing web framework
- The open-source community for inspiration and support

## 📞 Contact

For any queries or suggestions, please open an issue in the GitHub repository or contact [your-email@example.com].

## 🔮 Future Improvements

- [ ] Add more AI models
- [ ] Implement batch processing
- [ ] Add user authentication
- [ ] Improve error handling
- [ ] Add more customization options
- [ ] Implement caching for better performance
- [ ] Add support for more image formats
