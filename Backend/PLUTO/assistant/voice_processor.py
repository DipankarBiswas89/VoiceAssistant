from gtts import gTTS
import os


def text_to_speech(text, output_file= "response.wav"):
    
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        tts.save(output_file)
    
        return{
        "text" : text,
        "audio_files" : output_file
        }
    
    except Exception as e:
        return{
            "error": f"TTS conversion failed: {str(e)}",
            "text": text,
            "audio_file": None
        }
    