import pygame
import pygame.gfxdraw
import time
import math

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

        # feature storage
        self.features = {}
        self.biggest_amplitude = 0.0000001 # python cant divide by 0
        self.biggest_bass = 0.0000001
        self.biggest_mid = 0.0000001
        self.biggest_treble = 0.0000001
        self.biggest_centroid = 0.0000001
        self.biggest_onset = 0.0000001

        self.smallest_amplitude = 100000000000 
        self.smallest_bass = 10000000000
        self.smallest_mid = 10000000000
        self.smallest_treble = 10000000000
        self.smallest_centroid = 10000000000
        self.smallest_onset = 10000000000

        # features normalised
        self.treble_normalised = 0
        self.mid_normalised = 0
        self.bass_normalised = 0
        self.amplitude_normalised = 0
        self.centroid_normalised = 0
        self.onset_normalised = 0

        # screen space share
        self.total_share = 0
        self.bass_width_share = 0
        self.mid_width_share = 0
        self.treble_width_share = 0
        self.centroid_width_share = 0
        self.onset_width_share = 0

        # amplitude circle
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

        # smoothing is 1 - math.exp(-rate * delta_time)
        self.smoothing_rate = 6
        self.smooth_bass = self.width / 2 # the bars slide away from the middle, where they would be on frame 0
        self.smooth_treble = self.width / 2
        self.smooth_mid = self.width / 2
        self.smooth_centroid = self.width / 2
        self.smooth_onset = self.width / 2

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

        # dt logic
        if USE_DELTA_TIME == True:
            dt = self.clock.tick(self.target_fps) / 1000.0 # real time frames
        else:
            dt = 1 / self.target_fps # every frame takes the same time
            if self.dt_warning == False: # a print warning incase i forgor to turn on dt
                print("WARNING: DT is off")
                self.dt_warning = True
        if dt >= self.max_dt: # set dt back to 0.1 if it goes over
            dt = self.max_dt

        # amplitutde circle movement & radius logic
        self.amplitude_radius = 100 + (2700 * self.features.get("amplitude", 0)) # 2700 is my scaler for amplitutude 

        self.amp_position_x = self.amp_position_x + (self.circle_speed * dt) # means the circle will move the same speed no matter the frame rate
        if self.amp_position_x > self.width - self.amplitude_radius: # if the circle hits the right border
            self.circle_speed = -120
        elif self.amp_position_x < 0 + self.amplitude_radius: # if the circle hits the left border
            self.circle_speed = 120

        # feature storage update
        if self.features.get("amplitude", 0) > self.biggest_amplitude: 
            self.biggest_amplitude = self.features.get("amplitude", 0)
        if self.features.get("bass", 0) > self.biggest_bass:
            self.biggest_bass = self.features.get("bass", 0)
        if self.features.get("treble", 0) > self.biggest_treble:
            self.biggest_treble = self.features.get("treble", 0)
        if self.features.get("mid", 0) > self.biggest_mid:
            self.biggest_mid = self.features.get("mid", 0)
        if self.features.get("centroid", 0) > self.biggest_centroid:
            self.biggest_centroid = self.features.get("centroid", 0)
        if self.features.get("onset", 0) > self.biggest_onset:
            self.biggest_onset = self.features.get("onset", 0)

        if self.features.get("amplitude", 0) < self.smallest_amplitude:
            self.smallest_amplitude = self.features.get("amplitude", 0)
        if self.features.get("bass", 0) < self.smallest_bass:
            self.smallest_bass = self.features.get("bass", 0)
        if self.features.get("treble", 0) < self.smallest_treble:
            self.smallest_treble = self.features.get("treble", 0)
        if self.features.get("mid", 0) < self.smallest_mid:
            self.smallest_mid = self.features.get("mid", 0)
        if self.features.get("centroid", 0) < self.smallest_centroid:
            self.smallest_centroid = self.features.get("centroid", 0)
        if self.features.get("onset", 0) < self.smallest_onset:
            self.smallest_onset = self.features.get("onset", 0)

        # features normalised update
        if self.biggest_treble > self.smallest_treble:
            self.treble_normalised = (self.features.get("treble", 0) - self.smallest_treble) / (self.biggest_treble - self.smallest_treble)
        else:
            self.treble_normalised = 0 # stops python from diving by 0 on the first frame
        if self.biggest_bass > self.smallest_bass:
            self.bass_normalised = (self.features.get("bass", 0) - self.smallest_bass) / (self.biggest_bass - self.smallest_bass)
        else:
            self.bass_normalised = 0
        if self.biggest_amplitude > self.smallest_amplitude:
            self.amplitude_normalised = (self.features.get("amplitude", 0) - self.smallest_amplitude) / (self.biggest_amplitude - self.smallest_amplitude)
        else:
            self.amplitude_normalised = 0
        if self.biggest_mid > self.smallest_mid:
            self.mid_normalised = (self.features.get("mid", 0) - self.smallest_mid) / (self.biggest_mid - self.smallest_mid)
        else:
            self.mid_normalised = 0
        if self.biggest_centroid > self.smallest_centroid:
            self.centroid_normalised = (self.features.get("centroid", 0) - self.smallest_centroid) / (self.biggest_centroid - self.smallest_centroid)
        else:
            self.centroid_normalised = 0
        if self.biggest_onset > self.smallest_onset:
            self.onset_normalised = (self.features.get("onset", 0) - self.smallest_onset) / (self.biggest_onset - self.smallest_onset)
        else:
            self.onset_normalised = 0

        # screen space share update
        self.total_share = self.bass_normalised + self.treble_normalised + self.mid_normalised + self.centroid_normalised + self.onset_normalised # we need to know what to divide by get individual share           
        if self.total_share > 0: # stops a 0 division
            self.bass_width_share = self.bass_normalised / self.total_share * self.width
            self.treble_width_share = self.treble_normalised / self.total_share * self.width
            self.mid_width_share = self.mid_normalised / self.total_share * self.width
            self.centroid_width_share = self.centroid_normalised / self.total_share * self.width
            self.onset_width_share = self.onset_normalised / self.total_share * self.width
        else: # each rectangle gets an equal share of the screen if its 0 
            self.bass_width_share = self.width / 5 # 2 is the number of features i've put into this logic
            self.treble_width_share = self.width / 5
            self.mid_width_share = self.width / 5
            self.centroid_width_share = self.width / 5
            self.onset_width_share = self.width / 5

        # smoothing        starting point                how far away it is                             smoothing equation
        self.smooth_bass = self.smooth_bass + (self.bass_width_share - self.smooth_bass) * (1 - math.exp(-self.smoothing_rate * dt))
        self.smooth_treble = self.smooth_treble + (self.treble_width_share - self.smooth_treble) * (1 - math.exp(-self.smoothing_rate * dt))
        self.smooth_mid = self.smooth_mid + (self.mid_width_share - self.smooth_mid) * (1 - math.exp(-self.smoothing_rate * dt))
        self.smooth_centroid = self.smooth_centroid + (self.centroid_width_share - self.smooth_centroid) * (1 - math.exp(-self.smoothing_rate * dt))
        self.smooth_onset = self.smooth_onset + (self.onset_width_share - self.smooth_onset) * (1 - math.exp(-self.smoothing_rate * dt))
        # it means where it is now + (where it wants to be - where it is now) then the smoothing equation

       
       
       
       
       
       
       
       
       
       
       
       
        # checking normalisations
        # print("treble normalised: ", round(self.treble_normalised, 2))
        # print("bass normalised: ", round(self.bass_normalised, 2))

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

        # screen share rectangles
        pygame.gfxdraw.box(self.screen, pygame.Rect(0, 0, int(self.smooth_bass), self.height), (0, 255, 0)) # draw bass rectangle
        pygame.gfxdraw.box(self.screen, pygame.Rect(int(self.smooth_bass), 0, int(self.smooth_treble), self.height), (0, 0, 255)) # draw treble rectangle directly after bass 
        pygame.gfxdraw.box(self.screen, pygame.Rect(int(self.smooth_bass + self.smooth_treble), 0, int(self.smooth_mid), self.height), (255, 0, 255)) 
        pygame.gfxdraw.box(self.screen, pygame.Rect(int(self.smooth_bass + self.smooth_treble + self.smooth_mid), 0, int(self.smooth_centroid), self.height), (0, 255, 255)) 
        pygame.gfxdraw.box(self.screen, pygame.Rect(int(self.smooth_bass + self.smooth_treble + self.smooth_mid + self.smooth_centroid), 0, int(self.smooth_onset), self.height), (255, 255, 0))

        # buttons
        pygame.gfxdraw.box(self.screen, self.button_left, (255, 255, 0)) # draw button box
        pygame.gfxdraw.box(self.screen, self.button_right, (255, 255, 0))
        self.screen.blit(self.button_left_text, (self.button_left.x + 75, self.button_left.y + 50)) # draw button text
        self.screen.blit(self.button_right_text, (self.button_right.x + 75, self.button_right.y + 50))

        pygame.display.flip()
        

    def teardown(self) -> None:
        pygame.quit()
