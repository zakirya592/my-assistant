import cv2
import numpy as np
import time

# =========================
# LOAD FACE CASCADE
# =========================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# =========================
# LOAD USER IMAGE
# =========================

known_image = cv2.imread("user2.jpg")

known_gray = cv2.cvtColor(known_image, cv2.COLOR_BGR2GRAY)

known_faces = face_cascade.detectMultiScale(
    known_gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(100, 100)
)

if len(known_faces) == 0:
    print("No face found in user.jpg")
    exit()

(x, y, w, h) = known_faces[0]

known_face = known_gray[y:y+h, x:x+w]

# =========================
# START CAMERA
# =========================

camera = cv2.VideoCapture(0)

print("Face Login Started...")

login_success = False
scan_line_position = 0
scan_direction = 1
scan_speed = 3
start_time = time.time()
timeout_duration = 20  # 20 seconds
scan_delay = 3  # 3 seconds delay before scanning starts
scanning_started = False
timeout_completed = False
timeout_display_duration = 3  # 3 seconds red line display after timeout
timeout_display_start_time = 0

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    # Check timeout
    elapsed_time = time.time() - start_time
    remaining_time = max(0, timeout_duration - elapsed_time)
    
    # Check if scanning should start
    if elapsed_time >= scan_delay and not scanning_started:
        scanning_started = True
        scan_start_time = time.time()
    
    if scanning_started:
        # Update scan line position
        scan_line_position += scan_speed * scan_direction
        if scan_line_position >= frame.shape[0] - 10 or scan_line_position <= 10:
            scan_direction *= -1

        # Draw scanning line
        cv2.line(frame, (0, scan_line_position), (frame.shape[1], scan_line_position), (0, 255, 255), 2)
        
        # Add scanning text with countdown
        cv2.putText(
            frame,
            f"SCANNING... {int(remaining_time)}s",
            (50, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )
    else:
        # Show countdown before scanning starts
        pre_scan_countdown = scan_delay - elapsed_time
        cv2.putText(
            frame,
            f"GET READY... {int(pre_scan_countdown)}s",
            (50, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
    
    # Check if timeout reached
    if remaining_time <= 0:
        if not timeout_completed:
            timeout_completed = True
            timeout_display_start_time = time.time()
        
        # Calculate how long to show red line
        timeout_display_elapsed = time.time() - timeout_display_start_time
        
        # Continue scanning animation with red line
        scan_line_position += scan_speed * scan_direction
        if scan_line_position >= frame.shape[0] - 10 or scan_line_position <= 10:
            scan_direction *= -1
        
        # Draw red scanning line
        cv2.line(frame, (0, scan_line_position), (frame.shape[1], scan_line_position), (0, 0, 255), 3)
        
        # Show timeout message with remaining red line display time
        red_line_remaining = max(0, timeout_display_duration - timeout_display_elapsed)
        cv2.putText(
            frame,
            f"LOGIN FAILED - TIMEOUT {int(red_line_remaining)}s",
            (50, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )
        
        # Exit after red line display duration
        if timeout_display_elapsed >= timeout_display_duration:
            break

    for (x, y, w, h) in faces:
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        if scanning_started:
            # Draw scanning line on face
            face_scan_y = y + (scan_line_position - y) % h
            if y <= scan_line_position <= y + h:
                cv2.line(frame, (x, face_scan_y), (x+w, face_scan_y), (0, 0, 255), 3)

            face = gray[y:y+h, x:x+w]

            # Resize both images
            known_resized = cv2.resize(known_face, (200, 200))
            current_resized = cv2.resize(face, (200, 200))

            # Compare
            difference = cv2.absdiff(known_resized, current_resized)

            score = np.mean(difference)

            # Lower score = better match
            if score < 50:
                login_success = True

                cv2.putText(
                    frame,
                    "LOGIN SUCCESS",
                    (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                print("Face Recognized")

            else:
                cv2.putText(
                    frame,
                    "SCANNING FACE...",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )
        else:
            # Show getting ready message on face
            cv2.putText(
                frame,
                "GET READY",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

    cv2.imshow("Face Login", frame)

    if login_success:
        cv2.waitKey(2000)
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()

# =========================
# RESULT
# =========================

if login_success:
    print("Login successful")
else:
    print("Login failed")