import cv2
import numpy as np
import imutils
import easyocr
import tkinter as tk
from tkinter import messagebox
from PIL import ImageFont, ImageDraw, Image

# Load the Thai OCR model
reader = easyocr.Reader(['th'])

# Initialize the video capture object for the camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open camera")
    exit()

# Create a database of registered license plates
registered_plates = ['ABC123', 'XYZ789']

# Specify the font path for displaying Thai text on the screen
font_path = '/Users/ak/Desktop/liscesneplate/font/THSarabunNew.ttf'

# Create a Tkinter GUI window
window = tk.Tk()
window.title("License Plate Database")
window.geometry("300x200")

# Create a listbox to display the registered plates
listbox = tk.Listbox(window)
listbox.pack(pady=10)

# Function to add a license plate to the database
def add_plate():
    plate = plate_entry.get().upper()
    if plate not in registered_plates:
        registered_plates.append(plate)
        listbox.insert(tk.END, plate)
        messagebox.showinfo("Success", "License Plate Added!")
    else:
        messagebox.showwarning("Error", "License Plate Already Exists!")

# Function to remove a license plate from the database
def remove_plate():
    selected_plate = listbox.get(tk.ACTIVE)
    registered_plates.remove(selected_plate)
    listbox.delete(tk.ACTIVE)
    messagebox.showinfo("Success", "License Plate Removed!")

# Create labels and entry widgets for adding a license plate
plate_label = tk.Label(window, text="License Plate:")
plate_label.pack()
plate_entry = tk.Entry(window)
plate_entry.pack(pady=5)
add_button = tk.Button(window, text="Add", command=add_plate)
add_button.pack(pady=5)

# Create a button to remove a license plate
remove_button = tk.Button(window, text="Remove", command=remove_plate)
remove_button.pack()

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
        result = reader.readtext(cropped_image, detail=0)

        # Render result
        if len(result) > 0:
            number = result[0]

            # Check if the license plate is in the database
            if number in registered_plates:
                cv2.putText(frame, text="You are allowed to enter", org=(location[0][0][0], location[1][0][1] + 60),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0),
                            thickness=2, lineType=cv2.LINE_AA)

                # Create a PIL Image from the frame for drawing Thai text
                pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_frame)

                # Load the Thai font and specify the font size
                font_size = 30
                font = ImageFont.truetype(font_path, font_size)

                # Specify the position and text to be displayed
                text_position = (location[0][0][0], location[1][0][1] + 100)
                text = "ยินดีต้อนรับ"

                # Draw the Thai text on the image
                draw.text(text_position, text, font=font, fill=(0, 255, 0))

                # Convert the PIL Image back to OpenCV format
                frame = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)

            else:
                cv2.putText(frame, text="Access Denied", org=(location[0][0][0], location[1][0][1] + 60),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255),
                            thickness=2, lineType=cv2.LINE_AA)

            cv2.rectangle(frame, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)

    # Display the frame on the screen
    cv2.imshow('License Plate Recognition', frame)

    # Check for key press to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()

# Start the Tkinter event loop
window.mainloop()
