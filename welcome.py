from kivy.app import App


# from kivy.uix.pagelayout import PageLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
# from kivy.uix.scatter import Scatter
# from kivy.uix.popup import Popup
# from kivy.factory import Factory
# from kivy.properties import ObjectProperty

from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock



from threading import Thread
from multiprocessing import Process, Queue
from time import sleep
import os

import sys
sys.path.insert(0, './../')
import pre_works_train as phase1





class splashClass(FloatLayout):
	"""docstring for splashClass"""
	def callSecondScreen(self, *args):
		self.clear_widgets()
		self.add_widget( secondClass())


	def secondSplash(self,  *args):
		self.clear_widgets()
		label = Label(text="Coloriser", font_size=80, color=[1,1,1,0])
		self.add_widget(label)
		def hide_label(w): 
		 	w.hidden = True
		Animation(color=[1,1,1,1], duration=3, t='in_out_cubic').start(label)
		Clock.schedule_once(self.callSecondScreen, 4)

	def __init__(self, **kwargs):
		super(splashClass, self).__init__(**kwargs)

		# Splash Screen
		wing = Image(source='./splash.png',pos=(800,800))
		animation = Animation(x=0, y=0, d=2, t='out_bounce');
		animation.start(wing)

		Clock.schedule_once(self.secondSplash, 5)
		self.add_widget(wing)
		return 

class secondClass(BoxLayout):
	path = './dataset/train'
	def __init__(self, **kwargs):
		# self.path = './dataset/train'
		super(secondClass, self).__init__(**kwargs)


	def pathset(self):
		self.path = self.ids.pathInput.text
		print("New PATH: ",self.path)

	def sublu(self,	queue ):
		# pid=os.fork()
		# if pid:
		phase1.begin_threaded_execution(queue, self.path)


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
		return splashClass()

if __name__ == '__main__':
	ColoriserGUIApp().run()

