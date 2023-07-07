from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem , IconLeftWidgetWithoutTouch
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDCustomBottomSheet
import shutil
import os

from CustomWidgets import CustomInputField,RightCheckBox

class ExplorerScreen(MDScreen):
	
	def unselectAll(self):
		self.ids.appbar.left_action_items = [['content-paste',lambda x:self.pasteContent()]]
		self.ids.appbar.right_action_items = [['folder-plus',lambda x:self.getNewFolderName()]]
		nameList = self.currentPath.split("/")
		folder = nameList[len(nameList)-2]
		if folder == "0":
			self.ids.appbar.title = "Internal Storage"
		else:
			self.ids.appbar.title = folder
		self.initScreen(self.currentPath)
	
	def deleteSelected(self):
		for i in self.selectedList:
			if os.path.isdir(i):
				shutil.rmtree(i)
			else:
				os.remove(i)
		toast("Selected Files Deleted ! ")
		self.unselectAll()
	
	def cutSelected(self):
		for i in self.selectedList:
			self.cutContent.append(i)
		toast("Selected Files Copied ! ")
		self.unselectAll()
	
	def copySelected(self):
		for i in self.selectedList:
			self.copiedContent.append(i)
		toast("Selected Files Copied ! ")
		self.unselectAll()
	
	def renameFile(self,old,new):
		old = self.currentPath + old
		new = self.currentPath + new
		os.rename(old,new)
		self.sheet1.dismiss()
		toast("File Renamed ! ")
		self.unselectAll()
	
	def renameSelected(self):
		nameList = self.selectedList[0].split("/")
		filename = nameList[len(nameList)-1]
		self.sheet1 = MDCustomBottomSheet(screen=CustomInputField(title="Rename",hint=filename,btnText="[b]UPDATE[/b]"))
		self.sheet1.open()
	
	def pasteContent(self):
		if len(self.cutContent) != 0:
			for i in self.cutContent:
				filename = i.split("/")[len(i.split("/")) - 1]
				if os.path.exists(self.currentPath+filename):
					toast(filename+" already Exists ! ")
				else:
					os.rename(i,self.currentPath+filename)
			toast("Files Pasted Here ! ")
			self.cutContent = []
			self.initScreen(self.currentPath)
		elif len(self.copiedContent) != 0:
			for i in self.copiedContent:
				filename = i.split("/")[len(i.split("/")) - 1]
				if os.path.exists(self.currentPath+filename):
					toast(filename+" already Exists ! ")
				else:
					if os.path.isdir(i):
						shutil.copytree(i,self.currentPath+filename)
					else:
						shutil.copyfile(i,self.currentPath+filename)
			toast("Files Pasted Here ! ")
			self.copiedContent = []
			self.initScreen(self.currentPath)
		else:
			toast("Nothing to Paste ! ")
	
	def checkboxActive(self,instance):
		if instance.active:
			self.selectedList.append(self.currentPath+instance.parent.parent.text)
			self.ids.appbar.title = str(len(self.selectedList)) + " Selected"
			if len(self.selectedList) == 1:
				self.ids.appbar.left_action_items = []
				self.ids.appbar.right_action_items = [['delete-outline',lambda x:self.deleteSelected()],['content-cut',lambda x:self.cutSelected()],['content-copy',lambda x:self.copySelected()],['rename-box',lambda x:self.renameSelected()]]
			elif len(self.selectedList) == 2:
				self.ids.appbar.right_action_items = [['delete-outline',lambda x:self.deleteSelected()],['content-cut',lambda x:self.cutSelected()],['content-copy',lambda x:self.copySelected()]]
		else:
			self.selectedList.remove(self.currentPath+instance.parent.parent.text)
			if len(self.selectedList) == 1:
				self.ids.appbar.right_action_items = [['delete-outline',lambda x:self.deleteSelected()],['content-cut',lambda x:self.cutSelected()],['content-copy',lambda x:self.copySelected()],['rename-box',lambda x:self.renameSelected()]]
			if len(self.selectedList) > 0:
				self.ids.appbar.title = str(len(self.selectedList)) + " Selected"
			else:
				self.unselectAll()
	
	def getNewFolderName(self):
		self.sheet = MDCustomBottomSheet(screen=CustomInputField(title="New Folder",hint="Folder Name",btnText="[b]CREATE[/b]"))
		self.sheet.open()
	
	def createNewFolder(self,filename):
		file = self.currentPath + filename
		try:
			os.mkdir(file)
			self.sheet.dismiss()
			wid = OneLineAvatarIconListItem(text=filename,on_release=self.listItemClicked)
			wid.add_widget(RightCheckBox(on_release=self.checkboxActive))
			wid.add_widget(IconLeftWidgetWithoutTouch(icon="folder-outline"))
			self.ids.explorer_list.add_widget(wid)
		except PermissionError:
			toast("No Permission to create Folder here !")
	
	def openFile(self,path):
		ext = self.getFileExtension(path)
		filename = path.split("/")[len(path.split("/")) - 1]
		if ext in ["jpg","png","jpeg"]:
			self.manager.get_screen("imageview").initScreen(filename,path)
		else:
			toast("File Type Not Supported ! ")
		
	def listItemClicked(self,instance):
		path = self.currentPath + instance.text
		if os.path.isdir(path):
			self.ids.appbar.title = instance.text
			self.initScreen(path)
		else:
			self.openFile(path)
	
	def getFileExtension(self,path):
		filenamelist = path.split(".")
		ext = filenamelist[len(filenamelist)-1]
		return ext
	
	def getFileIcon(self,path):
		ext = self.getFileExtension(path)
		if ext == "mp3":
			return "music"
		elif ext == "mp4":
			return "movie"
		elif ext in ["jpg","png","jpeg"]:
			return "image"
		elif ext == "py":
			return "language-python"
		elif ext == "c":
			return "language-c"
		elif ext == "cpp":
			return "language-cpp"
		elif ext == "js":
			return "language-javascript"
		elif ext == "java":
			return "language-java"
		elif ext == "html":
			return "language-html5"
		elif ext == "css":
			return "language-css"
		elif ext == "cs":
			return "language-csharp"
		else:
			return "file-outline"
	
	def initScreen(self,path):
		try:
			self.selectedList = []
			if not path.endswith("/"):
				path += "/"
			self.ids.explorer_list.clear_widgets()
			filesList = os.listdir(path)
			filesList.sort()
			for file in filesList:
				if os.path.isdir(path+file):
					ico  = IconLeftWidgetWithoutTouch(icon="folder-outline")
				else:
					ico = IconLeftWidgetWithoutTouch(icon=self.getFileIcon(path+file))
				wid = OneLineAvatarIconListItem(text=file,on_release=self.listItemClicked)
				wid.add_widget(RightCheckBox(on_release=self.checkboxActive))
				wid.add_widget(ico)
				self.ids.explorer_list.add_widget(wid)
			self.currentPath = path
		except PermissionError:
			toast("No Permission to access this location ! ")
			self.initScreen(self.currentPath)
	
	def initExplorerList(self,homepath):
		self.homePath = homepath
		self.copiedContent = []
		self.cutContent = []
		self.ids.appbar.title = "Internal Storage"
		self.manager.current = "explorersc"
		self.manager.transition.direction = "left"
		self.initScreen(self.homePath)
	
	def goUp(self):
		if self.currentPath == self.homePath:
			self.manager.current = "homesc"
			self.manager.transition.direction = "right"
		else:
			tree = self.currentPath.split("/")
			tree = tree[:-2]
			if tree[len(tree)-1] == "0":
				self.ids.appbar.title = "Internal Storage"
			else:
				self.ids.appbar.title = tree[len(tree)-1]
			path = ""
			for i in tree:
				path += i + "/"
			self.initScreen(path)