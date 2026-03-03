import cv2
import numpy as np
import imutils
import easyocr
from PIL import Image, ImageDraw, ImageFont

# Load the Thai OCR model
reader = easyocr.Reader(['th'])

# Specify the font path for displaying Thai text on the screen
font_path = '/Users/ak/Desktop/liscesneplate/font/THSarabunNew.ttf'

# Initialize the video capture object for the camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open camera")
    exit()

# Read and process frames from the camera
while True:
    # Capture frame from the camera
    ret, frame = cap.read()

    # Check if frame is successfully captured
    if not ret:
        print("Failed to capture frame")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply filter and find edges for localization
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
    edged = cv2.Canny(bfilter, 30, 200)  # Edge detection

    # Find contours and apply mask
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    # Check if license plate location is found
    if location is not None:
        # Create mask and apply it to the frame
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(frame, frame, mask=mask)

        # Crop the license plate region
        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

        # Use EasyOCR to read text
        result = reader.readtext(cropped_image, detail=0, paragraph=True)

        # Render result
        if len(result) > 0:
            number = result[0]

            # Display the recognized number on the frame
            cv2.putText(frame, text=number, org=(location[0][0][0], location[1][0][1] + 60),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0),
                        thickness=2, lineType=cv2.LINE_AA)

            # Display the recognized number on the screen with the specified font
            pil_image = Image.fromarray(frame)
            draw = ImageDraw.Draw(pil_image)
            thai_font = ImageFont.truetype(font_path, size=30)
            draw.text((50, 50), number, font=thai_font, fill=(0, 255, 0))
            frame = np.array(pil_image)

            # Print the output on the terminal
            print("Recognized License Plate:", number)

        # Display the frame on the screen
        cv2.imshow('License Plate Recognition', frame)
    else:
        # Display the frame on the screen
        cv2.imshow('License Plate Recognition', frame)

    # Check for key press to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
