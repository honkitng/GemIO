#!/usr/bin/env python3.6

#Last modified 01/17/20 by Honkit Ng.

import os
import sys
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QLabel, QPushButton, QRadioButton, QTabWidget, QWidget, QFormLayout, QHBoxLayout, QVBoxLayout, QCheckBox, QMessageBox, QFileDialog, QScrollArea, QWidget, QComboBox, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread



class micsLocation(QMainWindow):
	def __init__(self):
		super(micsLocation, self).__init__()

		self.setGeometry(200, 200, 570, 100)
		self.setWindowTitle("GemIO")

		self.tabWidget = tabWidgetSetup(self)
		self.setCentralWidget(self.tabWidget)



class tabWidgetSetup(QWidget):
	def __init__(self, parent):
		super(tabWidgetSetup, self).__init__(parent)

		self.layout = QFormLayout()

		self.tabs = QTabWidget()
		self.motioncorTab = QWidget()
		self.jpegTab = QWidget()
		#self.ctfTab = QWidget()
		#self.relionTab = QWidget()

		self.tabs.addTab(self.motioncorTab,"Remove with JPEG's")
		self.motioncorUI()
		if sys.platform == 'linux':
			self.tabs.addTab(self.jpegTab,"Generate JPEG's")
			self.jpegUI()
			#self.tabs.setTabEnabled(1,False)
		#self.tabs.addTab(self.ctfTab,"Remove with JPEG and CTF")
		#self.tabs.addTab(self.relionTab,"Relion GUI")
		#self.ctfUI()
		#self.relionUI()
		#self.tabs.setTabEnabled(1,False)
		#self.tabs.setTabEnabled(2,False)

		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)

	def motioncorUI(self):
		self.motioncorTab.layout = QFormLayout()

		if sys.platform == 'linux':
			self.starLabel1 = QLabel("Micrograph star file:")
			self.starEntry1 = QHBoxLayout()
			self.starText1 = QLineEdit()
			self.starEntry1.addWidget(self.starText1)
			self.starButton1 = QPushButton("Browse")
			self.starButton1.clicked.connect(self.fileOpen1)
			self.starEntry1.addWidget(self.starButton1)
			self.motioncorTab.layout.addRow(self.starLabel1, self.starEntry1)

			self.tiffLabel1 = QLabel("TIF directory:")
			self.tiffEntry1 = QHBoxLayout()
			self.tiffText1 = QLineEdit()
			self.tiffEntry1.addWidget(self.tiffText1)
			self.tiffButton1 = QPushButton("Browse")
			self.tiffButton1.clicked.connect(lambda:self.folderOpen1(1))
			self.tiffEntry1.addWidget(self.tiffButton1)
			self.motioncorTab.layout.addRow(self.tiffLabel1, self.tiffEntry1)

			self.micLabel1 = QLabel("Corrected micrographs directory:")
			self.micEntry1 = QHBoxLayout()
			self.micText1 = QLineEdit("Micrographs")
			self.micEntry1.addWidget(self.micText1)
			self.micButton1 = QPushButton("Browse")
			self.micButton1.clicked.connect(lambda:self.folderOpen1(2))
			self.micEntry1.addWidget(self.micButton1)
			self.motioncorTab.layout.addRow(self.micLabel1, self.micEntry1)

		self.jpegLabel1 = QLabel("JPEG directory:")
		self.jpegEntry1 = QHBoxLayout()
		self.jpegText1 = QLineEdit("jpgs")
		self.jpegEntry1.addWidget(self.jpegText1)
		self.jpegButton1 = QPushButton("Browse")
		self.jpegButton1.clicked.connect(lambda:self.folderOpen1(3))
		self.jpegEntry1.addWidget(self.jpegButton1)
		self.motioncorTab.layout.addRow(self.jpegLabel1, self.jpegEntry1)

		self.multiLabel1 = QLabel("Display all in one screen?")
		self.multiSelect1 = QComboBox()
		self.multiSelect1.addItems(["No","Yes"])
		self.multiSelect1.activated.connect(self.columnsSelection1)
		self.motioncorTab.layout.addRow(self.multiLabel1, self.multiSelect1)

		self.columnsLabel1 = QLabel("Number of columns:")
		self.columnsText1 = QLineEdit("4")
		#self.columnsText1.setFixedWidth(30)
		#self.columnsText1.setAlignment(QtCore.Qt.AlignCenter)
		self.columnsText1.setDisabled(True)
		self.motioncorTab.layout.addRow(self.columnsLabel1, self.columnsText1)

		self.scaleLabel1 = QLabel("Micrograph scaling:")
		self.scaleText1 = QLineEdit(".5")
		#self.scaleText1.setFixedWidth(30)
		#self.scaleText1.setAlignment(QtCore.Qt.AlignCenter)
		self.scaleText1.setDisabled(True)
		self.motioncorTab.layout.addRow(self.scaleLabel1, self.scaleText1)

		self.motioncorSubmit = QPushButton("Submit")
		self.motioncorSubmit.clicked.connect(self.motioncorGoNext)
		self.motioncorTab.layout.addRow(self.motioncorSubmit)

		self.motioncorTab.setLayout(self.motioncorTab.layout)

	def fileOpen1(self):
		self.openFile = QFileDialog.getOpenFileName(self, "Open", ".", "STAR file (*.star)")
		if self.openFile[0] != "":
			self.starText1.setText(self.openFile[0])

	def folderOpen1(self,x):
		self.openFolder = QFileDialog.getExistingDirectory(self, "Open")
		if x == 1:
			self.tiffText1.setText(self.openFolder)
		elif x == 2:
			self.micText1.setText(self.openFolder)
		elif x ==3:
			self.jpegText1.setText(self.openFolder)

	def columnsSelection1(self):
		if self.multiSelect1.currentText() == "Yes":
			self.columnsText1.setDisabled(False)
			self.scaleText1.setDisabled(False)
		else:
			self.columnsText1.setDisabled(True)
			self.scaleText1.setDisabled(True)

	def motioncorGoNext(self):
		if sys.platform != 'linux':
			tabWidgetSetup.starFile1 = "None_Entered"
			tabWidgetSetup.tiffDir1 = "None_Entered"
			tabWidgetSetup.micDir1 = "None_Entered"
		else:
			tabWidgetSetup.starFile1 = self.starText1.text()
			tabWidgetSetup.tiffDir1 = self.tiffText1.text()
			tabWidgetSetup.micDir1 = self.micText1.text()
		tabWidgetSetup.jpegDir1 = self.jpegText1.text()
		if self.multiSelect1.currentText() == "Yes":
			try:
				tabWidgetSetup.jpegColumns1 = int(self.columnsText1.text())
				tabWidgetSetup.jpegScaling1 = float(self.scaleText1.text())
				badNumbers = 0
			except ValueError:
				badNumbers = 1
		if " " not in tabWidgetSetup.tiffDir1 and " " not in tabWidgetSetup.micDir1 and " " not in tabWidgetSetup.jpegDir1:
			try:
				if sys.platform == 'linux' and tabWidgetSetup.tiffDir1 != '' and not any(files.endswith(".tif") for files in os.listdir("%s" % (tabWidgetSetup.tiffDir1))):
					noTIFF = QMessageBox.warning(self, 'Error', "There are no tif files in the input directory.\n\n Please enter a different directory.", QMessageBox.Ok)
				else:
					if sys.platform == 'linux' and not any(files.endswith(".mrc") for files in os.listdir("%s" % (tabWidgetSetup.micDir1))):
						noTIFF = QMessageBox.warning(self, 'Error', "There are no mrc files in the input directory.\n\n Please enter a different directory.", QMessageBox.Ok)
					else:
						if any(files.endswith(".jpeg") for files in os.listdir("%s" % (tabWidgetSetup.jpegDir1))):
							if self.multiSelect1.currentText() == "Yes":
								if badNumbers == 0:
									self.motioncorSubmit.setEnabled(False)
									self.jpegProgress = QProgressBar()
									self.jpegProgress.setRange(0,0)
									self.motioncorTab.layout.addRow(self.jpegProgress)
									self.rmMics = removeMics2(self)
									self.rmMics.show()
									window1.hide()
								else:
									numWarning = QMessageBox.warning(self, 'Error', "Invalid number entered for columns/scaling.", QMessageBox.Ok)
							else:
									self.rmMics = removeMics1(self)
									self.rmMics.show()
									window1.hide()
						else:
							noJPEG = QMessageBox.warning(self, 'Error', "There are no jpeg files in the input directory.\n\n Please enter a different directory.", QMessageBox.Ok)
			except FileNotFoundError:
				noDir = QMessageBox.warning(self, 'Error', "Invalid directory entered.\n\n Please enter a different directory.", QMessageBox.Ok)
		else:
			spaceWarning = QMessageBox.warning(self, 'Error', "Please remove all spaces from inputs.", QMessageBox.Ok)

	def jpegUI(self):
		self.jpegTab.layout = QFormLayout(self)

		self.micLabel0 = QLabel("Input micrographs:")
		self.micEntry0 = QHBoxLayout()
		self.micText0 = QLineEdit("Micrographs/*.mrc")
		self.micEntry0.addWidget(self.micText0)
		self.micButton0 = QPushButton("Browse")
		self.micButton0.clicked.connect(self.fileOpen0)
		self.micEntry0.addWidget(self.micButton0)
		self.jpegTab.layout.addRow(self.micLabel0, self.micEntry0)

		self.outputLabel0 = QLabel("Output JPEG directory:")
		self.outputEntry0 = QHBoxLayout()
		self.outputText0 = QLineEdit("Micrographs/jpeg")
		self.outputEntry0.addWidget(self.outputText0)
		self.outputButton0 = QPushButton("Browse")
		self.outputButton0.clicked.connect(self.folderOpen0)
		self.outputEntry0.addWidget(self.outputButton0)
		self.jpegTab.layout.addRow(self.outputLabel0, self.outputEntry0)

		self.e2proc2dLabel0 = QLabel("e2proc2d.py location")
		self.e2proc2dEntry0 = QHBoxLayout()
		self.e2proc2dText0 = QLineEdit("/bin/e2proc2d.py")
		self.e2proc2dEntry0.addWidget(self.e2proc2dText0)
		self.e2proc2dButton0 = QPushButton("Browse")
		self.e2proc2dButton0.clicked.connect(self.e2proc2dOpen0)
		self.e2proc2dEntry0.addWidget(self.e2proc2dButton0)
		self.jpegTab.layout.addRow(self.e2proc2dLabel0, self.e2proc2dEntry0)

		self.apixLabel0 = QLabel("Pixel size (A/pix):")
		self.apixText0 = QLineEdit("1")
		self.jpegTab.layout.addRow(self.apixLabel0, self.apixText0)

		self.filterLabel0 = QLabel("Low-pass filter (A):")
		self.filterText0 = QLineEdit("20")
		self.jpegTab.layout.addRow(self.filterLabel0, self.filterText0)

		self.shrinkLabel0 = QLabel("Shrink image:")
		self.shrinkText0 = QLineEdit("4")
		self.jpegTab.layout.addRow(self.shrinkLabel0, self.shrinkText0)

		self.additionalLabel0 = QLabel("Additional arguments:")
		self.additionalText0 = QLineEdit()
		self.jpegTab.layout.addRow(self.additionalLabel0, self.additionalText0)

		self.blankLabel0 = QLabel()
		self.blankLabel0.setFixedWidth(200)
		self.jpegEntry0 = QHBoxLayout()
		self.jpegCmd = QPushButton("Print Command")
		#self.jpegCmd.setFixedWidth(200)
		self.jpegCmd.clicked.connect(self.jpegPrintCmd)
		self.jpegEntry0.addWidget(self.jpegCmd)
		self.jpegSubmit = QPushButton("Submit")
		#self.jpegSubmit.setFixedWidth(200)
		self.jpegSubmit.clicked.connect(self.jpegGoNext)
		self.jpegEntry0.addWidget(self.jpegSubmit)
		self.jpegTab.layout.addRow(self.blankLabel0, self.jpegEntry0)

		self.jpegTab.setLayout(self.jpegTab.layout)

	def fileOpen0(self):
		self.openFile = QFileDialog.getOpenFileName(self, "Open", ".", "Micrographs (*.tif *.mrc *.hdf);;All files (*.*)")
		if self.openFile[0] != "":
			self.micText0.setText(self.openFile[0])

	def folderOpen0(self):
		self.openFolder = QFileDialog.getExistingDirectory(self, "Open")
		if self.openFolder != "":
			self.outputText0.setText(self.openFolder)

	def e2proc2dOpen0(self):
		self.openE2proc2d = QFileDialog.getOpenFileName(self, "Open", ".", "e2proc2d.py (e2proc2d.py);;All files (*.*)")
		if self.openE2proc2d[0] != "":
			self.e2proc2dText0.setText(self.openE2proc2d[0])

	def jpegSetup(self):
		self.micLoc0 = self.micText0.text()
		self.outputDir0 = self.outputText0.text()
		self.e2proc2dLoc0 = self.e2proc2dText0.text()
		self.apixVal0 = self.apixText0.text()
		self.filterVal0 = self.filterText0.text()
		self.shrinkVal0 = self.shrinkText0.text()
		self.additionalArgs0 = self.additionalText0.text()

		if "/" in self.micLoc0:
			self.micDir0 = self.micLoc0.rsplit("/",1)[0]
			if "*" in self.micLoc0:
				self.micExt0 = self.micLoc0.rsplit("/",1)[1].split("*",1)[1]
			else:
				self.micExt0 = self.micLoc0.rsplit("/",1)[1]
		else:
			if "*" in self.micLoc0:
				self.micDir0 = os.path.abspath(self.micLoc0.split("*",1)[0])
				self.micExt0 = self.micLoc0.split("*",1)[1]
			else:
				self.micDir0 = os.path.abspath(".")
				self.micExt0 = self.micLoc0

	def jpegPrintCmd(self):
		self.jpegSetup()

		try:
			for file in os.listdir(self.micDir0):
				if file.endswith(self.micExt0):
					newFile = file.split(".",1)[0] + ".jpeg"
					print(f'{self.e2proc2dLoc0} {os.path.join(self.micDir0, file)} {os.path.join(self.outputDir0, newFile)} '
						f'--apix={self.apixVal0} --process filter.lowpass.gauss:cutoff_freq={self.filterVal0} --meanshrink={self.shrinkVal0} {self.additionalArgs0}')
		except FileNotFoundError:
			noDir = QMessageBox.warning(self, 'Error', "Invalid directory entered.\n\n Please enter a different directory.", QMessageBox.Ok)

	def jpegGoNext(self):
		self.jpegSetup()

		self.micCountFunc = subprocess.Popen(f'ls {self.micLoc0} | wc -l', stdout=subprocess.PIPE, shell=True)
		self.micCount = int(self.micCountFunc.stdout.read())
		if self.micCount == 0:
			inputWarning = QMessageBox.warning(self, 'Error', "No micrographs found in input.", QMessageBox.Ok)
		else:
			if os.path.exists(self.outputDir0) == False:
				outputWarning = QMessageBox.warning(self, 'Error', "Output directory missing.", QMessageBox.Ok)
			else:				
				self.convertProgress = QProgressBar()
				self.convertProgress.setRange(0,self.micCount)
				self.jpegTab.layout.addRow(self.convertProgress)

				i = 0

				for file in os.listdir(self.micDir0):
					if file.endswith(self.micExt0):
						QtWidgets.QApplication.processEvents()

						newFile = os.path.join(self.outputDir0, file.split(".",1)[0] + ".jpeg")
						if os.path.exists(newFile) == False:
							os.system(f'{self.e2proc2dLoc0} {os.path.join(self.micDir0, file)} {os.path.join(newFile)} '
								f'--apix={self.apixVal0} --process filter.lowpass.gauss:cutoff_freq={self.filterVal0} --meanshrink={self.shrinkVal0} {self.additionalArgs0}')
							i+=1
							self.convertProgress.setValue(i)
						else:
							i+=1
							self.convertProgress.setValue(i)
				convertDone = QMessageBox.information(self, 'Complete', "All micrographs have been converted!", QMessageBox.Ok)
				self.convertProgress.hide()

	"""def ctfUI(self):
		self.ctfTab.layout = QFormLayout(self)

		self.curateLabel2 = QLabel(self)
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
		self.ctfTab.layout.addRow(self.ctfSubmit)

		self.ctfTab.setLayout(self.ctfTab.layout)
		self.curateJPEG2.setChecked(True)
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

	"""def relionUI(self):
		self.relionTab.layout = QFormLayout(self)

		self.curateLabel3 = QLabel(self)
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
		self.relionTab.layout.addRow(self.relionSubmit)

		self.relionTab.setLayout(self.relionTab.layout)
		self.curateJPEG3.setChecked(True)
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



