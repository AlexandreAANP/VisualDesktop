import Utils
import cv2 as cv
import mediapipe as mp
from Icon import Icon
from MiniApps.MiniApp import MiniApp
from MiniApps.FaceReplaceApp.CloseDetection import CloseDetection
from MiniApps.FaceReplaceApp.ImageFaceDetection import ImageFaceDetection
from Events.Event import Event
from Events.CloseAppEvent import CloseAppEvent
from EventInteraction import EventInteraction

import os
class FaceReplace(MiniApp, EventInteraction):
    __app_name = "FaceReplaceApp"
    __instance = None
    PATH = os.path.dirname(os.path.realpath(__file__)).replace("\MiniApps\FaceReplaceApp", "")
    
    PATH_ARROW_ICON = PATH+"\\images\\FaceReplaceApp\\arrow.png"
    
    def __init__(self, width, height):
        FaceReplace.__instance = self
        super().__init__(FaceReplace.__app_name,
                         Icon(Utils.PROJECT_PATH+"/images/obama.png",(0,45), FaceReplace.__app_name))
        
        
        self.rigth_icon = Icon(FaceReplace.PATH_ARROW_ICON, (0,int(height/2 - Icon.HEIGHT/2)), "FaceReplaceApp_Arrow_Left", flip = True)
        self.left_icon = Icon(FaceReplace.PATH_ARROW_ICON, (width-70,int(height/2 - Icon.HEIGHT/2)), "FaceReplaceApp_Arrow_Rigth", flip=False)
        self.close_detection = CloseDetection(2, width, height)
        
        list_path_replace_face = Utils.get_all_files_path_from_folder(Utils.PROJECT_PATH+ "/images/FaceReplaceApp/faces/")
        self.images_face_detected = self.__detect_faces_from_images(list_path_replace_face)
        self.faceIndex = 0
        self.isOpen = False
        self.event_type = None
        self.timer = None
    
    def event(self, event:Event, frame):
        if self.should_trigger_event(event):
            if self.in_range_left_icon(event.coords, frame):
                self.change_face("left")
                self.reset_event()
            elif self.in_range_right_icon(event.coords, frame):
                self.change_face("right")
                self.reset_event()
        
    def change_face(self, direction):
        if direction == "left":
            self.faceIndex -= 1 if self.faceIndex > 0 else 0
            return True
        elif direction == "right":
            self.faceIndex += 1 if self.faceIndex < len(self.images_face_detected)-1 else 0
            return True
        return False
    
    def in_range_left_icon(self, coords, frame):
        return self.left_icon.in_range(coords, frame)
    def in_range_right_icon(self, coords, frame):
        return self.rigth_icon.in_range(coords, frame)
          
    def open(self):
        self.isOpen = True
    
    def close(self):
        self.isOpen = False
        CloseAppEvent((0,0), FaceReplace.__app_name)    
            
    def run(self,landmarks,frame):
        if not self.isOpen:
            return frame
        self.rigth_icon.put_image_in_frame(frame)
        self.left_icon.put_image_in_frame(frame)
        
        if self.close_detection.should_close(landmarks):
            self.close()
            
        if landmarks is None or landmarks.face_landmarks is None:
            return frame

        return self.images_face_detected[self.faceIndex].replaceFace(landmarks, frame)

    
    def __detect_faces_from_images(self, list_path_replace_face):
        l= []
        for path in list_path_replace_face:
            l.append(ImageFaceDetection(path))
        return l 
    @classmethod  
    def get(cls):
        if cls.__instance:
            return cls.__instance
        raise Exception("FaceReplaceApp not initialized")
    
    @classmethod
    def get_app_name(cls):
        return cls.__app_name