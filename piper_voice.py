import sys
import argparse
import numpy as np
from io import BytesIO
import wave

from fastrtc import ReplyOnPause, Stream, get_stt_model
from loguru import logger
from ollama import chat
from piper import PiperVoice



# STT model
stt_model = get_stt_model()

# TTS: Load Piper model
piper_voice = "en_US-lessac-medium.onnx"
tts_model = PiperVoice.load(piper_voice)

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")



def echo(audio):
    transcript = stt_model.stt(audio)
    logger.debug(f"🎤 Transcript: {transcript}")

    # Get LLM response
    response = chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful LLM in a WebRTC call. Respond clearly and naturally.",
            },
            {"role": "user", "content": transcript},
        ],
        options={"num_predict": 200},
    )
    response_text = response["message"]["content"]
    logger.debug(f"🤖 Response: {response_text}")

    # Piper streaming synth
    for chunk in tts_model.synthesize(response_text):
        # Convert Piper PCM16 bytes → numpy array
        pcm_np = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)

        # Yield tuple (sample_rate, numpy_array)
        yield (chunk.sample_rate, pcm_np)




def create_stream():
    return Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local Voice Chat with Piper TTS")
    parser.add_argument("--phone", action="store_true",
                        help="Launch with FastRTC phone interface")
    args = parser.parse_args()

    stream = create_stream()

    if args.phone:
        logger.info("Launching with FastRTC phone interface...")
        stream.fastphone()
    else:
        logger.info("Launching with Gradio UI...")
        stream.ui.launch(share=True)