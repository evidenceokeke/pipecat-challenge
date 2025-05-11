import asyncio
import time
from pipecat.audio.vad.silero import SileroVADAnalyzer
from loguru import logger


class SilenceDetector:
    def __init__(self, vad_analyzer=None, silence_threshold=10, callback=None):
        self.vad_analyzer = vad_analyzer or SileroVADAnalyzer()
        self.silence_threshold = silence_threshold
        self.callback = callback
        self.silence_start_time = None
        self.active = False

    async def start_detection(self):
        self.active = True
        logger.info("Silence detection started")

        while self.active:
            is_speech = self.vad_analyzer.is_speech()
            current_time = time.time()

            if not is_speech:
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

