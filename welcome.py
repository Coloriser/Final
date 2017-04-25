from kivy.app import App

from kivy.uix.pagelayout import PageLayout

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from threading import Thread,Event
# from multiprocessing import Process, Queue
from time import sleep
import os

# import sys
# sys.path.insert(0, './..')
import pre_works_train as phase1
import create_model as phase2
import pre_works_test as phase3
import test as phase4

import sys
sys.path.insert(0, './helper_modules')
import front_end_helper as hfg
import helper_functions as hf


class splashClass(FloatLayout):
	"""docstring for splashClass"""
	def callSecondScreen(self, *args):
		self.clear_widgets()
		self.add_widget( screenClass())
		# self.add_widget( firstClass() )


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


class firstClass(BoxLayout):
	"""docstring for firstClass"""
	def __init__(self, **kwargs):
		super(firstClass, self).__init__(**kwargs)

	def trainClick(self):
		print("YUMMY")	
		




class secondClass(Screen):
	path = './dataset/train'
	def __init__(self, **kwargs):
		# self.path = './dataset/train'
		super(secondClass, self).__init__(**kwargs)

	def pathset(self):
		self.path = self.ids.pathInput.text
		print("New PATH: ",self.path)

	def callBack(self, image_no):
		self.ids.statusBar.text = "Preprocessing of "+image_no+" images complete."
		self.ids.nextBut.disabled = False

	def updateBar(self, x):
		self.ids.progressBarIndicator.value = x
		self.ids.progressLabel.text = str(x) + '%'
		

	def sublu(self ):
		# pid=os.fork()
		# if pid:
		callBack_to_call = self.callBack
		callBack_to_update = self.updateBar
		Thread( target = phase1.begin_threaded_execution, args=(callBack_to_call, self.path, callBack_to_update)).start()

	def begin_phase_1(self):
		# queue = Queue()
		# queue.put(0)
		self.ids.progressLabel.text = "begin disco"
		self.ids.statusBar.text = "Preprocessing  .  .  ."
		self.ids.nextBut.disabled = True
		self.ids.beginButton.disabled = True		
		self.sublu()

class thirdClass( Screen ):
	"""docstring for thirdClass"""
	def __init__(self, **kwargs):
		super(thirdClass, self).__init__(**kwargs)

	def callBack(self, model_name):
		self.ids.statusBox.text = "Model " + model_name +" created"
		self.ids.a_model_but.disabled = False
		self.ids.b_model_but.disabled = False
		self.ids.nextBut.disabled = False
		self.ids.backBut.disabled = False


	def begin_phase_2a(self):
		callBack_to_call = self.callBack
		self.ids.a_model_but.disabled = True
		self.ids.b_model_but.disabled = True
		self.ids.nextBut.disabled = True
		self.ids.backBut.disabled = True
		Thread( target = phase2.make_a_model, args=((callBack_to_call),)).start()
		self.ids.statusBox.text = "Creating a_model"
		
	def begin_phase_2b(self):
		callBack_to_call = self.callBack
		self.ids.a_model_but.disabled = True
		self.ids.b_model_but.disabled = True
		self.ids.nextBut.disabled = True
		self.ids.backBut.disabled = True
		Thread( target = phase2.make_b_model, args=((callBack_to_call),)).start()
		self.ids.statusBox.text = "Creating b_model"





class fourthClass(Screen):
	path = './dataset/test'
	def __init__(self, **kwargs):
		super(fourthClass, self).__init__(**kwargs)

	def pathset(self):
		self.path = self.ids.pathInput.text
		print("New PATH: ",self.path)

	def callBack(self, image_no):
		self.ids.statusBar.text = "Preprocessing of "+image_no+" images complete."
		self.ids.nextBut.disabled = False
		self.ids.backBut.disabled = False

	def updateBar(self, x):
		self.ids.progressBarIndicator.value = x
		self.ids.progressLabel.text = str(x) + '%'
		

	def lasagu(self ):
		# pid=os.fork()
		# if pid:
		callBack_to_call = self.callBack
		callBack_to_update = self.updateBar
		Thread( target = phase3.begin_threaded_execution, args=(callBack_to_call, self.path, callBack_to_update)).start()


	def begin_phase_3(self):
		self.ids.progressLabel.text = "begin disco"
		self.ids.statusBar.text = "Preprocessing  .  .  ."
		self.ids.nextBut.disabled = True
		self.ids.backBut.disabled = True
		self.ids.beginButton.disabled = True		
		self.lasagu()


