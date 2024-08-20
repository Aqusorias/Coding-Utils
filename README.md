# Modules - made by Aqusorias

![GitHub downloads](https://img.shields.io/github/downloads/Aqusorias/Coding-Utils/total?style=flat-square)

These are some Modules that I've made that might come in handy at some point. They mostly are useful for streaming, but it's not restricted for it

---

- [Different Modules](https://github.com/Aqusorias/Coding-Utils#different-modules)
- [How to use](https://github.com/Aqusorias/Coding-Utils#how-to-use)
- [Different Infos](https://github.com/Aqusorias/Coding-Utils#different-infos)
- [Special Thanks](https://github.com/Aqusorias/Coding-Utils#special-thanks)

---

# Different Modules
- **Audioplayer.py** - The Audio Player lets you play audio files via pygame.
- **obsWebsockets.py*** - obsWebsockets lets you connect with your OBS and change different things such as changing the source visibility, filter visibility
- **AzureSpeech.py*** - AzureSpeech lets you convert text into TTS with different voices and voice styles (angry, cheerful, whispering, ...)
- **ElevenLabsSpeech.py*** - ElevenLabsSpeech lets you convert text into TTS with a premade voice in [ElevenLabs](https://elevenlabs.io).
- **AmazonPollySpeech.py** - AmazonPollySpeech lets you convert text into TTS with different voices (used by StreamElements and StreamLabs).
- **gTTSSpeech.py** - ~Comming soon~

****Needs some pre-preparations, explained in How to use*** 

The Speech modules convert text into an audio file which then can be played with my Audioplayer. Exception is ElevenLabsSpeech, that also can play- and stream it itself.

> AzureSpeech & ElevenLabsSpeech rely on Microsoft Azure's and ElevenLab's API, which aren't free. 11Labs for example only has 10 minutes of free tts per month


---

# How to use
- Download the module you want to use and put it into your workspace. **Must be in the same folder where it will be used**
- Import the module in your main file with "from [filename] import [class]". To get the class, just open the module you've just downloaded and check it
- Initialize it with "(variable) = [class]()"
- Finished! After you have initialized it, you can just use it normally

In each module on top of the file is more information on how to use it, how to set it up, and docs if you want to modify it.

> *Pre-preparations for each module that needs it:
> - obsWebsockets.py: In OBS, go to Tools -> WebSockets Server Settings -> Enable the WebSockets Server checkbox, set Server Port to 4455, set the Password to 'OBSWebSocketPassword'
> - AzureSpeech.py: Login into [Azure](https://azure.microsoft.com/en-us/products/ai-services/ai-speech), create a Speech Recourse and get the API key- and region. Add these into your Windows User Variables with the names 'AZURE_TTS_KEY' & 'AZURE_TTS_REGION'
> - ElevenLabsSpeech.py: Login into [ElevenLabs](https://elevenlabs.io), get your API key and add it into your Windows User Variables with the name 'ELEVENLABS_API_KEY'

---

# Different Infos

Some modules return a value, and in some cases, in some functions, it CAN return None if there's a problem. Don't forget that and in some cases you should add a if-None to restrain your problem from breaking

- Coloring explained: 
- - green: Success! Everything worked as expected
- - red: Error.. Something broke
- - bright red: Warning. Something happened, but nothing major. Everything still should work well

---

# Special Thanks

Special thanks to [SietseT](https://github.com/SietseT) which made the [Elundus Core](https://github.com/SietseT/ElundusCoreApp) App! It gave me the idea to make the AmazonPollySpeech and how to do it

Also special thanks to [DougDoug](https://github.com/DougDougGithub) that made me do all this Coding and also brought me to the idea of doing it this way, go watch him on [Youtube](https://www.youtube.com/@DougDoug) ^^