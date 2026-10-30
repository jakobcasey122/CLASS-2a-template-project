import pygame
import pygame.gfxdraw

from audio import pipeline
from engines.base_engine import BACKGROUND_COLOR, BaseEngine
from audio.pipeline import AudioPipeline

pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()


class PygameEngine(BaseEngine):
    def setup(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True

    def update(self, audio_features: dict) -> None:
        pass

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        # for i in range(5):
        #     circleradius = int(pipeline.get_features()['amplitude']) * 50000
        #     pygame.gfxdraw.circle(self.screen, 400, 400, circleradius, (255, 0, 0))
        #     print(circleradius)
        #     # int(pipeline.get_features()['amplitude'])
        #     pygame.display.update()
        pygame.display.flip()

    def teardown(self) -> None:
        pygame.quit()
