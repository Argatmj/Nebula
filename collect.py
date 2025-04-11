import cv2
import json
import time 
import mediapipe as mp
import keyboard as key

N_FRAMES = 15
FILE_PATH = "exp.json"
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
        gesture_data = collectCoords(results.multi_hand_landmarks, w, h)
        if len(gesture_data) == len(INDEX)*2:
          movement["frames"].append(gesture_data)
          print(f"Collected frame {len(movement['frames'])}")
        else:
          print(f"Record again. data was corrupted!")
        #time.sleep(0.1)
  
    # add data to collections 
    if recording and (len(movement["frames"])) == N_FRAMES:
      movement["label"] = current_label
      data.append(movement)
      with open(FILE_PATH, "w", newline= '') as f:
        json.dump(data,f)
        print("Data saved!")
        print(f"Number of moves : {len(data)}")
      recording = False
      time.sleep(0.2)

     # remove last data from collections
    if key.is_pressed('d') and not delete_last_row:
      delete_last_row = True
      with open(FILE_PATH,"r") as f:
        collected_movements = json.load(f)
        new_movements = collected_movements[:-1]
        data = new_movements
      with open(FILE_PATH,"w") as f:
        json.dump(new_movements,f)
      print("Last row removed!")

    if key.is_pressed('d') and delete_last_row:
      delete_last_row = False
      time.sleep(0.2)
  
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
  cap.release()