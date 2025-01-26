import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import face_recognition
import pandas as pd
import cv2
import os
import ttkbootstrap as ttk  # مكتبة لدعم الأنماط الحديثة في Tkinter
from prettytable import PrettyTable  # لاستخدام الجداول

# تحميل البيانات من ملف CSV
try:
    data = pd.read_csv('people_data/people_data.csv')
except FileNotFoundError:
    messagebox.showerror("Error", "'people_data.csv' not found.")
    exit()

# قاموس لتخزين ترميزات وبيانات الأشخاص
known_faces = {}

# إضافة بيانات الأشخاص إلى القاموس
def add_person(name, image_path, age, university, major, id_number, marital_status, surname, level):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
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
        else:
            print(f"No face found in image {image_path}.")
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")


# تحميل بيانات الأشخاص
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


# وظائف الأزرار
def open_camera():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        messagebox.showerror("Error", "Could not open video camera.")
        return

    messagebox.showinfo("Info", "Press 'q' to quit the camera.")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            distances = face_recognition.face_distance([data['encoding'] for data in known_faces.values()],
                                                       face_encoding)
            best_match_index = None
            if distances.any():
                best_match_index = distances.argmin()

            if best_match_index is not None and distances[best_match_index] < 0.6:
                name = list(known_faces.keys())[best_match_index]

            # رسم مربع حول الوجه
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def upload_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        recognize_faces_from_file(file_path)


def enter_image_path():
    file_path = filedialog.askopenfilename(title="Select Image Path", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        recognize_faces_from_file(file_path)


def capture_image():
    messagebox.showinfo("Capture Image", "Function to capture image will be implemented here.")


def quit_app():
    root.quit()


# دالة لعرض بيانات الشخص
def show_person_data(person_data, name):
    # إنشاء نافذة جديدة لعرض البيانات
    new_window = ttk.Toplevel(root)
    new_window.title(f"Data for {name}")
    new_window.geometry("800x350")

    # عرض صورة الشخص
    person_image = Image.open(person_data['image_path'])
    person_image = person_image.resize((150, 150), Image.Resampling.LANCZOS)
    person_photo = ImageTk.PhotoImage(person_image)

    img_label = ttk.Label(new_window, image=person_photo)
    img_label.image = person_photo  # حفظ المرجع للصور
    img_label.grid(row=0, column=0, padx=20, pady=20)

    # عرض بيانات الشخص في جدول
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

    data_label = ttk.Label(new_window, text=str(table), font=("Courier", 10), anchor="w")
    data_label.grid(row=0, column=1, padx=20, pady=20)


# دالة للتعرف على الوجوه من الصورة
def recognize_faces_from_file(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        for face_encoding in face_encodings:
            name = "Unknown"
            distances = face_recognition.face_distance([data['encoding'] for data in known_faces.values()],
                                                       face_encoding)
            best_match_index = distances.argmin() if distances.any() else None

            if best_match_index is not None and distances[best_match_index] < 0.6:
                name = list(known_faces.keys())[best_match_index]

            if name != "Unknown":
                person_data = known_faces[name]
                show_person_data(person_data, name)
            else:
                messagebox.showinfo("Face Not Recognized", "Face not recognized.")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")


# إنشاء نافذة Tkinter باستخدام ttkbootstrap
root = ttk.Window(themename="darkly")  # يمكنك اختيار ثيم مختلف
root.title("Programing Rakan AL-Muliki")
root.geometry("900x700")

# إضافة صورة كخلفية
bg_image = Image.open("background/backgrond.jpg")
bg_image = bg_image.resize((900, 700), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# تعيين الخلفية
bg_label = ttk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

title_label = ttk.Label(
    root,
    text=" R Welcome programe Getting to know people L",
    font=("Arial", 22, "bold italic"),  # الخط عريض ومائل
    foreground="#00aaff",
    anchor="center"
)
title_label.place(relx=0.5, y=50, anchor="center")
# تصميم الأزرار مع توهج دائم وحواف دائرية باستخدام تعديل مباشر
def create_button(text, command):
    return ttk.Button(
        root,
        text=text,
        bootstyle="primary",  # اللون الأزرق الفاتح
        width=25,
        command=command,
        style="Custom.TButton"  # استخدام نمط مخصص
    )


# إضافة نمط مخصص للأزرار مع توهج دائم
style = ttk.Style()
style.configure("Custom.TButton",
                borderwidth=7,
                relief="solid",
                padding=10,
                font=("Helvetica", 12, "bold"),
                foreground="white",
                background="#00aaff",  # الأزرق الفاتح
                width=20,
                anchor="center",
                highlightbackground="#0099cc",  # توهج ثابت على الحدود
                highlightcolor="#99ccff",  # توهج ثابت عند التفاعل
                )

# زر فتح الكاميرا
camera_button = create_button("Open Camera", open_camera)
camera_button.place(x=50, y=500)

# زر تحميل الصورة
upload_button = create_button("Upload Image", upload_image)
upload_button.place(x=50, y=550)

# زر إدخال مسار الصورة
path_button = create_button("Enter Image Path", enter_image_path)
path_button.place(x=560, y=500)

# زر التقاط صورة
capture_button = create_button("Capture Image", capture_image)
capture_button.place(x=560, y=550)

# زر الخروج
exit_button = create_button("Exit", quit_app)
exit_button.place(x=310, y=610)

# تشغيل التطبيق
root.mainloop()
