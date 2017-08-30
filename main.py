import pyttsx, os, threading
import kivy
kivy.require("1.9.0")
from kivy.app import App
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

selected_file=''
rate=120
engine=pyttsx.init()
voices=engine.getProperty('voices')
voice=voices[1].id
read_pos=0

class Home(Screen):
	def __init__(self, **kwargs):
		super(Home,self).__init__(**kwargs)

		select_layout=GridLayout(size_hint=(1,1),cols=1, orientation='vertical')
		box=BoxLayout(orientation='horizontal', size_hint=(1,.9))
		self.file=FileChooserListView(path='C:\Users\defi\Desktop', filters=['*.txt','*.py','*.kv'])
		box.add_widget(self.file)
		select_layout.add_widget(box)
		box=BoxLayout(orientation='horizontal', size_hint=(1,.1))
		select_but=Button(text='Select', size_hint=(.5,1))
		select_but.bind(on_release=self.file_select)
		box.add_widget(select_but)
		cancel_but=Button(text='Cancel', size_hint=(.5,1))
		cancel_but.bind(on_release=self.cancel_select_file)
		box.add_widget(cancel_but)
		select_layout.add_widget(box)
		self.popup=Popup(title='Select File', content=select_layout, size_hint=(.89,.9))

	def on_pre_leave(self):
		self.manager.transition.direction='left'

	def select_file(self):
		self.popup.open()

	def cancel_select_file(self, instance):
		self.popup.dismiss()

	def file_select(self, instance):
		global selected_file
		selected_file=self.file.selection[0]
		self.ids.selected_file_lbl.text=selected_file
		self.popup.dismiss()

	def Play(self):
		try:
			self.reading_thread=threading.Thread(target=self.read_file, args=())
			self.reading_thread.start()
			play_but=self.ids.play_btn
			pause_but=self.ids.pause_btn
			stop_but=self.ids.stop_btn
			play_but.disabled=True
			pause_but.disabled=False
			stop_but.disabled=False
			play_but.text='Playing'
		except:
			self.ids.selected_file_lbl.text='We are Sorry, Cant Play'


	def Pause(self):
		pass

	def Stop(self):
		pass

	def say(self,text):
		global rate
		global voice
		global engine
		engine.setProperty('voice',voice)
		engine.setProperty('rate',rate)
		try:	
			engine.say(text)
			engine.runAndWait()
		except:
			pass


	def read_file(self):
		global engine
		global selected_file
		try:
			reading_file=open(selected_file, 'rb')
			text=reading_file.read()
			text_list=(text.split('\r\n\r'))
			for statement in text_list:
				self.ids.content_lbl.text=statement
				self.say(statement)
		
		except:
			text="No File is Selected"
			self.ids.selected_file_lbl.text=text
			self.say(text)
			
		play_but=self.ids.play_btn
		pause_but=self.ids.pause_btn
		stop_but=self.ids.stop_btn
		play_but.text='Play'
		pause_but.disabled=True
		stop_but.disabled=True
		play_but.disabled=False


class Settings(Screen):
	def __init__(self, **kwargs):
		super(Settings, self).__init__(**kwargs)

	def on_pre_leave(self):
		self.manager.transition.direction='right'

	def set_voice(self,gender):
		global voices
		global voice
		if(gender=='Female'):
			voice=voices[1].id
			self.ids.female_voice.background_color=(.09,.6,.08,1)
			self.ids.male_voice.background_color=(.6,.08,.08,1)
		else:
			voice=voices[0].id
			self.ids.male_voice.background_color=(.09,.6,.08,1)
			self.ids.female_voice.background_color=(.6,.08,.08,1)

	def set_rate(self,value):
		global rate
		rate=value


class MyManager(ScreenManager):
	def __init__(self,**kwargs):
		global voices
		super(MyManager, self).__init__(**kwargs)
		self.add_widget(Home(name='home',))
		self.add_widget(Settings(name='settings',))
		self.transition=SlideTransition()
		self.transition.duration=.35
		self.current='home'


class ReaderApp(App):
	def build(self):
		return MyManager()


if __name__=='__main__':
	app=ReaderApp()
	app.run()