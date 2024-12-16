import cv2
import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

# GPIO setup for the motor
MOTOR_PIN = 18  # Motor control pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

# LCD setup (using I2C)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8)

# Face detection setup using Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
camera = cv2.VideoCapture(0)

# Placeholder for fingerprint verification (to be added later)
def fingerprint_verification():
    # Simulate fingerprint verification (returns True for now)
    print("Fingerprint Check: Simulated success")
    return True  # Change this later with actual sensor code

# Function to control the motor
def run_motor(duration=5):
    print("Motor running...")
    GPIO.output(MOTOR_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(MOTOR_PIN, GPIO.LOW)
    print("Motor stopped.")

# Main program
try:
    lcd.write_string("System Ready...")
    time.sleep(2)
    lcd.clear()
    
    while True:
        # Capture frame
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            continue

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            print("Face Detected!")
            lcd.clear()
            lcd.write_string("Face Detected!")
            time.sleep(1)

            # Placeholder for fingerprint check
            if fingerprint_verification():  # Replace with actual GPIO fingerprint code later
                lcd.clear()
                lcd.write_string("Access Granted!")
                run_motor(5)  # Run motor for 5 seconds
                lcd.clear()
                lcd.write_string("Gate Opened!")
                time.sleep(2)
            else:
                lcd.clear()
                lcd.write_string("Fingerprint Fail")
                print("Fingerprint verification failed")
                time.sleep(2)
            
            lcd.clear()
            lcd.write_string("System Ready...")
        else:
            print("No face detected")
        
        # Display frame (optional for debugging)
        cv2.imshow("Face Detection", frame)

        # Quit program on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted!")

finally:
    # Cleanup resources
    camera.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    lcd.clear()
    lcd.write_string("System Stopped.")
    print("Cleaned up resources!")
