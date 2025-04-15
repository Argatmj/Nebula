import cv2
import json
import time 
import mediapipe as mp
import keyboard as key
from functools import reduce

N_FRAMES = 15
FILE_PATH = "data.json"
INDEX = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

#INDEX = [0,4,8,12,16,20]

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def collectCoords(multi_hand_landmarks,index_landmarks=INDEX):
  data = []
  for hand_landmarks in multi_hand_landmarks:
    for index, landmark in enumerate(hand_landmarks.landmark):
      if index in index_landmarks:
        coords = [landmark.x,landmark.y]
        data.extend(coords)
  return data

def print_label_count(data):
  label_dict = {}
  for movements in data:
      label = movements["label"]
      if label in label_dict:
        label_dict[label] += 1
      else:
        label_dict[label] = 1
  if label_dict:
    for key, value in label_dict.items():
      print(f"Label {key}: {value}.")
  else:
     print("data is empty")

def read_file(file=FILE_PATH):
  with open(FILE_PATH,"r") as f:
    data = json.load(f)
  return data

def write_file(data,file=FILE_PATH):
  with open(file,"w") as f:
        json.dump(data,f)
    
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  current_label = 1
  recording = False
  delete_last_row = False
  process = False
  frames = []
  data = read_file()
  label_flag = False
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
        mp_drawing.draw_landmarks(image,hand_landmarks)

    # set label     
    def set_label(id):
      global current_label
      current_label = id
      print(f"Label is set to {current_label}!")

    # listen for label keys
    for i in range(1,10):
      if key.is_pressed(str(i)):
        set_label(i)
       
    # start recording
    if key.is_pressed('r') and not recording:
      print("Recording started...")
      recording = True
      frames = []
      movement = {
        "label": "",
        "frames": frames
      }

    # collect frames
    if recording and (len(movement["frames"])) < N_FRAMES:
      if results.multi_hand_landmarks:
        gesture_data = collectCoords(results.multi_hand_landmarks)
        if len(gesture_data) == len(INDEX)*2:
          movement["frames"].append(gesture_data)
          print(f"Collected frame {len(movement['frames'])}")
        else:
          print(f"Record again. data was corrupted!")
  
    # add data to collections 
    if recording and (len(movement["frames"])) == N_FRAMES:
      movement["label"] = current_label
      data.append(movement)
      write_file(data)
      print("Data saved!")
      recording = False
      print_label_count(read_file())
      # time.sleep(0.2)

     # remove last data from collections
    if key.is_pressed('d') and not delete_last_row:
      delete_last_row = True
      data = data[:-1]
      write_file(data)
      print("Last row removed!")
      print_label_count(read_file())

    if key.is_pressed('d') and delete_last_row:
      delete_last_row = False
      time.sleep(0.2)
  
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
  cap.release()