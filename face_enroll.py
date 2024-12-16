import cv2
import face_recognition
import pickle
import os

# Directory to save enrolled face encodings
ENCODINGS_FILE = "face_encodings.pkl"
KNOWN_FACES_DIR = "known_faces"

# Function to load existing face encodings
def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as file:
            return pickle.load(file)
    return {}

# Function to save updated face encodings
def save_encodings(encodings):
    with open(ENCODINGS_FILE, "wb") as file:
        pickle.dump(encodings, file)

# Face Enrollment Function
def enroll_face():
    print("Starting Face Enrollment...")
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return

    camera = cv2.VideoCapture(0)
    face_captured = False

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame!")
            continue

        # Show frame
        cv2.imshow("Enrollment - Press 's' to Save Face", frame)

        # Press 's' to save the face
        if cv2.waitKey(1) & 0xFF == ord('s'):
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) == 1:
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

                # Load existing encodings and update
                encodings = load_encodings()
                encodings[name] = face_encoding
                save_encodings(encodings)

                print(f"Face for '{name}' saved successfully!")
                face_captured = True
                break
            else:
                print("Ensure only one face is visible and try again.")

        # Exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    if not face_captured:
        print("No face saved.")

# Face Recognition Function
def recognize_faces():
    print("Starting Face Recognition...")
    encodings = load_encodings()
    if not encodings:
        print("No faces enrolled. Please enroll faces first.")
        return

    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame!")
            continue

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known encodings
            matches = face_recognition.compare_faces(list(encodings.values()), face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = list(encodings.keys())[match_index]

            # Draw box and label
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display video frame
        cv2.imshow("Face Recognition - Press 'q' to Exit", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

# Main Program
if __name__ == "__main__":
    print("1. Enroll Face")
    print("2. Recognize Faces")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        enroll_face()
    elif choice == "2":
        recognize_faces()
    else:
        print("Invalid choice. Exiting.")
