import os
from rich import time
from elevenlabs import generate, stream, set_api_key, voices, play, save


''' -Information: SETUP: in your Windows environment variables, set the ELEVENLABS_API_KEY to your 11Labs API key
Import: `from ElevenLabsSpeech import ElevenLabsManager`
Initialize: `elevenlabs_manager = ElevenLabsManager()`
--------------------------
Documentations: https://elevenlabs.io/docs/api-reference/text-to-speech
--------------------------

>>:-  pip install elevenlabs==1.7.0

Usage: 
1. elevenlabs_output = elevenlabs_manager.convertTextToAudio(text, voice="", save_as_wave=True, subdirectory="")!?                   // Converts tts and returns the file path
2. elevenlabs_output = elevenlabs_manager.play_tts(text, voice="", saveFile=True, save_as_wave=True, subdirectory="")!?              // Converts tts and plays it instantly, waits for it to finish until continuing, if saveFile=True, it will return the file path
3. elevenlabs_output = elevenlabs_manager.stream_tts(text, voice="", saveFile=True, save_as_wave=True, subdirectory="")!?            // Converts tts and streams it instantly without waiting for it to finish, if saveFile=True, it will return the file path

text = Text that should be converted to audio with 11Labs
voice = Name of the Voice in 11Labs you want to use
saveFile = True: Saves the audio file, False: Doesn't save the audio file  --: If True, it will return the file path
save_as_wave = True: Saves the audio file as a .wav, False: Saves the audio file as a .mp3
subdirectory = Subdirectory where the audio file should be saved (Empty will be the same directory)

!? - Nullable. May in some circumstances return "None"
'''


class ElevenLabsManager:
    def __init__(self):
        try:
            set_api_key(os.getenv('ELEVENLABS_API_KEY'))
        except TypeError:
            exit("[orange4]ElevenLabsSpeech[/orange4]-> [red]COULD NOT CONNECT TO AZURE!\nDon't forget to set your ELEVENLABS_API_KEY environment variables.")
        print("[orange4]ElevenLabsSpeech[/orange4]-> [green]Successfully connected to ElevenLabs!")
        voices() # Need to call this for some reason
        

    # Convert tts ---> Returns the file path
    def convertTextToAudio(self, text, voice="", save_as_wave=True, subdirectory=""):
        elevenlabs_audio = generate( text=text, voice=voice, model="eleven_monolingual_v1" )

        if save_as_wave:
            file_name = f"___Msg{str(hash(text))}.wav"
        else:
            file_name = f"___Msg{str(hash(text))}.mp3"
            
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(elevenlabs_audio, tts_file)
        return tts_file
            

    # Convert tts, play instantly
    def play_tts(self, text, voice="", saveFile=True, save_as_wave=True, subdirectory=""):
        elevenlabs_audio = generate( text=text, voice=voice, model="eleven_monolingual_v1" )
        
        if saveFile:
          if save_as_wave:
              file_name = f"___Msg{str(hash(text))}.wav"
          else:
              file_name = f"___Msg{str(hash(text))}.mp3"
          tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
          save(elevenlabs_audio, tts_file)
              
          play(elevenlabs_audio)
          if saveFile:
              return tts_file


    # Convert tts, stream instantly (doesn't wait until finished)
    def stream_tts(self, text, voice="", saveFile=True, save_as_wave=True, subdirectory=""):
        elevenlabs_audio = generate( text=text, voice=voice, model="eleven_monolingual_v1", stream=True)
        
        if saveFile:
          if save_as_wave:
              file_name = f"___Msg{str(hash(text))}.wav"
          else:
              file_name = f"___Msg{str(hash(text))}.mp3"
          tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
          save(elevenlabs_audio, tts_file)
        
        stream(elevenlabs_audio)
        if saveFile:
            return tts_file
            

if __name__ == '__main__':
  exit("Do not run this file directly")
