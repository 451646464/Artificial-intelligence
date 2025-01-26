import cv2
import dlib
import pandas as pd
import os
from colorama import Fore, Style, init
import pyfiglet
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np
import face_recognition  # استخدم مكتبة face_recognition

# Initialize colorama
init(autoreset=True)


def print_welcome_message():
    ascii_art = pyfiglet.figlet_format("#$*R_CS_L*$#", font="slant")
    print(Fore.BLUE + "--------------------CS------------*_*----------CS------------------------")
    print(Fore.BLUE + Style.DIM + ascii_art)
    print(Fore.BLUE + "--------------------CS------------*_*----------CS------------------------")


# Load data from CSV
try:
    data = pd.read_csv('people_data/people_data.csv')
except FileNotFoundError:
    print(Fore.RED + "Error: 'people_data.csv' not found.")
    exit()

known_faces = {}


def add_person(name, image_path, age, university, major, id_number, marital_status, surname, level):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:  # تأكد من وجود ترميز
            known_faces[name] = {
                'encoding': face_encodings[0],
                'age': age,
                'university': university,
                'major': major,
                'id_number': id_number,
                'marital_status': marital_status,
                'surname': surname,
                'level': level,
                'image_path': image_path
            }
            print(f"Encoding for {name}: {face_encodings[0]}")  # طباعة الترميز
        else:
            print(Fore.RED + f"No face found in image {image_path}.")
    except Exception as e:
        print(Fore.RED + f"Error loading image {image_path}: {e}")


# Read images from folder
image_folder = 'image/'

for index, row in data.iterrows():
    name = row['name']
    age = row['age']
    university = row['university']
    major = row['major']
    id_number = row['id_number']
    marital_status = row['marital_status']
    surname = row['surname']
    level = row['level']

    image_path = os.path.join(image_folder, f"{index + 1}.jpg")
    add_person(name, image_path, age, university, major, id_number, marital_status, surname, level)


def recognize_faces_from_camera():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print(Fore.RED + "Error: Could not open video camera.")
        return

    print(Fore.YELLOW + "Press 'q' to quit the camera.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print(Fore.RED + "Error: Could not read frame.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            # مقارنة مع الوجوه المعروفة
            distances = face_recognition.face_distance([data['encoding'] for data in known_faces.values()],
                                                       face_encoding)
            best_match_index = np.argmin(distances)

            if distances[best_match_index] < 0.6:  # عتبة المقارنة
                name = list(known_faces.keys())[best_match_index]

            # رسم مربع حول الوجه
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def recognize_faces_from_file(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        for face_encoding in face_encodings:
            name = "Unknown"
            distances = face_recognition.face_distance([data['encoding'] for data in known_faces.values()],
                                                       face_encoding)
            best_match_index = np.argmin(distances)

            if distances[best_match_index] < 0.6:
                name = list(known_faces.keys())[best_match_index]

            # Display information in a table
            if name != "Unknown":
                person_data = known_faces[name]
                table = PrettyTable()
                table.field_names = ["Field", "Value"]
                table.add_row(["Name", name])
                table.add_row(["Age", person_data['age']])
                table.add_row(["University", person_data['university']])
                table.add_row(["Major", person_data['major']])
                table.add_row(["ID Number", person_data['id_number']])
                table.add_row(["Marital Status", person_data['marital_status']])
                table.add_row(["Surname", person_data['surname']])
                table.add_row(["Level", person_data['level']])
                print(Fore.MAGENTA + str(table))

                # Display the person's image
                person_image = cv2.imread(person_data['image_path'])
                plt.imshow(cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB))
                plt.axis('off')
                plt.title(str(table))

                plt.show()
            else:
                print(Fore.RED + "Face not recognized.")

    except Exception as e:
        print(Fore.RED + f"Error processing image {image_path}: {e}")


def main():
    print_welcome_message()

    while True:
        print(Fore.BLUE + "Please select an option:")
        print(Fore.YELLOW + "1. Open camera for face recognition")
        print(Fore.YELLOW + "2. Import image from files")
        print(Fore.YELLOW + "3. Exit")

        choice = input(Fore.YELLOW + "Enter your choice (1, 2, or 3): ")

        if choice == '1':
            recognize_faces_from_camera()
        elif choice == '2':
            image_path = input(Fore.CYAN + "Enter the path to the image file: ")
            recognize_faces_from_file(image_path)
        elif choice == '3':
            print(Fore.GREEN + "Exiting the program.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
