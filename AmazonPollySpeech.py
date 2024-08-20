import random
import requests
from rich import print
import urllib.parse


''' -Information:
Import: `from AmazonPollySpeech import AmazonPollyManager`
Initialize: `amazonpolly_manager = AmazonPollyManager()`
--------------------------
Thanks to SietseT, the creator of [ElundusCore](https://github.com/SietseT/ElundusCoreApp)! I got the idea with Amazon Polly TTS from his project and checked out how he did it
--------------------------

>>:-  pip install requests==2.32.3
      pip install urllib.parse

Usage: 
1. amazonpolly_output = amazonpolly_manager.convertTextToAudio(text, voice_name="Brian", language="en")!?            // Converts tts and returns the file path

text = Text that should be converted to audio with Amazon Polly
voice_name = Name of the Voice in Amazon Polly you want to use (Default: Brian)
language = If you choose a random voice, you can specify the language here (Default: en)
    languages: en, ar, zh, da, nl, fr, de, hi, is, it, ja, ko, no, pl, pt, ro, ru, es, sv, tr, cy
    
!? - Nullable. May in some circumstances return "None"
'''


languages = {
    "en": {
        "English (British)": ["Amy", "Brian", "Emma"],
        "English (US)": ["Ivy", "Joanna", "Joey", "Justin", "Kendra", "Kimberly", "Matthew", "Salli"],
        "English (Australian)": ["Nicole", "Russell"],
        "English (Welsh)": ["Geraint"],
        "English (Indian)": ["Aditi", "Raveena"],
    }, "ar": {
        "Arabic": ["Zeina"],
    }, "zh": {
        "Chinese, Mandarin": ["Zhiyu"],
    }, "da": {
        "Danish": ["Naja", "Mads"],
    }, "nl": {
        "Dutch": ["Lotte", "Ruben"],
    }, "fr": {
        "French": ["Celine", "Lea", "Mathieu"],
        "French (Canadian)": ["Chantal"],
    }, "de": {
        "German": ["Marlene", "Vicki", "Hans"],
    }, "hi": {
        "Hindi": ["Aditi"],
    }, "is": {
        "Icelandic": ["Dora", "Karl"],
    }, "it": {
        "Italian": ["Bianca", "Carla", "Giorgio"],
    }, "ja": {
        "Japanese": ["Mizuki", "Takumi"],
    }, "ko": {
        "Korean": ["Seoyeon"],
    }, "no": {
        "Norwegian": ["Liv"],
    }, "pl": {
        "Polish": ["Ewa", "Jacek", "Jan", "Maja"],
    }, "pt": {
        "Portuguese (Brazilian)": ["Camila", "Ricardo", "Vitoria"],
        "Portuguese (European)": ["Cristiano", "Ines"],
    }, "ro": {
        "Romanian": ["Carmen"],
    }, "ru": {
        "Russian": ["Maxim", "Tatyana"],
    }, "es": {
        "Spanish (European)": ["Conchita", "Enrique", "Lucia"],
        "Spanish (Mexican)": ["Mia"],
        "Spanish (US)": ["Lupe", "Miguel", "Penelope"],
    }, "sv": {
        "Swedish": ["Astrid"],
    }, "tr": {
        "Turkish": ["Filiz"],
    }, "cy": {
        "Welsh": ["Gwyneth"],
    }
}   


class AmazonPollyManager:

    def __init__(self):
        print("[orange]AmazonPollySpeech[/orange]-> [green]Successfully connected to Amazon Polly")


    # Convert tts ---> Returns the file path
    def convertTextToAudio(self, text, voice_name="Brian", language="en"):
        if len(text) == 0:
            print("[orange]AmazonPollySpeech[/orange]-> [yellow]convertTextToAudio[/yellow] - [red]The message that was supposed to be converted to audio was empty. Could not convert to audio. Sorry!! [blue](Returned: None)")
            return
        
        names = []
        
        for subcategory in languages.get(language, {}).values():
            names.extend(subcategory)
        
        if voice_name == "random":
            voice_name = random.choice(names)
            
            
        temp_text = text
        temp_text = text.replace(' ', '%26')
        temp_text = text.replace('#', '%23')
        
        temp_text = text.strip()
        encoded_text = urllib.parse.quote(temp_text)
        
        response = requests.get(f'https://api.streamelements.com/kappa/v2/speech?voice={voice_name}&text={encoded_text}')
        if response.status_code == 422:
            print('[orange]AmazonPollySpeech[/orange]-> [yellow]convertTextToAudio[/yellow] - [red]Text length too long. Cannot convert to audio. Sorry!! [blue](Returned: None)')
            return
        if response.status_code == 429:
            print('[orange]AmazonPollySpeech[/orange]-> [yellow]convertTextToAudio[/yellow] - [red]Rate limit reached. Please try again in a minute. Cannot convert to audio. Sorry!! [blue](Returned: None)')
            return

        with open((f"_Msg{str(hash(text))}{str(hash(voice_name))}"[:245] + ".wav"), 'wb') as f:
            f.write(response.content)


if __name__ == '__main__': 
    exit("Do not run this file directly")