import math
import random
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 44100
SOUNDS_DIR = Path(__file__).parent / "sounds" # imports all the sounds to be used in the game.
SOUNDS_DIR.mkdir(exist_ok=True) # Create folder in the project directory if it doesnt already exist.


def save_wav(filename: Path, samples: list[float], sample_rate: int = SAMPLE_RATE):
    """Encodes a list of float audio samples (-1.0 to 1.0) into a 16-bit Mono WAV file."""
    with wave.open(str(filename), "w") as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)      # 16-bit (2 bytes per sample)
        wav_file.setframerate(sample_rate)

        raw_bytes = bytearray()
        for s in samples:
            # Clamp value between -1.0 and 1.0, then scale to 16-bit signed int (-32767 to 32767)
            clamped = max(-1.0, min(1.0, s))
            int_sample = int(clamped * 32767)
            raw_bytes.extend(struct.pack("<h", int_sample))

        wav_file.writeframes(raw_bytes)

def create_pop_sound() -> Path:
    """Fast high-to-low drop mixed with a touch of white noise to simulate a pop sound"""
    duration = 0.07
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    phase = 0.0

    for i in range(total_samples):
        progress = i / total_samples
        # Very steep frequency drop: 850 Hz -> 90 Hz
        freq = 850.0 - (760.0 * (progress ** 0.8))
        phase += 2.0 * math.pi * freq / SAMPLE_RATE

        envelope = (1.0 - progress) ** 2
        sine_wave = math.sin(phase)
        noise = random.uniform(-0.35, 0.35)
        # Mix 75% tone + 25% noise burst
        samples.append((0.75 * sine_wave + 0.25 * noise) * envelope * 0.6)

    path = SOUNDS_DIR / "pop.wav"
    save_wav(path, samples)
    return path

def create_damage_sound() -> Path:
    """Low crunchy impact crackle to simulate like a brick crack"""
    duration = 0.18
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    phase = 0.0

    for i in range(total_samples):
        progress = i / total_samples
        # Heavy low frequency drop: 160 Hz -> 40 Hz
        freq = 160.0 - (120.0 * progress)
        phase += 2.0 * math.pi * freq / SAMPLE_RATE

        envelope = (1.0 - progress) ** 1.8
        # Rough square-ish wave for grit/crunch
        raw_wave = 1.0 if math.sin(phase) > 0 else -1.0
        noise = random.uniform(-0.5, 0.5)
        samples.append((0.5 * raw_wave + 0.5 * noise) * envelope * 0.7)

    path = SOUNDS_DIR / "damage.wav"
    save_wav(path, samples)
    return path

def create_correct_sound() -> Path:
    """Bright two-tone arcade chime: Note 1 (E5) quickly ascending to Note 2 (B5)."""
    note1_dur = 0.07
    note2_dur = 0.14
    total_samples = int(SAMPLE_RATE * (note1_dur + note2_dur))
    samples = []
    phase = 0.0

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        if t < note1_dur:
            freq = 659.25  # E5
            progress = t / note1_dur
            envelope = 1.0 - (progress * 0.4)
        else:
            freq = 987.77  # B5
            progress = (t - note1_dur) / note2_dur
            envelope = (1.0 - progress) ** 1.3

        phase += 2.0 * math.pi * freq / SAMPLE_RATE
        # Add a subtle 2nd harmonic (octave) for bell-like brightness
        harmonic = 0.25 * math.sin(phase * 2.0)
        samples.append((math.sin(phase) + harmonic) * envelope * 0.45)

    path = SOUNDS_DIR / "correct.wav"
    save_wav(path, samples)
    return path

def create_wrong_sound() -> Path:
    """Subtle, low-frequency buzz/thud to signal incorrect answer from the user."""
    duration = 0.16
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    phase1 = 0.0
    phase2 = 0.0

    for i in range(total_samples):
        progress = i / total_samples
        # Low, slightly detuned dissonance (180 Hz & 135 Hz)
        freq1 = 180.0 - (40.0 * progress)
        freq2 = 135.0 - (30.0 * progress)
        phase1 += 2.0 * math.pi * freq1 / SAMPLE_RATE
        phase2 += 2.0 * math.pi * freq2 / SAMPLE_RATE

        envelope = (1.0 - progress) ** 1.4
        buzz = 0.5 * math.sin(phase1) + 0.5 * math.sin(phase2)
        samples.append(buzz * envelope * 0.5)

    path = SOUNDS_DIR / "wrong.wav"
    save_wav(path, samples)
    return path


if __name__ == "__main__":
    print("Synthesizing Genius Arcade audio pack...")
    p = create_pop_sound()
    d = create_damage_sound()
    c = create_correct_sound()
    w = create_wrong_sound()
    print(f"Done! Generated 5 retro arcade sound effects in: {SOUNDS_DIR}")
    # Main thing is that to ensure you have all the audio files so it works same on every system playing the game.
    # This can be deleted once the audio files are installed on your hard drive when this code is ran.
