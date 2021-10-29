import threading
import cv2
import time
from GRU import *
import torch
import mediapipe as mp
import numpy as np


class Identify:
    def __init__(self, win):
        self.win = win
        self.isEnd = False

    def start(self):
        threading.Thread(target=self.run).start()

    def run(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 摄像头图像采集
        movement = {0: "点击", 1: "平移", 2: "缩放", 3: "抓取", 4: "旋转", 5: "无", 6: "截图", 7:'放大'}
        S = 0  # 每帧的处理时间
        device = torch.device('cpu')  # 初始化于cpu上处理
        if torch.cuda.is_available():  # 判断是否能使用cuda
            device = torch.device('cuda:0')

        model = torch.load(r'model.pt', map_location='cpu').to(device)  # 载入模型
        # print(model)
        hiddem_dim = 30  # 隐藏层大小
        num_layers = 2  # GRU层数

        h_t = torch.zeros(num_layers, 1, hiddem_dim)  # 初始化全0的h_t
        h_t = h_t.to(device)  # 载入设备

        last_gesture = '无'  # 初始化最后输出，用于判断是否与当前输出一致
        prin_time = time.time()  # 初始化输出时间

        mp_drawing = mp.solutions.drawing_utils  # 坐标点绘制工具
        mp_hands = mp.solutions.hands
        ratio = self.cap.get(4) / self.cap.get(3)  # 高宽比

        with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,  # 最大的手的数量
                min_detection_confidence=0.65,  # 置信度高于0.65，输出手部模型
                min_tracking_confidence=0.5) as hands:
            start_time = time.time()  # 初始化当前帧帧起始时间

            while self.cap.isOpened():
                if self.isEnd:
                    break
                self.win.eventRunning.wait()

                in_dim = torch.zeros(126)  # 使得一开始的帧为全0

                # 判断是否满足当前帧率
                wait_time = S - (time.time() - start_time)
                if wait_time > 0:
                    time.sleep(wait_time)
                start_time = time.time()  # 重置起始时间

                success, image = self.cap.read()  # 获取摄像头输出
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

                image.flags.writeable = False
                results = hands.process(image)

                # 将指关节点绘于image
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 获取当前帧指关节点数据
                if results.multi_hand_landmarks:

                    # 判断手掌个数
                    if len(results.multi_handedness) == 1 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 1:
                        # 判断左右手先后
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            index_1 = []
                            # 将指关节点数据依次存入index
                            for k in range(0, 21):
                                index_1.append(hand_landmarks.landmark[k].x)
                                index_1.append(hand_landmarks.landmark[k].y)
                                index_1.append(hand_landmarks.landmark[k].z)
                            for k_1 in range(0, 63):
                                index_1.append(0)
                        # 最后将index（126）添加至in_dim（x，126）末尾
                        in_dim = torch.from_numpy(np.array(index_1))
                    elif len(results.multi_handedness) == 1 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 0:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            index_0 = []
                            for k_1 in range(0, 63):
                                index_0.append(0)
                            for k in range(0, 21):
                                index_0.append(hand_landmarks.landmark[k].x)
                                index_0.append(hand_landmarks.landmark[k].y)
                                index_0.append(hand_landmarks.landmark[k].z)
                        in_dim = torch.from_numpy(np.array(index_0))
                    elif len(results.multi_handedness) == 2 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 1:
                        index_1_first = []
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                            for k in range(0, 21):
                                index_1_first.append(hand_landmarks.landmark[k].x)
                                index_1_first.append(hand_landmarks.landmark[k].y)
                                index_1_first.append(hand_landmarks.landmark[k].z)
                        in_dim = torch.from_numpy(np.array(index_1_first))
                    elif len(results.multi_handedness) == 2 and results.multi_handedness[0].classification.__getitem__(
                            0).index == 0:
                        results.multi_hand_landmarks.reverse()
                        index_0_first = []
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                            for k in range(0, 21):
                                index_0_first.append(hand_landmarks.landmark[k].x)
                                index_0_first.append(hand_landmarks.landmark[k].y)
                                index_0_first.append(hand_landmarks.landmark[k].z)
                        in_dim = torch.from_numpy(np.array(index_0_first))

                # cv2.imshow('MediaPipe Hands', image)
                # cv2.waitKey(1)
                if self.win.eventRunning.isSet():
                    self.win.flash_img(image, ratio)

                in_dim = in_dim.unsqueeze(dim=0)
                in_dim = in_dim.unsqueeze(dim=0)
                in_dim = in_dim.to(torch.float32).to(device)
                h_t = h_t.to(torch.float32).to(device)
                if time.time() - prin_time < 2:
                    in_dim = torch.zeros(1, 1, 126).to(device)

                rel, h_t = model((in_dim, h_t))
                rel = torch.sigmoid(rel)
                confidence, rel = rel.max(1)

                # 对每个动作设置单独的置信度阈值
                cfd = {'点击': 0.90, '平移': 0.90, '缩放': 0.99, '抓取': 0.985, '旋转': 0.99, '无': 0, '截图': 0.99, '放大': 0.9}
                if confidence > cfd[movement[rel.item()]]:  # 超过阈值的动作将会被输出
                    now_gesture = last_gesture
                    last_gesture = movement[rel.item()]
                    if not (now_gesture == last_gesture):  # 判断是否与上次的输出相同，若相同则不输出
                        if time.time() - prin_time > 2:  # 若距离上次输出时间小于2秒，则不输出
                            # print(movement[rel.item()], ' \t置信度：', round(confidence.item(), 2))
                            self.win.set_gesture(movement[rel.item()])
                            prin_time = time.time()  # 重置输出时间
                            h_t = torch.zeros(num_layers, 1, hiddem_dim).to(device)  # 将当前的h_t重置
        self.cap.release()

    def break_loop(self):
        self.isEnd = True
