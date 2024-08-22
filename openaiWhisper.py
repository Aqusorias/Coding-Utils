import os
import whisper
import warnings
from rich import print
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")


''' -Information:
Import: `from openaiWhisper import openaiWhisperManager`
Initialize: `openaiwhisper_manager = openaiWhisperManager()`
--------------------------
Documentations: https://github.com/openai/whisper
--------------------------

>>:-  pip install -U openai-whisper
      pip install rich

Usage: 
1. openaiwhisper_output = openaiwhuisper_manager.convertAudioToText(file_path, model="base")!?            // Converts stt and returns the text

file_path = Path to the audio file that should be converted to text
model = Model that should be used for the STT
    32x tiny, 16x base, 6x small, 2x medium, 1x large (x = relative speed)
detect_lang = True: Detects the language of the audio, False: Doesn't detect the language of the audio. Returns "result" & "detected_lang"
    
!? - Nullable. May in some circumstances return "None"
'''


class openaiWhisperManager:
    
    def __init__(self):
        print("[orange4]openaiWhisperManager[/orange4]-> [green]Successfully connected to OpenAI Whisper!")
        
    
    # Convert stt ---> Returns the text
    def convertAudioToText(self, file_path, model="base"): 
        if not os.path.exists(file_path):
            return None
        
        try:
            model = whisper.load_model(model)
            result = model.transcribe(file_path)
            
            return result["text"]
        
        except Exception:
            return None



if __name__ == '__main__':
    exit("Do not run this file directly")