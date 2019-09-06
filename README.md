# guppyCam
guppyCam  module is a Python user interface for allied Vision's camera based on pymba : 
https://github.com/morefigs/pymba.git

install alliedVision SDK (https://www.alliedvision.com/en/products/software.html)

test on windows only

## Requirements
*   python 3.x
*   Numpy
*   PyQt5
*   pyqtgraph (https://github.com/pyqtgraph/pyqtgraph.git) 
    pip intall pyqtgraph
*   qdarkstyle (https://github.com/ColinDuquesnoy/QDarkStyleSheet.git)
    pip install qdarkstyle
*   pymba (https://github.com/morefigs/pymba.git )
    pip install pymba
*   visu (https://github.com/julienGautier77/visu)
    pip install visu
    
on pymba module modify vimba.camera :acquire_frame(self) : self._single_frame.wait_for_capture(1000000)


## Usage


    from PyQt5.QtWidgets import QApplication
    import sys
    import guppyCam
    appli = QApplication(sys.argv)   
    appli.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    e =guppyCam.GUPPY('camDefault')  
    e.show()
    appli.exec_() 

-----------------------------------------
-----------------------------------------
