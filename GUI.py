import tkinter as tk
import cv2
import numpy as np
import imutils
import easyocr
from PIL import Image, ImageDraw, ImageFont
import mysql.connector

class LicensePlateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("License Plate Recognition & CRUD App")

        # Load the Thai OCR model
        self.reader = easyocr.Reader(['th'])

        # Initialize the video capture object for the camera
        self.cap = cv2.VideoCapture(0)

        self.font_path = '/Users/ak/Desktop/liscesneplate/font/THSarabunNew.ttf'

        self.result = []  # Initialize result list

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Initialize MySQL connection parameters
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",  # Replace with your MySQL password
            database="licenseDB"   # Replace with your database name
        )

        self.update_camera()

    def update_camera(self):
        ret, frame = self.cap.read()

        if ret:
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
                self.result = self.reader.readtext(cropped_image, detail=0, paragraph=True)

                if len(self.result) > 0:
                    number = self.result[0]

                    # Display the recognized number on the frame
                    cv2.putText(frame, text=number, org=(location[0][0][0], location[1][0][1] + 60),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0),
                                thickness=2, lineType=cv2.LINE_AA)

                    # Insert recognized license plate number into the database
                    self.insert_license_plate(number)

            # Display the frame on the screen
            self.display_frame(frame)

        self.root.after(10, self.update_camera)

    def insert_license_plate(self, license_plate):
        # Create a cursor to execute SQL commands
        cursor = self.db_connection.cursor()

        # Define the SQL query to insert the license plate number
        sql_query = "INSERT INTO LicensePlateData (license_number) VALUES (%s)"

        # Execute the query with the license plate number as a parameter
        cursor.execute(sql_query, (license_plate,))

        # Commit the changes to the database
        self.db_connection.commit()

        # Close the cursor
        cursor.close()

    def display_frame(self, frame):
        # Convert the OpenCV frame to a format suitable for Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(frame)

        # Create a drawing object
        draw = ImageDraw.Draw(pil_frame)

        # Display the recognized license plate on the frame
        if len(self.result) > 0:
            number = self.result[0]
            text = f"Recognized License Plate: {number}"

            # Specify the Thai font and size
            thai_font = ImageFont.truetype(self.font_path, size=20)

            # Draw the Thai text on the frame
            draw.text((10, pil_frame.height - 30), text, font=thai_font, fill=(0, 255, 0))

        # Convert the modified PIL frame back to OpenCV format
        frame_with_text = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)

        # Resize the camera frame to match the size of the license plate text
        resized_frame = cv2.resize(frame, (frame_with_text.shape[1], frame_with_text.shape[0]))

        # Combine the resized camera frame and the frame with license plate text
        composite_frame = np.hstack((resized_frame, frame_with_text))

        # Display the composite frame on the screen using OpenCV's imshow
        cv2.imshow('License Plate Recognition', composite_frame)

        # Check for key press to exit
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LicensePlateApp(root)
    root.mainloop()
