#！ /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Cao Xiumian

import numpy as np 
import pyqtgraph as pg
import array
from driver import device

lockin = device()
app = pg.mkQApp()
# 数据缓存数组
data_f = array.array('d')
data_r = array.array('d')

win = pg.GraphicsWindow()
win.setWindowTitle("动态刷新的波形图表")
win.resize(500, 300)

p = win.addPlot()
p.showGrid(x=True, y=True)
p.setLabels(left='y / V', bottom='x / point', title='y = sin(x)')
p.setRange(xRange=[0, 20000], yRange=[0, 0.1])

curve = p.plot(pen='y')

lockin_data = lockin.get_all()
tmp_r = float(lockin_data.split(',')[2])
tmp_f = float(lockin.get_freq())

def plotData():
	global tmp_r
	global tmp_f
	global data_f
	global data_r

	lockin_data = lockin.get_all()

	tmp_r_old = tmp_r
	tmp_f_old = tmp_f

	tmp_r = float(lockin_data.split(',')[2])
	tmp_f = float(lockin.get_freq())

	if(tmp_f < tmp_f_old):
		curve.clear()
		data_f = array.array('d')
		data_r = array.array('d')

	data_f.append(tmp_f)
	data_r.append(tmp_r)
	curve.setData(data_f, data_r)
	

timer = pg.QtCore.QTimer()
timer.timeout.connect(plotData)
timer.start(1)
app.exec_()