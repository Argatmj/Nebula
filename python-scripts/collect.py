import cv2
import time 
import json
import mediapipe as mp
import keyboard as key
from lib.Collections import Collections

N_FRAMES = 15
FILE_PATH = "data.json"

def main():
  mp_drawing = mp.solutions.drawing_utils
  mp_hands = mp.solutions.hands
      
  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
    with open(FILE_PATH,"r") as f:
      data = json.load(f)
    collect = Collections(FILE_PATH,data)
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

      # listen for label keys
      for i in range(1,10):
        if key.is_pressed(str(i)):
          collect.set_label(i)
        
      # start recording
      if key.is_pressed('r') and not collect.recording:
        collect.start()

      # collect frames
      if collect.recording and collect.length_of_frames() < N_FRAMES:
        if results.multi_hand_landmarks:
          collect.collect_frames(results.multi_hand_landmarks)
    
      # add movement to collections 
      if collect.recording and collect.length_of_frames() == N_FRAMES:
        collect.add_movement()

      # remove last movement from collections
      if key.is_pressed('d') and not collect.delete:
        collect.remove_last_movement()
      if key.is_pressed('d') and collect.delete:
        collect.delete = False
        time.sleep(0.2)
    
      cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == 27:
        break
    cap.release()


if __name__ == "__main__":
  main()