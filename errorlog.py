__author__ = 'micha'

from numpy import zeros
from ROOT import TH2F, TCanvas, TPad
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('log', nargs='?', default="log")
args = parser.parse_args()


f = open(args.log, 'r')
line = f.readline().split()
f.close()
for l in range(len(line)):
    line[l] = int(line[l])


class SingleEvent:
    """show hitmaps of single events"""

    def __init__(self):
        self.info = line
        self.ultrablack = 0
        self.black = 0
        self.planes = 0
        self.pixel_hits = 0
        self.get_b_ub()
        self.level_s = (self.black - self.ultrablack) / 8
        self.level_0 = self.black
        self.level_1 = (self.black - self.ultrablack) / 4
        self.levels = []
        self.pulseheights = []
        self.cols = []
        self.rows = []
        self.data = []
        self.get_levels()
        self.normalise_pulseheight()
        self.get_addresses()

    def translate_level(self, level):
        y = level - self.level_0
        y += self.level_s
        return y / self.level_1 + 1 if self.level_1 else 0

    def normalise_pulseheight(self):
        min_ph = self.pulseheights[0][0]
        max_ph = self.pulseheights[0][0]
        for i in range(self.planes):
            for j in range(len(self.pulseheights[i])):
                if min_ph > self.pulseheights[i][j]:
                    min_ph = self.pulseheights[i][j]
                if max_ph < self.pulseheights[i][j]:
                    max_ph = self.pulseheights[i][j]
        for i in range(self.planes):
            for j in range(len(self.pulseheights[i])):
                self.pulseheights[i][j] = int((self.pulseheights[i][j] + abs(min_ph))/float(max_ph + abs(min_ph)) * 100)

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
                while line[a + i + 2] > -170 and a + i + 4 < len(line):
                    level = int(line[i + 2 + a])
                    if a % 6 != 0:
                        self.levels[ct].append(self.translate_level(level))
                    if a % 6 == 0:
                        self.pulseheights[ct].append(level)
                    a += 1
                ct += 1
    
    def get_addresses(self):
        for j in range(self.planes):
            self.data.append([])
            self.data[j] = zeros((53, 81))
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
                self.data[j][col + 1][row + 1] = self.pulseheights[j][i]
                self.pixel_hits +=1



class DrawHisto(SingleEvent):
    def __init__(self):
        SingleEvent.__init__(self)
        self.canvas = TCanvas('c', "Single Event Hitmap", 1000, 1000)
        self.canvas.Divide(2, 2)
        self.histos = []
        self.pads = []
        self.draw_histos()

    def draw_histos(self):
        for i in range(self.planes):
            self.histos.append([])
            self.pads.append([])
            self.canvas.cd(i+1)
            name = 'ROC' + str(i)
            p = TPad('name','',0,0,1,1)
            p.SetRightMargin(0.15)
            self.pads[i].append(p)
            p.Draw()
            p.cd()
            th2 = TH2F(name, name, self.data[i].shape[0],
                       0, 53, self.data[i].shape[1], 0, 81)
            th2.SetStats(False)
            th2.SetDirectory(0)
            th2.SetMarkerSize(10)
            th2.GetXaxis().SetTitle('pixels x')
            th2.GetYaxis().SetTitle('pixels y')
            th2.GetYaxis().SetTitleOffset(1.2)
            th2.GetYaxis().CenterTitle()
            th2.GetXaxis().CenterTitle()
            th2.GetZaxis().SetTitle('pulse height')
            th2.GetZaxis().SetTitleOffset(1.2)
            th2.GetZaxis().CenterTitle()
            th2.SetDrawOption('COLZ')
            self.histos[i].append(th2)
            for ix, x in enumerate(self.data[i]):
                for iy, y in enumerate(x):
                    th2.SetBinContent(ix, iy, y)
            th2.Draw('COLZ')
            self.canvas.Update()

xx = DrawHisto()
print xx.pixel_hits, 'pixels were hit'

# histo = create_th2(xx.matrix, 0, 4 * 52 + 1, 0, 81, 'Single Event Hitmap', 'pixels x', 'pixels y', '')
# histo.Draw("COLZ")

raw_input()
