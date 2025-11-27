# Helper functions for Vision2Lang
# This file contains utility functions for the application

from gtts import gTTS
import os
import tempfile
from PIL import Image
import numpy as np
import cv2

def text_to_speech(text, lang='en', slow=False):
    """
    Convert text to speech using gTTS (Google Text-to-Speech)
    
    Args:
        text: str, text to convert to speech
        lang: str, language code (default: 'en')
        slow: bool, speak slowly (default: False)
        
    Returns:
        str: Path to the generated audio file
    """
    try:
        if not text or text.strip() == "":
            return None
        
        # Create a temporary file for the audio
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        audio_path = temp_audio.name
        temp_audio.close()
        
        # Generate speech
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(audio_path)
        
        print(f"🔊 Audio generated: {audio_path}")
        return audio_path
    
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        return None

def preprocess_image(image, target_size=None):
    """
    Preprocess image for display or model input
    
    Args:
        image: PIL Image, numpy array, or file path
        target_size: tuple (width, height) to resize to (optional)
        
    Returns:
        PIL.Image: Preprocessed image
    """
    # Convert to PIL Image if needed
    if isinstance(image, str):
        pil_image = Image.open(image).convert('RGB')
    elif isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image).convert('RGB')
    elif isinstance(image, Image.Image):
        pil_image = image.convert('RGB')
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")
    
    # Resize if target size is specified
    if target_size:
        pil_image = pil_image.resize(target_size, Image.LANCZOS)
    
    return pil_image

def save_uploaded_image(image, directory="data", filename="uploaded_image.jpg"):
    """
    Save uploaded image to disk
    
    Args:
        image: PIL Image or numpy array
        directory: str, directory to save to
        filename: str, name of the file to save
        
    Returns:
        str: Path to saved image
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Convert to PIL Image if needed
        if isinstance(image, np.ndarray):
            pil_image = Image.fromarray(image)
        elif isinstance(image, Image.Image):
            pil_image = image
        else:
            raise ValueError(f"Unsupported image type: {type(image)}")
        
        # Save the image
        save_path = os.path.join(directory, filename)
        pil_image.save(save_path)
        
        print(f"💾 Image saved: {save_path}")
        return save_path
    
    except Exception as e:
        print(f"❌ Error saving image: {e}")
        return None

def resize_image_for_display(image, max_width=800, max_height=600):
    """
    Resize image while maintaining aspect ratio for better display
    
    Args:
        image: PIL Image or numpy array
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        
    Returns:
        PIL.Image: Resized image
    """
    # Convert to PIL Image if needed
    if isinstance(image, np.ndarray):
        pil_image = Image.fromarray(image)
    elif isinstance(image, Image.Image):
        pil_image = image
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")
    
    # Get current dimensions
    width, height = pil_image.size
    
    # Calculate scaling factor
    scale = min(max_width / width, max_height / height, 1.0)
    
    if scale < 1.0:
        new_width = int(width * scale)
        new_height = int(height * scale)
        pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
    
    return pil_image

def capture_webcam_frame():
    """
    Capture a single frame from the default webcam
    
    Returns:
        numpy.ndarray: Captured frame as BGR image, or None if failed
    """
    try:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot open webcam")
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame_rgb
        else:
            print("❌ Failed to capture frame")
            return None
    
    except Exception as e:
        print(f"❌ Error capturing webcam frame: {e}")
        return None

