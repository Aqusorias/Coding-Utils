import os
import re
import random
from rich import print
import azure.cognitiveservices.speech as speechsdk


''' -Information: SETUP: in your Windows environment variables, set the AZURE_TTS_KEY & AZURE_TTS_REGION to your AzureSpeech API key- and region
Import: `from AzureSpeech import AzureTTSManager`
Initialize: `azuretts_manager = AzureTTSManager()`
--------------------------
Documentations: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=windows%2Cterminal&pivots=programming-language-python
                https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt#prebuilt-neural-voices
                https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-speech-synthesis?tabs=browserjs%2Cterminal&pivots=programming-language-python
--------------------------

>>:-  pip install azure-cognitiveservices-speech==1.40.0

Usage: 
1. azuretts_output = azuretts_manager.convertTextToAudio(text, voice_name="random", voice_style="random")!?            // Converts tts and returns the file path
2. azuretts_output = azuretts_manager.getAllPrefixes()                                                                 // Returns a list of all available prefixes (emotions)
3. azuretts_output = azuretts_manager.cutTextIntoParts(text)                                                           // Cuts a text into parts based on the prefixes

text = Text that should be converted to audio with Azure
voice_name = Name of the Voice in Azure you want to use (Default: random)
voice_style = Name of the Voice Style in Azure you want to use (Default: random)

!? - Nullable. May in some circumstances return "None"
'''


AZURE_VOICES = [
    "en-US-DavisNeural",
    "en-US-TonyNeural",
    "en-US-JasonNeural",
    "en-US-GuyNeural",
    "en-US-JaneNeural",
    "en-US-NancyNeural",
    "en-US-JennyNeural",
    "en-US-AriaNeural",
]

AZURE_VOICE_STYLES = [
    "angry",
    "cheerful",
    "excited",
    "hopeful",
    "sad",
    "shouting",
    "terrified",
    "unfriendly",
    "whispering"
]

AZURE_PREFIXES = {
    "(angry)" : "angry",
    "(cheerful)" : "cheerful",
    "(excited)" : "excited",
    "(hopeful)" : "hopeful",
    "(sad)" : "sad",
    "(shouting)" : "shouting",
    "(shout)" : "shouting",
    "(terrified)" : "terrified",
    "(unfriendly)" : "unfriendly",
    "(whispering)" : "whispering",
    "(whisper)" : "whispering",
    "(random)" : "random"
}


class AzureTTSManager:

    def __init__(self):
        self.azure_speechconfig = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_TTS_KEY'), region=os.getenv('AZURE_TTS_REGION'))
        self.azure_speechconfig.speech_synthesis_voice_name = "en-US-AriaNeural"
        self.azure_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.azure_speechconfig, audio_config=None) # None means it wont play the synthesized text out loud
        if not self.azure_speechconfig:
            raise Exception("[orange]AzureSpeech[/orange]-> [red]COULD NOT CONNECT TO AZURE!\nDon't forget to set your AZURE_TTS_KEY and AZURE_TTS_REGION environment variables.")
        else:
            print("[orange]AzureSpeech[/orange]-> [green]Successfully connected to Azure TTS!")


    # Convert tts ---> Returns the file path
    def convertTextToAudio(self, text, voice_name="random", voice_style="random"):
        if len(text) == 0:
            print("[orange]AzureSpeech[/orange]-> [yellow]convertTextToAudio[/yellow] - [red]The message that was supposed to be converted to audio was empty. Could not convert to audio. Sorry!! [blue](Returned: None)")
            return
        
        if voice_name == "random":
            voice_name = random.choice(AZURE_VOICES)
        if voice_style == "random":
            voice_style = random.choice(AZURE_VOICE_STYLES)
        parts = self.cutMessageIntoParts(text)

        ssml_parts = []
        
        for part in enumerate(parts, start=1):
            text = part[1]
        
            if text.lower().startswith("(") and ")" in text:
                prefix = text[0:(text.find(")")+1)]
                if prefix in AZURE_PREFIXES:
                    voice_style = AZURE_PREFIXES[prefix]
                    text = text.removeprefix(prefix)
                
            ssml_part = f"<mstts:express-as style='{voice_style}'>{text}</mstts:express-as><break time='25ms'/>"
            ssml_parts.append(ssml_part)
            
        ssml_text = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml' xml:lang='en-US'><voice name='{voice_name}'><prosody rate='medium'>{''.join(ssml_parts)}</prosody></voice></speak>"
        result = self.azure_synthesizer.speak_ssml_async(ssml_text).get()

        output = os.path.join(os.path.abspath(os.curdir), f"_Msg{str(hash(text))}{str(hash(voice_name))}{str(hash(voice_style))}"[:245] + ".wav")
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            stream = speechsdk.AudioDataStream(result)
            stream.save_to_wav_file(output)
        else:
            print("[orange]AzureSpeech[/orange]-> [yellow]convertTextToAudio[/yellow] - [red]Azure failed. Could not convert to audio. Sorry!! [blue](Returned: None)")
            return
        
        return output


    def getAllPrefixes(self):
        return list(AZURE_PREFIXES.keys())
    
    
    def cutMessageIntoParts(self, text):
        matches = [(match.group(), match.start(), match.end()) for match in re.finditer(r'\(\w+\)', text)]
        prevparts = []
        parts = []
        prev_end = 0
        
        for match in matches:
            prevparts.append(match[1])
        if len(prevparts) == 1:
            end = len(text)
            prevparts.append((end))
        
        ranges = [(prevparts[i], prevparts[i + 1]) for i in range(0, len(prevparts), 2)]
        
        for start, end in ranges:
            if start > prev_end:
                parts.append(text[prev_end:start])
            parts.append(text[start:end])
            prev_end = end
        
        if prev_end < len(text):
            parts.append(text[prev_end:])
        return parts


if __name__ == '__main__': 
    exit("Do not run this file directly")