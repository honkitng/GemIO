#!/usr/bin/env python3.6

import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QLabel, QPushButton, QRadioButton, QTabWidget, QWidget, QFormLayout, QHBoxLayout, QCheckBox, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap

class micsLocation(QMainWindow):
	def __init__(self):
		super(micsLocation, self).__init__()

		self.setGeometry(200, 200, 570, 100)
		self.setWindowTitle("Settings")

		self.tabWidget = tabWidgetSetup(self)
		self.setCentralWidget(self.tabWidget)



class tabWidgetSetup(QWidget):
	def __init__(self, parent):
		super(tabWidgetSetup, self).__init__(parent)

		self.layout = QFormLayout()

		self.tabs = QTabWidget()
		self.motioncorTab = QWidget()
		self.ctfTab = QWidget()
		self.relionTab = QWidget()

		self.tabs.addTab(self.motioncorTab,"Remove with JPEG")
		self.tabs.addTab(self.ctfTab,"Remove with JPEG and CTF")
		self.tabs.addTab(self.relionTab,"Relion GUI")
		self.motioncorUI()
		self.ctfUI()
		self.relionUI()
		self.tabs.setTabEnabled(1,False)
		self.tabs.setTabEnabled(2,False)

		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)

	def motioncorUI(self):
		self.motioncorTab.layout = QFormLayout(self)

		if os.name != 'nt':
			self.tiffLabel1 = QLabel(self)
			self.tiffLabel1.setText("TIF directory:")
			self.tiffText1 = QLineEdit(self)
			self.motioncorTab.layout.addRow(self.tiffLabel1, self.tiffText1)

			self.micLabel1 = QLabel(self)
			self.micLabel1.setText("Corrected micrographs directory:")
			self.micText1 = QLineEdit(self)
			self.motioncorTab.layout.addRow(self.micLabel1, self.micText1)

		self.jpegLabel1 = QLabel(self)
		self.jpegLabel1.setText("JPEG directory:")
		self.jpegText1 = QLineEdit(self)
		self.motioncorTab.layout.addRow(self.jpegLabel1, self.jpegText1)

		self.motioncorSubmit = QPushButton(self)
		self.motioncorSubmit.setText("Submit")
		self.motioncorSubmit.clicked.connect(self.motioncorGoNext)
		self.motioncorTab.layout.addRow(self.motioncorSubmit)

		self.motioncorTab.setLayout(self.motioncorTab.layout)

	def motioncorGoNext(self):
		if os.name == 'nt':
			tabWidgetSetup.tiffDir1 = "None_Entered"
			tabWidgetSetup.micDir1 = "None_Entered"
		else:
			tabWidgetSetup.tiffDir1 = self.tiffText1.text()
			tabWidgetSetup.micDir1 = self.micText1.text()
		tabWidgetSetup.jpegDir1 = self.jpegText1.text()
		window1.hide()
		self.rmMics = removeMics(self)
		self.rmMics.show()

	def ctfUI(self):
		self.ctfTab.layout = QFormLayout(self)

		"""self.curateLabel2 = QLabel(self)
		self.curateLabel2.setText("Curate with jpeg or mrc files:")

		self.curateType2 = QHBoxLayout()

		self.curateJPEG2 = QRadioButton(self)
		self.curateJPEG2.setText("jpeg")
		self.curateJPEG2.toggled.connect(lambda:self.btnSelection2(self.curateJPEG2))
		self.curateType2.addWidget(self.curateJPEG2)

		self.curateMRC2 = QRadioButton(self)
		self.curateMRC2.setText("mrc")
		self.curateMRC2.toggled.connect(lambda:self.btnSelection2(self.curateMRC2))
		self.curateType2.addWidget(self.curateMRC2)

		self.curateType2.setAlignment(QtCore.Qt.AlignCenter)
		self.ctfTab.layout.addRow(self.curateLabel2, self.curateType2)

		self.updateLabel2 = QLabel(self)
		self.updateLabel2.setText("Update star files:")

		self.updateType2 = QHBoxLayout()

		self.updateMovies2 = QCheckBox(self)
		self.updateMovies2.setText("movies")
		self.updateMovies2.toggled.connect(lambda:self.chkSelection2(self.updateMovies2))
		self.updateType2.addWidget(self.updateMovies2)

		self.updateMics2 = QCheckBox(self)
		self.updateMics2.setText("micrographs")
		self.updateMics2.toggled.connect(lambda:self.chkSelection2(self.updateMics2))
		self.updateType2.addWidget(self.updateMics2)

		self.updateCTF2 = QCheckBox(self)
		self.updateCTF2.setText("ctf")
		self.updateCTF2.toggled.connect(lambda:self.chkSelection2(self.updateCTF2))
		self.updateType2.addWidget(self.updateCTF2)

		self.updateType2.setAlignment(QtCore.Qt.AlignCenter)
		self.ctfTab.layout.addRow(self.updateLabel2, self.updateType2)

		self.moviesLabel2 = QLabel(self)
		self.moviesLabel2.setText("Movies star file:")
		self.moviesText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.moviesLabel2, self.moviesText2)

		self.micLabel2 = QLabel(self)
		self.micLabel2.setText("Micrograph star file:")
		self.micText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.micLabel2, self.micText2)

		self.ctfLabel2 = QLabel(self)
		self.ctfLabel2.setText("CTF star file:")
		self.ctfText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.ctfLabel2, self.ctfText2)
		
		self.jpegLabel2 = QLabel(self)
		self.jpegLabel2.setText("Corrected micrographs directory:")
		self.jpegText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.jpegLabel2, self.jpegText2)

		self.jpegLabel2 = QLabel(self)
		self.jpegLabel2.setText("JPEG directory:")
		self.jpegText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.jpegLabel2, self.jpegText2)

		self.scaleLabel2 = QLabel(self)
		self.scaleLabel2.setText("Micrograph scale:")
		self.scaleText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.scaleLabel2, self.scaleText2)

		self.contrastLabel2 = QLabel(self)
		self.contrastLabel2.setText("Sigma contrast:")
		self.contrastText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.contrastLabel2, self.contrastText2)

		self.filterLabel2 = QLabel(self)
		self.filterLabel2.setText("Low pass filter (A):")
		self.filterText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.filterLabel2, self.filterText2)

		self.pixLabel2 = QLabel(self)
		self.pixLabel2.setText("Apix (A):")
		self.pixText2 = QLineEdit(self)
		self.ctfTab.layout.addRow(self.pixLabel2, self.pixText2)

		self.ctfSubmit = QPushButton(self)
		self.ctfSubmit.setText("Submit")
		self.ctfSubmit.clicked.connect(self.ctfGoNext)
		self.ctfTab.layout.addRow(self.ctfSubmit)"""

		self.ctfTab.setLayout(self.ctfTab.layout)
		"""self.curateJPEG2.setChecked(True)
		self.moviesText2.setDisabled(True)
		self.micText2.setDisabled(True)
		self.ctfText2.setDisabled(True)

	def ctfGoNext(self):
		window1.hide()
		self.rmMics = removeMics(self)
		self.rmMics.show()

	def btnSelection2(self, button):
		if button.text() == "jpeg":
			if button.isChecked() == True:
				self.jpegText2.setDisabled(False)
				self.scaleText2.setDisabled(True)
				self.contrastText2.setDisabled(True)
				self.filterText2.setDisabled(True)
				self.pixText2.setDisabled(True)
		else:
			if button.isChecked() == True:
				self.jpegText2.setDisabled(True)
				self.scaleText2.setDisabled(False)
				self.contrastText2.setDisabled(False)
				self.filterText2.setDisabled(False)
				self.pixText2.setDisabled(False)

	def chkSelection2(self, checkbox):
		if checkbox.text() == "movies":
			if checkbox.isChecked() == True:
				self.moviesText2.setDisabled(False)
			else:
				self.moviesText2.setDisabled(True)
		if checkbox.text() == "micrographs":
			if checkbox.isChecked() == True:
				self.micText2.setDisabled(False)
			else:
				self.micText2.setDisabled(True)
		if checkbox.text() == "ctf":
			if checkbox.isChecked() == True:
				self.ctfText2.setDisabled(False)
			else:
				self.ctfText2.setDisabled(True)"""

	def relionUI(self):
		self.relionTab.layout = QFormLayout(self)

		"""self.curateLabel3 = QLabel(self)
		self.curateLabel3.setText("Curate with jpeg or mrc files:")

		self.curateType3 = QHBoxLayout()

		self.curateJPEG3 = QRadioButton(self)
		self.curateJPEG3.setText("jpeg")
		self.curateJPEG3.toggled.connect(lambda:self.btnSelection3(self.curateJPEG3))
		self.curateType3.addWidget(self.curateJPEG3)

		self.curateMRC3 = QRadioButton(self)
		self.curateMRC3.setText("mrc")
		self.curateMRC3.toggled.connect(lambda:self.btnSelection3(self.curateMRC3))
		self.curateType3.addWidget(self.curateMRC3)

		self.curateType3.setAlignment(QtCore.Qt.AlignCenter)
		self.relionTab.layout.addRow(self.curateLabel3, self.curateType3)

		self.updateLabel3 = QLabel(self)
		self.updateLabel3.setText("Update star files:")

		self.updateType3 = QHBoxLayout()

		self.updateMovies3 = QCheckBox(self)
		self.updateMovies3.setText("movies")
		self.updateMovies3.toggled.connect(lambda:self.chkSelection3(self.updateMovies3))
		self.updateType3.addWidget(self.updateMovies3)

		self.updateMics3 = QCheckBox(self)
		self.updateMics3.setText("micrographs")
		self.updateMics3.toggled.connect(lambda:self.chkSelection3(self.updateMics3))
		self.updateType3.addWidget(self.updateMics3)

		self.updateCTF3 = QCheckBox(self)
		self.updateCTF3.setText("ctf")
		self.updateCTF3.toggled.connect(lambda:self.chkSelection3(self.updateCTF3))
		self.updateType3.addWidget(self.updateCTF3)

		self.updateType3.setAlignment(QtCore.Qt.AlignCenter)
		self.relionTab.layout.addRow(self.updateLabel3, self.updateType3)

		self.moviesLabel3 = QLabel(self)
		self.moviesLabel3.setText("Movies star file:")
		self.moviesText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.moviesLabel3, self.moviesText3)

		self.micLabel3 = QLabel(self)
		self.micLabel3.setText("Micrograph star file:")
		self.micText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.micLabel3, self.micText3)

		self.ctfLabel3 = QLabel(self)
		self.ctfLabel3.setText("CTF star file:")
		self.ctfText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.ctfLabel3, self.ctfText3)
		
		self.jpegLabel3 = QLabel(self)
		self.jpegLabel3.setText("Corrected micrographs directory:")
		self.jpegText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.jpegLabel3, self.jpegText3)

		self.jpegLabel3 = QLabel(self)
		self.jpegLabel3.setText("JPEG directory:")
		self.jpegText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.jpegLabel3, self.jpegText3)

		self.scaleLabel3 = QLabel(self)
		self.scaleLabel3.setText("Micrograph scale:")
		self.scaleText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.scaleLabel3, self.scaleText3)

		self.contrastLabel3 = QLabel(self)
		self.contrastLabel3.setText("Sigma contrast:")
		self.contrastText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.contrastLabel3, self.contrastText3)

		self.filterLabel3 = QLabel(self)
		self.filterLabel3.setText("Low pass filter (A):")
		self.filterText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.filterLabel3, self.filterText3)

		self.pixLabel3 = QLabel(self)
		self.pixLabel3.setText("Apix (A):")
		self.pixText3 = QLineEdit(self)
		self.relionTab.layout.addRow(self.pixLabel3, self.pixText3)

		self.relionSubmit = QPushButton(self)
		self.relionSubmit.setText("Submit")
		self.relionSubmit.clicked.connect(self.relionGoNext)
		self.relionTab.layout.addRow(self.relionSubmit)"""

		self.relionTab.setLayout(self.relionTab.layout)
		"""self.curateJPEG3.setChecked(True)
		self.moviesText3.setDisabled(True)
		self.micText3.setDisabled(True)
		self.ctfText3.setDisabled(True)

	def relionGoNext(self):
		window1.hide()
		self.rmMics = removeMics(self)
		self.rmMics.show()

	def btnSelection3(self, button):
		if button.text() == "jpeg":
			if button.isChecked() == True:
				self.jpegText3.setDisabled(False)
				self.scaleText3.setDisabled(True)
				self.contrastText3.setDisabled(True)
				self.filterText3.setDisabled(True)
				self.pixText3.setDisabled(True)
		else:
			if button.isChecked() == True:
				self.jpegText3.setDisabled(True)
				self.scaleText3.setDisabled(False)
				self.contrastText3.setDisabled(False)
				self.filterText3.setDisabled(False)
				self.pixText3.setDisabled(False)

	def chkSelection3(self, checkbox):
		if checkbox.text() == "movies":
			if checkbox.isChecked() == True:
				self.moviesText3.setDisabled(False)
			else:
				self.moviesText3.setDisabled(True)
		if checkbox.text() == "micrographs":
			if checkbox.isChecked() == True:
				self.micText3.setDisabled(False)
			else:
				self.micText3.setDisabled(True)
		if checkbox.text() == "ctf":
			if checkbox.isChecked() == True:
				self.ctfText3.setDisabled(False)
			else:
				self.ctfText3.setDisabled(True)"""



