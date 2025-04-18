import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np
import math 
from collections import deque

N_FRAMES = 15
THRESHOLD = 90
label = {
  0 : "left_swipe",
  1 : "right_swipe",
  2 : "still",
  3 : "volume"
}
INDEX = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

#INDEX = [0,4,8,12,16,20]

#TODO: improve volume and still dataset 

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def normalize(sequence):
  # find center
  arr = np.array(sequence)
  arr = arr.reshape(-1,2)
  center = arr.mean(axis=0)
  # find scale
  scale = arr.std(axis=0)
  # normalize
  normalized = (arr - center) / scale 
  return normalized.reshape(N_FRAMES,42)

def collectCoords(multi_hand_landmarks,index_landmarks=INDEX):
    data = []
    for hand_landmarks in multi_hand_landmarks:
      for index, landmark in enumerate(hand_landmarks.landmark):
        if index in index_landmarks:
          coords = [landmark.x,landmark.y]
          data.extend(coords)
    return data

# load model 
model = tf.keras.models.load_model('my_model.keras')

def calculate_distance(thumb, index):
  x, y = index[0] - thumb[0], index[1] - thumb[1]
  return math.hypot(x,y)

def draw_line(img, hand_landmarks):
  height, width, _ = img.shape
  landmarks = hand_landmarks.landmark
  thumb, index = landmarks[4], landmarks[8]
  thumb_coords = (int(thumb.x * width), int(thumb.y * height))
  index_coords = (int(index.x * width), int(index.y * height))
  thick, colour = 4, (255, 0, 0)
  cv2.line(img, thumb_coords, index_coords, colour, thick)
  return thumb_coords, index_coords, width, height

def get_hand_size(hand_landmark, w, h):
  hand = hand_landmark.landmark
  bottom, top = hand[0], hand[12]
  x, y = top.x*w - bottom.x*w, top.y*h - bottom.y*h
  return math.hypot(x,y)

def change_volume(img, hand_landmarks):
  thumb, index, w, h = draw_line(img, hand_landmarks)
  size = get_hand_size(hand_landmarks,w,h)
  min_d, max_d = 0.1, 0.6
  dist = calculate_distance(thumb, index) / size 
  values = (dist - min_d) / (max_d - min_d)
  value = max(0.0, min(values,1.0))
  percent = value * 100
  print(round(percent))
  return percent

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  frames = []
  recent_volumes = deque(maxlen=20)
  percentages = []
  text = "Not Recognized"
  flag = False
  while cap.isOpened():
    success, image = cap.read()

    if not success:
      print("Ignoring empty camera frame.")
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # draw landmark
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        #mp_drawing.draw_landmarks(image,hand_landmarks)
        # change volume 
        if flag: 
          percent = change_volume(image,hand_landmarks)
          recent_volumes.append(round(percent))
          std = np.std(recent_volumes)
          if len(recent_volumes) == 20 and std < 1.5:
            print(f"Volume saved : {recent_volumes[-1]}")
            flag = False
            recent_volumes.clear()
  
    # collect all frames
    if len(frames) < N_FRAMES and results.multi_hand_landmarks:
      coords = collectCoords(results.multi_hand_landmarks)
      frames.append(coords)
    else:
      frames.clear()
        
    # classify movement 
    if len(frames) == N_FRAMES:
      # if data is not uniformed, slice
      if not all(map(lambda x: len(x) == len(INDEX)*2, frames)) : 
        fixed_movement = []
        for frame in frames:
          fixed_movement.append(frame[:len(INDEX)*2])
        frames = fixed_movement
      else:
        x = normalize(frames)
        x = x.reshape(1, N_FRAMES,42)
        pred = model.predict(x,verbose=0)
        # show percentage 
        for indx, percent in enumerate(pred[0]):
          value = percent*100
          #print(f"Class {indx + 1}: {value:.2f}%")
          percentages.append(value)
        frames = []
  
    # show label 
    if percentages:
      h = max(percentages)
      index = percentages.index(h)
      if index == 3:
        flag = True
      if h >= THRESHOLD:
          text = f"{label[index]}"
      else:
          text = "Not Recognized"
      percentages.clear()

    cv2.putText(
        image,
        text,             
        (50, 50),                     
        cv2.FONT_HERSHEY_SIMPLEX,   
        1,                            
        (0, 255, 0),                  
        2,                            
        cv2.LINE_AA                 
      )
    
    cv2.imshow('MediaPipe Hands',image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
  cap.release()