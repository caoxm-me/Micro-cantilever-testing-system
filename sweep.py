#！ /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Cao Xiumian

from ui_sweep import sweep_ui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QTimer
import sys
import numpy as np
import time
import array 

class sweep(QWidget, sweep_ui):
	def __init__(self):
		super(sweep, self).__init__()

		# 该类继承了sweep_ui界面类，因此可以直接调用ui初始化方法
		self.setup_ui(self)

		self.button_init()

		self.edit_init()

	def button_init(self):
		self.plot_button.clicked.connect(self.sweep_setup)

	def edit_init(self):
		print("ok")
		self.edit1.setPlaceholderText('KHz')
		self.edit2.setPlaceholderText('KHz')
		self.edit3.setPlaceholderText('个')

	def sweep_setup(self):
		# 读取QLineEdit控件的文本内容
		edit1_content = self.edit1.displayText()
		edit2_content = self.edit2.displayText()
		edit3_content = self.edit3.displayText()
		# 判断是否输入
		if edit1_content == '' or edit2_content == '' or edit3_content == '':
			# 弹出警告
			QMessageBox.warning(self, '输入错误', '请输入完整的信息后再执行扫频')
		else:
			start_freq_tmp = float(edit1_content)
			self.start_freq = int(start_freq_tmp * 1000)
			stop_freq_tmp = float(edit2_content)
			self.stop_freq = int(stop_freq_tmp * 1000)
			self.sweep_points = int(edit3_content)

			if self.start_freq >= self.stop_freq:
				tmp = self.start_freq
				self.start_freq = self.stop_freq
				self.stop_freq = tmp
				
			# 生成扫频序列
			self.freq_list = np.linspace(self.start_freq, self.stop_freq, self.sweep_points)

			# 此处的定时器一定要定义为类成员(self限定)，否则函数结束后定时器会随着函数栈的回收而消失
			self.timer = QTimer()
			# 设置定时器的溢出信号对应的槽函数
			self.timer.timeout.connect(self.plotData)
			# 开启定时器
			self.timer.start(1)
			# 调试信息
			print('timer on')


	def plotData(self):
		print('run')

		current_freq = self.freq_list[self.count]

		self.device.set_freq(current_freq)
		# print(current_freq)
		time.sleep(0.1)

		tmp_r = float(self.device.get_all().split(',')[2])
		self.data_r.insert(self.count, tmp_r)
		self.data_f.insert(self.count, current_freq)

		self.count = self.count + 1
		# 调试信息
		print('*************************************************')
		print(self.data_r)
		print(self.data_f)
		print('*************************************************')
		self.plot_data.setData(self.data_f, self.data_r)

		if current_freq == self.stop_freq:
			self.count = 0
			self.plot_data.clear()
			self.data_r = array.array('d')
			self.data_f = array.array('d')
			time.sleep(3)



# 测试代码
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = sweep()
	window.show()
	sys.exit(app.exec_())