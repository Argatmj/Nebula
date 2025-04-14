import cv2
import json
import time 
import math
import mediapipe as mp
import keyboard as key
import copy 
from functools import reduce

N_FRAMES = 15
FILE_PATH = "data.json"
INDEX = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

#INDEX = [0,4,8,12,16,20]

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#TODO: make utils library?


def normalize_data(data):
  for movement in data:
    for frame in movement["frames"]:
      anchor_x, anchor_y = frame[0], frame[1]
      top_x, top_y = frame[24], frame[25]
      size = math.sqrt((top_x - anchor_x) ** 2 + (top_y - anchor_y) ** 2)
      for i in range(0, len(frame), 2):
        x, y = frame[i], frame[i + 1]
        frame[i] = (x - anchor_x) / size
        frame[i + 1] = (y - anchor_y) / size
  return data

def average_data(data, window_size=3):
  new_data = []

  for movement in data:
    frames = movement["frames"]
    num_frames = len(frames)
    num_coords = len(frames[0])

    # group by index
    index_coords = [[] for _ in range(num_coords)]
    for frame in frames:
      for i in range(num_coords):
        index_coords[i].append(frame[i])

    # apply moving average
    avg_index_coords = []
    for coord_list in index_coords:
      padded = [coord_list[0]] * (window_size // 2) + coord_list + [coord_list[-1]] * (window_size // 2)
      avg_group = []
      for i in range(num_frames):
        window = padded[i:i + window_size]
        avg = reduce(lambda acc, x: acc + x, window) / window_size
        avg_group.append(avg)
      avg_index_coords.append(avg_group)

    # reconstruct data
    new_frames = []
    for i in range(num_frames):
      frame = []
      for j in range(num_coords):
        frame.append(avg_index_coords[j][i])
      new_frames.append(frame)

    new_data.append({
      "label": movement["label"],
      "frames": new_frames
    })

  return new_data

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

def read_file():
  with open(FILE_PATH,"r") as f:
    data = json.load(f)
  return data

def write_file(data):
  with open(FILE_PATH,"w") as f:
        json.dump(data,f)
    
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  current_label = 1
  recording = False
  delete_last_row = False
  frames = []
  data = []
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
      data = read_file()
      data.append(movement)
      write_file(data)
      print("Data saved!")
      recording = False
      print_label_count(read_file())
      # time.sleep(0.2)

     # remove last data from collections
    if key.is_pressed('d') and not delete_last_row:
      delete_last_row = True
      new_movements = read_file()[:-1]
      write_file(new_movements)
      print("Last row removed!")
      print_label_count(read_file())

    if key.is_pressed('d') and delete_last_row:
      delete_last_row = False
      time.sleep(0.2)
  
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
  cap.release()