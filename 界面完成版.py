import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import mediapipe as mp
import math


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)

        # 创建画布，用于显示图像
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # create label for eye detection
        self.label = tk.Label(window, text="Eye Opened", font=('Arial', 15), fg="#f00")
        self.label.place(relx=0.4, rely=0.91)

        # 创建按钮，用于退出程序
        self.btn_quit = tk.Button(window, text="Quit", command=self.quit)
        self.btn_quit.pack(anchor=tk.SE, padx=10, pady=10)

        # 开始显示摄像头数据
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # 读取摄像头数据
        # ret, frame = self.cap.read()
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh

        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:
            # while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
            #                continue
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
            leftEar = self.EAR(left1, left2, left3, left4, left5, left6)

            right1 = results.multi_face_landmarks[0].landmark[33]
            right2 = results.multi_face_landmarks[0].landmark[160]
            right3 = results.multi_face_landmarks[0].landmark[158]
            right4 = results.multi_face_landmarks[0].landmark[133]
            right5 = results.multi_face_landmarks[0].landmark[153]
            right6 = results.multi_face_landmarks[0].landmark[144]
            rightEar = self.EAR(right1, right2, right3, right4, right5, right6)

            avgEar = (leftEar + rightEar) / 2

            if success:
                # 将图像转换为 RGB 格式
                frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # 将图像转换为 PIL.Image 格式
                image = PIL.Image.fromarray(frame)

                # 将 PIL.Image 转换为 Tkinter PhotoImage 格式
                self.photo = PIL.ImageTk.PhotoImage(image)

                # 在画布上显示图像
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

                # update label for eye detection
                if avgEar > 0.1:
                    self.label = tk.Label(self.window, text="Eye Opened", font=('Arial', 15), fg="#f00")
                    self.label.place(relx=0.4, rely=0.91)
                else:
                    self.label = tk.Label(self.window, text="Eye Closed", font=('Arial', 16), fg="#f00")
                    self.label.place(relx=0.4, rely=0.91)

        # 每隔一段时间更新一次画面
        self.window.after(self.delay, self.update)

    def dist(self, P1, P2):
        return math.sqrt((abs(P1.x - P2.x) ** 2) + (abs(P1.y - P2.y) ** 2))

    def EAR(self, P1, P2, P3, P4, P5, P6):
        P26 = self.dist(P2, P6)
        P35 = self.dist(P3, P5)
        P14 = self.dist(P1, P4)
        return (P26 + P35) / (2 * P14)

    def quit(self):
        # 释放摄像头资源
        self.cap.release()
        # 关闭窗口
        self.window.destroy()


# 创建窗口
App(tk.Tk(), "Tkinter and OpenCV")
