import numpy as np
import math 
import cv2
import tensorflow as tf
from collections import deque
import paho.mqtt.publish as publish

# class for classifying hand movements and sending commands
class Classification:

    # store settings 
    def __init__(self, model, labels, threshold, index, n_frames):
        self.model = tf.keras.models.load_model(model) # load pretrained model 
        self.labels = labels
        self.threshold = threshold
        self.index = index
        self.n_frames = n_frames
        self.length = len(index) * 2
    
        self.frames = []
        self.volumes = deque(maxlen=30)
        self.percentages = []
        self.text = "Not Recognized"
        self.flag = False

    # normalize movement data 
    def normalize(self, sequence):
        # find center
        arr = np.array(sequence)
        arr = arr.reshape(-1,2)
        center = arr.mean(axis=0)
        # find scale
        scale = arr.std(axis=0)
        # normalize
        normalized = (arr - center) / scale 
        return normalized.reshape(self.n_frames,self.length)

    # extract landmarks coordinates
    def collect_coordinates(self,multi_hand_landmarks):
        data = []
        for hand_landmarks in multi_hand_landmarks:
            for index, landmark in enumerate(hand_landmarks.landmark):
                if index in self.index:
                    coords = [landmark.x,landmark.y]
                    data.extend(coords)
        return data 

    # calculate the euclidean distance between the thumb and index finger
    @staticmethod
    def calculate_distance(thumb, index):
        x, y = index[0] - thumb[0], index[1] - thumb[1]
        return math.hypot(x,y)

    # draw a line between the thumb and index finger
    @staticmethod
    def draw_line(img, hand_landmarks):
        height, width, _ = img.shape
        landmarks = hand_landmarks.landmark
        thumb, index = landmarks[4], landmarks[8]
        thumb_coords = (int(thumb.x * width), int(thumb.y * height))
        index_coords = (int(index.x * width), int(index.y * height))
        thick, colour = 4, (255, 0, 0)
        cv2.line(img, thumb_coords, index_coords, colour, thick)
        return thumb_coords, index_coords, width, height

    # calculate the size of the hand 
    @staticmethod
    def get_hand_size(hand_landmark, w, h):
        hand = hand_landmark.landmark
        bottom, top = hand[0], hand[12]
        x, y = top.x*w - bottom.x*w, top.y*h - bottom.y*h
        return math.hypot(x,y)
    
    # calculate volume based on euclidean distance 
    def change_volume(self, img, hand_landmarks):
        thumb, index, w, h = self.draw_line(img, hand_landmarks)
        size = self.get_hand_size(hand_landmarks,w,h)
        min_d, max_d = 0.1, 0.6
        dist = self.calculate_distance(thumb, index) / size 
        values = (dist - min_d) / (max_d - min_d)
        value = max(0.0, min(values,1.0))
        value = value * 1
        value = round(value, 1)
        self.text = (f"Volume : {value}")
        self.put_text(img)
        self.send_command(4,value)
        return value
    
    # send command through MQTT based on index
    def send_command(self, index, value=0):
        match index:
            case 0:
                publish.single("Position", "Previous")
            case 1:
                publish.single("Position", "Next")
            case 3:
                publish.single("State", "Switch")
            case 4: 
                publish.single("Volume", value)
            case _:
                pass
                # print(f"{index} does not match")

    # set the volume if its stable 
    def set_volume(self, image, hand_landmarks):
        percent = self.change_volume(image,hand_landmarks)
        self.volumes.append(percent)
        std = np.std(self.volumes)
        if len(self.volumes) == 30 and std < 0.080:
            self.text = (f"Volume: {self.volumes[-1]}")
            self.flag = False
            self.volumes.clear()

    # classify the movement 
    def classify_movement(self):
        if not all(map(lambda x: len(x) == self.length, self.frames)) : 
            fixed_movement = []
            for frame in self.frames:
                fixed_movement.append(frame[:self.length])
            self.frames = fixed_movement
        else:
            x = self.normalize(self.frames)
            x = x.reshape(1, self.n_frames,self.length)
            pred = self.model.predict(x,verbose=0)
            # show percentage 
            for indx, percent in enumerate(pred[0]):
                value = percent*100
                # print(f"Class {indx + 1}: {value:.2f}%")
                self.percentages.append(value)
            self.frames = []

    # display the command based on highest percentage 
    def show_command(self):
        h = max(self.percentages)
        if h >= self.threshold:
            index = self.percentages.index(h)
            self.text = f"{self.labels[index]}"
            if index in range(0,len(self.labels)):
                self.send_command(index)
            if index == 4 :
                self.flag = True
        else:
            self.text = "Not Recognized"
        self.percentages.clear()

    # draw text
    def put_text(self, image, coords=(50,50)):
        cv2.putText(
            image,
            self.text,             
            coords,                     
            cv2.FONT_HERSHEY_SIMPLEX,   
            1,                            
            (0, 255, 0),                  
            2,                            
            cv2.LINE_AA                 
      )





    
        
        
    
    


    


        
