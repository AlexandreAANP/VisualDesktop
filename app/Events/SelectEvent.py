from Events.Event import Event
class SelectEvent(Event):
    FINGER_SHOULD_BE_UP="INDEX"
    HAND = {
        "THUMB": [4, 3, 2, 1],#from to to bottom
        "INDEX": [8,7,6,5,],
        "MIDDLE": [12,11,10,9],
        "RING": [16,15,14,13],
        "PINKY": [20,19,18,17]
    }
    WRIST = 0
    
    
    @classmethod
    def detect(cls,landsmark) -> Event:
        if landsmark is None:
            return None
        #The click should be detected when the finger 1 is the only one up
        FingersUp = cls.detect_which_finger_is_up(landsmark.landmark)
        fingers_up = len(FingersUp.keys())
        if (fingers_up == 2 and "THUMB" in FingersUp.keys()) or fingers_up == 1:
            if cls.FINGER_SHOULD_BE_UP in FingersUp.keys():
                coords = (FingersUp[cls.FINGER_SHOULD_BE_UP][0].x, FingersUp[cls.FINGER_SHOULD_BE_UP][0].y)
                return SelectEvent(coords, SelectEvent)
        return None
    

    @classmethod
    def detect_which_finger_is_up(cls, landsmark):
        list_of_fingers_up = {
            #index: [points]
        }
        for index in cls.HAND.keys():
            finger = cls.HAND[index]
            isUp = True
            lastPoint = 0
            PointsList = []
            for key in finger[:-2]:
                PointsList.append(landsmark[key])
                if landsmark[key].y < lastPoint:
                    isUp = False
                    break
                lastPoint = landsmark[key].y
            if isUp:
                list_of_fingers_up[index] = PointsList
        return list_of_fingers_up
                
    

    
    
