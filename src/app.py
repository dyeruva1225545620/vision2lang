# Gradio app for Vision2Lang
# This file contains the web interface for the multimodal assistant

import sys
import gradio as gr
from inference import caption_image, answer_question
from utils import text_to_speech, capture_webcam_frame
import os

# Check Python version and provide helpful message
if sys.version_info < (3, 10):
    print("=" * 70)
    print("⚠️  WARNING: Python 3.10 or higher is required!")
    print(f"   You are using Python {sys.version_info.major}.{sys.version_info.minor}")
    print("   Please upgrade to Python 3.10, 3.11, or 3.12")
    print("=" * 70)
    sys.exit(1)

def generate_caption_with_audio(image, enable_tts=True):
    """
    Generate a caption for the image and optionally convert it to speech
    
    Args:
        image: Uploaded image
        enable_tts: Whether to generate audio output
        
    Returns:
        tuple: (caption_text, audio_path or None)
    """
    if image is None:
        return "Please upload an image first.", None
    
    try:
        # Generate caption
        print("🖼️ Generating caption...")
        caption = caption_image(image)
        print(f"✅ Caption: {caption}")
        
        # Generate audio if enabled
        audio_path = None
        if enable_tts:
            print("🔊 Generating audio...")
            audio_path = text_to_speech(caption)
        
        return caption, audio_path
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        return error_msg, None

def answer_with_audio(image, question, enable_tts=True):
    """
    Answer a question about the image and optionally convert it to speech
    
    Args:
        image: Uploaded image
        question: User's question
        enable_tts: Whether to generate audio output
        
    Returns:
        tuple: (answer_text, audio_path or None)
    """
    if image is None:
        return "Please upload an image first.", None
    
    if not question or question.strip() == "":
        return "Please enter a question.", None
    
    try:
        # Answer the question
        print(f"❓ Question: {question}")
        answer = answer_question(image, question)
        print(f"✅ Answer: {answer}")
        
        # Generate audio if enabled
        audio_path = None
        if enable_tts:
            print("🔊 Generating audio...")
            audio_path = text_to_speech(answer)
        
        return answer, audio_path
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        return error_msg, None

def capture_and_caption(enable_tts=True):
    """
    Capture an image from webcam and generate a caption
    
    Args:
        enable_tts: Whether to generate audio output
        
    Returns:
        tuple: (captured_image, caption_text, audio_path or None)
    """
    try:
        # Capture webcam frame
        print("📸 Capturing webcam frame...")
        frame = capture_webcam_frame()
        
        if frame is None:
            return None, "Failed to capture webcam frame. Make sure your webcam is connected.", None
        
        # Generate caption
        caption = caption_image(frame)
        print(f"✅ Caption: {caption}")
        
        # Generate audio if enabled
        audio_path = None
        if enable_tts:
            audio_path = text_to_speech(caption)
        
        return frame, caption, audio_path
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        print(error_msg)
        return None, error_msg, None

