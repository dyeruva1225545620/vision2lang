# 🚀 Quick Start Guide

Get Vision2Lang running in 5 minutes!

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/vision2lang.git
cd vision2lang

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** First install will download ~500MB of pretrained models from Hugging Face.

## Step 3: Run the Application

```bash
python src/app.py
```

You should see:
```
🚀 Starting Vision2Lang Assistant...
============================================================
Loading BLIP captioning model...
Using device: cuda  (or cpu/mps)
✅ Captioning model loaded successfully!
Running on local URL:  http://127.0.0.1:7860
```

## Step 4: Open in Browser

Navigate to: **http://localhost:7860**

## 🎮 Try These Examples

### Image Captioning
1. Go to "🖼️ Image Captioning" tab
2. Upload any image (or drag & drop)
3. Click "Generate Caption"
4. Listen to the audio description! 🔊

### Visual Q&A
1. Go to "💬 Visual Q&A" tab
2. Upload an image
3. Ask: "What is in this image?"
4. Get an AI-powered answer!

### Webcam Mode
1. Go to "📸 Webcam Mode" tab
2. Click "Capture & Describe"
3. Your webcam will capture and describe what it sees

## 🎯 Example Questions to Ask

- "What color is the object?"
- "How many people are in the image?"
- "What is the person doing?"
- "Where is this photo taken?"
- "Is it daytime or nighttime?"

## 🐛 Troubleshooting

### "No module named 'torch'"
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### "CUDA out of memory"
- The app will automatically use CPU
- Close other GPU-intensive applications

### "Connection error" when loading models
- Check your internet connection
- Models download from Hugging Face on first run

### Webcam not working
- Grant camera permissions
- Close other apps using the webcam

## 📖 What's Next?

- Read the full [README.md](README.md) for architecture details
- Explore the code in `src/` directory
- Try different BLIP models
- Build your own features!

---

**Happy coding! 🎉**

