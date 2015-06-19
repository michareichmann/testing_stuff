__author__ = 'micha'

from numpy import zeros
from ROOT import TH2F


def create_th2(data, x_min, x_max, y_min, y_max, name, x_title, y_title, z_title):
    th2 = TH2F(name, name, data.shape[0], x_min, x_max, data.shape[1], y_min, y_max)
    th2.SetDirectory(0)
    th2.SetMarkerSize(10)
    th2.GetXaxis().SetTitle(x_title)
    th2.GetYaxis().SetTitle(y_title)
    th2.GetZaxis().SetTitle(z_title)
    th2.SetDrawOption('COLZ')
    for ix, x in enumerate(data):
        for iy, y in enumerate(x):
            th2.SetBinContent(ix, iy, y)
    return th2


f = open("log", 'r')
line = f.readline().split()
f.close()
for i in range(len(line)):
    line[i] = int(line[i])


class SingleEvent:
    """show hitmaps of single events"""

    def __init__(self):
        self.data = line
        self.ultrablack = 0
        self.black = 0
        self.planes = 0
        self.get_b_ub()
        self.level_s = (self.black - self.ultrablack) / 8
        self.level_0 = self.black
        self.level_1 = (self.black - self.ultrablack) / 4
        self.matrix = zeros((4 * 52 + 1, 80 + 1))
        self.levels = []
        self.pulseheights = []
        self.cols = []
        self.rows = []
        self.get_levels()
        self.adapt_pulseheight()
        self.get_addresses()

    def translate_level(self, level):
        y = level - self.level_0
        y += self.level_s
        return y / self.level_1 + 1 if self.level_1 else 0

    def adapt_pulseheight(self):
        min = self.pulseheights[0][0]
        max = self.pulseheights[0][0]
        for i in range(self.planes):
            for j in range(len(self.pulseheights[i])):
                if min > self.pulseheights[i][j]:
                    min = self.pulseheights[i][j]
                if max < self.pulseheights[i][j]:
                    max = self.pulseheights[i][j]
        print min, max
        for i in range(self.planes):
            for j in range(len(self.pulseheights[i])):
                self.pulseheights[i][j] = int((self.pulseheights[i][j]  + abs(min))/float(max + abs(min)) * 100)

    def get_b_ub(self):
        ct = 0
        for i in range(len(line)):
            if line[i] < -170:
                self.ultrablack += line[i]
                self.black += line[i + 1]
                ct += 1
        self.ultrablack /= ct
        self.black /= ct
        self.planes = ct

    def get_levels(self):
        ct = 0
        for i in range(len(line)):
            if line[i] < -170:
                self.levels.append([])
                self.pulseheights.append([])
                self.cols.append([])
                self.rows.append([])
                a = 1
                while line[a + i + 2] > -170 and a + i + 3 < len(line):
                    level = int(line[i + 2 + a])
                    if a % 6 != 0:
                        self.levels[ct].append(self.translate_level(level))
                    if a % 6 == 0:
                        self.pulseheights[ct].append(level)
                    a += 1
                ct += 1
    
    def get_addresses(self):
        for j in range(self.planes):
            for k in range(0, len(self.levels[j]) / 5 * 5, 5):
                i = k/5
                if self.levels[j][i * 5 + 4] % 2 != 0:
                    col = self.levels[j][i * 5] * 2 * 6 + self.levels[j][i * 5 + 1] * 2 * 1 + 1
                else:
                    col = self.levels[j][i * 5] * 2 * 6 + self.levels[j][i * 5 + 1] * 2 * 1
                if self.levels[j][i * 5 + 4] < 2:
                    row = 80 - self.levels[j][i * 5 + 2] * 3 * 6 + self.levels[j][i * 5 + 3] * 3 * 1
                elif self.levels[j][i * 5 + 4] < 4:
                    row = 80 - self.levels[j][i * 5 + 2] * 3 * 6 + self.levels[j][i * 5 + 3] * 3 * 1 + 1
                else:
                    row = 80 - self.levels[j][i * 5 + 2] * 3 * 6 + self.levels[j][i * 5 + 3] * 3 * 1 + 2
                self.cols[j].append(col)
                self.rows[j].append(row)
                self.matrix[col + 1 + 52 * j][row + 1] += self.pulseheights[j][i]


xx = SingleEvent()

th2 = create_th2(xx.matrix, 0, 4 * 52 + 1, 0, 81, 'bla', 'pixels x', 'pixels y', 'bla')
th2.Draw("COLZ")

raw_input()
