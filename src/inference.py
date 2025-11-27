# Model logic for Vision2Lang
# This file contains the inference functions for vision-language models

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering
from PIL import Image
import numpy as np

# Global variables to store loaded models
caption_model = None
caption_processor = None
vqa_model = None
vqa_processor = None
device = None

def get_device():
    """
    Determine the best device to run inference on
    """
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():  # For Apple Silicon
        return "mps"
    else:
        return "cpu"

def load_caption_model():
    """
    Load the pretrained BLIP model for image captioning
    
    Returns:
        tuple: (model, processor, device)
    """
    global caption_model, caption_processor, device
    
    if caption_model is None:
        print("Loading BLIP captioning model...")
        device = get_device()
        print(f"Using device: {device}")
        
        # Load the model and processor
        caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        caption_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(device)
        
        print("✅ Captioning model loaded successfully!")
    
    return caption_model, caption_processor, device

def load_vqa_model():
    """
    Load the pretrained BLIP model for visual question answering
    
    Returns:
        tuple: (model, processor, device)
    """
    global vqa_model, vqa_processor, device
    
    if vqa_model is None:
        print("Loading BLIP VQA model...")
        device = get_device()
        print(f"Using device: {device}")
        
        # Load the VQA model and processor
        vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        vqa_model = BlipForQuestionAnswering.from_pretrained(
            "Salesforce/blip-vqa-base"
        ).to(device)
        
        print("✅ VQA model loaded successfully!")
    
    return vqa_model, vqa_processor, device

def prepare_image(image):
    """
    Convert various image formats to PIL Image
    
    Args:
        image: PIL Image, numpy array, or file path
        
    Returns:
        PIL.Image: Converted image
    """
    if isinstance(image, str):
        # If it's a file path
        return Image.open(image).convert('RGB')
    elif isinstance(image, np.ndarray):
        # If it's a numpy array
        return Image.fromarray(image).convert('RGB')
    elif isinstance(image, Image.Image):
        # Already a PIL Image
        return image.convert('RGB')
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")

def caption_image(image, max_length=50):
    """
    Generate a caption for the given image using BLIP
    
    Args:
        image: PIL Image, numpy array, or file path
        max_length: Maximum length of generated caption
        
    Returns:
        str: Generated caption describing the image
    """
    # Load model if not already loaded
    model, processor, dev = load_caption_model()
    
    # Prepare the image
    pil_image = prepare_image(image)
    
    # Process the image
    inputs = processor(images=pil_image, return_tensors="pt").to(dev)
    
    # Generate caption
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=max_length)
    
    # Decode the generated caption
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    
    return caption

def answer_question(image, question, max_length=50):
    """
    Answer a question about the given image using BLIP VQA
    
    Args:
        image: PIL Image, numpy array, or file path
        question: str, question about the image
        max_length: Maximum length of generated answer
        
    Returns:
        str: Answer to the question based on the image content
    """
    if not question or question.strip() == "":
        return "Please ask a question about the image."
    
    # Load VQA model if not already loaded
    model, processor, dev = load_vqa_model()
    
    # Prepare the image
    pil_image = prepare_image(image)
    
    # Process the image and question together
    inputs = processor(images=pil_image, text=question, return_tensors="pt").to(dev)
    
    # Generate answer
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=max_length)
    
    # Decode the generated answer
    answer = processor.decode(outputs[0], skip_special_tokens=True)
    
    return answer