class fifthClass( Screen ):
	"""docstring for thirdClass"""
	def __init__(self, **kwargs):
		super(fifthClass, self).__init__(**kwargs)

	def callBack(self, model_name):
		self.ids.statusBox.text = "Model " + model_name +" created"
		if(model_name=='b'):
			Thread( target = phase4.start, args=('a',(callBack_to_call),)).start()
		elif model_name=='ab':
			self.ids.test_model_but.disabled = False
			# self.ids.b_model_but.disabled = False
			self.ids.nextBut.disabled = False
			self.ids.backBut.disabled = False

	def beginTest(self):
		callBack_to_call = self.callBack
		self.ids.test_model_but.disabled = False
		# self.ids.b_model_but.disabled = True
		self.ids.nextBut.disabled = True
		self.ids.backBut.disabled = True
		Thread( target = phase4.start, args=('a',(callBack_to_call),)).start()
		self.ids.statusBox.text = "Creating a_model"
		
	
class sixthClass( Screen ):
	"""docstring for thirdClass"""
	callBack_to_call = 0

	def __init__(self, **kwargs):
		super(sixthClass, self).__init__(**kwargs)
		callBack_to_call =  self.callBack
		# initialise references
		imageGray = self.ids.imageGray
		imagePredicted = self.ids.imagePredicted
		imageGround = self.ids.imageGround


		imageList = []
		imageList = hfg.getAndFilterPaths( )

		def loadImages(base_name):	
			self.ids.btn.text = base_name
			base_name = "./predicted_images/" + base_name.split('_')[0]
			imageGray.source = base_name+"_G.jpg"
			imagePredicted.source = base_name + "_A.jpg"
			imageGround.source = base_name + "_AB.jpg"


		loadImages(hfg.refineName(imageList[0]))
		
		# Name on default placeholder
		dropdownIdentifier = self.ids.dropdown	


		def changeName(instance):
			base_name = instance.text
			loadImages(base_name)

		for eachImage in imageList:
			name = hfg.refineName(eachImage)
			dropdownButton = Button(text=name, height='48dp', size_hint_y=None)
			dropdownButton.bind(on_release=changeName)
			dropdownIdentifier.add_widget(dropdownButton)


		# for i in range(1,5):
		# 	src = "http://placehold.it/480x270.png&text=slide-%d&.png" % i
		# 	#load images asynchronously
		# 	image = Factory.AsyncImage(source=src, allow_stretch=True)
		# 	# self.ids.carousel.add_widget(image)
		



	def callBack(self, model_name):
		# self.ids.statusBox.text = "Model " + model_name +" created"
		if(model_name=='b'):
			Thread( target = phase4.start, args=('a',(callBack_to_call),)).start()
		elif model_name=='ab':
			self.ids.test_model_but.disabled = False
			# self.ids.b_model_but.disabled = False
			self.ids.nextBut.disabled = False
			self.ids.backBut.disabled = False


class screenClass(ScreenManager):
	"""docstring for screenClass"""
	def __init__(self, **kwargs):
		super(screenClass, self).__init__(**kwargs)
		self.transition=SlideTransition()
		screen1 = secondClass(name='second_screen')
		screen2 = thirdClass(name='third_screen')
		screen3 = fourthClass(name='fourth_screen')
		screen4 = fifthClass(name='fifth_screen')
		screen5 = sixthClass(name='sixth_screen')
		self.add_widget(screen1)
		self.add_widget(screen2)
		self.add_widget(screen3)
		self.add_widget(screen4)
		self.add_widget(screen5)




class ColoriserGUIApp(App):
	def build(self):
		return splashClass()
		# return secondClass()
		# return thirdClass()
		# return firstClass()
		# return screenClass()
		# return fifthClass()
		# return sixthClass()

if __name__ == '__main__':
	ColoriserGUIApp().run()

