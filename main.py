import random

import cv2
from cvzone.HandTrackingModule import HandDetector

from Shape import Circle, Block

# OpenCV BGR颜色对照表
colors = {'黑色': (0, 0, 0), '红色': (0, 0, 255), '绿色': (0, 255, 0), '蓝色': (255, 0, 0), '紫色': (128, 0, 128),
          '白色': (255, 255, 255), '深红色': (255, 0, 255), '青色': (255, 255, 0), '黄色': (0, 255, 255)}

cap = cv2.VideoCapture(0)  # 使用默认摄像头
width, height = 1280, 720
cap.set(3, width)  # 宽
cap.set(4, height)  # 高
detector = HandDetector(detectionCon=0.8)  # 置信度

Shapes = []  # 存储图形
generate_time = 40  # 生成新图形的频率(每隔50帧生成一个新图形)
now = 0  # 记录当前时刻
score = 0  # 得分
combo = 0  # 连续击中次数
cordon = height - 50  # 警戒线高度
while True:
    now += 1
    success, img = cap.read()
    img = detector.findHands(img)
    landmarks, bbox = detector.findPosition(img)
    if Shapes:  # 显示当前帧内所有块
        if landmarks:
            distance, _, _ = detector.findDistance(8, 7, img)  # 获取关节8和7之间的距离
            print(distance)
            if distance < 40:  # 关节之间的距离小于40认为是点击操作
                for b in Shapes:
                    if b.include(landmarks[8][0], landmarks[8][1]):  # 若触碰到，块消失
                        Shapes.remove(b)
                        combo += 1
                        if combo < 3:
                            score += 1
                        elif 3 <= combo < 5:
                            score += 2
                        elif 5 <= combo < 10:
                            score += 3
                        elif 10 <= combo:
                            score += 5

        for b in Shapes:  # 显示所有剩余块
            if b.escape(cordon):  # 图形触碰到警戒线，扣2分，图形消失
                score -= 2
                combo = 0
                Shapes.remove(b)
            else:
                b.show(img)
                b.fall()
    if now % generate_time == 0:  # 每隔generate_time帧，生成一个新的块
        shape = random.randint(0, 1)  # 随机选择形状
        r = random.randint(30, 60)  # 图形半径范围
        w = random.randint(150, width - 2 * r - 150)  # 图形左侧x坐标
        v = random.randint(1, 10)  # 图形下落速度
        color = random.sample(colors.keys(), 1)[0]  # 随机选取颜色键
        if shape == 0:
            Shapes.append(Block(w, v, r, colors[color]))
        elif shape == 1:
            Shapes.append(Circle(w, v, r, colors[color]))
    img = cv2.flip(img, 1)  # 显示画面对称翻转，更加符合人体感官
    cv2.rectangle(img, (width - 400, 0), (width, 150), colors['深红色'], cv2.FILLED)  # 得分框
    cv2.putText(img, 'Score:%d' % score, (width - 380, 50), cv2.FONT_HERSHEY_COMPLEX, 2, colors['白色'], 3)  # 得分
    cv2.putText(img, 'Combo:%d' % combo, (width - 380, 130), cv2.FONT_HERSHEY_COMPLEX, 2, colors['白色'], 3)  # 连击次数
    cv2.rectangle(img, (0, cordon), (width, cordon + 12), colors['深红色'], cv2.FILLED)  # 线外框
    cv2.line(img, (0, cordon + 6), (width, cordon + 6), colors['白色'], 4)  # 警戒线
    cv2.imshow('Just Click', img)
    if cv2.waitKey(1) & 0XFF == 27:  # 按"ESC"退出
        break
    if cv2.getWindowProperty('Just Click', cv2.WND_PROP_AUTOSIZE) < 1:  # 关闭窗口退出
        break
cap.release()
cv2.destroyAllWindows()