class removeMics1(QMainWindow):
	def __init__(self,parent):
		super(removeMics1, self).__init__(parent)

		self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

		if sys.platform == 'win32':
			self.fullPath = os.path.abspath(tabWidgetSetup.jpegDir1)
			os.system("dir /b %s\*.jpeg > jpeglist.txt" % (self.fullPath))
			os.system("copy nul jpeglist_new.txt")
			with open("jpeglist.txt") as f1:
				self.jpegList = f1.readlines()
			with open("jpeglist_new.txt","a") as f3:
				for self.jpegFile in self.jpegList:
					f3.write(self.fullPath + "\\" + self.jpegFile)
			os.system("move jpeglist_new.txt jpeglist.txt")
		else:
			os.system("ls %s/*.jpeg > jpeglist.txt" % (tabWidgetSetup.jpegDir1))

		if os.path.isfile("badjpeg_selected.log") == False:
			if sys.platform == 'win32':
				os.system("copy nul badjpeg_selected.log")
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
		self.starMenu = self.fileMenu.addAction("&Export star file")
		self.StarMenu.triggered.connect(self.exportStar)
		if tabWidgetSetup.starFile1 != "" and " " not in tabWidgetSetup.starFile1:
			self.StarMenu.setDisabled(True)
		
		self.editMenu = self.menu.addMenu('&Edit')
		self.undoSelMenu = self.editMenu.addAction("&Undo all selected")
		self.undoSelMenu.triggered.connect(self.undoSelected)
		self.invertSelMenu = self.editMenu.addAction("&Invert selection")
		self.invertSelMenu.triggered.connect(self.invertSelected)

		if sys.platform == 'linux':
			self.trashMenu = self.fileMenu.addAction("&Trash all selected")
			self.trashMenu.triggered.connect(self.lastNext)
			self.deleteMenu = self.fileMenu.addAction("&Delete all trash directories")
			self.deleteMenu.triggered.connect(self.deleteTrash)
			
			self.undoTrashMenu = self.editMenu.addAction("&Undo all trashed")
			self.undoTrashMenu.triggered.connect(self.undoTrash)

		self.menu.show()
		self.i = 0
		self.viewJPEG1()

	def viewJPEG1(self):
		self.jpeg = self.jpeglist[self.i].replace("\n","")

		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()

		self.setWindowTitle(self.jpeg)

		self.label = QLabel(self)
		if os.path.isfile(self.jpeg) == True:
			self.pixmap = QPixmap(self.jpeg)
			self.screenRes = app.desktop().screenGeometry()
			self.widRes, self.lenRes = self.screenRes.width(), self.screenRes.height()
			self.pixmap = self.pixmap.scaled(self.widRes - 150, self.lenRes - 150, Qt.KeepAspectRatio)
			self.label.setPixmap(self.pixmap)
			self.label.resize(self.pixmap.width(),self.pixmap.height())
			self.label.move(0,25)
			self.setGeometry(50, 50, self.pixmap.width() + 220,self.pixmap.height() + 25)
		else:
			self.label.setText("File has been trashed.")
			self.label.resize(150,20)
			self.label.move(50,250)
			self.setGeometry(50, 50, 500, 525)
		self.label.show()

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
			if sys.platform == 'linux':
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
			self.label.setStyleSheet("QLabel {border: 5px solid red;}")
		else:
			self.selectCheck.setChecked(False)
			self.label.setStyleSheet("QLabel {border: 0px solid red;}")
		self.selectCheck.show()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_B:
			if self.jpeglist[self.i] != self.jpeglist[0]:
				self.backMic()
		elif event.key() == QtCore.Qt.Key_N:
			if self.jpeglist[self.i] != self.jpeglist[-1]:
				self.nextMic()
			else:
				if sys.platform == 'linux':
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
		self.viewJPEG1()

	def nextMic(self):
		self.i = self.i + 1
		self.resetGUI()

	def backMic(self):
		self.i = self.i - 1
		self.resetGUI()

	def importLog(self):
		self.importFile = QFileDialog.getOpenFileName(self, "Import log", "." , "Log files (*.log);;All files (*.*)")
		if self.importFile[0] != "":
			if sys.platform == 'win32':
				self.importFile = self.importFile[0].replace("/","\\")
				os.system("copy nul importFile_new.txt")
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
		self.mic2open_full = QFileDialog.getOpenFileName(self, "Open", "%s" % (tabWidgetSetup.jpegDir1) , "Image files (*.jpeg);;All files (*.*)")
		try:
			if sys.platform == 'win32':
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
		except ValueError:
			missMic = QMessageBox.warning(self, 'Error', "Micrograph not originally in input directory.\n Please select a different micrograph.", QMessageBox.Ok)

	def exportStar(self):
		if tabWidgetSetup.starFile1 != "" and " " not in tabWidgetSetup.starFile1:
			with open(tabWidgetSetup.starFile1) as f7:
				starlines = f7.readlines()
		starlines_new = []
		with open("badjpeg_selected.log") as f2:
			lines = f2.readlines()
			for starline in starlines:
				n = 0
				missing = True
				try:
					while lines[n] not in starline and missing:
						n += 1
					else:
						missing = False
				except IndexError:
					starlines_new.append(starline)
		with open("micrographs_clean.star", "w+") as f8:
			f8.write(starlines_new)

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
					mrcName = jpegName.replace(".jpeg","*")
					mrcName = mrcName.replace(tabWidgetSetup.jpegDir1, tabWidgetSetup.micDir1)

					if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
						os.system("mv %s %s/tiffsTrash" % (tiffName,tabWidgetSetup.tiffDir1))
					os.system("mv %s %s/mrcTrash" % (mrcName,tabWidgetSetup.micDir1))
					os.system("mv %s %s/jpegTrash" % (jpegName,tabWidgetSetup.jpegDir1))

	def deleteMic(self):
		if self.jpeglist[self.i] in self.badjpeg:
			self.selectCheck.setChecked(False)
			self.label.setStyleSheet("QLabel {border: 0px solid red;}")
			with open("badjpeg_selected.log", "r") as f2:
				lines = f2.readlines()
			with open("badjpeg_selected.log", "w+") as f2:
				for line in lines:
					if line.strip("\n") != self.jpeglist[self.i].strip("\n"):
						f2.write(line)
		else:
			self.selectCheck.setChecked(True)
			self.label.setStyleSheet("QLabel {border: 5px solid red;}")
			with open("badjpeg_selected.log", "a+") as f2:
				f2.write(self.jpeglist[self.i])
				f2.seek(0)
		with open("badjpeg_selected.log") as f2:
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
		undoSelMessage = QMessageBox.question(self, 'Undo', "Undo ALL selected micrographs?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if undoSelMessage == QMessageBox.Yes:
			open("badjpeg_selected.log", "w").close()
			self.resetGUI()

	def invertSelected(self):
		invertSelMessage = QMessageBox.question(self, 'Invert', "Invert selection?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if invertSelMessage == QMessageBox.Yes:
			for line in self.jpeglist:
				if line not in self.badjpeg:
					with open("badjpeg_new.log" , "a+") as f6:
						f6.write(line)
			if sys.platform == 'win32':
				os.system("move badjpeg_new.log badjpeg_selected.log")
			else:
				os.system("mv badjpeg_new.log badjpeg_selected.log")
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
		if sys.platform == 'win32':
			os.system("move badjpeg_selected.log badjpeg_deleted_%s.log" % (fileNum))
			os.system("del jpeglist.txt")
		else:
			os.system("mv badjpeg_selected.log badjpeg_deleted_%s.log" % (fileNum))
			os.system("rm jpeglist.txt")
			
	def closeEvent(self, event):
		if sys.platform == 'win32':
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



class removeMics2(QMainWindow):
	def __init__(self,parent):
		super(removeMics2, self).__init__(parent)

		if sys.platform == 'win32':
			self.fullPath = os.path.abspath(tabWidgetSetup.jpegDir1)
			os.system("dir /b %s\*.jpeg > jpeglist.txt" % (self.fullPath))
			os.system("copy nul jpeglist_new.txt")
			with open("jpeglist.txt") as f1:
				self.jpegList = f1.readlines()
			with open("jpeglist_new.txt","a") as f3:
				for self.jpegFile in self.jpegList:
					f3.write(self.fullPath + "\\" + self.jpegFile)
			os.system("move jpeglist_new.txt jpeglist.txt")
		else:
			os.system("ls %s/*.jpeg > jpeglist.txt" % (tabWidgetSetup.jpegDir1))

		if os.path.isfile("badjpeg_selected.log") == False:
			if sys.platform == 'win32':
				os.system("copy nul badjpeg_selected.log")
			else:
				os.system("touch badjpeg_selected.log")

		with open("jpeglist.txt") as f1:
			self.jpeglist = f1.readlines()

		self.menu = self.menuBar()
		self.fileMenu = self.menu.addMenu('&File')
		self.importMenu = self.fileMenu.addAction("&Import log file")
		self.importMenu.triggered.connect(self.importLog)
		self.starMenu = self.fileMenu.addAction("&Export star file")
		self.StarMenu.triggered.connect(self.exportStar)
		if tabWidgetSetup.starFile1 != "" and " " not in tabWidgetSetup.starFile1:
			self.StarMenu.setDisabled(True)
		
		self.editMenu = self.menu.addMenu('&Edit')
		self.undoSelMenu = self.editMenu.addAction("&Undo all selected")
		self.undoSelMenu.triggered.connect(self.undoSelected)
		self.invertSelMenu = self.editMenu.addAction("&Invert selection")
		self.invertSelMenu.triggered.connect(self.invertSelected)

		if sys.platform == 'linux':
			self.trashMenu = self.fileMenu.addAction("&Trash all selected")
			self.trashMenu.triggered.connect(self.lastNext)
			self.deleteMenu = self.fileMenu.addAction("&Delete all trash directories")
			self.deleteMenu.triggered.connect(self.deleteTrash)
			
			self.undoTrashMenu = self.editMenu.addAction("&Undo all trashed")
			self.undoTrashMenu.triggered.connect(self.undoTrash)

		self.menu.show()
		self.i = 0
		self.viewJPEG2()

	def viewJPEG2(self):
		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()

		self.screenRes = app.desktop().screenGeometry()
		self.widRes, self.lenRes = self.screenRes.width(), self.screenRes.height()
		self.setGeometry(200, 200, self.widRes - 400, self.lenRes - 200)
		self.setWindowTitle("GemIO")

		self.scrollVWidget = QWidget()
		self.scrollVBox = QVBoxLayout()
		self.scrollArea = QScrollArea()

		self.i = 0
		self.labelList = {}
		self.jpegGrid()

		self.scrollVWidget.setLayout(self.scrollVBox)
		self.scrollArea.setWidget(self.scrollVWidget)
		self.setCentralWidget(self.scrollArea)

	def jpegGrid(self):
		self.scrollHWidget = QWidget()
		self.scrollHBox = QHBoxLayout()
		self.scrollHBox.setAlignment(QtCore.Qt.AlignLeft)
		for self.jpeg in self.jpeglist[self.i:self.i + tabWidgetSetup.jpegColumns1]:
			self.pixmap = QPixmap(self.jpeg.replace("\n",""))
			self.pixmapWScale = self.pixmap.width()*tabWidgetSetup.jpegScaling1
			self.pixmapHScale = self.pixmap.height()*tabWidgetSetup.jpegScaling1
			self.pixmap = self.pixmap.scaled(self.pixmapWScale,self.pixmapHScale, Qt.KeepAspectRatio)
			self.label = QLabel()
			self.label.resize(self.pixmapWScale, self.pixmapHScale)
			self.label.setPixmap(self.pixmap)
			self.labelList[self.jpeg.replace("\n","")] = self.label
			self.scrollHBox.addWidget(self.label)
		self.scrollHWidget.setLayout(self.scrollHBox)
		self.scrollVBox.addWidget(self.scrollHWidget)
		for jpegFile in self.labelList:
			self.labelList[jpegFile].mousePressEvent = lambda event, pixLabel = self.labelList[jpegFile], jpegFile = jpegFile: self.clickLabel(event,pixLabel,jpegFile)
		QtWidgets.QApplication.processEvents()
		try:
			self.jpeglist[self.i].replace("\n","")
			self.i = self.i + tabWidgetSetup.jpegColumns1
			self.jpegGrid()
		except IndexError:
			pass

	def clickLabel(self, event, pixLabel, jpegFile):
		if event.button() == Qt.LeftButton:
			if jpegFile + "\n" in self.badjpeg:
				pixLabel.setStyleSheet("QLabel {border: 0px solid red;}")
				with open("badjpeg_selected.log", "r") as f2:
					lines = f2.readlines()
				with open("badjpeg_selected.log", "w+") as f2:
					for line in lines:
						if line.strip("\n") != jpegFile:
							f2.write(line)
			else:
				pixLabel.setStyleSheet("QLabel {border: 5px solid red;}")
				with open("badjpeg_selected.log", "a+") as f2:
					f2.write(jpegFile + "\n")
					f2.seek(0)
		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()

	def importLog(self):
		self.importFile = QFileDialog.getOpenFileName(self, "Import log", "." , "Log files (*.log);;All files (*.*)")
		if self.importFile[0] != "":
			if sys.platform == 'win32':
				self.importFile = self.importFile[0].replace("/","\\")
				os.system("copy nul importFile_new.txt")
				with open(self.importFile) as f4:
					self.importBad = f4.readlines()
				with open("importFile_new.txt","a") as f5:
					for self.importMic in self.importBad:
						f5.write(self.fullPath + "\\" + self.importMic.rsplit("/",1)[-1].rsplit("\\",1)[-1])
				os.system("move importFile_new.txt badjpeg_selected.log")
			else:
				os.system("touch importFile_new.txt")
				with open(self.importFile[0]) as f4:
					self.importBad = f4.readlines()
				with open("importFile_new.txt","a") as f5:
					for self.importMic in self.importBad:
						f5.write(tabWidgetSetup.jpegDir1 + "/" + self.importMic.rsplit("/",1)[-1].rsplit("\\",1)[-1])
				os.system("mv importFile_new.txt badjpeg_selected.log")
		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()
		for jpegFile in self.labelList:
			self.labelList[jpegFile].setStyleSheet("QLabel {border: 0px solid red;}")
		for importedJPEG in self.badjpeg:
			self.labelList[importedJPEG.strip("\n")].setStyleSheet("QLabel {border: 5px solid red;}")

	def exportStar(self):
		if tabWidgetSetup.starFile1 != "" and " " not in tabWidgetSetup.starFile1:
			with open(tabWidgetSetup.starFile1) as f7:
				starlines = f7.readlines()
		starlines_new = []
		with open("badjpeg_selected.log") as f2:
			lines = f2.readlines()
			for starline in starlines:
				n = 0
				missing = True
				try:
					while lines[n] not in starline and missing:
						n += 1
					else:
						missing = False
				except IndexError:
					starlines_new.append(starline)
		with open("micrographs_clean.star", "w+") as f8:
			f8.write(starlines_new)

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
					mrcName = jpegName.replace(".jpeg","*")
					mrcName = mrcName.replace(tabWidgetSetup.jpegDir1, tabWidgetSetup.micDir1)

					if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
						os.system("mv %s %s/tiffsTrash" % (tiffName,tabWidgetSetup.tiffDir1))
					os.system("mv %s %s/mrcTrash" % (mrcName,tabWidgetSetup.micDir1))
					os.system("mv %s %s/jpegTrash" % (jpegName,tabWidgetSetup.jpegDir1))

	def deleteTrash(self):
		trashMessage = QMessageBox.question(self, 'Delete', "Delete trash directories?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if trashMessage == QMessageBox.Yes:
			if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
				os.system("rm -rf %s/tiffsTrash" % (tabWidgetSetup.tiffDir1))
			os.system("rm -rf %s/jpegTrash" % (tabWidgetSetup.jpegDir1))
			os.system("rm -rf %s/mrcTrash" % (tabWidgetSetup.micDir1))

	def undoSelected(self):
		undoSelMessage = QMessageBox.question(self, 'Undo', "Undo ALL selected micrographs?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if undoSelMessage == QMessageBox.Yes:
			open("badjpeg_selected.log", "w").close()
		for jpegFile in self.labelList:
			self.labelList[jpegFile].setStyleSheet("QLabel {border: 0px solid red;}")
		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()

	def invertSelected(self):
		invertSelMessage = QMessageBox.question(self, 'Invert', "Invert selection?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if invertSelMessage == QMessageBox.Yes:
			for line in self.jpeglist:
				if line not in self.badjpeg:
					with open("badjpeg_new.log" , "a+") as f6:
						f6.write(line)
					self.labelList[line.strip("\n")].setStyleSheet("QLabel {border: 5px solid red;}")
				else:
					self.labelList[line.strip("\n")].setStyleSheet("QLabel {border: 0px solid red;}")
			if sys.platform == 'win32':
				os.system("move badjpeg_new.log badjpeg_selected.log")
			else:
				os.system("mv badjpeg_new.log badjpeg_selected.log")
		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()

	def undoTrash(self):
		undoTrashMessage = QMessageBox.question(self, 'Undo Trash', "Undo ALL trashed micrographs?\nNote: This will also unselect all your selected micrographs.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if undoTrashMessage == QMessageBox.Yes:
			if tabWidgetSetup.tiffDir1 != "" and " " not in tabWidgetSetup.tiffDir1:
				os.system("mv %s/tiffsTrash/* %s" % (tabWidgetSetup.tiffDir1,tabWidgetSetup.tiffDir1))
			os.system("mv %s/jpegTrash/* %s" % (tabWidgetSetup.jpegDir1,tabWidgetSetup.jpegDir1))
			os.system("mv %s/mrcTrash/* %s" % (tabWidgetSetup.micDir1,tabWidgetSetup.micDir1))
			open("badjpeg_selected.log", "w").close()
		for jpegFile in self.labelList:
			self.labelList[jpegFile].setStyleSheet("QLabel {border: 0px solid red;}")
		with open("badjpeg_selected.log") as f2:
			self.badjpeg = f2.readlines()
			
	def saveLog(self):
		fileNum = 0
		while os.path.isfile("badjpeg_deleted_%s.log" % (fileNum)) == True:
			fileNum += 1
		if sys.platform == 'win32':
			os.system("move badjpeg_selected.log badjpeg_deleted_%s.log" % (fileNum))
			os.system("del jpeglist.txt")
		else:
			os.system("mv badjpeg_selected.log badjpeg_deleted_%s.log" % (fileNum))
			os.system("rm jpeglist.txt")
			
	def closeEvent(self, event):
		if sys.platform == 'win32':
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
