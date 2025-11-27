# 🧠 Vision2Lang: A Multimodal Vision-to-Language Assistant

**Vision2Lang** is a multimodal AI assistant that can *see* and *speak* — it generates natural language descriptions and answers questions about images in real time.

<p align="center">
  <img src="https://github.com/<your-username>/vision2lang/assets/demo.gif" width="600"/>
</p>

---

## 🚀 Features
- 🖼️ Image captioning using pretrained vision-language models (BLIP)
- 💬 Visual question answering (ask about the image)
- 🔊 Optional speech output using TTS
- 🎥 Real-time webcam mode (optional)
- 🌐 Simple Gradio web interface for demo

---

## 🧩 Tech Stack
- **Python**, **PyTorch**, **Transformers**
- **BLIP / BLIP-2** for vision-language modeling
- **Gradio** for interactive UI
- **gTTS** for text-to-speech

---

## ⚙️ Installation

### Prerequisites
- **Python 3.10, 3.11, or 3.12** (Python 3.13+ may have compatibility issues)
- **pip** (Python package manager)
- **4GB+ RAM** (8GB recommended)
- **GPU with CUDA** (optional, for faster inference)

```bash
# Check your Python version
python --version  # Should be 3.10.x, 3.11.x, or 3.12.x

# If you have Python 3.13, use Python 3.12 instead:
# py -3.12 -m pip install -r requirements.txt
# py -3.12 src/app.py

git clone https://github.com/<your-username>/vision2lang.git
cd vision2lang
python -m venv venv
source venv/bin/activate  # (venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

---

## 🎯 Usage

### Start the Application

```bash
python src/app.py
```

The Gradio interface will launch at `http://localhost:7860`

### Features Overview

#### 1. 🖼️ Image Captioning
- Upload any image (JPG, PNG, etc.)
- Click "Generate Caption" to get an AI description
- Toggle text-to-speech for audio output

#### 2. 💬 Visual Question Answering
- Upload an image
- Ask questions like:
  - "What is in this image?"
  - "What color is the car?"
  - "How many people are there?"
- Get instant AI-powered answers

#### 3. 📸 Webcam Mode
- Click "Capture & Describe" to take a photo
- Get instant descriptions of your surroundings
- Perfect for accessibility applications

---

## 🧪 How It Works

### The Multimodal Pipeline

```
Image Input → Visual Encoder → Shared Embedding Space → Language Decoder → Text Output
```

**Vision2Lang** uses **BLIP** (Bootstrapping Language-Image Pre-training) models:

1. **Image Encoder**: Converts images into vector embeddings
2. **Shared Space**: Aligns visual and textual representations
3. **Language Decoder**: Generates natural language from embeddings

### Models Used

- `Salesforce/blip-image-captioning-base` - For generating descriptions
- `Salesforce/blip-vqa-base` - For answering questions about images

---

## 📁 Project Structure

```
vision2lang/
├── src/
│   ├── app.py          # Gradio web interface
│   ├── inference.py    # BLIP model inference logic
│   └── utils.py        # Helper functions (TTS, image processing)
├── data/               # Sample images directory
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

---

## 🚀 Advanced Usage

### Public Access

To create a public link (share with others):

```python
# In src/app.py, change:
demo.launch(share=True)
```

### Custom Configuration

Modify inference parameters in `src/inference.py`:

```python
caption = caption_image(image, max_length=100)  # Longer captions
```

---

## 🎓 Learning Outcomes

By building this project, you'll understand:

- ✅ Multimodal AI architecture (vision + language)
- ✅ Using pretrained transformer models
- ✅ Building interactive ML demos with Gradio
- ✅ Image preprocessing and embedding generation
- ✅ Real-world AI application deployment

---

## 🔧 Troubleshooting

**Python 3.13 Compatibility Issue**
```bash
ModuleNotFoundError: No module named 'pyaudioop'
```
**Solution:** Use Python 3.10, 3.11, or 3.12 instead:
```bash
# Check available Python versions
py -0  # Windows
python3 --version  # Mac/Linux

# Install with specific version
py -3.12 -m pip install -r requirements.txt
py -3.12 src/app.py
```

**CUDA Out of Memory?**
- Models automatically fall back to CPU
- Or use smaller batch sizes

**Webcam not working?**
- Check camera permissions
- Ensure no other app is using the webcam

**Slow inference?**
- First run downloads models (~500MB)
- Subsequent runs are much faster
- GPU highly recommended for real-time use

**"No module named X" errors?**
- Make sure you installed requirements: `pip install -r requirements.txt`
- Try upgrading pip: `pip install --upgrade pip`

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new vision-language models
- Improve the UI/UX
- Add more features (batch processing, API endpoint, etc.)

---

## 📚 References

- [BLIP Paper](https://arxiv.org/abs/2201.12086)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [Gradio Documentation](https://gradio.app/docs/)

---

## 📄 License

This project is for educational purposes. Model licenses apply from Hugging Face.

---

**Built with ❤️ for learning multimodal AI**

