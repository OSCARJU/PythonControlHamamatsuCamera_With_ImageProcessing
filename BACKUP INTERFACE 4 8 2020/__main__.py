import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from HMIV1 import Ui_MainWindow
from functools import partial
try:
    import queue as Queue
except ImportError:
    import Queue as Queue
import numpy as np
import CameraInterfaces
import time

import cv2
import os
from os.path import isfile, join
import json
#from matplotlib import pyplot as plt
# from multiprocessing import Queue


class Main(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.PBCheckCam.clicked.connect( self.Check_Camera)
        self.ui.CBCamera.currentTextChanged.connect(self.Camera_Settings)
        self.ui.PBReset.clicked.connect( self.Reset_Settings)
        self.ui.CBCamera.activated.connect(self.Live_Button)
        self.ui.PBLive.clicked.connect(self.preview_slot)
        self.ui.PBLive_2.clicked.connect(self.preview_slot)
        self.ui.PBApply.clicked.connect(self.bgkSubtractor)
        self.ui.PBApply.clicked.connect(self.Set_Camera_Settings)
        self.ui.PBApply.clicked.connect(self.update_preview)
        self.ui.PBApplyBGK.clicked.connect(self.update_preview)


        #self.ui.PBApply.clicked.connect(self.update_preview)
        self.ui.CBBinning.currentTextChanged.connect(self.Camera_Settings)
        self.ui.CBBinning_2.currentTextChanged.connect(self.Camera_Settings)
        self.ui.PBSetF.clicked.connect(self.set_img_seq_save_path)
        self.ui.PBAcquire.clicked.connect(self.acquire_slot)
        self.ui.TBBGK.currentChanged.connect(self.setTabBKG)

        self.ui.PBFolderFrame.clicked.connect(self.get_img_seq_path)
        self.ui.PBOutputF.clicked.connect(self.get_vid_path)
        self.ui.PBMakeV.clicked.connect(self.convert_frames_to_video)

        self.ui.PBFolderVideo.clicked.connect(self.get_video_path)
        self.ui.PBOutputV.clicked.connect(self.get_frames_path)
        self.ui.PBFrames.clicked.connect(self.convert_video_to_frames)
        self.__version__ = '4107ff58a0c3d4d5d3c15c3d6a69f8798a20e3de'

        self.ui.TlistFrame.clicked.connect(self.Plot_Frame)
        self.ui.PBPVideo.clicked.connect(self.BackgroundSettings)
        self.ui.PBPVideo.clicked.connect(self.PlayVideo)
        self.ui.PBResetLive.clicked.connect(self.StopReset)
        self.ui.PBReset_2.clicked.connect(self.StopVideo)

        self.ui.PBFramesVideo.clicked.connect(self.GetFrames)
        self.ui.TlistVideo.clicked.connect(self.GetVideoInfo)

        self.ui.GVImage.setLevels(0, 256)
        self.ui.TWImageA.setLevels(0, 256)
        self.ui.TWImageB.setLevels(0, 256)
        self.ui.TWImageC.setLevels(0, 256)
        self.ui.TWImageD.setLevels(0, 256)




#FUNCTION TO READ PARAMETERS
    #to confirm the size of the vide
    def GetVideoInfo(self):
        pathIn = self.ui.LEPATHVideo.text()
        print(pathIn)
        dirmodel = QtWidgets.QFileSystemModel(self)
        dirmodel.setRootPath(pathIn)
        indexvideo = self.ui.TlistVideo.currentIndex()
        print(indexvideo)
        VideoName = dirmodel.fileName(indexvideo)
        VideofilePath = dirmodel.filePath(indexvideo)
        name, ext = os.path.splitext(VideoName)
        print(VideoName)
        print(VideofilePath)
        if ext == '.avi':
            Video = cv2.VideoCapture(VideofilePath)
            NUMBER = int(Video.get(cv2.CAP_PROP_FRAME_COUNT))
            print(NUMBER)
            self.length = int(Video.get(cv2.CAP_PROP_FRAME_COUNT))
            print(VideoName)
            print(VideofilePath)
            print(self.length)
        else:
            print('no video')

    ###folder to save image sequence
    def CreateBFfolder(self):
        pathIn = self.ui.LEOutPathV.text()
        # dirmodel = QtWidgets.QFileSystemModel(self)
        # dirmodel.setRootPath(pathIn)
        Mean_Dir = (os.path.dirname(pathIn))
        FolderNameM = (os.path.basename(pathIn.rsplit('.', 1)[0]))
        FileName = os.path.basename(pathIn)
        if (self.ui.RBImage.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Original Frames ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTCNT.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background CNT ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTGMG.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background GMG ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTGSOC.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background GSOC ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTKNN.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background KNN ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTLSBP.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background LSBP ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTMOG.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background MOG ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTMOG2.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background MOG2 ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTRNB.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background RNB ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTFZBL.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background FZBL ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName
        if (self.ui.RBTFZB.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Background FZB ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                # self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            path = FolderPathM + '/' + FileName

        return path
    def CreateFolder(self):
        pathIn = self.CreateBFfolder()
        # dirmodel = QtWidgets.QFileSystemModel(self)
        # dirmodel.setRootPath(pathIn)
        Mean_Dir = (os.path.dirname(pathIn))
        FolderNameM = (os.path.basename(pathIn.rsplit('.', 1)[0]))
        FileName = os.path.basename(pathIn)
        if(self.ui.RBOGetFrame.isChecked()==True):
            FolderPathM = Mean_Dir + '/' + 'Original Frames '+ FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                #self.OriginalFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            self.OriginalFrame = FolderPathM + '/' + FileName
        if (self.ui.RBISGetFrame.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Subtractor Frames ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                #self.SubtractorFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            self.SubtractorFrame = FolderPathM + '/' + FileName
        if (self.ui.RBFGetFrame.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + 'Foreground Frames ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                #self.ForegroundFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            self.ForegroundFrame = FolderPathM + '/' + FileName
        if (self.ui.RBBGetFrame.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + ' Background Frames ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                #self.BackgroundFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            self.BackgroundFrame = FolderPathM + '/' + FileName
        if (self.ui.RBLGetFrame.isChecked() == True):
            FolderPathM = Mean_Dir + '/' + ' Lapse Frames ' + FolderNameM
            # Create target Directory if don't exist
            if not os.path.exists(FolderPathM):
                os.mkdir(FolderPathM)
                #self.LapseFrame = FolderPathM
                print("Directory ", FolderPathM, " Created ")
            else:
                print("Directory ", FolderPathM, " already exists")
            self.LapseFrame = FolderPathM + '/' + FileName
    #MAKE FRAMES FROM OPTION IN UI
    def Vid2FrameSave(self):
        self.exitvideo = False
        if self.ui.PBFramesVideo.text() == 'Get Frames':
            #self.pause_video = 'q'
            self.ui.PBFramesVideo.setText('Processing')

            ### background options
            ### background options
            # BACKGROUND CNT
            if False:
                self.fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(minPixelStability=15,
                                                                     useHistory=True,
                                                                     maxPixelStability=15 * 60,
                                                                     isParallel=True)
                # BACKGROUND GMG
                self.fgbgGMG = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=1,
                                                                        decisionThreshold=0.8)
                # BackgroundGSOC
                self.fgbgGSOC = cv2.bgsegm.createBackgroundSubtractorGSOC(nSamples=20,
                                                                          replaceRate=0.003,
                                                                          propagationRate=0.01,
                                                                          hitsThreshold=32,
                                                                          alpha=0.01,
                                                                          beta=0.0022,
                                                                          blinkingSupressionDecay=0.1,
                                                                          blinkingSupressionMultiplier=0.1,
                                                                          noiseRemovalThresholdFacBG=0.0004,
                                                                          noiseRemovalThresholdFacFG=0.0008)
                # BackgroundKNN
                self.fgbgKNN = cv2.createBackgroundSubtractorKNN(history=500,
                                                                 dist2Threshold=400.0,
                                                                 detectShadows=True)
                # BackgroundLSBP
                self.fgbgLSBP = cv2.bgsegm.createBackgroundSubtractorLSBP(nSamples=20,
                                                                          LSBPRadius=16,
                                                                          Tlower=2.0,
                                                                          Tupper=32.0,
                                                                          Tinc=1.0,
                                                                          Tdec=0.05,
                                                                          Rscale=10.0,
                                                                          Rincdec=0.005,
                                                                          noiseRemovalThresholdFacBG=0.0004,
                                                                          noiseRemovalThresholdFacFG=0.0008,
                                                                          LSBPthreshold=8,
                                                                          minCount=2)
                # BackgroundMOG
                self.fgbgMOG = cv2.bgsegm.createBackgroundSubtractorMOG(history=200,
                                                                        nmixtures=5,
                                                                        backgroundRatio=0.7,
                                                                        noiseSigma=0)
                self.fgbgMOG2 = cv2.createBackgroundSubtractorMOG2(history=500,
                                                                   varThreshold=16,
                                                                   detectShadows=True)
            ###values of parameters
            self.fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(minPixelStability=self.minPixelStabilityCNT,
                                                                 useHistory=self.useHistoryCNT,
                                                                 maxPixelStability=self.maxPixelStabilityCNT,
                                                                 isParallel=self.isParallelCNT)
            # BACKGROUND GMG
            self.fgbgGMG = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=self.initializationFramesGMG,
                                                                    decisionThreshold=self.decisionThresholdGMG)
            # BackgroundGSOC
            self.fgbgGSOC = cv2.bgsegm.createBackgroundSubtractorGSOC(nSamples=self.nSamplesGSOC,
                                                                      replaceRate=self.replaceRateGSOC,
                                                                      propagationRate=self.propagationRateGSOC,
                                                                      hitsThreshold=self.hitsThresholdGSOC,
                                                                      alpha=self.alphaGSOC,
                                                                      beta=self.betaGSOC,
                                                                      blinkingSupressionDecay=0.1,
                                                                      blinkingSupressionMultiplier=0.1,
                                                                      noiseRemovalThresholdFacBG=0.0004,
                                                                      noiseRemovalThresholdFacFG=0.0008)
            # BackgroundKNN
            self.fgbgKNN = cv2.createBackgroundSubtractorKNN(history=self.historyKNN,
                                                             dist2Threshold=self.dist2ThresholdKNN,
                                                             detectShadows=self.detectShadowsKNN)
            # BackgroundLSBP
            self.fgbgLSBP = cv2.bgsegm.createBackgroundSubtractorLSBP(nSamples=self.nSamplesLSBP,
                                                                      LSBPRadius=self.LSBPRadius,
                                                                      Tlower=2.0,
                                                                      Tupper=self.TupperLSBP,
                                                                      Tinc=1.0,
                                                                      Tdec=0.05,
                                                                      Rscale=self.RscaleLSBP,
                                                                      Rincdec=0.005,
                                                                      noiseRemovalThresholdFacBG=0.0004,
                                                                      noiseRemovalThresholdFacFG=0.0008,
                                                                      LSBPthreshold=self.LSBPthreshold,
                                                                      minCount=self.minCountLSBP)
            # BackgroundMOG
            self.fgbgMOG = cv2.bgsegm.createBackgroundSubtractorMOG(history=self.historyMOG,
                                                                    nmixtures=self.nmixturesMOG,
                                                                    backgroundRatio=self.backgroundRatioMOG,
                                                                    noiseSigma=self.noiseSigmaMOG)
            self.fgbgMOG2 = cv2.createBackgroundSubtractorMOG2(history=self.historyMOG2,
                                                               varThreshold=self.varThresholdMOG2,
                                                               detectShadows=self.detectShadowsMOG2)

            first_img = True
            first_imgR = True
            first_imgFL = True
            first_imgF = True
            first_imgMOG = True
            first_imgGMG = True

            ####
            # find video in list
            pathIn = self.ui.LEPATHVideo.text()
            dirmodel = QtWidgets.QFileSystemModel(self)
            dirmodel.setRootPath(pathIn)
            indexvideo = self.ui.TlistVideo.currentIndex()
            VideoName = dirmodel.fileName(indexvideo)
            VideofilePath = dirmodel.filePath(indexvideo)
            Video = cv2.VideoCapture(VideofilePath)
            self.length = int(Video.get(cv2.CAP_PROP_FRAME_COUNT))
            print(self.length)
            success = 1
            cont = 0
            frameNum = 0
            endVideo = True
            while endVideo:
                ##frameNum = 1 + frameNum
                print(frameNum)
                if self.exitvideo == True:
                    Video.release()
                    endVideo = False
                    break
                ValueBar = (frameNum * 100) / self.length
                self.ui.PGBSaving.setValue(ValueBar)
                if frameNum == self.length:
                    Video.release()
                    endVideo = False
                    break
                ret, frame = Video.read()
                if not ret:
                    break
                Image2Plot = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #Image2Plot = cv2.rotate(Image2Plot, cv2.ROTATE_90_COUNTERCLOCKWISE)
                #Image2Plot = cv2.rotate(Image2Plot, cv2.ROTATE_90_CLOCKWISE)
                img = Image2Plot
                # here the image will be shown
                # if self.ui.TWImageV.currentIndex() == 0:
                print(self.ui.TWImageV.currentIndex())
                if False:
                    self.bgkSubtractor()
                    if (self.subtractor <= 8):
                        if (self.subtractor == 3):
                            if (self.subtractor == 3 and self.imagedisplay == 3):
                                if first_imgGMG:
                                    self.ForegroundGMG = img
                                    first_imgGMG = False
                                else:
                                    self.ForegroundGMG = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                                img = self.ForegroundGMG
                            else:
                                first_imgGMG = True
                                img = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                        if (self.subtractor == 7):
                            if (self.subtractor == 7 and self.imagedisplay == 3):
                                if first_imgMOG:
                                    self.ForegroundMOG = img
                                    first_imgMOG = False
                                else:
                                    self.ForegroundMOG = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                                img = self.ForegroundMOG
                            else:
                                first_imgMOG = True
                                img = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                        if (self.subtractor != 3 and self.subtractor != 7):
                            first_imgGMG = True
                            first_imgMOG = True
                            img = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                    #
                    # Running fuzzy  lineal
                    if (self.subtractor == 10):
                        Thu = 30
                        Ths = 30
                        Thfs = 0.4
                        alphamin = 0.9
                        Height, Width = img.shape
                        InputImage = np.asarray(img, dtype=np.float32)
                        if first_imgFL:
                            Background_Image = InputImage
                            Background_Updated = np.zeros((Height, Width))
                            Background_Updated = np.asarray(Background_Updated,
                                                            dtype=np.float32)
                            Result_Comparison = np.zeros((Height, Width))
                            Result_Comparison = np.asarray(Result_Comparison,
                                                           dtype=np.float32)
                            Background_Substraction = np.zeros((Height, Width))
                            Background_Substraction = np.asarray(Result_Comparison,
                                                                 dtype=np.float32)
                            alpha = np.zeros((Height, Width))
                            alpha = np.asarray(Result_Comparison,
                                               dtype=np.float32)
                            Saturating_Limiter = np.zeros((Height, Width))
                            Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                            Fuzzy_Background_Substraction = np.zeros((Height, Width))
                            Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                            first_imgFL = False

                        else:
                            Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                        Background_Image))
                            Saturating_Limiter = np.divide(Result_Comparison, Ths)
                            Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                     np.ones((Height, Width)),
                                                                     Saturating_Limiter)
                            Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                                Fuzzy_Background_Substraction, (3, 3)))

                            Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                               np.ones((Height, Width)), 0)
                            alpha = 1 + np.multiply(0.1, (np.subtract(Fuzzy_Background_Substraction, 1)))
                            Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                                (1 - alpha), InputImage))
                            Background_Image = Background_Updated
                        if (self.imagedisplay == 1):
                            img = img
                        if (self.imagedisplay == 2):
                            img = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        if (self.imagedisplay == 3):
                            img = np.asarray(Background_Image, dtype=np.uint8)
                        if (self.imagedisplay == 4):
                            bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                            fmg = np.asarray(Background_Image, dtype=np.uint8)
                            # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                            img = cv2.addWeighted(fmg, 0.25,
                                                  (np.where(bmg > fmg, img, 0)), 0.75, 0)

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                    else:
                        first_imgFL = True

                    # Running Fuzzy logic
                    if (self.subtractor == 11):
                        Thu = 30
                        Ths = 30
                        Thfs = 0.4
                        alphamin = 0.9
                        Height, Width = img.shape
                        InputImage = np.asarray(img, dtype=np.float32)
                        if first_imgF:
                            Background_Image = InputImage
                            Background_Updated = np.zeros((Height, Width))
                            Background_Updated = np.asarray(Background_Updated,
                                                            dtype=np.float32)
                            Result_Comparison = np.zeros((Height, Width))
                            Result_Comparison = np.asarray(Result_Comparison,
                                                           dtype=np.float32)
                            Background_Substraction = np.zeros((Height, Width))
                            Background_Substraction = np.asarray(Result_Comparison,
                                                                 dtype=np.float32)
                            alpha = np.zeros((Height, Width))
                            alpha = np.asarray(Result_Comparison,
                                               dtype=np.float32)
                            Saturating_Limiter = np.zeros((Height, Width))
                            Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                            Fuzzy_Background_Substraction = np.zeros((Height, Width))
                            Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                            first_imgF = False
                        else:
                            Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                        Background_Image))
                            Saturating_Limiter = np.divide(Result_Comparison, Ths)
                            Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                     np.ones((Height, Width)),
                                                                     Saturating_Limiter)
                            Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                                Fuzzy_Background_Substraction, (3, 3)))
                            Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                               np.ones((Height, Width)), 0)
                            alpha = np.subtract(1, np.multiply(
                                (1 - alphamin), np.exp(np.multiply(-5, Fuzzy_Background_Substraction))))
                            Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                                (1 - alpha), InputImage))
                            Background_Image = Background_Updated
                            # img = np.asarray(Background_Image, dtype=np.uint8)
                            # img = np.multiply(Background_Substraction, 255)
                        if (self.imagedisplay == 1):
                            img = img
                        if (self.imagedisplay == 2):
                            img = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        if (self.imagedisplay == 3):
                            img = np.asarray(Background_Image, dtype=np.uint8)
                        if (self.imagedisplay == 4):
                            bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                            fmg = np.asarray(Background_Image, dtype=np.uint8)
                            # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                            img = cv2.addWeighted(fmg, 0.25,
                                                  (np.where(bmg > fmg, img, 0)), 0.75, 0)

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                    else:
                        first_imgF = True

                    # Running average
                    if self.subtractor == 9:
                        alpha = 0.9
                        Thu = 30
                        Ths = 30
                        Frame = img
                        if first_imgR:
                            Background_Image = Frame.astype(np.float32)
                            Background_Substraction = np.zeros((Frame.shape[0], Frame.shape[1]))
                            first_imgR = False
                        else:
                            Result_Comparison = cv2.absdiff(Frame.astype(np.float32), Background_Image)
                            Background_Substraction = np.where(Result_Comparison > Ths,
                                                               np.ones((Frame.shape[0], Frame.shape[1])), 0)
                            Background_Updated = cv2.add(np.multiply(alpha, Background_Image),
                                                         np.multiply((1 - alpha), Frame.astype(np.float32)))
                            Running_Average_Method = np.where(Result_Comparison < Thu,
                                                              Background_Updated, Background_Image)
                            Background_Image = Running_Average_Method
                            # img = np.multiply(Background_Substraction,255)
                        if (self.imagedisplay == 1):
                            img = img
                        if (self.imagedisplay == 2):
                            img = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        if (self.imagedisplay == 3):
                            img = np.asarray(Background_Image, dtype=np.uint8)
                        if (self.imagedisplay == 4):
                            bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                            fmg = np.asarray(Background_Image, dtype=np.uint8)
                            # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                            img = cv2.addWeighted(fmg, 0.25,
                                                  (np.where(bmg > fmg, img, 0)), 0.75, 0)

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25, img, 0.75, 0)
                        # img = np.asarray(Background_Image, dtype=np.uint8)
                    else:
                        first_imgR = True

                    if (self.lapse == True):
                        if (cont == 0):
                            img0 = img
                            cont = 1
                        else:
                            img0 = cv2.addWeighted(img0, 0.95, img, 0.05, 0)
                        img = img0
                        # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    else:
                        cont = 0
                    ###end of tab 1
                # tab 2

                self.bgkSubtractor()
                if (self.subtractor <= 8):
                    if (self.subtractor == 3):
                        BGKimg = self.ImageBackground(img, self.subtractor, 2)
                        if first_imgGMG:
                            self.ForegroundGMG = img
                            first_imgGMG = False
                        else:
                            self.ForegroundGMG = self.ImageBackground(img, self.subtractor, 3)
                        FRGimg = self.ForegroundGMG
                        SUBimg = self.ImageBackground(img, self.subtractor, 4)

                    if (self.subtractor == 7):
                        BGKimg = self.ImageBackground(img, self.subtractor, 2)
                        if first_imgMOG:
                            self.ForegroundMOG = img
                            first_imgMOG = False
                        else:
                            self.ForegroundMOG = self.ImageBackground(img, self.subtractor, 3)
                        FRGimg = self.ForegroundMOG
                        SUBimg = self.ImageBackground(img, self.subtractor, 4)

                    if (self.subtractor != 3 and self.subtractor != 7):
                        first_imgGMG = True
                        first_imgMOG = True
                        BGKimg = self.ImageBackground(img, self.subtractor, 2)
                        FRGimg = self.ImageBackground(img, self.subtractor, 3)
                        SUBimg = self.ImageBackground(img, self.subtractor, 4)

                #
                # Running fuzzy  lineal
                if (self.subtractor == 10):
                    Thu = 30
                    # Ths = 30
                    # Thfs = 0.4
                    Ths = self.ThsFZBL
                    Thfs = self.ThfsFZBL
                    alphamin = 0.9
                    Height, Width = img.shape
                    InputImage = np.asarray(img, dtype=np.float32)
                    if first_imgFL:
                        Background_Image = InputImage
                        Background_Updated = np.zeros((Height, Width))
                        Background_Updated = np.asarray(Background_Updated,
                                                        dtype=np.float32)
                        Result_Comparison = np.zeros((Height, Width))
                        Result_Comparison = np.asarray(Result_Comparison,
                                                       dtype=np.float32)
                        Background_Substraction = np.zeros((Height, Width))
                        Background_Substraction = np.asarray(Result_Comparison,
                                                             dtype=np.float32)
                        alpha = np.zeros((Height, Width))
                        alpha = np.asarray(Result_Comparison,
                                           dtype=np.float32)
                        Saturating_Limiter = np.zeros((Height, Width))
                        Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                        Fuzzy_Background_Substraction = np.zeros((Height, Width))
                        Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                        first_imgFL = False

                    else:
                        Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                    Background_Image))
                        Saturating_Limiter = np.divide(Result_Comparison, Ths)
                        Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                 np.ones((Height, Width)),
                                                                 Saturating_Limiter)
                        Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                            Fuzzy_Background_Substraction, (3, 3)))

                        Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                           np.ones((Height, Width)), 0)
                        alpha = 1 + np.multiply(0.1, (np.subtract(Fuzzy_Background_Substraction, 1)))
                        Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                            (1 - alpha), InputImage))
                        Background_Image = Background_Updated

                    bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                    fmg = np.asarray(Background_Image, dtype=np.uint8)
                    # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                    SUBimg = cv2.addWeighted(fmg, self.alphaSUB,
                                             (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)
                    BGKimg = bmg
                    FRGimg = fmg

                    # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                    # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                else:
                    first_imgFL = True

                # Running Fuzzy logic
                if (self.subtractor == 11):
                    Thu = 30
                    # Ths = 30
                    # Thfs = 0.4
                    # alphamin = 0.9
                    Ths = self.ThsFZB
                    Thfs = self.ThfsFZB
                    alphamin = self.alphaMinFZB
                    Height, Width = img.shape
                    InputImage = np.asarray(img, dtype=np.float32)
                    if first_imgF:
                        Background_Image = InputImage
                        Background_Updated = np.zeros((Height, Width))
                        Background_Updated = np.asarray(Background_Updated,
                                                        dtype=np.float32)
                        Result_Comparison = np.zeros((Height, Width))
                        Result_Comparison = np.asarray(Result_Comparison,
                                                       dtype=np.float32)
                        Background_Substraction = np.zeros((Height, Width))
                        Background_Substraction = np.asarray(Result_Comparison,
                                                             dtype=np.float32)
                        alpha = np.zeros((Height, Width))
                        alpha = np.asarray(Result_Comparison,
                                           dtype=np.float32)
                        Saturating_Limiter = np.zeros((Height, Width))
                        Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                        Fuzzy_Background_Substraction = np.zeros((Height, Width))
                        Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                        first_imgF = False
                    else:
                        Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                    Background_Image))
                        Saturating_Limiter = np.divide(Result_Comparison, Ths)
                        Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                 np.ones((Height, Width)),
                                                                 Saturating_Limiter)
                        Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                            Fuzzy_Background_Substraction, (3, 3)))
                        Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                           np.ones((Height, Width)), 0)
                        alpha = np.subtract(1, np.multiply(
                            (1 - alphamin), np.exp(np.multiply(-5, Fuzzy_Background_Substraction))))
                        Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                            (1 - alpha), InputImage))
                        Background_Image = Background_Updated
                        # img = np.asarray(Background_Image, dtype=np.uint8)
                        # img = np.multiply(Background_Substraction, 255)
                    bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                    fmg = np.asarray(Background_Image, dtype=np.uint8)
                    # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                    SUBimg = cv2.addWeighted(fmg, self.alphaSUB,
                                             (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)
                    BGKimg = bmg
                    FRGimg = fmg

                    # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                    # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                else:
                    first_imgF = True

                # Running average
                if self.subtractor == 9:
                    # alpha = 0.9
                    # Thu = 30
                    # Ths = 30
                    alpha = self.alphaRNB
                    Thu = self.ThuRNB
                    Ths = self.ThsRNB
                    Frame = img
                    if first_imgR:
                        Background_Image = Frame.astype(np.float32)
                        Background_Substraction = np.zeros((Frame.shape[0], Frame.shape[1]))
                        first_imgR = False
                    else:
                        Result_Comparison = cv2.absdiff(Frame.astype(np.float32), Background_Image)
                        Background_Substraction = np.where(Result_Comparison > Ths,
                                                           np.ones((Frame.shape[0], Frame.shape[1])), 0)
                        Background_Updated = cv2.add(np.multiply(alpha, Background_Image),
                                                     np.multiply((1 - alpha), Frame.astype(np.float32)))
                        Running_Average_Method = np.where(Result_Comparison < Thu,
                                                          Background_Updated, Background_Image)
                        Background_Image = Running_Average_Method
                        # img = np.multiply(Background_Substraction,255)
                    bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                    fmg = np.asarray(Background_Image, dtype=np.uint8)
                    # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                    SUBimg = cv2.addWeighted(fmg, self.alphaSUB,
                                             (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)
                    BGKimg = bmg
                    FRGimg = fmg

                    # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                    # img = cv2.addWeighted(imb, 0.25, img, 0.75, 0)
                    # img = np.asarray(Background_Image, dtype=np.uint8)
                else:
                    first_imgR = True

                if (self.ui.RBLGetFrame.isChecked() == True):
                    if self.imagedisplay == 1:
                        img = img

                    if self.imagedisplay == 2:
                        img =BGKimg

                    if self.imagedisplay == 3:
                        img=FRGimg

                    if self.imagedisplay == 4:
                        img = SUBimg

                    if (cont == 0):
                        img0 = img
                        cont = 1
                    else:
                        img0 = cv2.addWeighted(img0, self.alphaLapse, img, self.bethaLapse, self.constantLapse)
                    Lapimg = img0
                    # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                else:
                    cont = 0

                    # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                # create effect
                # if first_img:
                #    img0 =  img
                # else:
                #    img0  = cv2.addWeighted(img0, 0.95,img, 0.05, 0)

                # (self.hcam.getPropertyValue('internal_frame_rate'))
                # img = cv2.normalize(img, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
                # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)

                # Image2Plot = cv2.rotate(Image2Plot, cv2.ROTATE_90_CLOCKWISE)
                key = cv2.waitKey(1) & 0xff
                if self.ui.PBReset_2.text() == 'Play Video':
                    while True:
                        key2 = cv2.waitKey(1) or 0xff
                        # self.ui.GVImage.show()
                        # self.ui.GVImage.setImage(Image2Plot)
                        if self.ui.CBHist.isChecked() == False:
                            self.ui.GVImage.ui.histogram.hide()

                        else:
                            self.ui.GVImage.ui.histogram.show()

                        if self.ui.PBReset_2.text() == 'Pause Video':
                            break
                if self.ui.CBProcess.isChecked()==True:
                    if self.imagedisplay == 1:
                        self.ui.GVImage.show()
                        imgP = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        imgP = cv2.flip(imgP, 0)
                        #imgP = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                        self.ui.GVImage.setImage(imgP, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    if self.imagedisplay == 2:
                        self.ui.GVImage.show()
                        BGKimgP = cv2.rotate(BGKimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        BGKimgP = cv2.flip(BGKimgP, 0)
                        self.ui.GVImage.setImage(BGKimgP, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    if self.imagedisplay == 3:
                        self.ui.GVImage.show()
                        FRGimgP = cv2.rotate(FRGimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        FRGimgP = cv2.flip(FRGimgP, 0)
                        self.ui.GVImage.setImage(FRGimgP, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    if self.imagedisplay == 4:
                        self.ui.GVImage.show()
                        SUBimgP = cv2.rotate(SUBimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        SUBimgP = cv2.flip(SUBimgP, 0)
                        self.ui.GVImage.setImage(SUBimgP, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    if self.imagedisplay == 5:
                        self.ui.GVImage.show()
                        LapimgP = cv2.rotate(Lapimg, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        LapimgP = cv2.flip(LapimgP, 0)
                        self.ui.GVImage.setImage(LapimgP, autoRange=False, autoLevels=False, autoHistogramRange=False)

                if self.ui.CBHist.isChecked() == False:
                    self.ui.GVImage.ui.histogram.hide()
                else:
                    self.ui.GVImage.ui.histogram.show()
                import imageio
                # print(count)

                if frameNum < 10:
                    new_num = "00000" + str(frameNum)
                if frameNum >= 10 and frameNum < 100:
                    new_num = "0000" + str(frameNum)
                if frameNum >= 100 and frameNum < 1000:
                    new_num = "000" + str(frameNum)
                if frameNum >= 1000 and frameNum < 10000:
                    new_num = "00" + str(frameNum)
                if frameNum >= 10000 and frameNum < 100000:
                    new_num = "0" + str(frameNum)
                if frameNum >= 100000:
                    new_num = str(frameNum)



                if (self.ui.RBOGetFrame.isChecked() == True):

                    path = (self.OriginalFrame + new_num + '.tiff')
                    imageio.imwrite(path, img)

                if (self.ui.RBISGetFrame.isChecked() == True):

                    path = (self.BackgroundFrame + new_num + '.tiff')
                    imageio.imwrite(path, BGKimg)

                if (self.ui.RBFGetFrame.isChecked() == True):

                   path = (self.ForegroundFrame + new_num + '.tiff')
                   imageio.imwrite(path, FRGimg)


                if (self.ui.RBBGetFrame.isChecked() == True):

                   path = (self.SubtractorFrame + new_num + '.tiff')
                   imageio.imwrite(path, SUBimg)

                if (self.ui.RBLGetFrame.isChecked() == True):

                   path = (self.LapseFrame + new_num + '.tiff')
                   imageio.imwrite(path, Lapimg)

                if key == 27:
                    break
                frameNum = 1 + frameNum
            Video.release()
        else:
            self.ui.PBFramesVideo.setText('Get Frames')

    def GetFrames(self):
        self.BackgroundSettings()
        print('getframes')
        self.CreateFolder()
        self.Vid2FrameSave()


    def StopVideo(self):
        if self.ui.PBReset_2.text() == 'Pause Video':
            self.ui.PBReset_2.setText('Play Video')

        else:
            self.ui.PBReset_2.setText('Pause Video')

    def StopReset(self):
        self.exitvideo = True
        self.ui.PBFramesVideo.setText('Get Frames')


    #plot video in the images
    def PlayVideo(self):
        self.exitvideo = False
        if True:
            ### background options
            # BACKGROUND CNT
            if False:
                self.fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(minPixelStability=15,
                                                                     useHistory=True,
                                                                     maxPixelStability=15 * 60,
                                                                     isParallel=True)
                # BACKGROUND GMG
                self.fgbgGMG = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=1,
                                                                        decisionThreshold=0.8)
                # BackgroundGSOC
                self.fgbgGSOC = cv2.bgsegm.createBackgroundSubtractorGSOC(nSamples=20,
                                                                          replaceRate=0.003,
                                                                          propagationRate=0.01,
                                                                          hitsThreshold=32,
                                                                          alpha=0.01,
                                                                          beta=0.0022,
                                                                          blinkingSupressionDecay=0.1,
                                                                          blinkingSupressionMultiplier=0.1,
                                                                          noiseRemovalThresholdFacBG=0.0004,
                                                                          noiseRemovalThresholdFacFG=0.0008)
                # BackgroundKNN
                self.fgbgKNN = cv2.createBackgroundSubtractorKNN(history=500,
                                                                 dist2Threshold=400.0,
                                                                 detectShadows=True)
                # BackgroundLSBP
                self.fgbgLSBP = cv2.bgsegm.createBackgroundSubtractorLSBP(nSamples=20,
                                                                          LSBPRadius=16,
                                                                          Tlower=2.0,
                                                                          Tupper=32.0,
                                                                          Tinc=1.0,
                                                                          Tdec=0.05,
                                                                          Rscale=10.0,
                                                                          Rincdec=0.005,
                                                                          noiseRemovalThresholdFacBG=0.0004,
                                                                          noiseRemovalThresholdFacFG=0.0008,
                                                                          LSBPthreshold=8,
                                                                          minCount=2)
                # BackgroundMOG
                self.fgbgMOG = cv2.bgsegm.createBackgroundSubtractorMOG(history=200,
                                                                        nmixtures=5,
                                                                        backgroundRatio=0.7,
                                                                        noiseSigma=0)
                self.fgbgMOG2 = cv2.createBackgroundSubtractorMOG2(history=500,
                                                                   varThreshold=16,
                                                                   detectShadows=True)
            ###values of parameters
            self.fgbg = cv2.bgsegm.createBackgroundSubtractorCNT(minPixelStability=self.minPixelStabilityCNT,
                                                                 useHistory=self.useHistoryCNT,
                                                                 maxPixelStability=self.maxPixelStabilityCNT,
                                                                 isParallel=self.isParallelCNT)
            # BACKGROUND GMG
            self.fgbgGMG = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames=self.initializationFramesGMG,
                                                                    decisionThreshold=self.decisionThresholdGMG)
            # BackgroundGSOC
            self.fgbgGSOC = cv2.bgsegm.createBackgroundSubtractorGSOC(nSamples=self.nSamplesGSOC,
                                                                      replaceRate=self.replaceRateGSOC,
                                                                      propagationRate=self.propagationRateGSOC,
                                                                      hitsThreshold=self.hitsThresholdGSOC,
                                                                      alpha=self.alphaGSOC,
                                                                      beta=self.betaGSOC,
                                                                      blinkingSupressionDecay=0.1,
                                                                      blinkingSupressionMultiplier=0.1,
                                                                      noiseRemovalThresholdFacBG=0.0004,
                                                                      noiseRemovalThresholdFacFG=0.0008)
            # BackgroundKNN
            self.fgbgKNN = cv2.createBackgroundSubtractorKNN(history=self.historyKNN,
                                                             dist2Threshold=self.dist2ThresholdKNN,
                                                             detectShadows=self.detectShadowsKNN)
            # BackgroundLSBP
            self.fgbgLSBP = cv2.bgsegm.createBackgroundSubtractorLSBP(nSamples=self.nSamplesLSBP,
                                                                      LSBPRadius=self.LSBPRadius,
                                                                      Tlower=2.0,
                                                                      Tupper=self.TupperLSBP,
                                                                      Tinc=1.0,
                                                                      Tdec=0.05,
                                                                      Rscale=self.RscaleLSBP,
                                                                      Rincdec=0.005,
                                                                      noiseRemovalThresholdFacBG=0.0004,
                                                                      noiseRemovalThresholdFacFG=0.0008,
                                                                      LSBPthreshold=self.LSBPthreshold,
                                                                      minCount=self.minCountLSBP)
            # BackgroundMOG
            self.fgbgMOG = cv2.bgsegm.createBackgroundSubtractorMOG(history=self.historyMOG,
                                                                    nmixtures=self.nmixturesMOG,
                                                                    backgroundRatio=self.backgroundRatioMOG,
                                                                    noiseSigma=self.noiseSigmaMOG)
            self.fgbgMOG2 = cv2.createBackgroundSubtractorMOG2(history=self.historyMOG2,
                                                               varThreshold=self.varThresholdMOG2,
                                                               detectShadows=self.detectShadowsMOG2)

            first_img = True
            first_imgR = True
            first_imgFL = True
            first_imgF = True
            first_imgMOG = True
            first_imgGMG = True

            ####
            #find video in list
            pathIn = self.ui.LEPATHVideo.text()
            dirmodel = QtWidgets.QFileSystemModel(self)
            dirmodel.setRootPath(pathIn)
            indexvideo = self.ui.TlistVideo.currentIndex()
            VideoName = dirmodel.fileName(indexvideo)
            VideofilePath = dirmodel.filePath(indexvideo)
            Video = cv2.VideoCapture(VideofilePath)
            self.length = int(Video.get(cv2.CAP_PROP_FRAME_COUNT))
            print(self.length)

            success = 1
            cont = 0
            frameNum = 0
            endVideo = True
            while endVideo:
                #self.BackgroundSettings()
                print(self.exitvideo)
                if self.exitvideo == True:
                    Video.release()
                    endVideo = False
                    break
                #frameNum = 1 + frameNum
                #print(frameNum)
                ValueBar = (frameNum*100)/self.length
                self.ui.PGBSaving.setValue(ValueBar)
                if frameNum==self.length:
                    Video.release()
                    endVideo = False
                    break
                ret, frame = Video.read()
                if not ret:
                    break
                Image2Plot = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                Image2Plot = cv2.rotate(Image2Plot, cv2.ROTATE_90_COUNTERCLOCKWISE)
                Image2Plot = cv2.flip(Image2Plot, 0)
                img = Image2Plot
                #here the image will be shown
                #if self.ui.TWImageV.currentIndex() == 0:
                #print(self.ui.TWImageV.currentIndex())
                if self.ui.TWImageV.currentIndex() == 0:
                    self.bgkSubtractor()
                    if (self.subtractor <= 8):
                        if (self.subtractor == 3):
                            if (self.subtractor == 3 and self.imagedisplay ==3 ):
                                if first_imgGMG:
                                    self.ForegroundGMG = img
                                    first_imgGMG = False
                                else:
                                    self.ForegroundGMG = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                                img = self.ForegroundGMG
                            else:
                                first_imgGMG = True
                                img = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                        if (self.subtractor == 7):
                            if (self.subtractor == 7 and self.imagedisplay ==3 ):
                                if first_imgMOG:
                                    self.ForegroundMOG = img
                                    first_imgMOG = False
                                else:
                                    self.ForegroundMOG = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                                img = self.ForegroundMOG
                            else:
                                first_imgMOG = True
                                img = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                        if (self.subtractor != 3 and self.subtractor != 7 ):
                            first_imgGMG = True
                            first_imgMOG = True
                            img = self.ImageBackground(img, self.subtractor, self.imagedisplay)
                    #
                    # Running fuzzy  lineal
                    if (self.subtractor == 10):
                        Thu = 30
                        #Ths = 30
                        #Thfs = 0.4
                        Ths = self.ThsFZBL
                        Thfs = self.ThfsFZBL
                        alphamin = 0.9
                        Height, Width = img.shape
                        InputImage = np.asarray(img, dtype=np.float32)
                        if first_imgFL:
                            Background_Image = InputImage
                            Background_Updated = np.zeros((Height, Width))
                            Background_Updated = np.asarray(Background_Updated,
                                                            dtype=np.float32)
                            Result_Comparison = np.zeros((Height, Width))
                            Result_Comparison = np.asarray(Result_Comparison,
                                                           dtype=np.float32)
                            Background_Substraction = np.zeros((Height, Width))
                            Background_Substraction = np.asarray(Result_Comparison,
                                                                 dtype=np.float32)
                            alpha = np.zeros((Height, Width))
                            alpha = np.asarray(Result_Comparison,
                                               dtype=np.float32)
                            Saturating_Limiter = np.zeros((Height, Width))
                            Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                            Fuzzy_Background_Substraction = np.zeros((Height, Width))
                            Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                            first_imgFL = False

                        else:
                            Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                        Background_Image))
                            Saturating_Limiter = np.divide(Result_Comparison, Ths)
                            Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                     np.ones((Height, Width)),
                                                                     Saturating_Limiter)
                            Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                                Fuzzy_Background_Substraction, (3, 3)))

                            Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                               np.ones((Height, Width)), 0)
                            alpha = 1 + np.multiply(0.1, (np.subtract(Fuzzy_Background_Substraction, 1)))
                            Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                                (1 - alpha), InputImage))
                            Background_Image = Background_Updated
                        if (self.imagedisplay == 1):
                            img = img
                        if (self.imagedisplay == 2):
                            img = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        if (self.imagedisplay == 3):
                            img = np.asarray(Background_Image, dtype=np.uint8)
                        if (self.imagedisplay == 4):
                            bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                            fmg = np.asarray(Background_Image, dtype=np.uint8)
                            # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                            #img = cv2.addWeighted(fmg, 0.25,
                            #                      (np.where(bmg > fmg, img, 0)), 0.75, 0)
                            img = cv2.addWeighted(fmg, self.alphaSUB,
                                                  (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                    else:
                        first_imgFL = True

                    # Running Fuzzy logic
                    if (self.subtractor == 11):
                        Thu = 30
                        #Ths = 30
                        #Thfs = 0.4
                        #alphamin = 0.9
                        Ths = self.ThsFZB
                        Thfs = self.ThfsFZB
                        alphamin = self.alphaMinFZB
                        Height, Width = img.shape
                        InputImage = np.asarray(img, dtype=np.float32)
                        if first_imgF:
                            Background_Image = InputImage
                            Background_Updated = np.zeros((Height, Width))
                            Background_Updated = np.asarray(Background_Updated,
                                                            dtype=np.float32)
                            Result_Comparison = np.zeros((Height, Width))
                            Result_Comparison = np.asarray(Result_Comparison,
                                                           dtype=np.float32)
                            Background_Substraction = np.zeros((Height, Width))
                            Background_Substraction = np.asarray(Result_Comparison,
                                                                 dtype=np.float32)
                            alpha = np.zeros((Height, Width))
                            alpha = np.asarray(Result_Comparison,
                                               dtype=np.float32)
                            Saturating_Limiter = np.zeros((Height, Width))
                            Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                            Fuzzy_Background_Substraction = np.zeros((Height, Width))
                            Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                            first_imgF = False
                        else:
                            Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                        Background_Image))
                            Saturating_Limiter = np.divide(Result_Comparison, Ths)
                            Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                     np.ones((Height, Width)),
                                                                     Saturating_Limiter)
                            Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                                Fuzzy_Background_Substraction, (3, 3)))
                            Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                               np.ones((Height, Width)), 0)
                            alpha = np.subtract(1, np.multiply(
                                (1 - alphamin), np.exp(np.multiply(-5, Fuzzy_Background_Substraction))))
                            Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                                (1 - alpha), InputImage))
                            Background_Image = Background_Updated
                            # img = np.asarray(Background_Image, dtype=np.uint8)
                            # img = np.multiply(Background_Substraction, 255)
                        if (self.imagedisplay == 1):
                            img = img
                        if (self.imagedisplay == 2):
                            img = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        if (self.imagedisplay == 3):
                            img = np.asarray(Background_Image, dtype=np.uint8)
                        if (self.imagedisplay == 4):
                            bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                            fmg = np.asarray(Background_Image, dtype=np.uint8)
                            # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                            #img = cv2.addWeighted(fmg, 0.25,
                            #                      (np.where(bmg > fmg, img, 0)), 0.75, 0)
                            img = cv2.addWeighted(fmg, self.alphaSUB,
                                                  (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                    else:
                        first_imgF = True

                    # Running average
                    if self.subtractor == 9:
                        #alpha = 0.9
                        #Thu = 30
                        #Ths = 30
                        alpha = self.alphaRNB
                        Thu = self.ThuRNB
                        Ths = self.ThsRNB
                        Frame = img
                        if first_imgR:
                            Background_Image = Frame.astype(np.float32)
                            Background_Substraction = np.zeros((Frame.shape[0], Frame.shape[1]))
                            first_imgR = False
                        else:
                            Result_Comparison = cv2.absdiff(Frame.astype(np.float32), Background_Image)
                            Background_Substraction = np.where(Result_Comparison > Ths,
                                                               np.ones((Frame.shape[0], Frame.shape[1])), 0)
                            Background_Updated = cv2.add(np.multiply(alpha, Background_Image),
                                                         np.multiply((1 - alpha), Frame.astype(np.float32)))
                            Running_Average_Method = np.where(Result_Comparison < Thu,
                                                              Background_Updated, Background_Image)
                            Background_Image = Running_Average_Method
                            # img = np.multiply(Background_Substraction,255)
                        if (self.imagedisplay == 1):
                            img = img
                        if (self.imagedisplay == 2):
                            img = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        if (self.imagedisplay == 3):
                            img = np.asarray(Background_Image, dtype=np.uint8)
                        if (self.imagedisplay == 4):
                            bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                            fmg = np.asarray(Background_Image, dtype=np.uint8)
                            # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                            #img = cv2.addWeighted(fmg, 0.25,
                            #                      (np.where(bmg > fmg, img, 0)), 0.75, 0)
                            img = cv2.addWeighted(fmg, self.alphaSUB,
                                                  (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25, img, 0.75, 0)
                        # img = np.asarray(Background_Image, dtype=np.uint8)
                    else:
                        first_imgR = True

                    if (self.lapse == True):
                        if (cont == 0):
                            img0 = img
                            cont = 1
                        else:
                            #img0 = cv2.addWeighted(img0, 0.95, img, 0.05, 0)
                            #NEW VALUE OF LAPSE VIDEO
                            img0 = cv2.addWeighted(img0, self.alphaLapse, img, self.bethaLapse, self.constantLapse)
                        img = img0
                        # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    else:
                        cont = 0
                    ###end of tab 1
                #tab 2
                if self.ui.TWImageV.currentIndex() == 1:
                    self.bgkSubtractor()
                    if (self.subtractor <= 8):
                        if (self.subtractor == 3):
                            BGKimg = self.ImageBackground(img, self.subtractor, 2)
                            if first_imgGMG:
                                self.ForegroundGMG = img
                                first_imgGMG = False
                            else:
                                self.ForegroundGMG = self.ImageBackground(img, self.subtractor, 3)
                            FRGimg = self.ForegroundGMG
                            SUBimg = self.ImageBackground(img, self.subtractor, 4)

                        if (self.subtractor == 7):
                            BGKimg = self.ImageBackground(img, self.subtractor, 2)
                            if first_imgMOG:
                                self.ForegroundMOG = img
                                first_imgMOG = False
                            else:
                                self.ForegroundMOG = self.ImageBackground(img, self.subtractor, 3)
                            FRGimg = self.ForegroundMOG
                            SUBimg = self.ImageBackground(img, self.subtractor, 4)


                        if (self.subtractor != 3 and self.subtractor != 7):
                            first_imgGMG = True
                            first_imgMOG = True
                            BGKimg = self.ImageBackground(img, self.subtractor, 2)
                            FRGimg = self.ImageBackground(img, self.subtractor, 3)
                            SUBimg = self.ImageBackground(img, self.subtractor, 4)

                    #
                    # Running fuzzy  lineal
                    if (self.subtractor == 10):
                        Thu = 30
                        # Ths = 30
                        # Thfs = 0.4
                        Ths = self.ThsFZBL
                        Thfs = self.ThfsFZBL
                        alphamin = 0.9
                        Height, Width = img.shape
                        InputImage = np.asarray(img, dtype=np.float32)
                        if first_imgFL:
                            Background_Image = InputImage
                            Background_Updated = np.zeros((Height, Width))
                            Background_Updated = np.asarray(Background_Updated,
                                                            dtype=np.float32)
                            Result_Comparison = np.zeros((Height, Width))
                            Result_Comparison = np.asarray(Result_Comparison,
                                                           dtype=np.float32)
                            Background_Substraction = np.zeros((Height, Width))
                            Background_Substraction = np.asarray(Result_Comparison,
                                                                 dtype=np.float32)
                            alpha = np.zeros((Height, Width))
                            alpha = np.asarray(Result_Comparison,
                                               dtype=np.float32)
                            Saturating_Limiter = np.zeros((Height, Width))
                            Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                            Fuzzy_Background_Substraction = np.zeros((Height, Width))
                            Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                            first_imgFL = False

                        else:
                            Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                        Background_Image))
                            Saturating_Limiter = np.divide(Result_Comparison, Ths)
                            Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                     np.ones((Height, Width)),
                                                                     Saturating_Limiter)
                            Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                                Fuzzy_Background_Substraction, (3, 3)))

                            Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                               np.ones((Height, Width)), 0)
                            alpha = 1 + np.multiply(0.1, (np.subtract(Fuzzy_Background_Substraction, 1)))
                            Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                                (1 - alpha), InputImage))
                            Background_Image = Background_Updated

                        bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        fmg = np.asarray(Background_Image, dtype=np.uint8)
                        # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                        #SUBimg = cv2.addWeighted(fmg, 0.25,
                        #                      (np.where(bmg > fmg, img, 0)), 0.75, 0)
                        SUBimg = cv2.addWeighted(fmg, self.alphaSUB,
                                                 (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)
                        BGKimg = bmg
                        FRGimg = fmg



                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                    else:
                        first_imgFL = True

                    # Running Fuzzy logic
                    if (self.subtractor == 11):
                        Thu = 30
                        # Ths = 30
                        # Thfs = 0.4
                        # alphamin = 0.9
                        Ths = self.ThsFZB
                        Thfs = self.ThfsFZB
                        alphamin = self.alphaMinFZB
                        Height, Width = img.shape
                        InputImage = np.asarray(img, dtype=np.float32)
                        if first_imgF:
                            Background_Image = InputImage
                            Background_Updated = np.zeros((Height, Width))
                            Background_Updated = np.asarray(Background_Updated,
                                                            dtype=np.float32)
                            Result_Comparison = np.zeros((Height, Width))
                            Result_Comparison = np.asarray(Result_Comparison,
                                                           dtype=np.float32)
                            Background_Substraction = np.zeros((Height, Width))
                            Background_Substraction = np.asarray(Result_Comparison,
                                                                 dtype=np.float32)
                            alpha = np.zeros((Height, Width))
                            alpha = np.asarray(Result_Comparison,
                                               dtype=np.float32)
                            Saturating_Limiter = np.zeros((Height, Width))
                            Saturating_Limiter = np.asarray(Saturating_Limiter, dtype=np.float32)
                            Fuzzy_Background_Substraction = np.zeros((Height, Width))
                            Fuzzy_Background_Substraction = np.asarray(Saturating_Limiter, dtype=np.float32)
                            first_imgF = False
                        else:
                            Result_Comparison = np.absolute(np.subtract(InputImage,
                                                                        Background_Image))
                            Saturating_Limiter = np.divide(Result_Comparison, Ths)
                            Fuzzy_Background_Substraction = np.where(Result_Comparison > Ths,
                                                                     np.ones((Height, Width)),
                                                                     Saturating_Limiter)
                            Abs_LPF_Fuzzy_Background_Substraction = np.absolute(cv2.blur(
                                Fuzzy_Background_Substraction, (3, 3)))
                            Background_Substraction = np.where(Abs_LPF_Fuzzy_Background_Substraction > Thfs,
                                                               np.ones((Height, Width)), 0)
                            alpha = np.subtract(1, np.multiply(
                                (1 - alphamin), np.exp(np.multiply(-5, Fuzzy_Background_Substraction))))
                            Background_Updated = np.add(np.multiply(alpha, Background_Image), np.multiply(
                                (1 - alpha), InputImage))
                            Background_Image = Background_Updated
                            # img = np.asarray(Background_Image, dtype=np.uint8)
                            # img = np.multiply(Background_Substraction, 255)
                        bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        fmg = np.asarray(Background_Image, dtype=np.uint8)
                        # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                        #SUBimg = cv2.addWeighted(fmg, 0.25,
                        #                         (np.where(bmg > fmg, img, 0)), 0.75, 0)
                        SUBimg = cv2.addWeighted(fmg, self.alphaSUB,
                                                 (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)
                        BGKimg = bmg
                        FRGimg = fmg

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25,img, 0.75, 0)
                    else:
                        first_imgF = True

                    # Running average
                    if self.subtractor == 9:
                        # alpha = 0.9
                        # Thu = 30
                        # Ths = 30
                        alpha = self.alphaRNB
                        Thu = self.ThuRNB
                        Ths = self.ThsRNB
                        Frame = img
                        if first_imgR:
                            Background_Image = Frame.astype(np.float32)
                            Background_Substraction = np.zeros((Frame.shape[0], Frame.shape[1]))
                            first_imgR = False
                        else:
                            Result_Comparison = cv2.absdiff(Frame.astype(np.float32), Background_Image)
                            Background_Substraction = np.where(Result_Comparison > Ths,
                                                               np.ones((Frame.shape[0], Frame.shape[1])), 0)
                            Background_Updated = cv2.add(np.multiply(alpha, Background_Image),
                                                         np.multiply((1 - alpha), Frame.astype(np.float32)))
                            Running_Average_Method = np.where(Result_Comparison < Thu,
                                                              Background_Updated, Background_Image)
                            Background_Image = Running_Average_Method
                            # img = np.multiply(Background_Substraction,255)
                        bmg = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        fmg = np.asarray(Background_Image, dtype=np.uint8)
                        # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                        #SUBimg = cv2.addWeighted(fmg, 0.25,
                        #                         (np.where(bmg > fmg, img, 0)), 0.75, 0)
                        SUBimg = cv2.addWeighted(fmg, self.alphaSUB,
                                                 (np.where(bmg > fmg, img, 0)), self.bethaSUB, self.constantSUB)
                        BGKimg = bmg
                        FRGimg = fmg

                        # imb = np.asarray(np.multiply(Background_Substraction, 255), dtype=np.uint8)
                        # img = cv2.addWeighted(imb, 0.25, img, 0.75, 0)
                        # img = np.asarray(Background_Image, dtype=np.uint8)
                    else:
                        first_imgR = True




                    # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                #self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                # create effect
                # if first_img:
                #    img0 =  img
                # else:
                #    img0  = cv2.addWeighted(img0, 0.95,img, 0.05, 0)

                # (self.hcam.getPropertyValue('internal_frame_rate'))
                # img = cv2.normalize(img, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
                # self.iv.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)


                #Image2Plot = cv2.rotate(Image2Plot, cv2.ROTATE_90_CLOCKWISE)
                key = cv2.waitKey(1) & 0xff
                if self.ui.PBReset_2.text() == 'Play Video':
                    while True:
                        key2 = cv2.waitKey(1) or 0xff
                        #self.ui.GVImage.show()
                        #self.ui.GVImage.setImage(Image2Plot)
                        if self.ui.CBHist.isChecked() == False:
                            self.ui.GVImage.ui.histogram.hide()
                            self.ui.TWImageA.ui.histogram.hide()
                            self.ui.TWImageB.ui.histogram.hide()
                            self.ui.TWImageC.ui.histogram.hide()
                            self.ui.TWImageD.ui.histogram.hide()
                        else:
                            self.ui.GVImage.ui.histogram.show()
                            self.ui.TWImageA.ui.histogram.show()
                            self.ui.TWImageB.ui.histogram.show()
                            self.ui.TWImageC.ui.histogram.show()
                            self.ui.TWImageD.ui.histogram.show()
                        if self.ui.PBReset_2.text() == 'Pause Video':
                            break
                if self.ui.TWImageV.currentIndex() == 0:
                    self.ui.GVImage.show()
                    self.ui.GVImage.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                if self.ui.TWImageV.currentIndex() == 1:
                    self.ui.TWImageA.show()
                    self.ui.TWImageA.setImage(img, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    self.ui.TWImageB.show()
                    self.ui.TWImageB.setImage(SUBimg, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    self.ui.TWImageC.show()
                    self.ui.TWImageC.setImage(FRGimg, autoRange=False, autoLevels=False, autoHistogramRange=False)
                    self.ui.TWImageD.show()
                    self.ui.TWImageD.setImage(BGKimg, autoRange=False, autoLevels=False, autoHistogramRange=False)
                if self.ui.CBHist.isChecked() == False:
                    self.ui.GVImage.ui.histogram.hide()
                    self.ui.TWImageA.ui.histogram.hide()
                    self.ui.TWImageB.ui.histogram.hide()
                    self.ui.TWImageC.ui.histogram.hide()
                    self.ui.TWImageD.ui.histogram.hide()
                else:
                    self.ui.GVImage.ui.histogram.show()
                    self.ui.TWImageA.ui.histogram.show()
                    self.ui.TWImageB.ui.histogram.show()
                    self.ui.TWImageC.ui.histogram.show()
                    self.ui.TWImageD.ui.histogram.show()
                if key == 27:
                    break
                frameNum = 1 + frameNum
            Video.release()
        #else:
         #   self.ui.PBPVideo.setText('Play Video')


    def ImageBackground(self, inputImage, BGKimage, Dimage):
        # ImageDefault
        if (BGKimage == 1):
            img = inputImage
            if (Dimage == 1):
                img = inputImage

        if (BGKimage == 2):
            if (Dimage == 1):
                img = inputImage
            if (Dimage == 2):
                img = self.fgbg.apply(inputImage)
            if (Dimage == 3):
                img = self.fgbg.apply(inputImage)
                img = self.fgbg.getBackgroundImage()
            if (Dimage == 4):
                # fimg = self.fgbg.getBackgroundImage()
                # bimg = img
                bmg = self.fgbg.apply(inputImage)
                # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                img = cv2.addWeighted(self.fgbg.getBackgroundImage(), self.alphaSUB,
                                      (np.where(bmg > self.fgbg.getBackgroundImage(), inputImage, 0)),self.bethaSUB, self.constantSUB)
        if (BGKimage == 3):
            if (Dimage == 1):
                img = inputImage
            if (Dimage == 2):
                img = self.fgbgGMG.apply(inputImage)
            if (Dimage == 3):
                # self.ForegroundGMG
                # img = self.fgbgGMG.apply(inputImage)
                # img = self.fgbgGMG.getBackgroundImage()
                product = np.multiply(np.asarray(inputImage, dtype=np.float32),
                                      np.asarray(self.fgbgGMG.apply(inputImage), dtype=np.float32))
                img = np.where(product == 0, inputImage, self.ForegroundGMG)
                # img = self.ForegroundGMG
            if (Dimage == 4):
                # fimg = self.fgbgGMG.getBackgroundImage()
                # bimg = img
                bmg = self.fgbgGMG.apply(inputImage)
                product = np.multiply(np.asarray(inputImage, dtype=np.float32),
                                      np.asarray(self.fgbgGMG.apply(inputImage), dtype=np.float32))
                fmg = np.where(product == 0, inputImage, self.ForegroundGMG)
                # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                img = cv2.addWeighted(fmg, self.alphaSUB,
                                      (np.where(bmg > fmg, inputImage, 0)),self.bethaSUB, self.constantSUB)

        if (BGKimage == 4):
            if (Dimage == 1):
                img = inputImage
            if (Dimage == 2):
                img = self.fgbgGSOC.apply(inputImage)
            if (Dimage == 3):
                img = self.fgbgGSOC.apply(inputImage)
                img = self.fgbgGSOC.getBackgroundImage()
            if (Dimage == 4):
                bmg = self.fgbgGSOC.apply(inputImage)
                fmg = cv2.cvtColor(self.fgbgGSOC.getBackgroundImage(), cv2.COLOR_BGR2GRAY)
                # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                img = cv2.addWeighted(fmg, self.alphaSUB,
                                      (np.where(bmg > fmg, inputImage, 0)), self.bethaSUB, self.constantSUB)

        if (BGKimage == 5):
            if (Dimage == 1):
                img = inputImage
            if (Dimage == 2):
                img = self.fgbgKNN.apply(inputImage)
            if (Dimage == 3):
                img = self.fgbgKNN.apply(inputImage)
                img = self.fgbgKNN.getBackgroundImage()
            if (Dimage == 4):
                bmg = self.fgbgKNN.apply(inputImage)
                # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                img = cv2.addWeighted(self.fgbgKNN.getBackgroundImage(), self.alphaSUB,
                                      (np.where(bmg > self.fgbgKNN.getBackgroundImage(), inputImage, 0)), self.bethaSUB, self.constantSUB)

        if (BGKimage == 6):
            if (Dimage == 1):
                img = inputImage
            if (Dimage == 2):
                img = self.fgbgLSBP.apply(inputImage)
            if (Dimage == 3):
                img = self.fgbgLSBP.apply(inputImage)
                img = self.fgbgLSBP.getBackgroundImage()
            if (Dimage == 4):
                bmg = self.fgbgLSBP.apply(inputImage)
                fmg = cv2.cvtColor(self.fgbgLSBP.getBackgroundImage(), cv2.COLOR_BGR2GRAY)
                # bmg = self.fgbgLSBP.apply(inputImage)
                # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                img = cv2.addWeighted(fmg, self.alphaSUB,
                                      (np.where(bmg > fmg, inputImage, 0)), self.bethaSUB, self.constantSUB)

        if (BGKimage == 7):
            if (Dimage == 1):
                img = inputImage
            if (Dimage == 2):
                img = self.fgbgMOG.apply(inputImage)
            if (Dimage == 3):
                # img = self.fgbgMOG.apply(inputImage)
                # img = self.fgbgMOG.getBackgroundImage()
                product = np.multiply(np.asarray(inputImage, dtype=np.float32),
                                      np.asarray(self.fgbgMOG.apply(inputImage), dtype=np.float32))
                img = np.where(product == 0, inputImage, self.ForegroundMOG)
                # img = self.ForegroundMOG
            if (Dimage == 4):
                bmg = self.fgbgMOG.apply(inputImage)
                product = np.multiply(np.asarray(inputImage, dtype=np.float32),
                                      np.asarray(self.fgbgMOG.apply(inputImage), dtype=np.float32))
                fmg = np.where(product == 0, inputImage, self.ForegroundMOG)
                # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                img = cv2.addWeighted(fmg, self.alphaSUB,
                                      (np.where(bmg > fmg, inputImage, 0)), self.bethaSUB, self.constantSUB)

        if (BGKimage == 8):
            if (Dimage == 1):
                img = inputImage
            if (Dimage == 2):
                img = self.fgbgMOG2.apply(inputImage)
            if (Dimage == 3):
                img = self.fgbgMOG2.apply(inputImage)
                img = self.fgbgMOG2.getBackgroundImage()
            if (Dimage == 4):
                bmg = self.fgbgMOG2.apply(inputImage)
                # img = cv2.addWeighted(self.fgbg.apply(inputImage), 0.25,inputImage, 0.75, 0)
                img = cv2.addWeighted(self.fgbgMOG2.getBackgroundImage(), self.alphaSUB,
                                      (np.where(bmg > self.fgbgMOG2.getBackgroundImage(), inputImage, 0)), self.bethaSUB, self.constantSUB)
        return img

            #plot image in new windows
    def Plot_Frame(self):
        pathIn = self.ui.LEPATH.text()
        dirmodel = QtWidgets.QFileSystemModel(self)
        dirmodel.setRootPath(pathIn)
        indexFrame = self.ui.TlistFrame.currentIndex()
        FramefilePath = dirmodel.filePath(indexFrame)
        name, ext = os.path.splitext(FramefilePath)
        print(ext)
        if  ext == '.tiff' or ext =='.png' or ext =='.jpg' or ext =='.tif':
            Image2Plot = cv2.imread(FramefilePath)
            Image2Plot = cv2.rotate(Image2Plot, cv2.ROTATE_90_COUNTERCLOCKWISE)
            #Image2Plot = cv2.rotate(Image2Plot, cv2.ROTATE_90_CLOCKWISE)
            self.ui.GVImage.show()
            self.ui.GVImage.setImage(Image2Plot, autoRange=False, autoLevels=False, autoHistogramRange=False)
            if self.ui.CBHist.isChecked() == False:
                self.ui.GVImage.ui.histogram.hide()
            else:
                self.ui.GVImage.ui.histogram.show()
        else:
            print('this is not an image')

        #print(FramefilePath)
    #video to frames
    # create video
    def convert_video_to_frames(self):
        self.BackgroundSettings()
        pathIn = self.ui.LEPATHVideo.text()

        dirmodel = QtWidgets.QFileSystemModel(self)
        dirmodel.setRootPath(pathIn)
        indexvideo = self.ui.TlistVideo.currentIndex()
        VideoName = dirmodel.fileName(indexvideo)
        VideofilePath = dirmodel.filePath(indexvideo)
        pathOut = self.ui.LEOutPathV.text()
        pathOut = pathOut.rsplit('.', 1)[0]
        # Path to video file
        vidObj = cv2.VideoCapture(VideofilePath)
        length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
        # Used as counter variable
        count = 0
        # checks whether frames were extracted
        success = 1
        while success:
            # vidObj object calls read
            # function extract frames
            success, image = vidObj.read()
            # Saves the frames with frame-count
            if success:
                import imageio
                #print(count)
                if count < 10:
                    new_num = "00000" + str(count)
                if count >= 10 and count < 100:
                    new_num = "0000" + str(count)
                if count >= 100 and count < 1000:
                    new_num = "000" + str(count)
                if count >= 1000 and count < 10000:
                    new_num = "00" + str(count)
                if count >= 10000 and count < 100000:
                    new_num = "0" + str(count)
                if count >= 100000:
                    new_num = str(count)

                ValueBar = (((count+1) * 100) / length)
                self.ui.PGBSaving.setValue(ValueBar)
                path = (pathOut + new_num + '.tiff')

                imageio.imwrite(path, image)
                #cv2.imwrite("pathOut%d.tiff" % count, image)
                count += 1



    def get_frames_path(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'frame as', '', '(*.tif)')
        if path == '':
            return
        if path[0].endswith('.tiff') or path[0].endswith('.tif'):
            path = path[0]
        else:
            path = path[0] + '.tif'
        self.ui.LEOutPathV.setText(path)
        # get new folder of image

    def get_video_path(self):
        path = (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        dirmodel = QtWidgets.QFileSystemModel(self)
        dirmodel.setRootPath(path)
        self.ui.TlistVideo.setModel(dirmodel)
        self.ui.TlistVideo.setRootIndex(dirmodel.setRootPath(path))
        self.ui.LEPATHVideo.setText(path)




    #images to video
    #create video
    def convert_frames_to_video(self):
        pathIn = self.ui.LEPATH.text()

        dirmodel = QtWidgets.QFileSystemModel(self)
        dirmodel.setRootPath(pathIn)

        pathOut = self.ui.LEOutPath.text()
        #video_name = self.ui.LEOutPath.text()+'/'+str(self.ui.TXBaseName.currentCharFormat())+'/'+'.avi'
        fps = self.ui.SBFrameRate.value()
        frame_array = []

        #files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
        files = [f for f in os.listdir(pathIn) if f.endswith(".tiff")]
        # for sorting the file names properly
        #files.sort(key=lambda x: int(x[5:-4]))
        for i in range(len(files)):

            filename = pathIn +'/'+ files[i]
            # reading each files
            img = cv2.imread(filename)
            #print(filename)
            height, width, layers = img.shape
            #print(width)
            #print(height)
            size = (width, height)
            #print(filename)
            # inserting the frames into an image array
            frame_array.append(img)
        out = cv2.VideoWriter(pathOut, 0, fps, size)
        for i in range(len(frame_array)):
            valueBar = (i * 100 / len(files)) + 4
            if valueBar > 99:
                path = os.path.dirname(self.ui.LEOutPath.text())
                self.ui.LEPATHVideo.setText(path)
                print(path)
                dirmodel = QtWidgets.QFileSystemModel(self)
                dirmodel.setRootPath(path)
                self.ui.TlistVideo.setModel(dirmodel)
                self.ui.TlistVideo.setRootIndex(dirmodel.setRootPath(path))

            self.ui.PGBSaving.setValue(valueBar)
            # writing to a image array
            print(i)
            out.write(frame_array[i])
        out.release()
    #path for vide
    def get_vid_path(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'video as', '', '(*.avi)')
        if path == '':
            return
        if path[0].endswith('.avi') or path[0].endswith('.avi'):
            path = path[0]
        else:
            path = path[0] + '.avi'
        self.ui.LEOutPath.setText(path)
    #get new folder of image
    def get_img_seq_path(self):
        path = (QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        dirmodel = QtWidgets.QFileSystemModel(self)
        dirmodel.setRootPath(path)
        self.ui.TlistFrame.setModel(dirmodel)
        self.ui.TlistFrame.setRootIndex(dirmodel.setRootPath(path))
        self.ui.LEPATH.setText(path)


    #Set kind of background subtractor
    def bgkSubtractor(self):
        if(self.ui.RBImage.isChecked() == True):
            self.subtractor = 1
        if (self.ui.RBTCNT.isChecked() == True):
            self.subtractor = 2
        if (self.ui.RBTGMG.isChecked() == True):
            self.subtractor = 3
        if (self.ui.RBTGSOC.isChecked() == True):
            self.subtractor = 4
        if (self.ui.RBTKNN.isChecked() == True):
            self.subtractor = 5
        if (self.ui.RBTLSBP.isChecked() == True):
            self.subtractor = 6
        if (self.ui.RBTMOG.isChecked() == True):
            self.subtractor = 7
        if (self.ui.RBTMOG2.isChecked() == True):
            self.subtractor = 8
        if (self.ui.RBTRNB.isChecked() == True):
            self.subtractor = 9
        if (self.ui.RBTFZBL.isChecked() == True):
            self.subtractor = 10
        if (self.ui.RBTFZB.isChecked() == True):
            self.subtractor = 11
        if (self.ui.RBOFrame.isChecked() == True):
            self.imagedisplay = 1
        if (self.ui.RBBFrame.isChecked() == True):
            self.imagedisplay = 2
        if (self.ui.RBFFrame.isChecked() == True):
            self.imagedisplay = 3
        if (self.ui.RBImg.isChecked() == True):
            self.imagedisplay = 4
        if (self.ui.RBLImg.isChecked() == True):
            self.lapse = True
        else:
            self.lapse = False

            #Reset the check button
    def setTabBKG(self):
        self.ui.RBImage.setChecked(False)
        self.ui.RBTCNT.setChecked(False)
        self.ui.RBTGMG.setChecked(False)
        self.ui.RBTGSOC.setChecked(False)
        self.ui.RBTKNN.setChecked(False)
        self.ui.RBTLSBP.setChecked(False)
        self.ui.RBTMOG.setChecked(False)
        self.ui.RBTMOG2.setChecked(False)
        self.ui.RBTRNB.setChecked(False)
        self.ui.RBTFZBL.setChecked(False)
        self.ui.RBTFZB.setChecked(False)

    # Reset Parameters to default options
    def Reset_Settings(self):
        #Defaults settings for camera ORCA SPARK C11440-36U
        if (self.ui.CBCamera.currentText()=='C11440-36U'):
            #print('C11440-36U')
            self.ui.DSBExposure.setValue(15.40832049)
            self.ui.SBCGain.setValue(0)
            self.ui.CBBits_2.hide()
            self.ui.CBBinning.hide()
            self.ui.CBBits.show()
            self.ui.CBBinning_2.show()
            self.ui.SBXP.setValue(0)
            self.ui.SBYP.setValue(0)
            if (self.ui.CBBinning_2.currentText() == 1):
                self.ui.SBWidth.setValue(1200)
                self.ui.SBHeight.setValue(1920)
            if (self.ui.CBBinning_2.currentText() == 2):
                self.ui.SBWidth.setValue(600)
                self.ui.SBHeight.setValue(960)

            self.ui.CBBits.setCurrentIndex(0)
            self.ui.CBBinning_2.setCurrentIndex(0)
        # Defaults settings for camera Orca-Flash4.0 v3 c13440-20CU
        if (self.ui.CBCamera.currentText() == 'C13440-20CU'):
            #print('C13440-20CU')
            self.ui.DSBExposure.setValue(10)
            self.ui.SBCGain.setValue(0)
            self.ui.CBBits.hide()
            self.ui.CBBinning_2.hide()
            self.ui.CBBits_2.show()
            self.ui.CBBinning.show()
            self.ui.SBXP.setValue(0)
            self.ui.SBYP.setValue(0)
            if(self.ui.CBBinning.currentText() == 1):
                self.ui.SBWidth.setValue(2048)
                self.ui.SBHeight.setValue(2048)
            if (self.ui.CBBinning.currentText() == 2):
                self.ui.SBWidth.setValue(1024)
                self.ui.SBHeight.setValue(1024)
            if (self.ui.CBBinning.currentText() == 3):
                self.ui.SBWidth.setValue(512)
                self.ui.SBHeight.setValue(512)
            if (self.ui.CBBinning.currentText() == 4):
                self.ui.SBWidth.setValue(512)
                self.ui.SBHeight.setValue(512)

            self.ui.CBBits_2.setCurrentIndex(0)
            self.ui.CBBinning.setCurrentIndex(0)
        if (self.ui.CBCamera.currentText() == 'no camera'):
            print('no camera')

    # Camera options show two cameras
    def Camera_Settings(self):
        if (self.ui.CBCamera.currentText() == 'C11440-36U'):
            #print('C11440-36U')
            self.ui.DSBExposure.setValue(15.40832049)
            self.ui.SBCGain.setValue(0)
            self.ui.CBBits_2.hide()
            self.ui.CBBinning.hide()
            self.ui.CBBits.show()
            self.ui.CBBinning_2.show()
            self.ui.SBXP.setValue(0)
            self.ui.SBYP.setValue(0)
            if (self.ui.CBBinning_2.currentText() == '1'):
                self.ui.SBWidth.setValue(1200)
                self.ui.SBHeight.setValue(1920)
            if (self.ui.CBBinning_2.currentText() == '2'):
                self.ui.SBWidth.setValue(600)
                self.ui.SBHeight.setValue(960)

        if (self.ui.CBCamera.currentText() == 'C13440-20CU'):
            #print('C13440-20CU')
            self.ui.DSBExposure.setValue(10)
            self.ui.SBCGain.setValue(0)
            self.ui.CBBits.hide()
            self.ui.CBBinning_2.hide()
            self.ui.CBBits_2.show()
            self.ui.CBBinning.show()
            self.ui.SBXP.setValue(0)
            self.ui.SBYP.setValue(0)
            if (self.ui.CBBinning.currentText() == '1'):
                self.ui.SBWidth.setValue(2048)
                self.ui.SBHeight.setValue(2048)
            if (self.ui.CBBinning.currentText() == '2'):
                self.ui.SBWidth.setValue(1024)
                self.ui.SBHeight.setValue(1024)
            if (self.ui.CBBinning.currentText() == '3'):
                self.ui.SBWidth.setValue(512)
                self.ui.SBHeight.setValue(512)
            if (self.ui.CBBinning.currentText() == '4'):
                self.ui.SBWidth.setValue(512)
                self.ui.SBHeight.setValue(512)
        if (self.ui.CBCamera.currentText() == 'no camera'):
            print('no camera')
    #check whether is a camera or not
    def Check_Camera(self):
        #row = self.ui.LVCamera.currentIndex()
        entries = ['no camera', 'no camera']
        model = CameraInterfaces.InfoHamamatsu()
        entries = [model.model[0], model.model[1]]
        #print(model.model[0])
        #print(model.model[1])
        model = QtGui.QStandardItemModel()
        self.ui.LVCamera.setModel(model)
        self.ui.CBCamera.setModel(model)
        for i in entries:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)

    # show button
    def Live_Button(self):
        if (self.ui.CBCamera.currentText() == 'no camera'):
            self.ui.PBLive.hide()
        else:
            self.ui.PBLive.show()


    def BackgroundSettings(self):
        #BKG CNT
        self.minPixelStabilityCNT = self.ui.SBMinPS.value()
        self.maxPixelStabilityCNT = self.ui.SBMaxPS.value()
        self.useHistoryCNT = self.ui.CBHistory.isChecked()
        self.isParallelCNT = self.ui.CBIsParallel.isChecked()
        #BGK GMG
        self.initializationFramesGMG = self.ui.SBInitialF.value()
        self.decisionThresholdGMG = self.ui.DSBThreshold.value()
        #BGK GSOC
        self.nSamplesGSOC = self.ui.SBNSamples.value()
        self.replaceRateGSOC = self.ui.DSBReplace.value()
        self.propagationRateGSOC = self.ui.DSBPropagation.value()
        self.hitsThresholdGSOC = self.ui.SBNThreshold.value()
        self.alphaGSOC = self.ui.DSBalpha.value()
        self.betaGSOC = self.ui.DSBBeta.value()
        #BGK KNN
        self.historyKNN = self.ui.SBHistory.value()
        self.dist2ThresholdKNN = self.ui.DSBThreshold_2.value()
        self.detectShadowsKNN  = self.ui.CBDShadowsKNN.isChecked()
        #BKG LSBP
        self.nSamplesLSBP = self.ui.SBNSamplesLSBP.value()
        self.LSBPRadius = self.ui.SBLRadius.value()
        self.TupperLSBP = self.ui.DSBTupper.value()
        self.RscaleLSBP = self.ui.DSRScale.value()
        self.LSBPthreshold = self.ui.SBLThreshold.value()
        self.minCountLSBP = self.ui.SBminCount.value()
        #print(self.minCountLSBP)
        #BKG MOG
        self.historyMOG = self.ui.SBHistoryMOG.value()
        self.nmixturesMOG = self.ui.SBMixtures.value()
        self.backgroundRatioMOG = self.ui.DSBRatio.value()
        self.noiseSigmaMOG = self.ui.SBNoise.value()
        #BKG MOG2
        self.historyMOG2 = self.ui.SBHistoryMOG2.value()
        self.varThresholdMOG2 = self.ui.SBThresholdMOG2.value()
        self.detectShadowsMOG2 = self.ui.CBDshadowsMOG2.isChecked()
        #BKG RNB
        self.alphaRNB = self.ui.DSBAlpha.value()
        self.ThuRNB = self.ui.SBThu.value()
        self.ThsRNB = self.ui.SBThs.value()
        #BKG FZBL
        self.alphaFZBL = self.ui.DSBAlphaFL.value()
        self.ThsFZBL = self.ui.SBThSFL.value()
        self.ThfsFZBL= self.ui.DSBThfsFL.value()
        #BKG FZB
        self.alphaFZB = self.ui.DSBAlphaFZB.value()
        self.alphaMinFZB = self.ui.DSBAlphaFZB_2.value()
        self.ThsFZB = self.ui.SBThSFZB.value()
        self.ThfsFZB = self.ui.DSBThfsFZB.value()
        #Image Img Subtractor
        self.alphaSUB = self.ui.DSBAlphaI.value()
        self.bethaSUB = self.ui.DSBBetaI.value()
        self.constantSUB = self.ui.DSBConstant.value()
        #Image Lapse
        self.alphaLapse = self.ui.DSBAlphaL.value()
        self.bethaLapse = self.ui.DSBBetaL.value()
        self.constantLapse = self.ui.DSBConstantL.value()
        #print(self.alphaLapse)
        #print(self.bethaLapse)
        #print(self.constantLapse)
        #print(self.ThfsFZB)
        #print(self.LSBPthreshold)
        #print(self.minCountLSBP)

    def Set_Camera_Settings(self):
        #camera orca spark
        self.bgkSubtractor()
        self.BackgroundSettings()
        self.PlotExtraWindow = self.ui.CBProcess.isChecked()
        if (self.ui.CBCamera.currentText() == 'C11440-36U'):
            #print('C11440-36U')


            self.Exposure = self.ui.DSBExposure.value()
            self.Contrast = self.ui.SBCGain.value()
            self.Bits = self.ui.CBBits.currentText()
            self.Binning = self.ui.CBBinning_2.currentText()
            self.x0pos = self.ui.SBXP.value()
            self.y0pos = self.ui.SBYP.value()
            self.ImWidth = self.ui.SBWidth.value()
            self.ImHeight = self.ui.SBHeight.value()
            #print(self.ImHeight)


        if (self.ui.CBCamera.currentText() == 'C13440-20CU'):
            #print('C13440-20CU')

            self.Exposure = self.ui.DSBExposure.value()
            self.Contrast = self.ui.SBCGain.value()
            self.Bits = self.ui.CBBits_2.currentText()
            self.Binning = self.ui.CBBinning.currentText()
            self.x0pos = self.ui.SBXP.value()
            self.y0pos = self.ui.SBYP.value()
            self.ImWidth = self.ui.SBWidth.value()
            self.ImHeight = self.ui.SBHeight.value()
            #print(self.ImHeight)

        if (self.ui.CBCamera.currentText() == 'no camera'):
            print('no camera')


##FUNCTIONS TO PLOT IMAGE
    def set_img_seq_save_path(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image Sequence as', '', '(*.tiff)')
        if path == '':
            return
        #print(path)
        #print(path[0].rsplit('.', 1)[0])
        if path[0].endswith('.tiff') or path[0].endswith('.tif'):
            path = path[0]
        else:
            #path = path[0] + '.tiff'
            print('no file name')
        #get subfolder for image visualization
        Mean_Dir = (os.path.dirname(path))
        FolderNameM = (os.path.basename(path.rsplit('.', 1)[0]))
        FileName = os.path.basename(path)
        FolderPathM = Mean_Dir + '/' + FolderNameM
        # Create target Directory if don't exist
        if not os.path.exists(FolderPathM):
            os.mkdir(FolderPathM)
            print("Directory ", FolderPathM, " Created ")
        else:
            print("Directory ", FolderPathM, " already exists")
        path = FolderPathM + '/' + FileName

        self.ui.LEFileP.setText(path)

    def preview_slot(self, ev):
        self.Set_Camera_Settings()
        self.BackgroundSettings()
        if (self.ui.PBLive.text()=='Live'):
            ev = True
            self.ui.PBLive.setText('Stop')
            self.ui.PBLive_2.setText('Stop')
        else:
            ev = False
            self.ui.PBLive.setText('Live')
            self.ui.PBLive_2.setText('Live')
        #print(ev)
        if ev:
            # set variables of the camera
            model = self.ui.CBCamera.currentText()
            exp = self.Exposure / 1000.0
            contra = self.Contrast
            bits = self.Bits
            binning = self.Binning
            x0pos = self.x0pos
            y0pos = self.y0pos
            width = self.ImWidth
            height = self.ImHeight
            self.bgkSubtractor()
            subtractor = self.subtractor
            image_display= self.imagedisplay
            lapse = self.lapse
            PlotExtraWindow = self.PlotExtraWindow
            #exp = self.ui.DSBExposure.value() / 1000.0
            params = {'model':      model,
                      'exposure':   exp,
                      'contrast':   contra,
                      'bits':       bits,
                      'binning':    binning,
                      'x0pos':      x0pos,
                      'y0pos':      y0pos,
                      'width':      width,
                      'height':     height,
                      'subtractor':  subtractor,
                      'image_display': image_display,
                      'lapse':          lapse,
                      'PlotExtraWindow': PlotExtraWindow,
                      # BGK CNT
                      'minPixelStabilityCNT': self.minPixelStabilityCNT,
                      'maxPixelStabilityCNT': self.maxPixelStabilityCNT,
                      'useHistoryCNT': self.useHistoryCNT,
                      'isParallelCNT': self.isParallelCNT,
                      # BGK GMG
                      'initializationFramesGMG': self.initializationFramesGMG,
                      'decisionThresholdGMG': self.decisionThresholdGMG,
                      # BGK GSOC
                      'nSamplesGSOC': self.nSamplesGSOC,
                      'replaceRateGSOC': self.replaceRateGSOC,
                      'propagationRateGSOC': self.propagationRateGSOC,
                      'hitsThresholdGSOC': self.hitsThresholdGSOC,
                      'alphaGSOC': self.alphaGSOC,
                      'betaGSOC': self.betaGSOC,
                      # BGK KNN
                      'historyKNN': self.historyKNN,
                      'dist2ThresholdKNN': self.dist2ThresholdKNN,
                      'detectShadowsKNN': self.detectShadowsKNN,
                      # BKG LSBP
                      'nSamplesLSBP': self.nSamplesLSBP,
                      'LSBPRadius': self.LSBPRadius,
                      'TupperLSBP': self.TupperLSBP,
                      'RscaleLSBP': self.RscaleLSBP,
                      'LSBPthreshold': self.LSBPthreshold,
                      'minCountLSBP': self.minCountLSBP,
                      # BKG MOG
                      'historyMOG': self.historyMOG,
                      'nmixturesMOG': self.nmixturesMOG,
                      'backgroundRatioMOG': self.backgroundRatioMOG,
                      'noiseSigmaMOG': self.noiseSigmaMOG,
                      # BKG MOG2
                      'historyMOG2': self.historyMOG2,
                      'varThresholdMOG2': self.varThresholdMOG2,
                      'detectShadowsMOG2': self.detectShadowsMOG2,
                      # BKG RNB
                      'alphaRNB': self.alphaRNB,
                      'ThuRNB': self.ThuRNB,
                      'ThsRNB': self.ThsRNB,
                      # BKG FZBL
                      'alphaFZBL': self.alphaFZBL,
                      'ThsFZBL': self.ThsFZBL,
                      'ThfsFZBL': self.ThfsFZBL,
                      # BKG FZB
                      'alphaFZB': self.alphaFZB,
                      'alphaMinFZB': self.alphaMinFZB,
                      'ThsFZB': self.ThsFZB,
                      'ThfsFZB': self.ThfsFZB,
                      # Image Img Subtractor
                      'alphaSUB': self.alphaSUB,
                      'bethaSUB': self.bethaSUB,
                      'constantSUB': self.constantSUB,
                      # Image Lapse
                      'alphaLapse': self.alphaLapse,
                      'bethaLapse': self.bethaLapse,
                      'constantLapse': self.constantLapse
                      }

            self.preview = CameraInterfaces.PreviewHamamatsu(**params)


            #print(self.preview.FrameRate)
            #print(self.preview.framerate)
            #print('subtractor')
            #print(subtractor)
            #print('image_display')
            #print(image_display)

            self.preview.start()

        else:
            self.levels = self.preview.levels
            mi = np.uint16(self.levels[0])
            mx = np.uint16(self.levels[1])
            self.levels = (mi, mx)
            levels = self.levels
            if ((levels[1] - levels[0] + 1) / 256) == 0:
                QtWidgets.QMessageBox.warning(self, 'Invalid min max',
                                              'Your min max values are\n' + str(levels[0]) + ', '
                                              + str(levels[1]) + '\nThey must have a range greater than 256')
                self.ui.PBAcquire.setDisabled(True)
            else:
                self.ui.PBAcquire.setEnabled(True)

            self.preview.end()

            while self.preview.camera_open:
                time.sleep(0.00000000000000000000001)

            self.preview = None

    def update_preview(self, v):
        self.Set_Camera_Settings()
        self.BackgroundSettings()
        if not hasattr(self, 'preview'):
            return
        if isinstance(self.preview, CameraInterfaces.PreviewHamamatsu):
            self.preview.exposure = self.Exposure / 1000.0
            self.preview.Contrast = self.Contrast
            self.bgkSubtractor()
            #subtractor = self.subtractor
            #image_display = self.imagedisplay
            #lapse = self.lapse
            self.bgkSubtractor()
            self.preview.subtractor = self.subtractor
            self.preview.imagedisplay = self.imagedisplay
            self.preview.lapse = self.lapse

            Bits = self.Bits
            if (Bits == '8'):
                self.preview.bits = 256.0
            if (Bits == '10'):
                self.preview.bits = 1024.0
            if (Bits == '12'):
                self.preview.bits = 4096.0
            if (Bits == '14'):
                self.preview.bits = 16384.0
            if (Bits == '16'):
                self.preview.bits = 65536.0
            #print(self.preview.hcam.getPropertyValue("binning"))
            if (self.Binning == 'Customize'):
                self.preview.vsize = self.ImHeight
                self.preview.hsize = self.ImWidth
            self.preview.binning = self.Binning
            #print(self.preview.hcam.getPropertyValue("binning"))

    def acquire_slot(self, ev):
        if (self.ui.PBAcquire.text()=='Acquire'):
            #self.ui.PBAcquire.setText('Abort')
            ev = True
            self.ui.PBAcquire.setText('Abort')
            #time.sleep(0.005)
            #self.ui.PBLive_2.setText('Stop')
        else:
            ev = False
            self.ui.PBAcquire.setText('Acquire')
            path = os.path.dirname(self.ui.LEFileP.text())
            self.ui.LEPATH.setText(path)
            print(path)
            dirmodel = QtWidgets.QFileSystemModel(self)
            dirmodel.setRootPath(path)
            self.ui.TlistFrame.setModel(dirmodel)
            self.ui.TlistFrame.setRootIndex(dirmodel.setRootPath(path))

            #time.sleep(0.005)
            #self.ui.PBLive_2.setText('Live')
        if ev:

            if (not self.ui.LEFileP.text().endswith('.tiff')) and \
                    (not self.ui.LEFileP.text().endswith('.tif')):
                QtWidgets.QMessageBox.warning(self, 'Invalid extension', 'Your must save your file with either an'
                                                                         ' .tiff or .tif extension!')
                self.ui.PBAcquire.setChecked(False)
                self.ui.PBAcquire.setText('Abort')
                return

            if hasattr(self, 'preview'):
                if isinstance(self.preview, CameraInterfaces.PreviewHamamatsu):
                    self.preview_slot(False)
            # Settings to record video
            self.Set_Camera_Settings()
            self.BackgroundSettings()
            model = self.ui.CBCamera.currentText()
            exp = self.Exposure / 1000.0
            contra = self.Contrast
            bits = self.Bits
            binning = self.Binning
            x0pos = self.x0pos
            y0pos = self.y0pos
            width = self.ImWidth
            height = self.ImHeight
            #
            s = self.ui.DSBTime.value()

            duration = s
            #exp = self.ui.sliderExposure.value() / 1000.0
            filename = self.ui.LEFileP.text()

            #compression = self.ui.sliderCompressionLevel.value()
            compression = 1
            FlagEndFrame = self.ui.RBFrames.isChecked()
            FlagEndTime  = self.ui.RBtime.isChecked()
            NumberOfFrames = self.ui.SBFrames.value()
            self.bgkSubtractor()
            subtractor = self.subtractor
            image_display = self.imagedisplay
            lapse = self.lapse
            PlotExtraWindow = self.PlotExtraWindow
            params = {'exposure': exp,
                      'compression': compression,
                      'levels': self.levels,
                      'stims': {},
                      'version': self.__version__,
                      'model': model,
                      'exposure': exp,
                      'contrast': contra,
                      'bits': bits,
                      'binning': binning,
                      'x0pos': x0pos,
                      'y0pos': y0pos,
                      'width': width,
                      'height': height,
                      'NumberOfFrames':0.0,
                      'LapseTime': 0.0,
                      'subtractor': subtractor,
                      'image_display': image_display,
                      'lapse': lapse,
                      'PlotExtraWindow': PlotExtraWindow,
                      # BGK CNT
                      'minPixelStabilityCNT': self.minPixelStabilityCNT,
                      'maxPixelStabilityCNT': self.maxPixelStabilityCNT,
                      'useHistoryCNT': self.useHistoryCNT,
                      'isParallelCNT': self.isParallelCNT,
                      # BGK GMG
                      'initializationFramesGMG': self.initializationFramesGMG,
                      'decisionThresholdGMG': self.decisionThresholdGMG,
                      # BGK GSOC
                      'nSamplesGSOC': self.nSamplesGSOC,
                      'replaceRateGSOC': self.replaceRateGSOC,
                      'propagationRateGSOC': self.propagationRateGSOC,
                      'hitsThresholdGSOC': self.hitsThresholdGSOC,
                      'alphaGSOC': self.alphaGSOC,
                      'betaGSOC': self.betaGSOC,
                      # BGK KNN
                      'historyKNN': self.historyKNN,
                      'dist2ThresholdKNN': self.dist2ThresholdKNN,
                      'detectShadowsKNN': self.detectShadowsKNN,
                      # BKG LSBP
                      'nSamplesLSBP': self.nSamplesLSBP,
                      'LSBPRadius': self.LSBPRadius,
                      'TupperLSBP': self.TupperLSBP,
                      'RscaleLSBP': self.RscaleLSBP,
                      'LSBPthreshold': self.LSBPthreshold,
                      'minCountLSBP': self.minCountLSBP,
                      # BKG MOG
                      'historyMOG': self.historyMOG,
                      'nmixturesMOG': self.nmixturesMOG,
                      'backgroundRatioMOG': self.backgroundRatioMOG,
                      'noiseSigmaMOG': self.noiseSigmaMOG,
                      # BKG MOG2
                      'historyMOG2': self.historyMOG2,
                      'varThresholdMOG2': self.varThresholdMOG2,
                      'detectShadowsMOG2': self.detectShadowsMOG2,
                      # BKG RNB
                      'alphaRNB': self.alphaRNB,
                      'ThuRNB': self.ThuRNB,
                      'ThsRNB': self.ThsRNB,
                      # BKG FZBL
                      'alphaFZBL': self.alphaFZBL,
                      'ThsFZBL': self.ThsFZBL,
                      'ThfsFZBL': self.ThfsFZBL,
                      # BKG FZB
                      'alphaFZB': self.alphaFZB,
                      'alphaMinFZB': self.alphaMinFZB,
                      'ThsFZB': self.ThsFZB,
                      'ThfsFZB': self.ThfsFZB,
                      # Image Img Subtractor
                      'alphaSUB': self.alphaSUB,
                      'bethaSUB': self.bethaSUB,
                      'constantSUB': self.constantSUB,
                      # Image Lapse
                      'alphaLapse': self.alphaLapse,
                      'bethaLapse': self.bethaLapse,
                      'constantLapse': self.constantLapse
                      }

            #self.ui.progressBarWriter.setMaximum(int((duration * 1000) / self.ui.sliderExposure.value()) - 1)
            self.ui.PBLive_2.setDisabled(True)
            #self.ui.PBAcquire.setText('Abort')

            q = Queue.Queue()

            self.writer = CameraInterfaces.WriterHamamatsu(q, filename, compression, self.levels, params)
            self.acquisition = CameraInterfaces.AcquireHamamatsu(params, q, duration, FlagEndFrame, FlagEndTime, NumberOfFrames)
            #self.ui.PBAcquire.setText('Abort')

            self.writer.start()
            self.acquisition.start()

        else:
            try:

                self.acquisition.end()
                self.writer.end()
                if QtWidgets.QMessageBox.question(self, 'Stop writer?', 'Would you like to abort the writer as well?\n'
                                                                        'You will loose any frames that are currently '
                                                                        'in the queue', QtWidgets.QMessageBox.Abort,
                                                  QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Abort:
                    print("oscar stop function")
                    #writer.end()
            except:
                pass
            self.ui.PBLive_2.setEnabled(True)
            self.ui.PBAcquire.setText('Acquire')
            self.ui.PBAcquire.setChecked(False)
            #print("end")


    def set_frames_written_progressBar(self, fnum, qsize):
        self.ui.progressBarAcquisition.setValue(fnum)
        self.ui.labelQSize.setText(str(qsize))

    def add_stim(self):
        pass

    def del_stim(self):
        pass

    def export_config(self):
        pass

    def import_config(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    ui = Main()
    ui.setWindowTitle('PARTICLE AND FLOW VISUALIZATION SOFTWARE V1.0')
    ui.show()
    sys.exit(app.exec_())
