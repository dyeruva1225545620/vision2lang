#!/usr/bin/env python3
"""
Demo script showing how to use Vision2Lang programmatically
This demonstrates using the inference functions without the Gradio UI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from inference import caption_image, answer_question
from utils import text_to_speech
from PIL import Image
import urllib.request

def download_sample_image():
    """
    Download a sample image for testing
    """
    url = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131"  # Cat image
    save_path = "data/sample_cat.jpg"
    
    os.makedirs("data", exist_ok=True)
    
    print("📥 Downloading sample image...")
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"✅ Image saved to: {save_path}")
        return save_path
    except Exception as e:
        print(f"❌ Failed to download: {e}")
        return None

def demo_captioning(image_path):
    """
    Demo: Image captioning
    """
    print("\n" + "="*60)
    print("🖼️  DEMO 1: Image Captioning")
    print("="*60)
    
    try:
        # Load image
        image = Image.open(image_path)
        print(f"📷 Loaded image: {image_path}")
        print(f"   Size: {image.size}")
        
        # Generate caption
        print("\n🤖 Generating caption...")
        caption = caption_image(image)
        
        print(f"\n✅ Caption: \"{caption}\"")
        
        # Generate audio
        print("\n🔊 Generating audio...")
        audio_path = text_to_speech(caption)
        if audio_path:
            print(f"✅ Audio saved to: {audio_path}")
        
        return caption
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def demo_vqa(image_path, questions):
    """
    Demo: Visual Question Answering
    """
    print("\n" + "="*60)
    print("💬 DEMO 2: Visual Question Answering")
    print("="*60)
    
    try:
        # Load image
        image = Image.open(image_path)
        print(f"📷 Using image: {image_path}")
        
        # Ask multiple questions
        for i, question in enumerate(questions, 1):
            print(f"\n❓ Question {i}: {question}")
            
            answer = answer_question(image, question)
            print(f"✅ Answer: {answer}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_batch_processing(image_paths):
    """
    Demo: Process multiple images
    """
    print("\n" + "="*60)
    print("📦 DEMO 3: Batch Processing")
    print("="*60)
    
    results = []
    
    for i, path in enumerate(image_paths, 1):
        print(f"\n[{i}/{len(image_paths)}] Processing: {path}")
        
        try:
            image = Image.open(path)
            caption = caption_image(image)
            results.append({
                "image": path,
                "caption": caption
            })
            print(f"   ✅ {caption}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return results

def main():
    """
    Run all demos
    """
    print("🧠 Vision2Lang - Programmatic Usage Demo")
    print("="*60)
    
    # Check if we have sample images
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Get image files in data directory
    image_files = [
        os.path.join(data_dir, f) 
        for f in os.listdir(data_dir) 
        if f.endswith(('.jpg', '.jpeg', '.png'))
    ] if os.path.exists(data_dir) else []
    
    # If no images, try to download one
    if not image_files:
        print("\n⚠️  No images found in data/ directory")
        print("Would you like to download a sample image? (y/n)")
        response = input("> ").strip().lower()
        
        if response == 'y':
            sample_path = download_sample_image()
            if sample_path:
                image_files = [sample_path]
    
    if not image_files:
        print("\n❌ No images available for demo")
        print("💡 Tip: Add some .jpg or .png images to the data/ directory")
        return
    
    # Use first image for demos
    test_image = image_files[0]
    
    # Demo 1: Image Captioning
    caption = demo_captioning(test_image)
    
    # Demo 2: Visual Question Answering
    demo_questions = [
        "What is in this image?",
        "What color is the main object?",
        "Is this indoors or outdoors?",
    ]
    demo_vqa(test_image, demo_questions)
    
    # Demo 3: Batch Processing (if multiple images)
    if len(image_files) > 1:
        demo_batch_processing(image_files[:3])  # Process first 3 images
    
    print("\n" + "="*60)
    print("✅ All demos completed!")
    print("="*60)
    print("\n💡 Next steps:")
    print("   - Run 'python src/app.py' for the web interface")
    print("   - Try your own images in the data/ directory")
    print("   - Explore src/inference.py to see how it works")

if __name__ == "__main__":
    main()

