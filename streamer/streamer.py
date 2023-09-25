import numpy as np
import matplotlib.pyplot as plt
import requests
from pydub import AudioSegment
from io import BytesIO

STREAM_URI = "https://netilradio.airtime.pro/api/live-info" # Need to parameterise/appsettings this
CHUNK_SIZE = 4096  # Adjust based on the required buffer size should be config 

def process_audio_chunk(chunk):
    """Sample function to process the audio chunk."""
    audio_data = BytesIO(chunk)
    try:
        audio = AudioSegment.from_mp3(audio_data)
        samples = np.array(audio.get_array_of_samples())
        
        # For demonstration, plot the waveform of the chunk
        plt.figure(figsize=(10, 4))
        plt.plot(samples)
        plt.title('Waveform of Chunk')
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.show()
        
        # TODO: Add more analysis or processing as required

    except Exception as e:
        print(f"Error processing audio chunk: {e}")

def stream_audio():
    with requests.get(STREAM_URI, stream=True) as response:
        response.raise_for_status()
        audio_chunk = b""
        for chunk in response.iter_content(CHUNK_SIZE):
            audio_chunk += chunk
            if len(audio_chunk) >= CHUNK_SIZE:
                process_audio_chunk(audio_chunk)
                audio_chunk = b""

        # Process the last remaining chunk, if any
        if audio_chunk:
            process_audio_chunk(audio_chunk)

if __name__ == "__main__":
    stream_audio()
