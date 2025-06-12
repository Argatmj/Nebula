import cv2
import mediapipe as mp
from lib.Classification import Classification

N_FRAMES = 15
THRESHOLD = 96
LABEL = {
  0 : "left_swipe",
  1 : "right_swipe",
  2 : "still",
  3 : "start",
  4 : "volume"
}
INDEX = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#INDEX = [0,4,8,12,16,20]

def main():
  # mp_drawing = mp.solutions.drawing_utils
  # mp_drawing_styles = mp.solutions.drawing_styles
  mp_hands = mp.solutions.hands

  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
    predict = Classification('my_model.keras',LABEL,THRESHOLD,INDEX,N_FRAMES)
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
          # mp_drawing.draw_landmarks(image,hand_landmarks)
          # change volume 
          if predict.flag: 
            predict.set_volume(image,hand_landmarks)
    
      # collect all frames
      if len(predict.frames) < N_FRAMES and results.multi_hand_landmarks:
        coords = predict.collect_coordinates(results.multi_hand_landmarks)
        predict.frames.append(coords)
      else:
        predict.frames.clear()
          
      # classify movement 
      if len(predict.frames) == N_FRAMES and not predict.flag:
        predict.classify_movement()
    
      # show label / send command 
      if predict.percentages:
        predict.show_command()
      predict.put_text(image)
      
      cv2.imshow('MediaPipe Hands',image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
    cap.release()

if __name__ == "__main__":
  main()