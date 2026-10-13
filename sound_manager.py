from pathlib import Path
import pygame

class SoundManager:
    """Manages audio loading, volume balancing, and playback for Genius Arcade."""
    def __init__(self):
        self.sounds_dir = Path(__file__).parent / "sounds"
        # Preload sound effects installed on the user's system
        self.pop_sound = pygame.mixer.Sound(self.sounds_dir / "pop.wav")
        self.damage_sound = pygame.mixer.Sound(self.sounds_dir / "damage.wav")
        self.correct_sound = pygame.mixer.Sound(self.sounds_dir / "correct.wav")
        self.wrong_sound = pygame.mixer.Sound(self.sounds_dir / "wrong.wav")
        # Set default balanced volumes for different game scenarios.
        self.pop_sound.set_volume(0.45)
        self.damage_sound.set_volume(0.55)
        self.correct_sound.set_volume(0.45)
        self.wrong_sound.set_volume(0.4)

    def play_pop(self):
        """Plays ball pop sound when destroyed by spike."""
        self.pop_sound.play()

    def play_damage(self):
        """Plays heavy impact sound when barrier strikes spike."""
        self.damage_sound.play()

    def play_correct(self):
        """Plays celebratory chime on correct math answer."""
        self.correct_sound.play()

    def play_wrong(self):
        """Plays subtle error tone on incorrect input."""
        self.wrong_sound.play()