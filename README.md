The provided code implements a facial recognition application using Python's Tkinter for the GUI, along with various libraries for image processing and data handling. Here’s a detailed explanation of how the tool operates:

### Functionality Overview

1. **Data Loading**:
   - The application begins by loading user data from a CSV file (`people_data.csv`). This data includes personal information such as name, age, university, and major.

2. **Face Encoding**:
   - For each person in the dataset, the application loads their corresponding image and computes a facial encoding using the `face_recognition` library. This encoding is a numerical representation of the facial features.

3. **Face Recognition**:
   - The application provides functionalities to recognize faces in real-time using a webcam or from uploaded images. 
   - When the camera is opened, it captures frames and identifies faces by comparing them against the known face encodings stored in the dictionary.

4. **User Interaction**:
   - Users can perform several actions:
     - **Open Camera**: Activates the webcam to detect and recognize faces in real-time.
     - **Upload Image**: Allows users to select an image file and recognize faces within it.
     - **Enter Image Path**: Similar to uploading, but the user can specify a file path directly.
     - **Capture Image**: A placeholder function for future implementation.
     - **Exit**: Closes the application.

5. **Displaying Data**:
   - When a face is recognized, the application retrieves the associated data and displays it in a new window, including a photo and personal details formatted in a table.

6. **Error Handling**:
   - The application includes error handling for file operations and image processing, displaying appropriate messages if issues arise (e.g., file not found or no face detected).

### Core Functions

- **Face Recognition Logic**:
  - The program calculates the face distance between the captured face encodings and the known faces. If the distance is below a threshold (0.6), it considers the face recognized.

- **User Interface**:
  - The GUI is built using `ttkbootstrap`, providing a modern look with styled buttons and labels. 
  - Background images are used to enhance the visual appeal, and buttons are created with custom styles for a unique user experience.

### install tools



```python
git clone 
```

### Conclusion

This application effectively combines facial recognition technology with a user-friendly interface, allowing users to easily identify individuals based on their facial features. It handles various file types, provides immediate feedback, and includes error management to enhance usability. Further enhancements could include refining the image capture functionality and expanding the dataset.
