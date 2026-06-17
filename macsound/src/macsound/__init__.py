import math
import wave
import struct
import tempfile
import subprocess
import os
import platform


def Beep(frequency=1000, duration=500):
    if platform.system() != "Darwin":
        raise RuntimeError("macsound.Beep() works only on macOS")

    sample_rate = 44100
    duration_seconds = duration / 1000
    volume = 0.5
    num_samples = int(sample_rate * duration_seconds)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    filename = temp_file.name
    temp_file.close()

    try:
        with wave.open(filename, "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            for i in range(num_samples):
                value = volume * math.sin(2 * math.pi * frequency * i / sample_rate)
                data = struct.pack("<h", int(value * 32767))
                wav_file.writeframesraw(data)

        subprocess.run(["afplay", filename], check=True)

    finally:
        if os.path.exists(filename):
            os.remove(filename)


def PlaySound(filename):
    if platform.system() != "Darwin":
        raise RuntimeError("macsound.PlaySound() works only on macOS")

    subprocess.run(["afplay", filename], check=True)