def create_interface():
    """
    Create and configure the Gradio interface with multiple tabs
    """
    # Gradio 6.x simplified API
    with gr.Blocks() as demo:
        gr.Markdown(
            """
            # 🧠 Vision2Lang: Multimodal AI Assistant
            
            **See, Understand, and Speak!** Upload images or use your webcam to generate natural language descriptions and answers.
            
            Powered by BLIP (Bootstrapping Language-Image Pre-training)
            """
        )
        
        # Tab 1: Image Captioning
        with gr.Tab("🖼️ Image Captioning"):
            gr.Markdown("### Upload an image and get an AI-generated description")
            
            with gr.Row():
                with gr.Column(scale=1):
                    caption_image_input = gr.Image(
                        type="pil",
                        label="Upload Image",
                        sources=["upload", "clipboard"]
                    )
                    caption_tts_checkbox = gr.Checkbox(
                        label="Enable Text-to-Speech 🔊",
                        value=True
                    )
                    caption_button = gr.Button("Generate Caption", variant="primary")
                
                with gr.Column(scale=1):
                    caption_output = gr.Textbox(
                        label="Generated Caption",
                        placeholder="Caption will appear here...",
                        lines=3
                    )
                    caption_audio_output = gr.Audio(
                        label="Audio Output",
                        type="filepath",
                        autoplay=True
                    )
            
            caption_button.click(
                fn=generate_caption_with_audio,
                inputs=[caption_image_input, caption_tts_checkbox],
                outputs=[caption_output, caption_audio_output]
            )
            
            # Example images
            gr.Examples(
                examples=[
                    os.path.join("data", f) for f in os.listdir("data") 
                    if f.endswith((".jpg", ".jpeg", ".png"))
                ] if os.path.exists("data") and os.listdir("data") else [],
                inputs=caption_image_input,
                label="Example Images (if available)"
            )
        
        # Tab 2: Visual Question Answering
        with gr.Tab("💬 Visual Q&A"):
            gr.Markdown("### Ask questions about your image")
            
            with gr.Row():
                with gr.Column(scale=1):
                    vqa_image_input = gr.Image(
                        type="pil",
                        label="Upload Image",
                        sources=["upload", "clipboard"]
                    )
                    vqa_question_input = gr.Textbox(
                        label="Your Question",
                        placeholder="What is in this image?",
                        lines=2
                    )
                    vqa_tts_checkbox = gr.Checkbox(
                        label="Enable Text-to-Speech 🔊",
                        value=True
                    )
                    vqa_button = gr.Button("Get Answer", variant="primary")
                
                with gr.Column(scale=1):
                    vqa_output = gr.Textbox(
                        label="Answer",
                        placeholder="Answer will appear here...",
                        lines=3
                    )
                    vqa_audio_output = gr.Audio(
                        label="Audio Output",
                        type="filepath",
                        autoplay=True
                    )
            
            vqa_button.click(
                fn=answer_with_audio,
                inputs=[vqa_image_input, vqa_question_input, vqa_tts_checkbox],
                outputs=[vqa_output, vqa_audio_output]
            )
            
            # Suggested questions
            gr.Markdown("""
            **Suggested Questions:**
            - What is in this image?
            - What color is the object?
            - How many people are in the image?
            - What is the person doing?
            - Where is this photo taken?
            """)
        
        # Tab 3: Webcam Mode (Optional)
        with gr.Tab("📸 Webcam Mode"):
            gr.Markdown("### Capture from your webcam and get instant descriptions")
            
            with gr.Row():
                with gr.Column(scale=1):
                    webcam_tts_checkbox = gr.Checkbox(
                        label="Enable Text-to-Speech 🔊",
                        value=True
                    )
                    webcam_button = gr.Button("📸 Capture & Describe", variant="primary")
                
                with gr.Column(scale=1):
                    webcam_image_output = gr.Image(
                        label="Captured Image",
                        type="pil"
                    )
            
            with gr.Row():
                webcam_caption_output = gr.Textbox(
                    label="Description",
                    placeholder="Capture an image to see description...",
                    lines=3
                )
                webcam_audio_output = gr.Audio(
                    label="Audio Output",
                    type="filepath",
                    autoplay=True
                )
            
            webcam_button.click(
                fn=capture_and_caption,
                inputs=[webcam_tts_checkbox],
                outputs=[webcam_image_output, webcam_caption_output, webcam_audio_output]
            )
        
        # Footer
        gr.Markdown(
            """
            ---
            
            ### 🚀 About Vision2Lang
            
            This multimodal AI assistant uses **BLIP** (Bootstrapping Language-Image Pre-training) 
            to understand images and generate natural language descriptions. It demonstrates the 
            power of vision-language models in bridging visual and textual information.
            
            **Features:**
            - 🖼️ Image captioning
            - 💬 Visual question answering
            - 🔊 Text-to-speech output
            - 📸 Real-time webcam support
            
            **Tech Stack:** PyTorch • Transformers • BLIP • Gradio • gTTS
            """
        )
    
    return demo

def main():
    """
    Main function to launch the Gradio interface
    """
    print("🚀 Starting Vision2Lang Assistant...")
    print("=" * 60)
    
    # Create and launch the interface
    demo = create_interface()
    
    # Launch with public link option
    demo.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,        # Default Gradio port
        share=False,             # Set to True to create a public link
        show_error=True
    )

if __name__ == "__main__":
    main()

