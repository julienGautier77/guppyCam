#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 17:07:24 2019
Modified on Fri Mar  1 15:21:38 2019
a Python user interface for allied Vision's camera


install aliiedVision SDK (https://www.alliedvision.com/en/products/software.html)

on conda prompt 
pip install pymba (https://github.com/morefigs/pymba.git )
pip install qdarkstyle (https://github.com/ColinDuquesnoy/QDarkStyleSheet.git)
pip install pyqtgraph (https://github.com/pyqtgraph/pyqtgraph.git)
pip install visu
modify vimba.camera :acquire_frame(self) : self._single_frame.wait_for_capture(1000000)
and comment the line (?)(?)

@author: juliengautier
version : 2019.3
"""
__version__='Guppy_2019.3'
__author__='julien Gautier'
version=__version__

from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget,QPushButton
from PyQt5.QtWidgets import QComboBox,QSlider,QLabel,QSpinBox
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys,time
import numpy as np
import pathlib



try:
    from pymba import Vimba  ## pisee p install pymba https://github.com/morefigs/pymba.git 
    Vimba().startup()
    system=Vimba().system()
    cameraIds=Vimba().camera_ids()
    print( "Cam available:",cameraIds)
except:
    print ('No pymba module installed see : https://github.com/morefigs/pymba.git ')
    
try :
    from visu import SEE
except:
    print ('No visu module installed :see' )
    
import qdarkstyle


class GUPPY(QWidget):
    '''GUPPY class for allied vision Camera
    '''
    def __init__(self,cam='camDefault'):
        
        super(GUPPY, self).__init__()
        p = pathlib.Path(__file__)
        self.conf=QtCore.QSettings(str(p.parent / 'confCCD.ini'), QtCore.QSettings.IniFormat)
        self.icon=str(p.parent) + '/icons/'
        self.setWindowIcon(QIcon(self.icon+'LOA.png'))
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.nbcam=cam
        self.initCam()
        self.setup()
        self.itrig=0
        self.actionButton()
        self.camIsRunnig=False
        
        
    def initCam(self):
        '''initialisation of cam parameter 
        '''
        
        if self.nbcam=='camDefault':
            try:
                self.cam0=Vimba().camera(cameraIds[0])
                self.ccdName='CAM0'
                self.camID=cameraIds[0]
                self.isConnected=True
            except:
                self.isConnected=False
                self.ccdName='no camera'
        else :
            self.camID=self.conf.value(self.nbcam+"/camID") ## read cam serial number
            try :
                self.cam0=Vimba().camera(self.camID)
                self.ccdName=self.conf.value(self.nbcam+"/nameCDD")
                self.isConnected=True
            except:# if it doesn't work we take the first one
                try:
                    self.nbcam='camDefault'
                    self.cam0=Vimba().camera(cameraIds[0])
                    self.ccdName='CAM0'
                    self.camID=cameraIds[0]
                    self.isConnected=True
                except:
                    print('not ccd connected')
                    self.isConnected=False
                    self.ccdName='no camera'
                    
        
        self.setWindowTitle(self.ccdName+'       v.'+ version)
        if self.isConnected==True:
            print(self.ccdName, 'is connected @:'  ,self.camID )
            self.cam0.open()
            ## init cam parameter##
            self.LineTrigger=str(self.conf.value(self.nbcam+"/LineTrigger")) # line2 for Mako Line 1 for guppy (not tested)
            self.cam0.feature('ExposureTime').value=float(self.conf.value(self.nbcam+"/shutter"))*1000
            self.cam0.feature('Gain').value=int(self.conf.value(self.nbcam+"/gain"))
            self.cam0.feature('TriggerMode').value='Off'
            self.cam0.feature('TriggerActivation').value='RisingEdge'
            self.cam0.feature('TriggerSelector').value='FrameStart'
            self.cam0.feature('TriggerSource').value='Software'
        
        
    def setup(self):  
        """ user interface definition: 
        """
        vbox1=QVBoxLayout() 
       
        self.camName=QLabel(self.ccdName,self)
        self.camName.setAlignment(Qt.AlignCenter)
        
        self.camName.setStyleSheet('font :bold  30pt;color: white')
        vbox1.addWidget(self.camName)
        
        hbox1=QHBoxLayout() # horizontal layout pour run et stop
        self.runButton=QPushButton(self)
        self.runButton.setMaximumWidth(60)
        self.runButton.setMinimumHeight(60)
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(%s);background-color: rgb(0, 0, 0,0) ;border-color: green;}""QPushButton:pressed{image: url(%s);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}"% (self.icon+'Play.svg',self.icon+'Play.svg') )
        self.stopButton=QPushButton(self)
        
        self.stopButton.setMaximumWidth(60)
        self.stopButton.setMinimumHeight(60)
        self.stopButton.setStyleSheet("QPushButton:!pressed{border-image: url(%s);background-color: gray ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(%s);background-color: gray ;border-color: rgb(0, 0, 0)}"% (self.icon+'Stop.svg',self.icon+'Stop.svg') )
        self.stopButton.setEnabled(False)
        
        hbox1.addWidget(self.runButton)
        hbox1.addWidget(self.stopButton)
        
        vbox1.addLayout(hbox1)
        
        self.trigg=QComboBox()
        self.trigg.setMaximumWidth(60)
        self.trigg.addItem('OFF')
        self.trigg.addItem('ON')
        self.labelTrigger=QLabel('Trigger')
        self.labelTrigger.setMaximumWidth(60)
        self.itrig=self.trigg.currentIndex()
        hbox2=QHBoxLayout()
        hbox2.addWidget(self.labelTrigger)
        hbox2.addWidget(self.trigg)
        vbox1.addLayout(hbox2)
        
        self.labelExp=QLabel('Exposure (ms)')
        self.labelExp.setMaximumWidth(120)
        self.labelExp.setAlignment(Qt.AlignCenter)
        vbox1.addWidget(self.labelExp)
        self.hSliderShutter=QSlider(Qt.Horizontal)
        self.hSliderShutter.setMinimum(1)
        self.hSliderShutter.setMaximum(1000)
        if self.isConnected==True:
            self.hSliderShutter.setValue(int(self.cam0.feature('ExposureTime').value)/1000)
        self.hSliderShutter.setMaximumWidth(80)
        self.shutterBox=QSpinBox()
        self.shutterBox.setMinimum(1)
        self.shutterBox.setMaximum(1000)
        self.shutterBox.setMaximumWidth(60)
        if self.isConnected==True:
            self.shutterBox.setValue(int(self.cam0.feature('ExposureTime').value)/1000)
        hboxShutter=QHBoxLayout()
        hboxShutter.addWidget(self.hSliderShutter)
        hboxShutter.addWidget(self.shutterBox)
        vbox1.addLayout(hboxShutter)
        
        self.labelGain=QLabel('Gain')
        self.labelGain.setMaximumWidth(120)
        self.labelGain.setAlignment(Qt.AlignCenter)
        vbox1.addWidget(self.labelGain)
        hboxGain=QHBoxLayout()
        self.hSliderGain=QSlider(Qt.Horizontal)
        self.hSliderGain.setMaximumWidth(80)
        if self.isConnected==True:
            self.hSliderGain.setMinimum(self.cam0.feature('Gain').range[0])
            self.hSliderGain.setMaximum(self.cam0.feature('Gain').range[1])
            self.hSliderGain.setValue(int(self.cam0.feature('Gain').value))
        self.gainBox=QSpinBox()
        if self.isConnected==True:
            self.gainBox.setMinimum(self.cam0.feature('Gain').range[0])
            self.gainBox.setMaximum(self.cam0.feature('Gain').range[1])
        self.gainBox.setMaximumWidth(60)
        if self.isConnected==True:
            self.gainBox.setValue(int(self.cam0.feature('Gain').value))
        hboxGain.addWidget(self.hSliderGain)
        hboxGain.addWidget(self.gainBox)
        vbox1.addLayout(hboxGain)
        
        self.TrigSoft=QPushButton('Trig Soft',self)
        self.TrigSoft.setMaximumWidth(100)
        vbox1.addWidget(self.TrigSoft)
        
        vbox1.addStretch(1)
        hMainLayout=QHBoxLayout()
        hMainLayout.addLayout(vbox1)
        
        
        self.visualisation=SEE() ## Widget for visualisation and tools 
        
        vbox2=QVBoxLayout() 
        vbox2.addWidget(self.visualisation)
        hMainLayout.addLayout(vbox2)
        
        self.setLayout(hMainLayout)
        
        
    def actionButton(self): 
        '''action when button are pressed
        '''
        self.runButton.clicked.connect(self.acquireMultiImage)
        self.stopButton.clicked.connect(self.stopAcq)      
        self.shutterBox.editingFinished.connect(self.shutter)    
        self.hSliderShutter.sliderReleased.connect(self.mSliderShutter)
        
        self.gainBox.editingFinished.connect(self.gain)    
        self.hSliderGain.sliderReleased.connect(self.mSliderGain)
        self.trigg.currentIndexChanged.connect(self.trigA)
        
        self.TrigSoft.clicked.connect(self.softTrigger)
    
    
    def softTrigger(self):
        '''to have a sofware trigger
        '''
        print('trig soft')
        self.cam0.feature('TriggerSource').value='Software'
        self.cam0.run_feature_command('TriggerSoftware') 
        if self.itrig==1:
            self.cam0.feature('TriggerSource').value=self.LineTrigger
    
    def shutter (self):
        '''set exposure time 
        '''
        sh=self.shutterBox.value() # 
        self.hSliderShutter.setValue(sh) # set value of slider
        time.sleep(0.1)
        if self.isConnected==True:
            self.cam0.feature('ExposureTime').value=float(sh*1000) # Set shutter CCD in microseconde
        self.conf.setValue(self.nbcam+"/shutter",float(sh))
        self.conf.sync()
    
    def mSliderShutter(self): # for shutter slider 
        sh=self.hSliderShutter.value() 
        self.shutterBox.setValue(sh) # 
        time.sleep(0.1)
        self.cam0.feature('ExposureTime').value=float(sh*1000) # Set shutter CCD in microseconde
        self.conf.setValue(self.nbcam+"/shutter",float(sh))
    
    def gain (self):
        '''set gain
        '''
        g=self.gainBox.value() # 
        self.hSliderGain.setValue(g) # set slider value
        time.sleep(0.1)
        self.cam0.feature('Gain').value=g
        
        print( "gain ", self.cam0.feature('Gain').value)
        self.conf.setValue(self.nbcam+"/gain",float(g))
        self.conf.sync()
    
    def mSliderGain(self):
        g=self.hSliderGain.value()
        self.gainBox.setValue(g) # set valeur de la box
        time.sleep(0.1)
        self.cam0.feature('Gain').value=g
        print( "gain ", self.cam0.feature('Gain').value)
        self.conf.setValue(self.nbcam+"/gain",float(g))
        self.conf.sync()
        
    def trigA(self):
        '''to select trigger mode
        '''
        self.itrig=self.trigg.currentIndex()
        if self.itrig==1:
            self.cam0.feature('TriggerMode').value='On'
            self.cam0.feature('TriggerSource').value=self.LineTrigger
        else:
            self.cam0.feature('TriggerMode').value='Off'
            
            
    def acquireMultiImage(self):    
        ''' start the acquisition thread
        '''
        self.runButton.setEnabled(False)
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(%s);background-color: gray ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(%s);background-color: gray ;border-color: rgb(0, 0, 0)}"%(self.icon+'Play.svg',self.icon+'Play.svg'))
        
        self.stopButton.setEnabled(True)
        self.stopButton.setStyleSheet("QPushButton:!pressed{border-image: url(%s);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(%s);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}"%(self.icon+'Stop.svg',self.icon+'Stop.svg') )
        
        self.trigg.setEnabled(False)
        self.threadRunAcq=ThreadRunAcq(cam0=self.cam0,itrig=self.itrig,LineTrigger=self.LineTrigger)
        self.threadRunAcq.newDataRun.connect(self.Display)
        self.threadRunAcq.start()
        self.camIsRunnig=True 
  
    
    def stopAcq(self):
        '''Stop     acquisition
        '''
        print('stop')
        if self.camIsRunnig==True:
            self.threadRunAcq.stopThreadRunAcq()
            self.camIsRunnig=False
            
        self.runButton.setEnabled(True)
        self.runButton.setStyleSheet("QPushButton:!pressed{border-image: url(%s);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(%s);background-color: rgb(0, 0, 0,0) ;border-color: rgb(0, 0, 0)}"%(self.icon+'Play.svg',self.icon+'Play.svg'))
        self.stopButton.setEnabled(False)
        self.stopButton.setStyleSheet("QPushButton:!pressed{border-image: url(%s);background-color: gray ;border-color: rgb(0, 0, 0,0);}""QPushButton:pressed{image: url(%s);background-color: gray ;border-color: rgb(0, 0, 0)}"%(self.icon+'Stop.svg',self.icon+'Stop.svg') )
        
        self.trigg.setEnabled(True)
        
    def Display(self,data):
        '''Display data with Visu module
        '''
        self.data=data
        self.visualisation.newDataReceived(self.data) # send data to visualisation widget
        
    def closeEvent(self,event):
        ''' closing window event (cross button)
        '''
        print(' close')
        self.stopAcq()
        time.sleep(0.1)
        if self.isConnected==True:
            self.cam0.close()
        
        
        
class ThreadRunAcq(QtCore.QThread):
    '''Second thread for controling acquisition independtly
    '''
    newDataRun=QtCore.Signal(object)
    
    def __init__(self, parent=None,cam0=None,itrig=None,LineTrigger='Line2'):
        
        super(ThreadRunAcq,self).__init__(parent)
        self.cam0 = cam0
        self.stopRunAcq=False
        self.itrig= itrig
        self.LineTrigger=LineTrigger
        
    def run(self):
        
        while self.stopRunAcq is not True :
            self.cam0.arm('SingleFrame')
            dat1=self.cam0.acquire_frame()     

            if dat1 is not None:
                data=dat1.buffer_data_numpy()
                data=np.rot90(data,3)
                if self.stopRunAcq==True:
                    pass
                else :
                    self.newDataRun.emit(data)
            self.cam0.disarm()
            
    def stopThreadRunAcq(self):
        #self.cam0.send_trigger()
        self.stopRunAcq=True
        self.cam0.feature('TriggerSource').value='Software'
        self.cam0.run_feature_command('TriggerSoftware')
        self.cam0.feature('TriggerSource').value=self.LineTrigger
        self.cam0.run_feature_command ('AcquisitionAbort')
            
    
if __name__ == "__main__":       
    
    appli = QApplication(sys.argv) 
    appli.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    e = GUPPY('camDefault')  
    e.show()
    appli.exec_()       
    
    