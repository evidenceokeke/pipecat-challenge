import asyncio
import time
from collections import deque
from pipecat.audio.vad.silero import SileroVADAnalyzer
from loguru import logger


class SilenceDetector:
    def __init__(self, vad_analyzer=None, silence_threshold=10, callback=None):
        self.vad_analyzer = vad_analyzer or SileroVADAnalyzer()
        self.silence_threshold = silence_threshold
        self.callback = callback
        self.silence_start_time = None
        self.active = False
        self.audio_buffer = deque(maxlen=10)

    def add_audio_chunk(self, chunk):
        """Store the latest audio chunk received."""
        self.audio_buffer.append(chunk)

    async def start_detection(self):
        self.active = True
        logger.info("Silence detection started")

        while self.active:
            if not self.audio_buffer:
                await asyncio.sleep(0.5)
                continue

            # Get speech confidence
            audio_data = b''.join(self.audio_buffer)
            speech_confidence = self.vad_analyzer.voice_confidence(audio_data)

            logger.debug(f"Speech confidence: {speech_confidence}")

            current_time = time.time()

            if speech_confidence < 0.3: # Is this a good threshold?
                if self.silence_start_time is None:
                    self.silence_start_time = current_time
                elif current_time - self.silence_start_time >= self.silence_threshold:
                    logger.info("Silence threshold reached")
                    if self.callback:
                        await self.callback()
                    self.silence_start_time = None # Reset
            else:
                self.silence_start_time = None

            await asyncio.sleep(1)


    def stop_detection(self):
        self.active = False
        logger.info("Silence detection stopped")

