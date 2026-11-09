import pygame
import pygame.gfxdraw
import time

from audio import pipeline
from engines.base_engine import BACKGROUND_COLOR, BaseEngine
from audio.pipeline import AudioPipeline


pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()

USE_DELTA_TIME = True 

class PygameEngine(BaseEngine): # these are values to be stored in by update and used in render
    def setup(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.features = {}
        self.position_x = 640
        self.position_y = 360
        self.amplitude_radius = 100
        self.circle_speed = 120 

        self.dt_warning = False
        self.max_dt = 0.1 # stops the objects from teleporting 

        # self.dt_print = False
        # self.frame_count = 0
        # self.time_total = 0

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True

    def update(self, audio_features: dict) -> None: # update something every frame
        self.features = audio_features
        if USE_DELTA_TIME == True:
            dt = self.clock.tick(self.target_fps) / 1000.0 # real time frames
        else:
            dt = 1 / self.target_fps # every frame takes the same time
            if self.dt_warning == False: # a print warning incase i forgor to turn on dt
                print("WARNING: DT is off")
                self.dt_warning = True


        if dt >= self.max_dt: # set dt back to 0.1 if it goes over
            dt = self.max_dt

        self.amplitude_radius = 100 + (2700 * self.features.get("amplitude", 0)) # 2700 is my scaler for amplitutude 
        self.position_x = self.position_x + (self.circle_speed * dt) # means the circle will move the same speed no matter the frame rate
        if self.position_x > self.width: # if the circle hits the right border
            self.circle_speed = -120
        elif self.position_x < 0: # if the circle hits the left border
            self.circle_speed = 120

        # self.frame_count = self.frame_count + 1
        # self.time_total = self.time_total + dt
        # if self.dt_print == False:
        #     print(dt)
        #     self.dt_print = True
        # if self.time_total >= 1:
        #     fps = self.frame_count / self.time_total
        #     print("FPS " + str(fps))
        #     self.frame_count = 0
        #     self.time_total = 0

    def render(self) -> None: # draw stuff every frame
        self.screen.fill(BACKGROUND_COLOR)
        pygame.gfxdraw.circle(self.screen, int(self.position_x), int(self.position_y), int(self.amplitude_radius), (255, 0, 0))
        pygame.display.flip()

    def teardown(self) -> None:
        pygame.quit()
