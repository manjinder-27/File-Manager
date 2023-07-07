from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
import os


#including local python files
import HomeScreen
import ExplorerScreen
import ImageViewer

#path to kvs folder
KVSPATH = os.getcwd()+"/kvs/"
#loading all kv files from kvs folder
for kvFile in os.listdir(KVSPATH):
	Builder.load_file(KVSPATH+kvFile)


#binding all screens to kivy screenmanager
kvCode = """
ScreenManager:
	HomeScreen:
	ExplorerScreen:
	ImageViewer:

"""


class MainApp(MDApp):
	def build(self):
		Window.softinput_mode = "below_target"
		self.theme_cls.material_style = "M3"
		self.wm = Builder.load_string(kvCode)
		return self.wm
	
	def on_start(self):
		self.wm.get_screen('homesc').initHomeScreen()


if __name__ == "__main__":
	MainApp().run()