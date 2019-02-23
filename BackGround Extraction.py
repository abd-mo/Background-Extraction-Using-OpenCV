# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 15:40:12 2019

@author: abdelrahman
"""

import cv2
import numpy as np


#
class AverageBackground:
#
    def __init__(self,Capture):
        self.Capture=Capture
        
    def initial_frame(self):
        self._,self.Frame=self.Capture.read()
        self.AVG=np.float32(self.Frame)
        
    def AvgImage(self,lr):
        self._,self.Frame=self.Capture.read()
        cv2.accumulateWeighted(self.Frame,self.AVG,lr)
        self.Res=cv2.convertScaleAbs(self.AVG)
        return self.Frame,self.Res
    
    def get_capture(self):
        return self.Capture
    
    
class Calculate_Diff:
    def __init__(self):
        self.Background=AverageBackground(cv2.VideoCapture(0))
        self.cap=self.Background.get_capture()
        self.biggestCounter=None
        self.finger=0
         
    def Do_nothing(self,args):
        pass
    
    
    def Img_prossesing(self):
        
        lr=cv2.getTrackbarPos('Alpha','Frame Image')
        lr/=100000.0
        Frame,Avg =self.Background.AvgImage(lr)
        f_Gray=cv2.cvtColor(Frame,cv2.COLOR_BGR2GRAY)
        Avg_Gray=cv2.cvtColor(Avg,cv2.COLOR_BGR2GRAY)
        diff=cv2.absdiff(f_Gray,Avg_Gray)
        ret,thresh=cv2.threshold(diff,50,255,0)
        return Avg,Frame,thresh
    
    def Release_GUI(self):
        cv2.destroyAllWindows()
        self.cap.release
        
        
    def show_GUI(self):
        Avg,Frame,thresh=self.Img_prossesing()
        cv2.imshow("thresh Image",thresh)
        cv2.imshow("Frame Image",Frame)
        cv2.imshow("avgerage Background",Avg)
        
        
    def initial_GUI(self):
        cv2.namedWindow('Frame Image',flags=0)
        cv2.createTrackbar('Alpha','Frame Image',0,1000,self.Do_nothing)
        self.Background.initial_frame()
       
        
    def RUN(self):
        self.initial_GUI()
        while True:
            self.show_GUI()
            k=cv2.waitKey(20)
            if k==27:
                break
        self.Release_GUI()
        
pro=Calculate_Diff()
pro.RUN()