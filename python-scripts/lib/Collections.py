import json

class Collections: 
    def __init__(self, file_path, data):
        self.file_path = file_path
        self.label = 1
        self.recording = False
        self.delete = False
        self.process = False
        self.data = data
        self.frames = []
        self.movement = {
            "label": "",
            "frames": self.frames
        }

    def start(self):
        print("Recording started...")
        self.recording = True
        self.frames = []
        self.movement = {
        "label": "",
        "frames": self.frames
        }

    def collect_coordinates(self, multi_hand_landmarks):
        new_data = []
        for hand_landmarks in multi_hand_landmarks:
            for _, landmark in enumerate(hand_landmarks.landmark):
                coords = [landmark.x,landmark.y]
                new_data.extend(coords)
        return new_data
    
    def length_of_frames(self):
        return len(self.movement["frames"])
    
    def print_label_count(self,data):
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

    def read_file(self):
        with open(self.file_path,"r") as f:
            data = json.load(f)
        return data
    
    def write_file(self,data):
        with open(self.file_path,"w") as f:
            json.dump(data,f)

    def set_label(self,id):
      self.label = id
      print(f"Label is set to {self.label}!")

    def collect_frames(self, multi_hand_landmarks):
        coords = self.collect_coordinates(multi_hand_landmarks)
        if len(coords) == 42:
            self.movement["frames"].append(coords)
            print(f"Collected frame {len(self.movement['frames'])}")
        else:
          print(f"Record again. data was corrupted!")
    
    def add_movement(self):
        self.movement["label"] = self.label
        self.data.append(self.movement)
        self.write_file(self.data)
        print("Data saved!")
        self.recording = False
        self.print_label_count(self.read_file())

    def remove_last_movement(self):
        self.delete = True
        self.data = self.data[:-1]
        self.write_file(self.data)
        print("Last row removed!")
        self.print_label_count(self.read_file())