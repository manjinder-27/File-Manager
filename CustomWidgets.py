from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

class CustomInputField(MDFloatLayout):
	hint = StringProperty("")
	title = StringProperty("")
	btnText = StringProperty("")
	
	def cancel(self):
		self.parent.parent.parent.dismiss()
	
	def create(self):
		filename = self.ids.field.text
		if len(filename) > 0:
			app = MDApp.get_running_app()
			if self.title == "New Folder":
				app.wm.get_screen('explorersc').createNewFolder(filename)
			else:
				app.wm.get_screen('explorersc').renameFile(self.hint,filename)
		else:
			toast("Name can't be Empty ! ")


class RightCheckBox(IRightBodyTouch,MDCheckbox):
	pass