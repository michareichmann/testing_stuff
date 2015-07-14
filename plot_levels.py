__author__ = 'micha'

from array import array
from ROOT import TCanvas, TGraph, TMultiGraph, TLegend, gPad
import ROOT

def make_graph(data_x, data_y, name, x_title="clk", y_title='lvl'):
    x = array('d', data_x)
    y = array('d', data_y)
    gr = TGraph(len(data_x), x, y)
    gr.SetTitle(name)
    gr.SetMarkerColor(2)
    gr.SetMarkerSize(0.5)
    gr.SetMarkerStyle(20)
    gr.GetXaxis().SetTitle(x_title)
    gr.GetYaxis().SetTitle(y_title)
    gr.GetYaxis().SetTitleOffset(1.4)
    gr.SetDrawOption('ALP')
    gr.SetLineWidth(2)
    return gr

f = open('levels.txt', 'r')
levels = []
ind = 0
skip = []
lines = 0
for line in f:
    lines += 1
f.seek(0)
for line in f:
    levels.append([])
    ii = 0
    for i in line.split():
        if abs(float(i)) < 0.01 and ii not in skip and ind < lines - 1:
            skip.append(ii)
        if ii in skip:
            ii += 1
            continue
        ii += 1
        levels[ind].append(float(i))
    ind += 1
f.close()
print skip
print levels[0]
print levels[-1]

graphs = []
for j in range(len(levels) - 1):
    graphs.append(make_graph(levels[-1], levels[j], 'test'))
mg = TMultiGraph('mg', 'clock level split')
colors = [1,2,3,4,5,6]
ind = 0
leg = TLegend(0.77, 0.7, 0.88, 0.88)
for gr in graphs:
    gr.SetMarkerColor(colors[ind])
    gr.SetLineColor(colors[ind])
    leg.AddEntry(gr, str(ind) + ' -> 2 -> ' + str(ind), 'l')
    mg.Add(gr)
    ind += 1

c = TCanvas("c",'c',800,800)
c.SetGrid()
mg.Draw("apl")
mg.GetXaxis().SetTitle('clock delay')
mg.GetYaxis().SetTitle('level')
leg.Draw()
gPad.Update()
raw_input()