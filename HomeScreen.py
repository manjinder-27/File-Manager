from kivymd.uix.screen import MDScreen
from android.permissions import request_permissions,check_permission,Permission
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from jnius import autoclass
import os

class HomeScreen(MDScreen):
	
	def hasStoragePermission(self):
		BuildVersion = autoclass("android.os.Build$VERSION")
		self.SDK_INT = BuildVersion.SDK_INT
		if self.SDK_INT > 29:
			return self.Environment.isExternalStorageManager()
		else:
			return check_permission(Permission.WRITE_EXTERNAL_STORAGE)
	
	def openAccessSettings(self,instance):
		self.dialog.dismiss()
		Intent = autoclass("android.content.Intent")
		Settings = autoclass("android.provider.Settings")
		mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
		intent = Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION)
		mActivity.startActivity(intent)
	
	def getStoragePermission(self):
		if self.SDK_INT > 29:
			self.dialog = MDDialog(title="Storage Access",text="Due to Android Restrictions , File Manager needs more permissions to work properly. Choose File Manager on the next screen and grant storage access permission.",buttons =[MDRaisedButton(text="OK",on_release=self.openAccessSettings)])
			self.dialog.open()
		else:
			request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
	
	def initHomeScreen(self):
		self.Environment = autoclass("android.os.Environment")
		StatFs = autoclass("android.os.StatFs")
		self.SPath = self.Environment.getRootDirectory()
		SStat = StatFs(self.SPath.path)
		blockSize = SStat.getBlockSizeLong()
		blockCount = SStat.getBlockCountLong()
		SAvailable = SStat.getAvailableBlocksLong()
		SAvailable = str(round((SAvailable*blockSize)/1000000000,2))+"GB"
		STotal = str(round((blockCount*blockSize)/1000000000,2))+"GB"
		self.ids.system_storage.secondary_text = SAvailable+" available out of "+STotal
		IPath = self.Environment.getDataDirectory()
		IStat = StatFs(IPath.path)
		blockSize = IStat.getBlockSizeLong()
		blockCount = IStat.getBlockCountLong()
		IAvailable = IStat.getAvailableBlocksLong()
		IAvailable = str(round((IAvailable*blockSize)/1000000000,2))+"GB"
		ITotal = str(round((blockCount*blockSize)/1000000000,2))+"GB"
		self.ids.internal_storage.secondary_text = IAvailable+" available out of "+ITotal
		EState = self.Environment.getExternalStorageState()
		if self.Environment.isExternalStorageRemovable() and EState == "mounted":
			self.EPath = self.Environment.getExternalStorageDirectory()
			EStat = StatFs(self.EPath.path)
			blockSize = EStat.getBlockSizeLong()
			blockCount = EStat.getBlockCountLong()
			EAvailable = EStat.getAvailableBlocksLong()
			EAvailable = str(round((EAvailable*blockSize)/1000000000,2))+"GB"
			ETotal = str(round((blockCount*blockSize)/1000000000,2))+"GB"
			self.ids.external_storage.secondary_text = EAvailable+" available out of "+ETotal
		else:
			self.ids.external_storage.secondary_text = "Unavailable"
			self.ids.external_storage.disabled = True
		if not self.hasStoragePermission():
			self.getStoragePermission()
	
	def openExternalStorage(self):
		if self.EPath.path.endswith("/"):
			self.manager.get_screen('explorersc').initExplorerList(self.EPath.path)
		else:
			self.manager.get_screen('explorersc').initExplorerList(self.EPath.path+"/")
	
	def openSystemStorage(self):
		if self.SPath.path.endswith("/"):
			self.manager.get_screen('explorersc').initExplorerList(self.SPath.path)
		else:
			self.manager.get_screen('explorersc').initExplorerList(self.SPath.path+"/")