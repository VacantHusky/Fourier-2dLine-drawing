# python3
#
# 作者qq: 1750686829
# 写的很乱，将就着看吧，懒得整理了
# 有不懂的可以问我
# fourier_data.py是数据
# 然后画出来

import pygame, math, os
from pygame.locals import *
from sys import exit

WINDOW_W = 1200
WINDOW_H = 600
one_time = 3  # 时间流速（默认1）
scale = 1  # 缩放（默认120）
FPS = 20  # 帧率
point_size = 2  # 点的大小
start_xy = (WINDOW_W // 2 + 100, WINDOW_H // 2)  # 圆的位置

# 波形图参数
b_scale = 1  # 图形缩放
b_color = (255, 10, 250)  # 图形颜色
b_length = 10000  # 图形显示的长度

from fourier_data import PP

fourier_list = PP[:]
# fourier_list = [
#     [-12.498542385850477, -6.2821854368251655, 1.5707963267948966],
#     [3.00050383132651, -6.280185696116324, 1.5707963267948966],
#     [2.5030219030606116, -6.281185566470744, 1.5707963267948966],
#     [2.4997029488005142, -0.0019997407088413704, 1.5707963267948966],
#     [-1.0003998778263687, -0.002999611063262056, 1.5707963267948966],
#     [0.5000686798258874, -0.003999481417682741, 1.5707963267948966],
#     [-0.49971051043998416, -0.0009998703544206852, 1.5707963267948966],
#     [0.4991197149614191, -6.279185825761904, 1.5707963267948966],
#     [-0.005090576598869052, -6.2821854368251655, 3.141592653589793],
#     [0.003666259842404127, -6.280185696116324, 3.141592653589793],
#     [0.0020389300523211344, -6.281185566470744, 3.141592653589793],
#     [-0.002036226474097552, -0.0019997407088413704, 3.141592653589793],
#     [0.001222370009870445, -0.002999611063262056, 3.141592653589793],
# ]

# 初始化pygame
pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 70)
# 创建一个窗口
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("傅里叶变换可视化")
font = pygame.font.SysFont('simhei', 20)


class Circle():
    x, y = 0, 0
    r = 0
    angle = 0
    angle_v = 0
    color = (0, 0, 0)
    father = None

    def __init__(self, r, angle_v, angle, color=None, father=None):
        self.r = r
        self.angle_v = angle_v
        self.angle = angle
        self.father = father
        if color is None:
            self.color = (250, 250, 250)
        else:
            self.color = color

    def set_xy(self, xy):
        self.x, self.y = xy

    def get_xy(self):
        return self.x, self.y

    def set_xy_by_angle(self):
        self.x = self.father.x + self.r * math.cos(self.angle) * scale
        self.y = self.father.y + self.r * math.sin(self.angle) * scale

    def run(self, step_time):
        if self.father is not None:
            self.angle += self.angle_v * step_time
            self.set_xy_by_angle()

    def draw(self, screen):
        color_an = tuple(map(lambda x: x // 3, self.color))
        # 画圆
        # print(color_an, int(round(self.x)), self.y)
        pygame.draw.circle(screen, self.color, (int(round(self.x)), int(round(self.y))), point_size)
        # 画轨道
        if self.father is not None:
            # print(color_an, self.father.x, self.father.y)
            pygame.draw.circle(screen, color_an, (int(round(self.father.x)), int(round(self.father.y))),
                               max(int(round(abs(self.r) * scale)), 1),
                               1)
            pygame.draw.line(screen, self.color, (self.father.x, self.father.y), (self.x, self.y),
                             1)


class Boxin():
    xys = []

    def add_point(self, xy):
        self.xys.append(xy)
        if len(self.xys) > b_length:
            self.xys.pop(0)

    def draw(self, screen):
        # 画一个圆
        # pygame.draw.circle(screen, b_color, (b_xy[0], int(b_xy[1] + self.ys[-1] * scale)), point_size)
        bl = len(self.xys)
        for i in range(bl - 1):
            pygame.draw.line(screen, (255, 250, 0), self.xys[i], self.xys[i + 1], 1)


# fourier_list = sorted(fourier_list, key=lambda x: abs(x[0]), reverse=True)
super_circle = Circle(0, 0, 0, color=b_color)
super_circle.set_xy(start_xy)
circle_list = [super_circle]
for i in range(len(fourier_list)):
    p = fourier_list[i]
    circle_list.append(Circle(p[0], p[1], p[2], color=b_color, father=circle_list[i]))

bx = Boxin()
clock = pygame.time.Clock()
# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key == K_LEFT and one_time > 0.1:
                one_time *= 0.9
                one_time = max(one_time, 0.1)
            elif event.key == K_RIGHT and one_time < 10:
                one_time *= 1.1
            elif (event.key == K_EQUALS or event.key == K_PLUS) and scale < 800:
                scale *= 1.1
            elif event.key == K_MINUS and scale > 0.001:
                scale *= 0.9
                scale = max(scale, 0.001)
            else:
                print(type(event.key), event.key)

    # 将背景图画上去
    screen.fill((0, 0, 0))
    # 运行
    for i, circle in enumerate(circle_list):
        circle.run(1)
        circle.draw(screen)

    last_circle = circle_list[-1]
    # 画波形
    bx.add_point((last_circle.x, last_circle.y))
    bx.draw(screen)

    pygame.display.update()
    time_passed = clock.tick(FPS)
