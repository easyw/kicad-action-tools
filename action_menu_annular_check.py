# -*- coding: utf-8 -*-
#
# A script to check for annular ring violations
# both for TH pads and vias 
# requirements: KiCAD pcbnew >= 4.0
# annular.py release "1.5.1"
# 
# annular.py checking PCB for Annular Ring in Vias and TH Pads
# (SMD, Connector and NPTH are skipped)
# default Annular Ring >= 0.15 both for TH Pads and Vias
# to change values modify:
# 
#     AR_SET = 0.150   #minimum annular accepted for pads
#     AR_SET_V = 0.150  #minimum annular accepted for vias

#  annular.py

___version___="1.5.3"
#wx.LogMessage("My message")
mm_ius = 1000000.0
# (consider always drill +0.1)
DRL_EXTRA=0.1
DRL_EXTRA_ius=DRL_EXTRA * mm_ius

AR_SET = 0.125   #minimum annular accepted for pads
MIN_AR_SIZE = AR_SET * mm_ius

AR_SET_V = 0.125  #minimum annular accepted for vias
MIN_AR_SIZE_V = AR_SET_V * mm_ius

import sys
import wx
import subprocess
import os
import pcbnew
from pcbnew import *
# import base64
from wx.lib.embeddedimage import PyEmbeddedImage

