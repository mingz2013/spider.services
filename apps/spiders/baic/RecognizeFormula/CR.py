# -*- coding: utf-8 -*-

import json

from PIL import Image


class CharacterRecognition:
    # --------------------------------------------------------------#
    def __init__(self, char):
        self.char = char

    # --------------------------------------------------------------#
    # 读取已处理的图
    def exp(self, name, i):
        im = Image.open('data/Database/' + name + '/' + name + ' (%d).png' % i)
        for x in range(im.size[1]):
            self.char[0].append([])
            for y in range(im.size[0]):
                if im.getpixel((y, x)) == 0:
                    self.char[0][x].append(1)
                else:
                    self.char[0][x].append(0)
        return self.char

    # --------------------------------------------------------------#
    def rec_symbol(self):
        self.symbol = ''
        with open('data/sym_data.json', 'r') as f:
            data = json.load(f)
        N = 1
        tmp = []
        for i in range(len(data)):
            if len(data[i][1]) == len(self.char[N]) and len(data[i][1][0]) == len(self.char[N][0]):
                s = 0
                for x in range(len(self.char[N])):
                    for y in range(len(self.char[N][0])):
                        if data[i][1][x][y] == self.char[N][x][y]:
                            s += 1
                tmp.append((s, i))
        result = 0
        for i in range(len(tmp)):
            if tmp[i][0] > result:
                result = tmp[i][0]
                self.symbol = data[tmp[i][1]][0]
        return self.symbol

    # --------------------------------------------------------------#
    def rec_number(self):
        self.number = ['', '']
        with open('data/num_data.json', 'r') as f:
            data = json.load(f)
        for N in (0, 2):
            tmp = []
            for i in range(len(data)):
                s = 0
                if len(data[i][1]) == len(self.char[N]) and len(data[i][1][0]) == len(self.char[N][0]):
                    for x in range(len(self.char[N])):
                        for y in range(len(self.char[N][0])):
                            if data[i][1][x][y] == self.char[N][x][y]:
                                s += 1
                tmp.append((s, i))
            result = 0
            for i in range(len(tmp)):
                if tmp[i][0] > result:
                    result = tmp[i][0]
                    self.number[N / 2] = data[tmp[i][1]][0]
        return self.number

    # --------------------------------------------------------------#
    def run(self):
        self.rec_symbol()
        '''
        # 无法识别符号时，认为是乘。如果不想这么做，就取消注释
        if self.symbol == '':
            return ''
        '''

        self.rec_number()
        if self.number[0] == '' or self.number[1] == '':
            return ''

        a = int(self.number[0])
        b = int(self.number[1])

        if self.symbol == 'add':
            return str(a + b)
        elif self.symbol == 'red':
            return str(a - b)
        elif self.symbol == 'mul':
            return str(a * b)
        else:
            return str(a * b)


if __name__ == '__main__':
    # '''
    pass
    '''
    # 删去上面的 # 即可运行
    # 一般不需要运行下面的函数

    # 本函数用于读取Database中的特征，存储在文件中
    # 验证码库越大，准确率越高，但是过大的验证码库对效率有一定影响

    data = []
    # data[i]是一条数据，每条数据格式为[0名称，1数组char]
    for name in ('add', 'red', 'mul'):
        for i in range(1, 1000):
            if os.path.exists('Database/' + name + '/' + name + ' (%d).png'%i) == False:
                break
            test = CharacterRecognition([[]])
            test.exp(name, i)
            data.append((name, test.char[0]))
    with open('sym_data.json', 'w') as f:
        json.dump(data, f)

    data = []
    # data[i]是一条数据，每条数据格式为[0名称，1数组char]
    for name in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
        for i in range(1, 1000):
            if os.path.exists('Database/' + name + '/' + name + ' (%d).png'%i) == False:
                break
            test = CharacterRecognition([[]])
            test.exp(name, i)
            data.append((name, test.char[0]))
    with open('num_data.json', 'w') as f:
        json.dump(data, f)
#'''
