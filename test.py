from tkinter import *
from PIL import Image, ImageTk
import time
import cv2
import mediapipe as mp
import math
import threading

data = "睁眼了"

def gui():
    window = Tk()
    window.geometry("1000x800")

    # The title bar
    frame = Frame(window, width=1000, height=100)
    img = Image.open("title.jpg")
    reimg = img.resize((1000, 100))
    newimg = ImageTk.PhotoImage(reimg)
    # The video stream shown
    frame2 = Frame(window, width=640, height=480)
    img2 = Image.open("image.png")
    newimg2 = ImageTk.PhotoImage(img2)
    # pack the title bar
    frame.pack(fill=BOTH, expand=True)
    label1 = Label(frame, image=newimg)
    label1.pack()
    # pack the video stream
    frame2.place(rely=0.5, relx=0.02, anchor=W)
    label2 = Label(frame2, image=newimg2)
    label2.pack()
    # create and pack the results
    label3 = Label(window, text=data, font=('Arial', 25), fg="#f00")
    label3.place(rely=0.5, relx=0.95, anchor=E)
    label4 = Label(window, text="状态:", font=('Arial', 25))
    label4.place(rely=0.5, relx=0.8, anchor=E)
    # create and pack the time
    timestr = time.strftime("%H:%M:%S")
    label5 = Label(window, text=timestr, font=('Arial', 10), fg="#555")
    label5.place(rely=1, relx=1, anchor=SE)

    # loop
    while True:
        label3 = Label(window, text=data, font=('Arial', 25), fg="#f00")
        label3.place(rely=0.5, relx=0.95, anchor=E)
        timestr = time.strftime("%H:%M:%S")
        label5 = Label(window, text=timestr, font=('Arial', 10), fg="#555")
        label5.place(rely=1, relx=1, anchor=SE)
        window.update()

    window.mainloop()


def core():
    def dist(P1, P2):
        return math.sqrt((abs(P1.x - P2.x) ** 2) + (abs(P1.y - P2.y) ** 2))

    def EAR(P1, P2, P3, P4, P5, P6):
        P26 = dist(P2, P6)
        P35 = dist(P3, P5)
        P14 = dist(P1, P4)
        return (P26 + P35) / (2 * P14)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    cap = cv2.VideoCapture(0)
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())
            # Flip the image horizontally for a selfie-view display.

            left1 = results.multi_face_landmarks[0].landmark[362]
            left2 = results.multi_face_landmarks[0].landmark[385]
            left3 = results.multi_face_landmarks[0].landmark[387]
            left4 = results.multi_face_landmarks[0].landmark[263]
            left5 = results.multi_face_landmarks[0].landmark[373]
            left6 = results.multi_face_landmarks[0].landmark[380]
            leftEar = EAR(left1, left2, left3, left4, left5, left6)

            right1 = results.multi_face_landmarks[0].landmark[33]
            right2 = results.multi_face_landmarks[0].landmark[160]
            right3 = results.multi_face_landmarks[0].landmark[158]
            right4 = results.multi_face_landmarks[0].landmark[133]
            right5 = results.multi_face_landmarks[0].landmark[153]
            right6 = results.multi_face_landmarks[0].landmark[144]
            rightEar = EAR(right1, right2, right3, right4, right5, right6)

            avgEar = (leftEar + rightEar) / 2
            global data
            if avgEar < 0.1:
                data = "闭眼了"
            else:
                data = "睁眼了"
            # cv2.imwrite('image.png', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
            # time.sleep(0.1)
    cap.release()

threading.Thread(target=core, daemon=True).start()
gui()