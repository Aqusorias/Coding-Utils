import os
from rich import print
from pydub import AudioSegment
from gtts import gTTS


''' -Information:
Import: `from gTTSSpeech import gTTSManager`
Initialize: `gtts_manager = gTTSManager()`
--------------------------
Documentations: https://gtts.readthedocs.io/en/latest/
--------------------------

>>:-  pip install gTTS==2.5.3
      pip install pyDub==0.25.1

Usage: 
1. gtts_output = gtts_manager.convertTextToAudio(text)!?            // Converts tts and returns the file path

text = Text that should be converted to audio with Amazon Polly
    
!? - Nullable. May in some circumstances return "None"
'''


class gTTSManager:

      def __init__(self):
            print("[orange4]AmazonPollySpeech[/orange4] -> [green]Successfully connected to Amazon Polly")


    # Convert tts ---> Returns the file path
      def convertTextToAudio(self, text):
            if len(text) == 0:
                  print("[orange4]gTTSSpeech[/orange4] -> [yellow]convertTextToAudio[/yellow] - [red]The message that was supposed to be converted to audio was empty. Could not convert to audio. Sorry!! [blue](Returned: None)")
                  return

            output = os.path.join(os.path.abspath(os.curdir), f"_Msg{str(hash(text))}"[:245] + ".wav")
            mp3Path = output.replace(".wav", ".mp3")

            gTTSAudio = gTTS(text=text, lang='en', slow=False)
            gTTSAudio.save(mp3Path)
            audiosegment = AudioSegment.from_mp3(mp3Path)
            audiosegment.export(output, format="wav")
            os.remove(mp3Path)

            return output


if __name__ == '__main__': 
    exit("Do not run this file directly")