class removeMics(QMainWindow):
	def __init__(self,parent):
		super(removeMics, self).__init__(parent)

		self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

		if os.name == 'nt':
			self.fullPath = os.path.abspath(tabWidgetSetup.jpegDir1)
			os.system("dir /b %s\*.jpeg > jpeglist.txt" % (self.fullPath))
			os.system("touch>jpeglist_new.txt")
			with open("jpeglist.txt") as f1:
				self.jpegList = f1.readlines()
			with open("jpeglist_new.txt","a") as f3:
				for self.jpegFile in self.jpegList:
					f3.write(self.fullPath + "\\" + self.jpegFile)
			os.system("move jpeglist_new.txt jpeglist.txt")
		else:
			os.system("ls %s/*.jpeg > jpeglist.txt" % (tabWidgetSetup.jpegDir1))

		if os.path.isfile("badjpeg_selected.log") == False:
			if os.name == 'nt':
				os.system("touch>badjpeg_selected.log")
			else:
				os.system("touch badjpeg_selected.log")

		with open("jpeglist.txt") as f1:
			self.jpeglist = f1.readlines()

		self.menu = self.menuBar()
		self.fileMenu = self.menu.addMenu('&File')
		self.importMenu = self.fileMenu.addAction("&Import log file")
		self.importMenu.triggered.connect(self.importLog)
		self.openMenu = self.fileMenu.addAction("&Open micrograph")
		self.openMenu.triggered.connect(self.openMic)
		
		self.editMenu = self.menu.addMenu('&Edit')
		self.undoSelMenu = self.editMenu.addAction("&Undo all selected")
		self.undoSelMenu.triggered.connect(self.undoSelected)

		if os.name != 'nt':
			self.trashMenu = self.fileMenu.addAction("&Trash all selected")
			self.trashMenu.triggered.connect(self.lastNext)
			self.deleteMenu = self.fileMenu.addAction("&Delete all trash directories")
			self.deleteMenu.triggered.connect(self.deleteTrash)
			
			self.undoTrashMenu = self.editMenu.addAction("&Undo all trashed")
			self.undoTrashMenu.triggered.connect(self.undoTrash)

		self.menu.show()
		self.i = 0
		self.viewJPEG()

	def viewJPEG(self):
		self.jpeg = self.jpeglist[self.i].replace("\n","")

		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()

		self.setWindowTitle(self.jpeg)

		if os.path.isfile(self.jpeg) == True:
			self.label = QLabel(self)
			self.pixmap = QPixmap(self.jpeg)
			self.label.setPixmap(self.pixmap)
			self.label.resize(self.pixmap.width(),self.pixmap.height())
			self.label.move(0,25)
			self.label.show()
		else:
			self.label = QLabel(self)
			self.label.setText("File has been trashed.")
			self.label.resize(360,20)
			self.label.move(50,250)
			self.label.show()

		if os.path.isfile(self.jpeg) == True:
			self.setGeometry(50, 50, self.pixmap.width() + 220,self.pixmap.height() + 25)
		else:
			self.setGeometry(50, 50, 500, 525)

		self.nextButton = QPushButton(self)
		self.nextButton.setText("Next (N)")
		if os.path.isfile(self.jpeg) == True:
			self.nextButton.move(self.pixmap.width() + 120,self.pixmap.height()/2 - 5)
		else:
			self.nextButton.move(400, 225)
		self.nextButton.resize(80,40)
		if self.jpeglist[self.i] != self.jpeglist[-1]:
			self.nextButton.clicked.connect(self.nextMic)
		else:
			if os.name != 'nt':
				self.nextButton.clicked.connect(self.lastNext)
		self.nextButton.show()

		self.backButton = QPushButton(self)
		self.backButton.setText("Back (B)")
		if os.path.isfile(self.jpeg) == True:		
			self.backButton.move(self.pixmap.width() + 20,self.pixmap.height()/2 - 5)
		else:
			self.backButton.move(300, 225)
		self.backButton.resize(80,40)
		if self.jpeglist[self.i] != self.jpeglist[0]:
			self.backButton.clicked.connect(self.backMic)
		self.backButton.show()

		self.deleteButton = QPushButton(self)
		self.deleteButton.setText("Select (S)")
		if os.path.isfile(self.jpeg) == True:
			self.deleteButton.move(self.pixmap.width() + 70,self.pixmap.height()/2 + 75)
		else:
			self.deleteButton.move(350,305)
		self.deleteButton.resize(80,40)
		self.deleteButton.clicked.connect(self.deleteMic)
		self.deleteButton.show()

		self.selectCheck = QCheckBox(self)
		if os.path.isfile(self.jpeg) == True:		
			self.selectCheck.move(self.pixmap.width() + 160,self.pixmap.height()/2 + 80)
		else:
			self.selectCheck.move(440,310)
		self.selectCheck.setEnabled(False)
		if self.jpeglist[self.i] in self.badjpeg:
			self.selectCheck.setChecked(True)
		else:
			self.selectCheck.setChecked(False)
		self.selectCheck.show()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_B:
			if self.jpeglist[self.i] != self.jpeglist[0]:
				self.backMic()
		elif event.key() == QtCore.Qt.Key_N:
			if self.jpeglist[self.i] != self.jpeglist[-1]:
				self.nextMic()
			else:
				if os.name != 'nt':
					self.lastNext()
		elif event.key() == QtCore.Qt.Key_S:
			self.deleteMic()
		event.accept()

	def resetGUI(self):
		self.label.hide()
		self.nextButton.hide()
		self.backButton.hide()
		self.deleteButton.hide()
		self.selectCheck.hide()
		self.viewJPEG()

	def nextMic(self):
		self.i = self.i + 1
		self.resetGUI()

	def backMic(self):
		self.i = self.i - 1
		self.resetGUI()

	def importLog(self):
		self.importFile = QFileDialog.getOpenFileName(self, "Import log", "." , "Log files (*.log)")
		if self.importFile[0] != "":
			if os.name == 'nt':
				self.importFile = self.importFile[0].replace("/","\\")
				os.system("touch>importFile_new.txt")
				with open(self.importFile) as f4:
					self.importBad = f4.readlines()
				with open("importFile_new.txt","a") as f5:
					for self.importMic in self.importBad:
						f5.write(self.fullPath + "\\" + self.importMic.rsplit("/",1)[-1].rsplit("\\",1)[-1])
				os.system("move importFile_new.txt badjpeg_selected.log")
				self.resetGUI()
			else:
				os.system("touch importFile_new.txt")
				with open(self.importFile[0]) as f4:
					self.importBad = f4.readlines()
				with open("importFile_new.txt","a") as f5:
					for self.importMic in self.importBad:
						f5.write(tabWidgetSetup.jpegDir1 + "/" + self.importMic.rsplit("/",1)[-1].rsplit("\\",1)[-1])
				os.system("mv importFile_new.txt badjpeg_selected.log")
				self.resetGUI()

	def openMic(self):
		self.mic2open_full = QFileDialog.getOpenFileName(self, "Open", "%s" % (tabWidgetSetup.jpegDir1) , "Image files (*.jpeg)")
		if os.name == 'nt':
			self.mic2open_trunc = self.mic2open_full[0].rsplit("/",1)[-1]
			self.mic2open = self.fullPath + "\\" + self.mic2open_trunc
			if self.mic2open_full[0] != "":
				self.i = self.jpeglist.index(self.mic2open + "\n")
				self.resetGUI()
		else:
			self.mic2open_trunc = self.mic2open_full[0].rsplit("/",1)[-1]
			self.mic2open_path = self.jpeg.rsplit("/",1)[0]
			self.mic2open = self.mic2open_path + "/" + self.mic2open_trunc
			if self.mic2open_full[0] != "":
				self.i = self.jpeglist.index(self.mic2open + "\n")
				self.resetGUI()

	def lastNext(self):
		deleteMessage = QMessageBox.question(self, 'Trash', "Trash all selected micrographs?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if deleteMessage == QMessageBox.Yes:
			if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
				if os.path.isdir("%s/tiffsTrash" % (tabWidgetSetup.tiffDir1)) == False:
					os.system("mkdir %s/tiffsTrash" % (tabWidgetSetup.tiffDir1))
			if os.path.isdir("%s/mrcTrash" % (tabWidgetSetup.micDir1)) == False:
				os.system("mkdir %s/mrcTrash" % (tabWidgetSetup.micDir1))
			if os.path.isdir("%s/jpegTrash" % (tabWidgetSetup.jpegDir1)) == False:
				os.system("mkdir %s/jpegTrash" % (tabWidgetSetup.jpegDir1))
			with open("badjpeg_selected.log") as f2:
				lines = f2.readlines()
				for line in lines:
					jpegName = line.strip("\n")
					if tabWidgetSetup.tiffDir1 != "":
						tiffName = jpegName.replace(".jpeg",".tif")
						tiffName = tiffName.replace(tabWidgetSetup.jpegDir1, tabWidgetSetup.tiffDir1)
					mrcName = jpegName.replace(".jpeg",".mrc")
					mrcName = mrcName.replace(tabWidgetSetup.jpegDir1, tabWidgetSetup.micDir1)

					if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
						os.system("mv %s %s/tiffsTrash" % (tiffName,tabWidgetSetup.tiffDir1))
					os.system("mv %s %s/mrcTrash" % (mrcName,tabWidgetSetup.micDir1))
					os.system("mv %s %s/jpegTrash" % (jpegName,tabWidgetSetup.jpegDir1))

	def deleteMic(self):
		if self.jpeglist[self.i] in self.badjpeg:
			self.selectCheck.setChecked(False)
			with open("badjpeg_selected.log", "r") as f2:
				lines = f2.readlines()
			with open("badjpeg_selected.log", "w+") as f2:
				for line in lines:
					if line.strip("\n") != self.jpeglist[self.i].strip("\n"):
						f2.write(line)
				self.badjpeg = f2.readlines()
		else:
			self.selectCheck.setChecked(True)
			with open("badjpeg_selected.log", "a+") as f2:
				f2.write(self.jpeglist[self.i])
				f2.seek(0)
				self.badjpeg = f2.readlines()
		self.selectCheck.show()

	def deleteTrash(self):
		trashMessage = QMessageBox.question(self, 'Delete', "Delete trash directories?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if trashMessage == QMessageBox.Yes:
			if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
				os.system("rm -rf %s/tiffsTrash" % (tabWidgetSetup.tiffDir1))
			os.system("rm -rf %s/jpegTrash" % (tabWidgetSetup.jpegDir1))
			os.system("rm -rf %s/mrcTrash" % (tabWidgetSetup.micDir1))

	def undoSelected(self):
		undoSelMessage = QMessageBox.question(self, 'Undo Selections', "Undo ALL selected micrographs?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if undoSelMessage == QMessageBox.Yes:
			open("badjpeg_selected.log", "w").close()
			self.resetGUI()

	def undoTrash(self):
		undoTrashMessage = QMessageBox.question(self, 'Undo Trash', "Undo ALL trashed micrographs?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if undoTrashMessage == QMessageBox.Yes:
			if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
				os.system("mv %s/tiffsTrash/* %s" % (tabWidgetSetup.tiffDir1,tabWidgetSetup.tiffDir1))
			os.system("mv %s/jpegTrash/* %s" % (tabWidgetSetup.jpegDir1,tabWidgetSetup.jpegDir1))
			os.system("mv %s/mrcTrash/* %s" % (tabWidgetSetup.micDir1,tabWidgetSetup.micDir1))
			open("badjpeg_selected.log", "w").close()
			self.resetGUI()
			
	def saveLog(self):
		fileNum = 0
		while os.path.isfile("badjpeg_deleted_%s.log" % (fileNum)) == True:
			fileNum += 1
		if os.name == 'nt':
			os.system("move badjpeg_selected.log badjpeg_deleted_%s.log" % (fileNum))
			os.system("del jpeglist.txt")
		else:
			os.system("mv badjpeg_selected.log badjpeg_deleted_%s.log" % (fileNum))
			os.system("rm jpeglist.txt")
			
	def closeEvent(self, event):
		if os.name == 'nt':
			self.endMessage = QMessageBox.question(self, 'Save', "Save and close?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if self.endMessage == QMessageBox.Yes:
				self.saveLog()
				event.accept()
			else:
				event.ignore()
		else:
			self.endMessage = QMessageBox.question(self, 'Delete', "Delete trash directories?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
			if self.endMessage == QMessageBox.Yes:
				if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
					os.system("rm -rf %s/tiffsTrash" % (tabWidgetSetup.tiffDir1))
				os.system("rm -rf %s/jpegTrash" % (tabWidgetSetup.jpegDir1))
				os.system("rm -rf %s/mrcTrash" % (tabWidgetSetup.micDir1))
			if self.endMessage != QMessageBox.Cancel:
				self.saveLog()
				event.accept()
			if self.endMessage == QMessageBox.Cancel:
				event.ignore()



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window1 = micsLocation()	
	window1.show()
	sys.exit(app.exec_())
