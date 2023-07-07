from kivymd.uix.screen import MDScreen

class ImageViewer(MDScreen):
	def initScreen(self,name,path):
		self.ids.appbar.title = name
		self.ids.img.source = path
		self.manager.current = "imageview"
		self.manager.transition.direction = "left"
	
	def goBack(self):
		self.manager.current = "explorersc"
		self.manager.transition.direction = "right"