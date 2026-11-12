import pygame
import pygame.gfxdraw
import time

from audio import pipeline
from engines.base_engine import BACKGROUND_COLOR, BaseEngine
from audio.pipeline import AudioPipeline


pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()

USE_DELTA_TIME = True 

class PygameEngine(BaseEngine): 
    def setup(self) -> None: # these are values to be stored in by update and used in render
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

        self.features = {}
        self.amp_position_x = 640
        self.amp_position_y = 360
        self.amplitude_radius = 100
        self.circle_speed = 120 

        # buttons
        self.button_left = pygame.Rect(700, 900, 250, 150)
        self.button_right = pygame.Rect(1000, 900, 250, 150)
        # button text
        self.button_font = pygame.font.Font(None, 40) # loads font (none is pygame default)
        self.button_left_text = self.button_font.render("Left", True, (0, 0, 0)) # text to image
        self.button_right_text = self.button_font.render("Right", True, (0, 0, 0))

        # dt
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
        
        self.amp_position_x = self.amp_position_x + (self.circle_speed * dt) # means the circle will move the same speed no matter the frame rate
        if self.amp_position_x > self.width - self.amplitude_radius: # if the circle hits the right border
            self.circle_speed = -120
        elif self.amp_position_x < 0 + self.amplitude_radius: # if the circle hits the left border
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
        pygame.gfxdraw.circle(self.screen, int(self.amp_position_x), int(self.amp_position_y), int(self.amplitude_radius), (255, 0, 0))
        pygame.gfxdraw.box(self.screen, self.button_left, (255, 255, 0)) # draw button box
        pygame.gfxdraw.box(self.screen, self.button_right, (255, 255, 0))
        self.screen.blit(self.button_left_text, (self.button_left.x + 75, self.button_left.y + 50)) # draw button text
        self.screen.blit(self.button_right_text, (self.button_right.x + 75, self.button_right.y + 50))
        pygame.display.flip()
        

    def teardown(self) -> None:
        pygame.quit()
