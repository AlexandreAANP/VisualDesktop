import cv2 as cv
from Utils import replace_background_of_image, create_mask
import time
from EventInteraction import EventInteraction
from Events.OpenAppEvent import OpenAppEvent
class Icon(EventInteraction):
    WIDTH = 70
    HEIGHT = 70
    CLICK_TIME_SECONDS = 2
    def __init__(self,path :str, coords: tuple,name, f:float = 1.0, isHidden = True, flip = False):
        self.name = name
        self.x = coords[0]
        self.y = coords[1]
        self.width = int(Icon.WIDTH * f)
        self.height = int(Icon.HEIGHT * f)
        if flip:
            self.image = cv.flip(cv.imread(path), 1)
            self.mask = create_mask(cv.flip(cv.imread(path, cv.IMREAD_UNCHANGED),1))
        else:
            self.image = cv.imread(path)
            self.mask = create_mask(cv.imread(path, cv.IMREAD_UNCHANGED))
        self.image = cv.resize(self.image, (self.width, self.height))
        self.mask = cv.resize(self.mask, (self.width, self.height))
        self.isHidden = False
        self.event_type = None
        self.timer = None

    def event(self, event, frame):
        if self.should_trigger_event(event):
            if self.in_range(event.coords, frame):
                OpenAppEvent(event.coords, self.name)
            else:
                self.reset_event()

    def hide(self):
        self.isHidden = True
    
    def show(self):
        self.isHidden = False
    def put_image_in_frame(self, screen):
        if self.isHidden:
            return screen
        partOfScreen = screen[self.y:self.y+self.height, self.x:self.x+self.width]
        self.image = replace_background_of_image(self.image, partOfScreen, self.mask)
        screen[self.y:self.y+self.height, self.x:self.x+self.width] = self.image
        return screen
    
    def in_range(self, coords, frame):
        if self.isHidden:
            return False
        return (coords[0]*frame.shape[1] >= self.x
                and coords[0]*frame.shape[1] <= self.x + self.width
                and coords[1]*frame.shape[0] >= self.y
                and coords[1]*frame.shape[0] <= self.y + self.height)
    
        
        