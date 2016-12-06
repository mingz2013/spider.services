# -*- coding: utf-8 -*-

from CR import *


class ImageProcessing:
    # --------------------------------------------------------------#
    def __init__(self, name='', im=None):
        self.name = name
        self.im = im

    # --------------------------------------------------------------#
    # 根据R*G*B来去除噪声
    def get_kind_by_rgb(self):
        self.kind = []
        VAL = 905000
        if len(self.name) != 0:
            im = Image.open(self.name)
        elif self.im != None:
            im = self.im
        else:
            return self.kind
        if im.mode != 'RGB':
            im = im.convert('RGB')
        for x in range(im.size[1]):
            self.kind.append([])
            for y in range(im.size[0]):
                tmp = im.getpixel((y, x))
                u = tmp[0] * tmp[1] * tmp[2]
                if u < VAL:
                    self.kind[x].append(1)
                else:
                    self.kind[x].append(0)
        return self.kind

    # --------------------------------------------------------------#
    # 根据预先估计的宽度截取字符，截取前4个即所有重要信息
    def get_char_by_width(self):
        self.char = []
        WIDTH = ((0, 35), (28, 70), (60, 95), (88, 129))
        for i in range(len(WIDTH)):
            self.char.append([])
            for x in range(50):
                self.char[i].append([])
                for y in range(WIDTH[i][0], WIDTH[i][1]):
                    self.char[i][x].append(self.kind[x][y])
        return self.char

    # --------------------------------------------------------------#
    # 根据截取的字符，获取真实所需的单一字符，删除多余的部分
    def cal_single_char(self):
        for i in range(len(self.char)):
            # 划分黑色为不同种类
            N = 0
            while (True):
                # 寻找黑色
                for x in range(len(self.char[i])):
                    if 1 in self.char[i][x]:
                        y = self.char[i][x].index(1)
                        break
                else:
                    break
                # 向四周探索
                tempPoint = set()
                self.char[i][x][y] = N + 2
                tempPoint.add((x, y))
                nextPoint = set()
                while len(tempPoint) != 0:
                    for (x, y) in tempPoint:
                        for (u, v) in (
                                (x + 3, y), (x - 3, y), (x, y + 3), (x, y - 3), (x - 1, y), (x + 1, y), (x, y - 1),
                                (x, y + 1),
                                (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1), (x - 2, y), (x + 2, y),
                                (x, y - 2), (x, y + 2)):
                            if u < 0 or v < 0 or u >= len(self.char[i]) or v >= len(self.char[i][0]):
                                continue
                            if self.char[i][u][v] == 1:
                                self.char[i][u][v] = N + 2
                                nextPoint.add((u, v))
                    tempPoint = nextPoint
                    nextPoint = set()
                N += 1
            # 筛选出单一字符
            size = [0] * N
            aveY = [0] * N
            for x in range(len(self.char[i])):
                for y in range(len(self.char[i][x])):
                    if self.char[i][x][y] != 0:
                        size[self.char[i][x][y] - 2] += 1
                        aveY[self.char[i][x][y] - 2] += y
            trueN = 0
            for j in range(N):
                aveY[j] /= size[j]
                if size[j] < 10:
                    aveY[j] = len(self.char[i][0])
                aveY[j] = abs(len(self.char[i][0]) / 2 - aveY[j])
            trueN = aveY.index(min(aveY)) + 2
            minY = 150
            maxY = 0
            minX = 50
            maxX = 0
            for x in range(len(self.char[i])):
                for y in range(len(self.char[i][x])):
                    if self.char[i][x][y] == trueN:
                        self.char[i][x][y] = 1
                        if minX > x:
                            minX = x
                        if maxX < x:
                            maxX = x
                        if minY > y:
                            minY = y
                        if maxY < y:
                            maxY = y
                    else:
                        self.char[i][x][y] = 0
            char = []
            for u in range(maxX - minX + 1):
                char.append([])
                for v in range(maxY - minY + 1):
                    char[u].append(self.char[i][u + minX][v + minY])
            self.char[i] = char
            '''
            if maxY - minY > 25:
                self.char = []
                return self.char
            '''
        return self.char

    # --------------------------------------------------------------#
    # 根据字符大小获取最终判断依据的字符
    def cal_final_char(self):
        if len(self.char) != 4:
            self.char = []
            return self.char
        # 第一个字符：数字
        if len(self.char[0]) > 14 and len(self.char[0][0]) > 14:
            self.char = []
            return self.char
        # 第二个字符：加减乘
        if len(self.char[1]) < 15 or len(self.char[1][0]) < 15:
            self.char = []
            return self.char
        # 第三个字符：上去以数字
        if len(self.char[2]) > 14 and len(self.char[2][0]) > 14:
            if len(self.char[3]) < 15 or len(self.char[3][0]) < 15:
                self.char.pop(2)
                return self.char
            else:
                self.char = []
                return self.char
        else:
            self.char.pop()
            return self.char

    # --------------------------------------------------------------#
    def run(self):
        self.output = ''
        if len(self.get_kind_by_rgb()) == 0:
            return self.output
        self.get_char_by_width()
        self.cal_single_char()
        self.cal_final_char()
        if len(self.char) == 0:
            return self.output
        self.output = CharacterRecognition(self.char).run()
        return self.output


if __name__ == '__main__':
    noResultTime = 0
    for i in range(1, 301):
        test = ImageProcessing('data/Fig/Fig_%03d.png' % i)
        result = test.run()
        print (i, '=', result)
        if len(result) == 0:
            noResultTime += 1
    print('noResultTime = %d' % noResultTime)
    # noResultTime = 46
