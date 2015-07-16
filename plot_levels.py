#!/usr/bin/python
__author__ = 'micha'

from array import array
from ROOT import TCanvas, TGraph, TMultiGraph, TLegend, gPad
import ROOT
import argparse

parser = argparse.ArgumentParser(prog='plot levels', description="split graph plotter")
parser.add_argument('--file', '-f', default="default", help="The digit rectory with all required config files.")
parser.add_argument("number", nargs='?', default=1, help="number of graphs")

args = parser.parse_args()
n_rocs = int(args.number)

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

test = []

def plot_graph(roc):
    graphs = []
    for j in range(len(levels[roc]) - 1):
        graphs.append(make_graph(levels[roc][-1], levels[roc][j], 'test'))
    mg = TMultiGraph('mg', 'clock level split roc ' + str(roc))
    colors = [1, 2, 3, 4, 5, 6]
    ind = 0
    leg = TLegend(0.77, 0.7, 0.88, 0.88)
    for gra in graphs:
        gra.SetMarkerColor(colors[ind])
        gra.SetLineColor(colors[ind])
        leg.AddEntry(gra, str(ind) + ' -> 2 -> ' + str(ind), 'l')
        mg.Add(gra)
        ind += 1
    mg.Draw("apl")
    mg.GetXaxis().SetTitle('clock delay')
    mg.GetYaxis().SetTitle('level')
    leg.Draw()
    test.append(leg)
    gPad.Update()
    return mg

def read_file(name):
    f = open(name, 'r')
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
    return levels

levels = []
if args.file != 'default':
    levels.append([])
    levels[0] = read_file(args.file)
else:
    for roc in range(n_rocs):
        levels.append([])
        file_name = 'levels_roc' + str(roc) + '.txt'
        levels[roc] = read_file(file_name)


mg = []
c = TCanvas("c", 'c', 800 * n_rocs, 800)
c.SetGrid()
c.Divide(n_rocs, 1)
for i in range(n_rocs):
    c.cd(i + 1)
    mg.append(plot_graph(i))
c.SaveAs('splits.png')

raw_input()
