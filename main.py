from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import draw
import os 

file_name = 'tourset'

class InterfaceApp(App):

    def build(self):
    	root_folder = os.path.dirname(os.path.realpath(__file__))
    	root = Interface()
    	root.setDir(root_folder)
    	return root
"""
class Interface(Widget):
	def __init__(self, **kwargs):
		super(Interface, self).__init__(**kwargs)
		self.params = Parameters()
		self.cols = 2
		self.add_widget(self.params)

class Parameters(GridLayout):
	def __init__(self, **kwargs):
		super(Parameters, self).__init__(**kwargs)
		self.cols = 2
		self.add_widget(Label(text = 'PARAMETERS', font_size = 30))
		self.add_widget(Label())
		self.add_widget(Label(text = 'DELTA', font_size = 25))
		self.idelta = TextInput(text = '0.2 or 0.3', multiline = False)
		self.add_widget(self.idelta)
		self.idata = TextInput(text = 'num < 5', multiline = False)
		self.add_widget(Label(text = 'DATA SIZE', font_size = 25))
		self.add_widget(self.idata)
"""
class Interface(Widget):
	program = draw.draw()
	param = ObjectProperty(None)
	cur_type = None
	folder = StringProperty('C:/')

	def setDir(self, folder):
		self.folder = folder
		print(self.folder)

	def runData(self, delta, dataSize):
		self.program.reset()
		self.param.status.text = 'STATUS: COMPILNG'
		for i in range(int(dataSize)):
			self.program.new(file_name + str(i + 1), delta)
			self.program.run(i + 1, delta)
		self.param.status.text = 'STATUS: RESULTS COMPILED'

	def saveDialog(self, t):
		self.cur_type = t
		content = SaveFiles(save=self.save, cancel=self.dismiss)
		self.popup = Popup(title = 'Save File')
		content.fileviewer.path = self.folder
		self.popup.content = content
		self.popup.save_hint = (0.9, 0.9)
		self.popup.open()

	def save(self, name, directory):
		self.program.write(self.cur_type, name, directory)
		self.cur_type = None
		self.dismiss()

	def dismiss(self):
		self.popup.dismiss()

class SaveFiles(FloatLayout):
	save = ObjectProperty(None)
	cancel = ObjectProperty(None)
	file_name = ObjectProperty(None)
	fileviewer = ObjectProperty(None)

if __name__ == '__main__':
    InterfaceApp().run()
    