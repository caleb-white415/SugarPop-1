import pygame as pg

class SoundManager:
    def __init__(self):
        self.sounds = {
            'exploding_bucket' : pg.mixer.Sound('explosion.wav'),
            'add_sugar' : pg.mixer.Sound ('add_sugar.ogg'),
            'complete_level' : pg.mixer.Sound('level_complete.wav')
        }


    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()