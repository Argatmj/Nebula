import cv2
import mediapipe as mp
import tensorflow as tf
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

N_FRAMES = 20
label = {
  0 : "left_swipe",
  1 : "right_swipe"
}

def collectCoords(multi_hand_landmarks, w, h):
    data = []
    for hand_landmarks in multi_hand_landmarks:
      for index, landmark in enumerate(hand_landmarks.landmark):
        nx, ny = int(landmark.x * w), int(landmark.y * h)
        data.extend([nx,ny])
    return data


cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  movement = {
    "frames" : []
  }
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
    # model.summary()

    # collect all frames
    if len(movement["frames"]) <= N_FRAMES:
      if results.multi_hand_landmarks:
        coords = collectCoords(results.multi_hand_landmarks,w,h)
        movement["frames"].append(coords)
        print(len( movement["frames"]))
        
    # classify movement 
    if len(movement["frames"]) == N_FRAMES:
      if all(map(lambda x: len(x) == 42, movement["frames"])) : 
        x = np.array(movement["frames"])
        x = np.reshape(x, (1, N_FRAMES, 42))
        pred = model.predict(x)
        pred_labels = np.argmax(pred,axis=1)
        print(pred_labels)
        movement["frames"] = []
      else:
        print("Data is corrupted!") 
        movement["frames"] = []

    # show label 
    
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
  cap.release()