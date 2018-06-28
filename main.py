from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import draw
import os 

file_name = 'tourset'

class InterfaceApp(App):

    def build(self):
    	return Interface()

class Parameters(GridLayout):
	status = ObjectProperty(None)
	inputdelta = ObjectProperty(None)

class SaveFiles(FloatLayout):
	save = ObjectProperty(None)
	cancel = ObjectProperty(None)
	file_name = ObjectProperty(None)
	fileviewer = ObjectProperty(None)

class DropDownSelection(DropDown):
	def __init___(self, **kwargs):
		super(DropDownSelection, self).__init__(**kwargs)
		self.mainButton = ObjectProperty(None)
	
	def select(self, button):
		self.mainButton.text = button.text
		self.dismiss()

	def main(self, button):
		self.mainButton = button
		self.mainButton.bind(on_release = self.open)

class Interface(Widget):
	def __init__(self, **kwargs):
		super(Interface, self).__init__(**kwargs)
		self.program = draw.draw()
		self.cur_type = None
		self.folder = os.path.dirname(os.path.realpath(__file__))
		self.dropdown = DropDownSelection()
		self.dropdown.main(self.param.inputdelta)

		self.validDelta = ['0.2', '0.3']
		self.maxDataSize = 5
		self.hasData = False

	def setDir(self, folder):
		self.folder = folder
		print(self.folder)

	def checkValid(self, delta, dataSize):
		valid = True
		if delta not in self.validDelta:
			valid = False
		elif int(dataSize) > self.maxDataSize:
			valid = False
		return valid

	def runData(self, delta, dataSize):
		self.program.reset(delta)
		if (self.checkValid(delta, dataSize)):
			self.param.status.text = 'STATUS: COMPILNG'
			for i in range(int(dataSize)):
				self.program.new(file_name + str(i + 1), delta)
				self.program.run(i + 1, delta)
			self.param.status.text = 'STATUS: RESULTS COMPILED'
			self.hasData = True
		else:
			self.param.status.text = 'STATUS: NOT VALID PARAMETERS'

	def saveDialog(self, t):
		if (not self.hasData):
			self.param.status.text = 'STATUS: NOT COMPILED'
			return
		self.cur_type = t
		content = SaveFiles(save=self.save, cancel=self.dismiss)
		self.popup = Popup(title = 'Save File')
		content.fileviewer.path = self.folder
		self.popup.content = content
		self.popup.save_hint = (0.9, 0.9)
		self.popup.open()

	def save(self, name, directory):
		try:
			self.program.write(self.cur_type, name, directory)
		except PermissionError:
			self.param.status.text = 'STATUS: FILE ERROR'
		self.cur_type = None
		self.dismiss()

	def dismiss(self):
		self.popup.dismiss()

if __name__ == '__main__':
    InterfaceApp().run()
    