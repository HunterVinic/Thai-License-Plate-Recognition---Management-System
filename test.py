self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",  # Replace with your MySQL password
            database="licenseDB"  # Replace with your database name
        )


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

    # Convert the composite frame to a PhotoImage for display in Tkinter canvas
    self.photo = ImageTk.PhotoImage(image=Image.fromarray(composite_frame))

    # Update the camera canvas with the new PhotoImage
    self.camera_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    # Check for key press to exit
    key = cv2.waitKey(1)
    if key == ord('q'):
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()
