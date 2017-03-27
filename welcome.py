from kivy.app import App


# from kivy.uix.pagelayout import PageLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.popup import Popup
from kivy.factory import Factory
# from kivy.properties import ObjectProperty

from kivy.uix.progressbar import ProgressBar
from threading import Thread
from multiprocessing import Process, Queue
from time import sleep
import os

import sys
sys.path.insert(0, './../')
import pre_works_train as phase1







# class PopupBox(Popup):
# 	pop_up_text = ObjectProperty()
# 	def update_pop_up_text(self, p_message):
# 		self.pop_up_text.text = p_message


class secondClass(BoxLayout):
	path = './dataset/train'
	def __init__(self, **kwargs):
		super(secondClass, self).__init__(**kwargs)


	def pathset(self):
		self.path = self.ids.pathInput.text
		print("New PATH: ",self.path)

	def sublu(self,	queue):
		# pid=os.fork()
		# if pid:
		phase1.begin_threaded_execution(queue)


	def begin_phase_1(self):
		queue = Queue()
		queue.put(0)
		# b = BoxLayout(orientation="horizontal")
		# but = ProgressBar(max=100)
		# but.id = progressBarIndicator
		# b.add_widget(but)
		# self.add_widget(b)
		# self.pop_up = Factory.PopupBox()
		# self.pop_up.update_pop_up_text('Running some task...')
		# self.pop_up.open()
		# print("ORIG",os.getpid())
		self.ids.progressLabel.text = "begin disco"
		# pid = os.fork()
		# if not pid:
		pre_works_process = Process(target=self.sublu, args=((queue),))
		pre_works_process.daemon = True
		pre_works_process.start()
			# phase1.begin_threaded_execution(queue)
		# else:
		print("Done")
		self.ids.progressLabel.text = "awesome disco"
		while True:
			x = queue.get()
			print(x)
			self.ids.progressBarIndicator.value = x
			self.ids.progressLabel.text = str(x) + '%'
			# sleep(1)
			if x==100:
				break
		self.ids.beginButton.disabled = True		
		self.ids.statusBar.text = "Preprocessing complete. Proceed to next step?"
		b = Button(text="Next")
		self.ids.statusBox.add_widget(b)

class ColoriserGUIApp(App):


	def build(self):
		# return PreWorksTrain(orientation="vertical")
		# print("THE GREAT FATHER")
		return secondClass()

if __name__ == '__main__':
	ColoriserGUIApp().run()


# class LoginScreen(FloatLayout):

# 	def __init__(self, **kwargs):
# 		super(LoginScreen, self).__init__(**kwargs)
# 		f = FloatLayout()
# 		s = Scatter()
# 		l = Label(text = "HELLO", font_size=150)
# 		s.add_widget(l)
# 		self.add_widget(s)
# 		# Button(text = "HELLO", background_color = (0, 0, 1, 1), font_size=150)
# 		return

# class BaseScreen(PageLayout):
# 			"""docstring for BaseScreen"""
# 			def __init__(self, **kwargs):
# 				super(BaseScreen, self).__init__(**kwargs)
# 				# l = Label(text = "HELLO", font_size=150)
# 				# self.add_widget(l)