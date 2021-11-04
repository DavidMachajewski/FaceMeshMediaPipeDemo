# #########################################
# To run the webcam in virtual box:
# 1. Check if you have installed extensions
#     to your virtual machine
# 2. go to your VirtualBox folder
#    and type VBoxManage list webcams
# 3. VBoxManage controlvm "Ubuntu 20.04" webcam attach .1
# 4. Under Devices enable webcam
# It should run now.
#
# This code is based on following sources:
# 1.
# 2.
# 3.
# #########################################
import numpy as np
import mediapipe as mp
from cv2 import cv2 as cv


class FaceMeshing:
    def __init__(self, args):
        self.args = args
        # init classes for face meshing
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        # init class for segmentation
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    def init_stream(self):
        stream = cv.VideoCapture(0)

        if not stream.isOpened():
            raise IOError("No access to webcam!")

        while stream.isOpened():
            while True:
                ret, frame = stream.read()
                frame = cv.resize(frame,
                                  None,
                                  fx=self.args.fx,
                                  fy=self.args.fy,
                                  interpolation=cv.INTER_AREA)
                # from now on media pipe code!
                with self.mp_face_mesh.FaceMesh(max_num_faces=1,
                                                refine_landmarks=True,
                                                min_detection_confidence=0.5,
                                                min_tracking_confidence=0.5) as face_mesh:
                    frame.flags.writeable = False
                    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                    results = face_mesh.process(frame)

                    # face mesh annotations
                    frame.flags.writeable = True
                    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
                    if results.multi_face_landmarks:
                        for face_landmarks in results.multi_face_landmarks:
                            frame = self.apply_mesh(frame, face_landmarks)
                            if self.args.segmentation:
                                frame = self.apply_segmentation(frame, face_landmarks)
                cv.imshow('Input', cv.flip(frame, 1))
                c = cv.waitKey(1)  # press escape
                if c == 27:
                    break
            stream.release()
            cv.destroyAllWindows()

    def apply_segmentation(self, image, landmarks):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results_segmentation = self.selfie_segmentation.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        condition = np.stack((results_segmentation.segmentation_mask,) * 3, axis=-1) > 0.5
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = (0, 237, 63)
        image = np.where(condition, image, bg_image)
        return image

    def apply_mesh(self, image, landmarks):
        self.mp_drawing.draw_landmarks(
            image=image,
            landmark_list=landmarks,
            connections=self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(102, 255, 102), thickness=1, circle_radius=1
            ))
        self.mp_drawing.draw_landmarks(
            image=image,
            landmark_list=landmarks,
            connections=self.mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(255, 255, 255), thickness=2, circle_radius=1
            )
        )
        self.mp_drawing.draw_landmarks(
            image=image,
            landmark_list=landmarks,
            connections=self.mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(255, 0, 0), thickness=1, circle_radius=1
            ),
            connection_drawing_spec=self.mp_drawing.DrawingSpec(
                color=(255, 0, 0), thickness=1, circle_radius=1
            )
        )
        return image
