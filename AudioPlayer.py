import os
import time
import pygame
import asyncio
import soundfile as sf
from mutagen.mp3 import MP3


''' -Information:
Import: `from AudioPlayer import AudioManager`
Initialize: `audio_manager = AudioManager()`

>>:-  pip install pygame==2.6.0
      pip install mutagen==1.47.0
      pip install soundfile==0.12.1

Usage: 
1. audio_manager.play_audio(file_path, sleep_during_playback=True, delete_file=False, pygame_music=True)
2. audio_manager.play_audio_async(file_path)

file_path = Path to the audio file that should be played
sleep_during_playback (bool): True: program will wait for the length of the audio before returning, False: program will return immediately
delete_file (bool): True: deletes the file after playing, False: keeps the file - WARNING: It will stop pygame, so it won't work if you play multiple audios
pygame_music (bool): True: Uses Pygame Music, False: Uses PyGame Sound
    PyGame Music: only 1 sound at a time, good for large files
    PyGame Sound: multiple sounds simultaneously, good for small/short files
'''


class AudioManager:
    def __init__(self):
        pygame.mixer.init(frequency=48000, buffer=1024) # default 44100, 512
        

    def play_audio(self, file_path, sleep_during_playback=True, delete_file=False, pygame_music=True):
        print(f"Playing file with pygame: {file_path}")
        
        if pygame_music:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        else:
            pygame_sound = pygame.mixer.Sound(file_path) 
            pygame_sound.play()
        
        if sleep_during_playback:
            extension = os.path.splittext(file_path)
            if extension.lower() == '.wav':
                wav_file = sf.SoundFile(file_path)
                file_length = wav_file.frames / wav_file.samplerate
                wav_file.close()
            elif extension.lower() == '.mp3':
                mp3_file = MP3(file_path)
                file_length = mp3_file.info.length
            else:
                print("Cannot play audio, unknown file type")
                return

            time.sleep(file_length)
            
            if delete_file:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                try:  
                    os.remove(file_path)
                    print(f"Deleted the audio file.")
                except PermissionError:
                    print(f"Couldn't remove {file_path} because it is being used by another process.")


    async def play_audio_async(self, file_path):
        print(f"Playing file with asynchronously with pygame: {file_path}")
        pygame_sound = pygame.mixer.Sound(file_path) 
        pygame_sound.play()

        extension = os.path.splittext(file_path)
        if extension.lower() == '.wav':
            wav_file = sf.SoundFile(file_path)
            file_length = wav_file.frames / wav_file.samplerate
            wav_file.close()
        elif extension.lower() == '.mp3':
            mp3_file = MP3(file_path)
            file_length = mp3_file.info.length
        else:
            print("Cannot play audio, unknown file type")
            return

        await asyncio.sleep(file_length)


if __name__ == '__main__':
    exit("Do not run this file directly")
