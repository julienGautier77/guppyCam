# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:56:20 2019

@author: loa
"""
from guppy import GUPPY
import sys
from PyQt5.QtWidgets import QApplication
import qdarkstyle

if __name__ == "__main__":       
    
    appli = QApplication(sys.argv) 
    appli.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    pathVisu='C:/Users/loa/Desktop/Python/guppyCam/guppyCam/confVisuFootPrint.ini'
    e = GUPPY(cam='cam1',confVisu=pathVisu) 
    e.show()
    appli.exec_() 