#!/usr/bin/python
__author__ = 'micha'

from array import array
from ROOT import TCanvas, TGraph, TMultiGraph, TLegend, gPad, TGaxis
import ROOT
import argparse

parser = argparse.ArgumentParser(prog='plot levels', description="split graph plotter")
parser.add_argument('--file', '-f', default="default", help="The digit rectory with all required config files.")
parser.add_argument("number", nargs='?', default=1, help="number of graphs")

args = parser.parse_args()
n_rocs = int(args.number)
legends = []
lines = []
spacings = []


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
    gr.SetDrawOption('ALP')
    gr.SetLineWidth(2)
    return gr


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
    mg.GetYaxis().SetTitleOffset(1.5)
    leg.Draw()
    draw_best_clk(levels, roc)
    draw_spacings()
    legends.append(leg)
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


def find_best_level(levels, roc=0):
    spread = []
    n_levels = len(levels[0]) - 1
    for i in range(len(levels[roc][0])):
        sum_level = 0
        sum_spread = 0
        for j in range(n_levels):
            sum_level += levels[roc][j][i]
        for j in range(n_levels):
            if levels[roc][j][i] != 0:
                sum_spread += abs(sum_level / n_levels - levels[roc][j][i])
            else:
                sum_spread = 99 * n_levels
                break
        spread.append(sum_spread / n_levels)
    best_clk = 99
    min_spread = 99
    for i in range(len(spread)):
        if spread[i] < min_spread:
            min_spread = spread[i]
            best_clk = levels[roc][-1][i]
    return best_clk


def draw_best_clk(levels, roc):
        for i in range(n_rocs):
            ymin = min(min(levels[roc]))
            ymax = max(max(levels[roc]))
            x = find_best_level(levels, roc)
            a2 = TGaxis(x, ymin, x, ymax, ymin, ymax, 510, "+SU")
            tit = "best clk = " + str(int(x)) + "   "
            a2.SetTitle(tit)
            a2.SetLineColor(1)
            a2.SetTickSize(0)
            a2.SetLabelSize(0)
            a2.SetTitleSize(0.03)
            a2.SetTitleOffset(0.3)
            a2.Draw()
            lines.append(a2)

def draw_spacings():
    y = [[], []]
    mid_lvl = 2
    black = header[1] + 10
    max_lvl = (black - header[0]) / 4 * (mid_lvl - 1) + black + (black - header[0]) / 8
    min_lvl = (black - header[0]) / 4 * (mid_lvl - 1) + black - (black - header[0]) / 8
    for i in range(len(levels[0][0])):
        y[0].append(min_lvl)
        y[1].append(max_lvl)
    for i in range(2):
        spacing = make_graph(levels[0][-1], y[i], 'bla')
        spacing.Draw('l')
        spacings.append(spacing)

header = []
f = open('levels_header.txt')
header.append(int(f.readline()))
header.append(int(f.readline()))
f.close()

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
c.Update()
c.SaveAs('splits.png')

raw_input()
