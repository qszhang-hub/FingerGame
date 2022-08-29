import cv2


class Shape:  # 图形基类    (w, h)为图形左上角坐标
    def __init__(self, w, v, r, color):  # 左侧x坐标，下落速度，半径，颜色
        self.w = w
        self.v = v
        self.h = 0
        self.r = r
        self.color = color

    def fall(self):
        self.h += self.v

    def escape(self, cordon):  # 判断图形是否触碰警戒线    cordon：警戒线
        if self.h + 2 * self.r > cordon:
            return True
        else:
            return False


class Block(Shape):  # 方块型
    def __init__(self, w, v, r, color):
        super(Block, self).__init__(w, v, r, color)  # 继承自父类

    def show(self, img):
        cv2.rectangle(img, (self.w, self.h), (self.w + 2 * self.r, self.h + 2 * self.r), self.color, cv2.FILLED)

    def include(self, x, y):  # 判断是否将关节8包含在内
        if self.w <= x <= self.w + 2 * self.r and self.h <= y <= self.h + 2 * self.r:
            return True
        else:
            return False


class Circle(Shape):  # 圆形
    def __init__(self, w, v, r, color):
        super(Circle, self).__init__(w, v, r, color)  # 继承自父类

    def show(self, img):
        cv2.circle(img, (self.w + self.r, self.h + self.r), self.r, self.color, cv2.FILLED)

    def include(self, x, y):  # 判断是否将关节8包含在内
        if (x - self.w - self.r) ** 2 + (y - self.h - self.r) ** 2 <= self.r ** 2:
            return True
        else:
            return False
