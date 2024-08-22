import os
import time
import wave
import pygame
import pyaudio
import keyboard
import soundfile as sf
from rich import print
from mutagen.mp3 import MP3
from datetime import datetime
from pydub import AudioSegment


''' -Information:
Import: `from AudioPlayer import AudioManager`
Initialize: `audio_manager = AudioManager()`

>>:-  pip install pygame==2.6.0
      pip install mutagen==1.47.0
      pip install soundfile==0.12.1
      pip install pyDub==0.25.1
      pip install pyaudio==0.2.14
      pip install wave==0.0.2
      pip instakk keyboard==0.13.5
      pip install datetime==5.5
      pip install rich

Usage: 
1. audio_manager.play_audio(file_path, sleep_during_playback=True, delete_file=False, pygame_music=True)!?            // Plays an audio file, waits for the length of the audio before returning
2. audio_manager.stop_audio()                                                                                         // Stops ALL the audios
3. audioplayer_output = audio_manager.convertFile(file_path, new_extension=".wav")!?                                  // Converts an audio file to a new format and returns the file path
4. audioplayer_output = audio_manager.record_audio(duration=0, save_as_wave=True)!?                                   // Records audio from the microphone and returns the file path

file_path = Path to the audio file that should be played
sleep_during_playback (bool): True: program will wait for the length of the audio before returning, False: program will return immediately
delete_file (bool): True: deletes the file after playing, False: keeps the file - WARNING: It will stop pygame, so it won't work if you play multiple audios
pygame_music (bool): True: Uses Pygame Music, False: Uses PyGame Sound
    PyGame Music: only 1 sound at a time, good for large files
    PyGame Sound: multiple sounds simultaneously, good for small/short files
new_extension: New file extension for the audio file
duration: Duration of the recording in seconds (0 = infinite)
save_as_wave: True: saves the recording as a .wav file, False: saves the recording as a .mp3 file

!? - Nullable. May in some circumstances return "None"
'''


class AudioManager:
    
    def __init__(self):
        pygame.mixer.init(frequency=48000, buffer=1024) # default 44100, 512
        print("[orange4]AudioManager[/orange4]-> [green]Successfully connected to AudioManager!")
        

    def play_audio(self, file_path, sleep_during_playback=True, delete_file=False, pygame_music=True): 
        pygame.mixer.init(frequency=48000, buffer=1024)
        if pygame_music:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        else:
            pygame_sound = pygame.mixer.Sound(file_path) 
            pygame_sound.play()
        
        if sleep_during_playback:
            extension = os.path.splitext(file_path)[1]
            if extension.lower() == '.wav':
                wav_file = sf.SoundFile(file_path)
                file_length = wav_file.frames / wav_file.samplerate
                wav_file.close()
            elif extension.lower() == '.mp3':
                mp3_file = MP3(file_path)
                file_length = mp3_file.info.length
            else:
                print("[orange4]AudioManager[/orange4]-> [yellow]play_audio[/yellow] - [red]Cannot play audio, unknown file type. Could not play the audio. Sorry!!")
                return

            time.sleep(file_length)
            
            if delete_file:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                try:  
                    os.remove(file_path)
                except PermissionError:
                    print(f"[orange4]AudioManager[/orange4]-> [yellow]play_audio[/yellow] - [bright_red]Couldn't remove {file_path} because it is being used by another process.")


    def stop_audio(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()


    def convertFile(self, file_path, new_extension=".wav"):
        old_extension = file_path.split('.')[-1].lower()
        new_file_path = file_path.replace(os.path.splitext(file_path)[1], new_extension)
        if os.path.exists(new_file_path):
            return new_file_path
        
        if old_extension == new_extension:
            print("[orange4]AudioManager[/orange4]-> [yellow]convertFile[/yellow] - [bright_red]Source and target formats are the same. No conversion needed. [blue](Returned: None)")
            return

        if old_extension == 'wav':
            audio = AudioSegment.from_wav(file_path)
        elif old_extension == 'mp3':
            audio = AudioSegment.from_mp3(file_path)
        elif old_extension == 'ogg':
            audio = AudioSegment.from_ogg(file_path)
        elif old_extension == 'flac':
            audio = AudioSegment.from_flac(file_path)
        else:
            print("[orange4]AudioManager[/orange4]-> [yellow]convertFile[/yellow] - [red]Cannot convert audio, unknown source file type. Could not convert the file. Sorry!! [blue](Returned: None)")
            return
        audio.export(new_file_path, format=new_extension.lstrip('.'))

        return new_file_path


    def record_audio(self, duration=0, save_as_wave=True):
        now = datetime.now()
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        
        if duration != 0:
            RECORD_SECONDS = duration
        else:
            RECORD_SECONDS = None
            
        outputwav = os.path.join(os.path.abspath(os.curdir), f"_MicRecording{str(hash(now))}"[:245] + ".wav")
        outputmp3 = os.path.join(os.path.abspath(os.curdir), f"_MicRecording{str(hash(now))}"[:245] + ".mp3")
        
        audio = pyaudio.PyAudio()
        
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        
        frames = []
        
        if RECORD_SECONDS:
            print(f'[orange4]AudioManager[/orange4]-> [yellow]record_audio[/yellow] - [cyan]Recording Microphone for [yellow]{RECORD_SECONDS}[/yellow] seconds...')
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                if keyboard.is_pressed('-'):
                    break
                data = stream.read(CHUNK)
                frames.append(data)
        else:
            print(f'[orange4]AudioManager[/orange4]-> [yellow]record_audio[/yellow] - [cyan]Recording Microphone... [/cyan]Press "-" to stop recording.')
            try:
                while True:
                    if keyboard.is_pressed('-'):
                        break
                    data = stream.read(CHUNK)
                    frames.append(data)
            except KeyboardInterrupt:
                pass

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        print(f'[orange4]AudioManager[/orange4]-> [yellow]record_audio[/yellow] - Finished recording.')
        
        
        with wave.open(outputwav, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        if not save_as_wave:
            audio = AudioSegment.from_wav(outputwav)
            audio.export(outputmp3, format="mp3")
            os.remove(outputwav)
            return outputmp3
        else:
            return outputwav
        

if __name__ == '__main__':
    exit("Do not run this file directly")