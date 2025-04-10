import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np
from collections import deque

N_FRAMES = 15
THRESHOLD = 70
label = {
  0 : "left_swipe",
  1 : "right_swipe"
}
INDEX = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def collectCoords(multi_hand_landmarks, w, h, index_landmarks=INDEX):
    data = []
    for hand_landmarks in multi_hand_landmarks:
      for index, landmark in enumerate(hand_landmarks.landmark):
        if index in index_landmarks:
          nx, ny = int(landmark.x * w), int(landmark.y * h)
          data.extend([nx,ny])
    return data

def initMovement():
  init_frames = []
  for _ in range(N_FRAMES):
      frame = []
      for _ in range(len(INDEX)*2):
        frame.append(0)
      init_frames.append(frame)  
  return init_frames

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  movement = {
    "frames" : []
  }
  percentages = []
  text = "Not Recognized"
  frames = deque(maxlen=N_FRAMES)
  init = initMovement()
  frames.extend(init)
  length = 0
  while cap.isOpened():
    success, image = cap.read()
    
    # get height and width from image
    h, w, _ = image.shape

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
        mp_drawing.draw_landmarks(image,hand_landmarks)

    # load model 
    model = tf.keras.models.load_model('my_model.keras')

    # collect all frames
    # if len(movement["frames"]) <= N_FRAMES:
    if results.multi_hand_landmarks:
      coords = collectCoords(results.multi_hand_landmarks,w,h)
      if len(coords) == len(INDEX)*2:
        frames.append(coords)
        print(len(frames))
      length += 1
        
    # classify movement 
    # if len(movement["frames"]) == N_FRAMES:
      # TODO: fix the different length with padding or trimming 
    if all(map(lambda x: len(x) == 42, frames)) and length == 8:
      movement["frames"] = frames 
      x = np.array(movement["frames"])
      x = np.reshape(x, (1, N_FRAMES, 42))
      pred = model.predict(x)
      length = 0
      # show percentage 
      for indx, percent in enumerate(pred[0]):
        value = percent*100
        print(f"Class {indx + 1}: {value:.2f}%")
        percentages.append(value)

    # show label 
    if percentages:
      h = max(percentages)
      index = percentages.index(h)
      if h >= THRESHOLD:
          text = f"Label = {index} ({h:.2f}%)"
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