class annular_check( pcbnew.ActionPlugin ):
    """
    A script to check for annular ring violations
    both for TH pads and vias 
    requirements: KiCAD pcbnew >= 4.0
    annular.py release "1.5.1"
    
    annular.py checking PCB for Annular Ring in Vias and TH Pads
    (SMD, Connector and NPTH are skipped)
    default Annular Ring >= 0.15 both for TH Pads and Vias
    to change values modify:
    
        AR_SET = 0.150   #minimum annular accepted for pads
        AR_SET_V = 0.150  #minimum annular accepted for vias
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Annular check"
        self.category = "Checking PCB"
        self.description = "Automaticaly check annular on an existing PCB"

    def Run( self ):
        
        #wx.MessageDialog(self.frame,"ciao")
        #subprocess.check_call(["C:\pathToYourProgram\yourProgram.exe", "your", "arguments", "comma", "separated"])
        #http://stackoverflow.com/questions/1811691/running-an-outside-program-executable-in-python
        class displayDialog(wx.Dialog):
            """
            The default frame
            http://stackoverflow.com/questions/3566603/how-do-i-make-wx-textctrl-multi-line-text-update-smoothly
            """
        
            #----------------------------------------------------------------------
            #def __init__(self):
            #    """Constructor"""
            #    wx.Frame.__init__(self, None, title="Display Frame", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)
            #    panel = wx.Panel(self)
            def __init__(self, parent):
                wx.Dialog.__init__(self, parent, id=-1, title="Annular Checker")#
                #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION) 
                #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION)
                #, pos=DefaultPosition, size=DefaultSize, style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX), name="fname")
                #, wx.ICON_INFORMATION) #, title="Annular Check", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)    
                #
                
                self.SetIcon(PyEmbeddedImage(annular_ico_b64_data).GetIcon())
                #wx.IconFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY)))
                self.panel = wx.Panel(self)     
                self.title = wx.StaticText(self.panel, label="Annular Check result:")
                #self.result = wx.StaticText(self.panel, label="")
                #self.result.SetForegroundColour('#FF0000')
                #self.button = wx.Button(self.panel, label="Save")
                #self.lblname = wx.StaticText(self.panel, label="Your name:")
                #self.editname = wx.TextCtrl(self.panel, size=(140, -1))
                self.editname = wx.TextCtrl(self.panel, size = (300, 400), style = wx.TE_MULTILINE|wx.TE_READONLY)
        
        
                # Set sizer for the frame, so we can change frame size to match widgets
                self.windowSizer = wx.BoxSizer()
                self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        
        
                # Set sizer for the panel content
                self.sizer = wx.GridBagSizer(5, 0)
                self.sizer.Add(self.title, (0, 0))
                #self.sizer.Add(self.result, (1, 0))
                #self.sizer.Add(self.lblname, (1, 0))
                self.sizer.Add(self.editname, (1, 0))
                #self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)
        
                # Set simple sizer for a nice border
                self.border = wx.BoxSizer()
                self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
        
                # Use the sizers
                self.panel.SetSizerAndFit(self.border)  
                self.SetSizerAndFit(self.windowSizer)  
                #self.result.SetLabel(msg)
                # Set event handlers
                #self.button.Bind(wx.EVT_BUTTON, self.OnButton)
                #self.Show()
                #self.Bind(wx.EVT_CLOSE,self.OnClose)
            
            #def OnClose(self,e):
            #    #wx.LogMessage("c")
            #    e.Skip()
                #self.Close()
            
            #def OnButton(self, e):
            #    self.result.SetLabel(self.editname.GetValue())
            def setMsg(self, t_msg):
                self.editname.SetValue(t_msg)
                
            
        def annring_size(pad):
            # valid for oval pad/drills
            annrX=(pad.GetSize()[0] - (pad.GetDrillSize()[0]+DRL_EXTRA_ius))/2
            annrY=(pad.GetSize()[1] - (pad.GetDrillSize()[1]+DRL_EXTRA_ius))/2
            #annr=min(pad.GetSize()) - max(pad.GetDrillSize())
            #if annr < MIN_AR_SIZE:
            #print annrX
            #print annrY
            #print pad.GetSize()[0]/mm_ius
            #print pad.GetSize()[0]#/mm_ius
            #print pad.GetDrillSize()[0]#/mm_ius
            #print DRL_EXTRA_ius
            #print pad.GetDrillSize()[0]/mm_ius
            #print (pad.GetDrillSize()[0]+DRL_EXTRA_ius)/mm_ius
            #print annrX/mm_ius
            return min(annrX,annrY)
        
        def annringNP_size(pad):
            # valid for oval pad/drills
            annrX=(pad.GetSize()[0] - (pad.GetDrillSize()[0]))/2
            annrY=(pad.GetSize()[1] - (pad.GetDrillSize()[1]))/2
            #annr=min(pad.GetSize()) - max(pad.GetDrillSize())
            #if annr < MIN_AR_SIZE:
            #print annrX
            #print annrY
            #print pad.GetSize()[0]/mm_ius
            #print pad.GetSize()[0]#/mm_ius
            #print pad.GetDrillSize()[0]#/mm_ius
            #print DRL_EXTRA_ius
            #print pad.GetDrillSize()[0]/mm_ius
            #print (pad.GetDrillSize()[0]+DRL_EXTRA_ius)/mm_ius
            #print annrX/mm_ius
            #return min(annrX,annrY)
            return annrX,annrY
        
        def vias_annring_size(via):
            # calculating via annular
            annr=(via.GetWidth() - (via.GetDrillValue()+DRL_EXTRA_ius))/2
            #print via.GetWidth()
            #print via.GetDrillValue()
            return annr
            
        def f_mm(raw):
            return repr(raw/mm_ius)
        
        board = pcbnew.GetBoard()
        PassC=FailC=0
        PassCV=FailCV=0
        
        PassCN=FailCN=0
        PassCVN=FailCVN=0
        
        fileName = GetBoard().GetFileName()
        if len(fileName)==0:
            wx.LogMessage("a board needs to be saved/loaded!")
        else:
                
            LogMsg=''
            msg="'action_menu_annular_check.py'\n"
            msg+="version = "+___version___
            msg+="\nTesting PCB for Annular Rings\nTH Pads >= "+repr(AR_SET)+" Vias >= "+repr(AR_SET_V)+"\nPHD margin on PTH = "+ repr(DRL_EXTRA)
             #print (msg)
            LogMsg+=msg+'\n\n'
            
            # print "LISTING VIAS:"
            for item in board.GetTracks():
                if type(item) is pcbnew.VIA:
                    pos = item.GetPosition()
                    drill = item.GetDrillValue()
                    width = item.GetWidth()
                    ARv = vias_annring_size(item)
                    if ARv  < MIN_AR_SIZE_V:
                    #            print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
                        XYpair =  item.GetPosition()
                        msg="AR Via violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) 
                        #print (msg)
                        LogMsg+=msg+'\n'
                        FailCV = FailCV+1
                    else:
                        PassCV = PassCV+1
                #print type(item)
            
            msg="VIAS that Pass = "+repr(PassCV)+"; Fails = "+repr(FailCV)
            print(msg)
            LogMsg+=msg+'\n'
            
            for module in board.GetModules():
                for pad in module.Pads():
                    #print(pad.GetAttribute())
                    if pad.GetAttribute() == PAD_ATTRIB_STANDARD: #TH pad
                        ARv = annring_size(pad)
                        #print(f_mm(ARv))
                        if ARv  < MIN_AR_SIZE:
            #                print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
                            XYpair =  pad.GetPosition()
                            msg="AR PTH violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) 
                            #print (msg)
                            LogMsg+=msg+'\n'
                            FailC = FailC+1
                        else:
                            PassC = PassC+1
                    if pad.GetAttribute() == PAD_ATTRIB_HOLE_NOT_PLATED:
                        ARvX, ARvY = annringNP_size(pad)
                        #print(f_mm(ARvX));print(f_mm(ARvY))
                        if (ARvX) != 0 or ARvY != 0:
                            ARv = min(ARvX, ARvY)
                            if ARv < MIN_AR_SIZE:
            #                    print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
                                XYpair =  pad.GetPosition()
                                msg="AR NPTH warning of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) 
                                #print (msg)
                                LogMsg+=msg+'\n'
                                FailCN = FailCN+1
                            else:
                                PassCN = PassCN+1
                        else:
                            PassCN = PassCN+1
                        
            msg = "TH PADS that Pass = "+repr(PassC)+"; Fails = "+repr(FailC)
            print(msg)
            LogMsg+=msg+'\n'
            
            msg="NPTH PADS that Pass = "+repr(PassCN)+"; Fails = "+repr(FailCN)
            print(msg)
            LogMsg+=msg+'\n'
            
            pcbName = (os.path.splitext(GetBoard().GetFileName())[0]) #filename no ext
            #wx.LogMessage(pcbName)#LogMsg)
            ##wx.LogMessage(LogMsg)
            FC=r"C:\FreeCAD\bin\freecad.exe"
            kSU=r"C:\Cad\Progetti_K\3D-FreeCad-tools\kicad-StepUp-tools.FCMacro"
            #subprocess.check_call([FC, kSU, pcbName])
            ##p = subprocess.Popen([FC, kSU, pcbName])
            
            frame = displayDialog(None)
            #frame = wx.Frame(None)
            frame.Center()
            frame.setMsg(LogMsg)
            frame.ShowModal()
            frame.Destroy()
            #frame = wx.wxFrame(None, 10110, 'T-Make', size=wx.wxSize(100,100),
            #           style=wx.wxSTAY_ON_TOP)
            #frame.show()
        
annular_check().register()



# "b64_data" is a variable containing your base64 encoded jpeg
annular_ico_b64_data =\
"""
iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAIQQAACEEB+v+u9gAAABl0RVh0U29mdHdhcmUAd3d
3Lmlua3NjYXBlLm9yZ5vuPBoAAAJ5SURBVDiNdZRNSFRRFMd/976ZJjeBn2PUoiLaiMFkFkHIQ0NBdBUlJuIqiixmIYjQRgiJYKAMXRRSi6TCD5gaWiSFsy
gixOyDpDAog8wn9SISapz33m0x82bmzcOzO/97/r973nn3XqGUojjCybIm4BhQD9Rl5XlgDnhi6ObTYo8oBIWTZeXAMNDlalW/FJYmMLd5fONA1NBN0wcKJ
8sagftAZWRJcWHS5vCiouJ3pnClUvC8VnDtpOTTDgGwCpwydHM2Bwony8LAe6koH7hjc37aQXN8XwzAv5DgUo9krF0C/ABqDN1ck9n1G0D54C2H6OTmEICt
KcXQTZvTCQegAhgFEFWzpW1A4uAHRaLfQhbPXgD+/8HfkKBhNMDXMACtEmgC6L/reCBWKGAzMmLxbQWWl2Fw0FJavqIkpYhO2m7aHADqNQcOLXq3DcSuKnp
6Ajmhry8g1tfTxGJBVzryLuepl0Bk16qiJJUHKU0qOjryEDe6u4OF6e7vitCGAohIAFk0XCWEQkp8oWmeVAAiu78EFj5vF6S2iFyBtGxJPJ72gSYmPNpyOH
McgAUJzFkazO/zetLRc4J43MayIJWCsTHLuTzkaellTa7rOVE1W9oOPDz6VjF90fI14QQ1RzhKCNsRhfpGEBqvB1jaKQDapKGbCeDBs/2C8Rb/XGTalsUQg
Fin5kKmDN185DrPAD8HzmrcbpUony0flgZXujSGT+SuSC94L20LcA8obXiduSp1H8kdiz8l8KJWEOvUeLNXuJAuQzdnPKAsrBoYAY4DaA7sWck8I1+qKex0
Cug1dHPNFcQmD1sL0AwcACJZeQF4BcwYuvm42PMfVgD11Y9MUIEAAAAASUVORK5CYII=
""" 


#  execfile("annular.py")
# annular.py Testing PCB for Annular Ring >= 0.15
# AR violation of 0.1 at XY 172.974,110.744
# VIAS that Pass = 100 Fails = 1
# AR violation of 0.1 at XY 172.212,110.744
# AR violation of 0.0 at XY 154.813,96.52
# PADS that Pass = 49 Fails = 2

