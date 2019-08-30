#！ /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Cao Xiumian

import sys
import random
import numpy as np
import pyqtgraph as pg
import array
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QTimer
from driver import device

class sweep_ui(object):
	# 界面构建函数，由于这个类是ui类，本着界面和逻辑分离的原则，该类不需要实例化
	# 我们不必给一个不需要实例化的类手动创建构造函数__init__()
	# arg1:self    指向调用该方法的对象本身
	# arg2:Form    调用该方法是传进来的窗口引用
	def setup_ui(self, Form):
		# 父类的构造方法是在子类构造方法中调用的，此处不应该出现 super(sweep_ui, self).__init__()
		Form.setWindowTitle("SR830 扫频")
		# 调整窗体大小
		Form.resize(1250, 700)
		Form.move(20, 20)

		# 实例化仪器类
		self.device = device()
		# print(self.device)

		# pyqtgraph的全局设置
		pg.setConfigOptions(leftButtonPan=False)
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')

		# 设置起止频率，扫描点数的控件
		self.start_label = QLabel('开始频率', self)
		self.edit1 = QLineEdit(self)
		self.stop_label = QLabel('终止频率', self)
		self.edit2 = QLineEdit(self)
		self.point_label = QLabel('扫描点数', self)
		self.edit3 = QLineEdit(self)

		# 绘图控件
		self.plot_widget = pg.PlotWidget(self)
		self.plot_widget.setLabels(left='amplitude/V', bottom='frequency/Hz', title='幅频响应曲线')
		self.plot_data = self.plot_widget.plot(pen=pg.mkPen(color='b', width=2), symbol='o')


		# 开始扫频按钮
		self.plot_button = QPushButton('开始', self)

		# 创建布局控件
		self.h_layout1 = QHBoxLayout()
		self.h_layout2 = QHBoxLayout()
		self.h_layout3 = QHBoxLayout()
		self.all_layout = QVBoxLayout()

		# 调用布局初始化方法，初始化界面布局
		self.layout_init()
		

		self.count = 0

		self.data_r = array.array('d')
		self.data_f = array.array('d')

	def layout_init(self):
		self.h_layout1.addWidget(self.start_label)
		self.h_layout1.addWidget(self.edit1)
		self.h_layout2.addWidget(self.stop_label)
		self.h_layout2.addWidget(self.edit2)
		self.h_layout3.addWidget(self.point_label)
		self.h_layout3.addWidget(self.edit3)

	
		self.all_layout.addWidget(self.plot_widget)	
		self.all_layout.addLayout(self.h_layout1)
		self.all_layout.addLayout(self.h_layout2)
		self.all_layout.addLayout(self.h_layout3)
		self.all_layout.addWidget(self.plot_button)


		self.setLayout(self.all_layout)

	
		

# 测试代码
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = sweep_ui()
	window.show()
	sys.exit(app.exec_())