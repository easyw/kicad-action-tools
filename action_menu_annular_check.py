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


___version___="1.5.8x"

global mm_ius, DRL_EXTRA, AR_SET, AR_SET_V, DRL_EXTRA_ius, MIN_AR_SIZE, MIN_AR_SIZE_V, found_violations, LogMsg
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
import wx.richtext
import subprocess
import os
import pcbnew
from pcbnew import *
import base64
from wx.lib.embeddedimage import PyEmbeddedImage
sys.path.append(os.path.dirname(__file__))


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
        
        ###########################################################################
        ## Class AR_Prm
        ###########################################################################
        
        class AR_Prm ( wx.Dialog ):
            
            def __init__( self, parent ):
                wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "AR parameters", pos = wx.DefaultPosition, size = wx.Size( 320,193 ), style = wx.DEFAULT_DIALOG_STYLE )
                
                self.SetSizeHints( 500,500 )
                
                self.SetIcon(PyEmbeddedImage(annular_ico_b64_data).GetIcon())
                
                bSizer1 = wx.BoxSizer( wx.VERTICAL )
                
                gSizer2 = wx.GridSizer( 0, 2, 0, 0 )
                
                self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"PHD margin", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
                self.m_staticText11.Wrap( -1 )
                
                gSizer2.Add( self.m_staticText11, 0, wx.ALL, 5 )
                
                self.m_textPHD = wx.TextCtrl( self, wx.ID_ANY, str(DRL_EXTRA), wx.DefaultPosition, wx.DefaultSize, 0 )
                gSizer2.Add( self.m_textPHD, 0, wx.ALL, 5 )
                
                self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"AR for pads", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
                self.m_staticText1.Wrap( -1 )
                
                gSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
                
                self.m_textAR_SET = wx.TextCtrl( self, wx.ID_ANY, str(AR_SET), wx.DefaultPosition, wx.DefaultSize, 0 )
                gSizer2.Add( self.m_textAR_SET, 0, wx.ALL, 5 )
                
                self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"AR for vias", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
                self.m_staticText12.Wrap( -1 )
                
                gSizer2.Add( self.m_staticText12, 0, wx.ALL, 5 )
                
                self.m_textAR_SET_V = wx.TextCtrl( self, wx.ID_ANY, str(AR_SET_V), wx.DefaultPosition, wx.DefaultSize, 0 )
                gSizer2.Add( self.m_textAR_SET_V, 0, wx.ALL, 5 )
                
                
                bSizer1.Add( gSizer2, 1, wx.EXPAND, 5 )
                
                gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
                
                self.m_ok_btn = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
                gSizer1.Add( self.m_ok_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
                
                # self.m_cancel_btn = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
                # gSizer1.Add( self.m_cancel_btn, 0, wx.ALL, 5 )
                
                
                bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )
                
                
                self.SetSizer( bSizer1 )
                self.Layout()
                
                self.Centre( wx.BOTH )
                
                #### ----- connections
                # Connect Events
                self.Bind(wx.EVT_BUTTON, self.OnClickOK, self.m_ok_btn)
                # self.Bind(wx.EVT_BUTTON, self.OnClickCancel, self.m_cancel_btn)
                # Tooltips
                #self.m_cancel_btn.SetToolTip( wx.ToolTip(u"Cancel" ))
                self.m_ok_btn.SetToolTip( wx.ToolTip(u"Confirm" ))
                self.m_ok_btn.SetFocus()
                self.m_staticText1.SetToolTip( wx.ToolTip(u"Annular Ring for Pads (mm)" ))
                self.m_textAR_SET.SetToolTip( wx.ToolTip(u"Annular Ring for Pads (mm)" ))
                self.m_textAR_SET_V.SetToolTip( wx.ToolTip(u"Annular Ring for Vias (mm)" ))
                self.m_staticText12.SetToolTip( wx.ToolTip(u"Annular Ring for Vias (mm)" ))
                self.m_textPHD.SetToolTip( wx.ToolTip(u"Drill extra margin (mm)" ))
                self.m_staticText11.SetToolTip( wx.ToolTip(u"Drill extra margin (mm)" ))
                
            def __del__( self ):
                pass
        
            def OnClickOK(self, event):  
                global mm_ius, DRL_EXTRA, AR_SET, AR_SET_V, DRL_EXTRA_ius, MIN_AR_SIZE, MIN_AR_SIZE_V
                
                self.m_ok_btn.SetLabel("Clicked")
                phd = float(self.m_textPHD.GetValue().replace(',','.'))
                ar  = float(self.m_textAR_SET.GetValue().replace(',','.'))
                arv = float(self.m_textAR_SET_V.GetValue().replace(',','.'))
                DRL_EXTRA=phd
                DRL_EXTRA_ius=DRL_EXTRA * mm_ius
                
                AR_SET = ar   #minimum annular accepted for pads
                MIN_AR_SIZE = AR_SET * mm_ius
                
                AR_SET_V = arv  #minimum annular accepted for vias
                MIN_AR_SIZE_V = AR_SET_V * mm_ius
                self.Destroy()
                
            def OnClickCancel(self, event):  
                self.m_cancel_btn.SetLabel("Clicked")
                self.Destroy()
        
        #wx.MessageDialog(self.frame,"ciao")
        #subprocess.check_call(["C:\pathToYourProgram\yourProgram.exe", "your", "arguments", "comma", "separated"])
        #http://stackoverflow.com/questions/1811691/running-an-outside-program-executable-in-python
        
        ## class displayDialog(wx.Dialog):
        ##     """
        ##     The default frame
        ##     http://stackoverflow.com/questions/3566603/how-do-i-make-wx-textctrl-multi-line-text-update-smoothly
        ##     """
        ##     global mm_ius, DRL_EXTRA, AR_SET, AR_SET_V, DRL_EXTRA_ius, MIN_AR_SIZE, MIN_AR_SIZE_V, found_violations
        ##     #----------------------------------------------------------------------
        ##     #def __init__(self):
        ##     #    """Constructor"""
        ##     #    wx.Frame.__init__(self, None, title="Display Frame", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)
        ##     #    panel = wx.Panel(self)
        ##     def __init__(self, parent):
        ##         wx.Dialog.__init__(self, parent, id=-1, title="Annular Checker")#
        ##         #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION) 
        ##         #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION)
        ##         #, pos=DefaultPosition, size=DefaultSize, style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX), name="fname")
        ##         #, wx.ICON_INFORMATION) #, title="Annular Check", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)    
        ##         #
        ##         
        ##         self.SetIcon(PyEmbeddedImage(annular_ico_b64_data).GetIcon())
        ##         #wx.IconFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY)))
        ##         self.panel = wx.Panel(self)     
        ##         
        ##         if found_violations:
        ##             self.title = wx.StaticText(self.panel, label="")
        ##             #self.title.SetForegroundColour('#FF0000')
        ##             #self.title.SetBackgroundColour('#FF0000')
        ##             #font = wx.Font(wx.DEFAULT, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        ##             #self.title.SetFont(font)
        ##         else:
        ##             self.title = wx.StaticText(self.panel, label="")
        ##             #self.title.SetBackgroundColour('#00FF00')
        ##             #font = wx.Font(wx.DEFAULT, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
        ##             #self.title.SetFont(font)
        ##         #self.result = wx.StaticText(self.panel, label="")
        ##         #self.result.SetForegroundColour('#FF0000')
        ##         #self.button = wx.Button(self.panel, label="Save")
        ##         #self.lblname = wx.StaticText(self.panel, label="Your name:")
        ##         #self.editname = wx.TextCtrl(self.panel, size=(140, -1))
        ##         ##self.editname = wx.TextCtrl(self.panel, size = (400, 400), style = wx.TE_MULTILINE|wx.TE_READONLY)
        ##         self.m_richText1 = wx.richtext.RichTextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size = (400, 400), style = 0|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS )#  wx.TE_MULTILINE|wx.TE_READONLY) #0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        ##         #bSizer1.Add( self.m_richText1, 1, wx.EXPAND |wx.ALL, 5 )
		## 
        ## 
        ##         # Set sizer for the frame, so we can change frame size to match widgets
        ##         self.windowSizer = wx.BoxSizer()
        ##         self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        
        ##         
        ##         # Set sizer for the panel content
        ##         self.sizer = wx.GridBagSizer(5, 0)
        ##         self.sizer.Add(self.title, (0, 0))
        ##         #self.sizer.Add(self.result, (1, 0))
        ##         #self.sizer.Add(self.lblname, (1, 0))
        ##         ## self.sizer.Add(self.editname, (1, 0))
        ##         self.sizer.Add(self.m_richText1, (1, 0))
        ##         #self.ok_btn = wx.Button( self, wx.ID_ANY, u"Copy errors", wx.DefaultPosition, wx.DefaultSize, 0 )
        ##         #self.sizer.Add( self.ok_btn, 0, wx.ALL | wx.EXPAND)
        ##         #self.sizer.Add(self.ok_btn, (2, 0)) #, wx.ALL | flag=wx.EXPAND)
        ##         #self.sizer.Add( self.ok_btn, 0, wx.ALL, 5 )
        ##         
        ##         #self.sizer.Add(self.ok_btn, (2, 0), (1, 2), flag=wx.EXPAND)
        ## 
        ##         # Set simple sizer for a nice border
        ##         self.border = wx.BoxSizer()
        ##         self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
        ##         
        ##         #self.ok_btn = wx.Button( self, wx.ID_ANY, u"Copy errors", wx.DefaultPosition, wx.DefaultSize, 0 )
        ##         #self.windowSizer.Add(self.ok_btn, 0, wx.ALL)
        ##         #self.sizer.Add( self.ok_btn, (2,0))
        ##         #self.sizer.Add( self.ok_btn, 0, wx.ALL, 5 )
        ##         # Use the sizers
        ##         self.panel.SetSizerAndFit(self.border)  
        ##         self.SetSizerAndFit(self.windowSizer)  
        ##         #self.result.SetLabel(msg)
        ##         # Set event handlers
        ##         #self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        ##         #self.Show()
        ##         #self.Bind(wx.EVT_CLOSE,self.OnClose)
        ##     
        ##     #def OnClose(self,e):
        ##     #    #wx.LogMessage("c")
        ##     #    e.Skip()
        ##         #self.Close()
        ###########################################################################
        ## Class displayDialog
        ###########################################################################
        
        class displayDialog ( wx.Dialog ):
            
            global mm_ius, DRL_EXTRA, AR_SET, AR_SET_V, DRL_EXTRA_ius, MIN_AR_SIZE, MIN_AR_SIZE_V, found_violations, LogMsg
        
            def __init__( self, parent ):
                wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Annular Checker", pos = wx.DefaultPosition, size = wx.Size( 450,521 ), style = wx.DEFAULT_DIALOG_STYLE )
                
                self.SetSizeHints( 300,100 )
                self.SetIcon(PyEmbeddedImage(annular_ico_b64_data).GetIcon())
                
                bSizer1 = wx.BoxSizer( wx.VERTICAL )
                
                bSizer2 = wx.BoxSizer( wx.VERTICAL )
                
                self.m_staticTitle = wx.StaticText( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticTitle.Wrap( -1 )
                
                bSizer2.Add( self.m_staticTitle, 0, wx.ALL, 5 )
                
                self.m_richText1 = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
                self.m_richText1.SetMinSize( wx.Size( 400,400 ) )
                
                bSizer2.Add( self.m_richText1, 1, wx.EXPAND |wx.ALL, 5 )
                
                gSizer3 = wx.GridSizer( 0, 2, 0, 0 )
                
                self.ok_btn = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
                gSizer3.Add( self.ok_btn, 0, wx.ALL, 5 )
                
                self.copy_btn = wx.Button( self, wx.ID_ANY, u"Copy Text", wx.DefaultPosition, wx.DefaultSize, 0 )
                gSizer3.Add( self.copy_btn, 0, wx.ALL, 5 )
                
                
                bSizer2.Add( gSizer3, 1, wx.EXPAND, 5 )
                
                
                bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
                
                
                self.SetSizer( bSizer1 )
                self.Layout()
                
                self.Centre( wx.BOTH )
            
                #### ----- connections
                # Connect Events
                self.Bind(wx.EVT_BUTTON, self.OnClickOK, self.ok_btn)
                self.Bind(wx.EVT_BUTTON, self.OnClickCopy, self.copy_btn)
                self.ok_btn.SetFocus()
                # Tooltips
                self.copy_btn.SetToolTip( wx.ToolTip(u"Copy Text to Clipboard" ))
                self.ok_btn.SetToolTip( wx.ToolTip(u"Exit" ))
                
            def __del__( self ):
                pass
	
            def OnClickOK(self, event):  
                self.Destroy()
            
            def OnClickCopy(self, event):  
                self.m_richText1.SelectAll()
                self.m_richText1.Copy()
                #global LogMsg
                #copy2clip(LogMsg)
                self.copy_btn.SetLabel("Text Copied")
                
            #def setMsg(self, t_msg):
            #    pass
                #self.editname.SetValue(t_msg)
                #self.m_richText1.BeginBold()
                #self.m_richText1.WriteText(" You are in ")
                #self.m_richText1.BeginTextColour('red')
                #self.m_richText1.WriteText("danger ")
                #self.m_richText1.EndTextColour()
                #self.m_richText1.WriteText("at that spot!")
                #self.m_richText1.EndBold()
                #self.m_richText1.SetValue(t_msg)
                #self.m_htmlWin1.SetPage(t_msg)
                
            
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
            found_violations=False
            frame1 = AR_Prm(None)
            #frame = wx.Frame(None)
            frame1.Center()
            #frame.setMsg(LogMsg)
            frame1.ShowModal()
            frame1.Destroy()
            
            frame = displayDialog(None)
            LogMsg=""
            writeTxt= frame.m_richText1.WriteText
            rt = frame.m_richText1
            rt.BeginItalic()
            writeTxt("'action_menu_annular_check.py'\n")
            #frame.m_richText1.WriteText("'action_menu_annular_check.py'\n")
            msg="'action_menu_annular_check.py'\n"
            msg+="version = "+___version___
            writeTxt("version = "+___version___)
            msg+="\nTesting PCB for Annular Rings\nTH Pads >= "+repr(AR_SET)+" Vias >= "+repr(AR_SET_V)+"\nPHD margin on PTH = "+ repr(DRL_EXTRA)
            writeTxt("\nTesting PCB for Annular Rings\nTH Pads >= "+repr(AR_SET)+" Vias >= "+repr(AR_SET_V)+"\nPHD margin on PTH = "+ repr(DRL_EXTRA))
            rt.EndItalic()
            writeTxt('\n\n')
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
                        rt.BeginTextColour('red')
                        writeTxt("AR Via violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1])+'\n')
                        rt.EndTextColour()
                        #print (msg)
                        LogMsg+=msg+'\n'
                        FailCV = FailCV+1
                    else:
                        PassCV = PassCV+1
                #print type(item)
            
            msg="VIAS that Pass = "+repr(PassCV)+"; Fails = "+repr(FailCV)
            if FailCV >0:
                rt.BeginBold()
            writeTxt("VIAS that Pass = "+repr(PassCV)+"; ")
            if FailCV >0:
                rt.BeginTextColour('red')
            writeTxt("Fails = "+repr(FailCV)+'\n\n')
            if FailCV >0:
                rt.EndTextColour()
                rt.EndBold()
            print(msg)
            LogMsg+=msg+'\n'
            
            for module in board.GetModules():
                try:
                    module_Pads=module.PadsList()
                except:
                    module_Pads=module.Pads()
                for pad in module_Pads:                    #print(pad.GetAttribute())
                    if pad.GetAttribute() == PAD_ATTRIB_STANDARD: #TH pad
                        ARv = annring_size(pad)
                        #print(f_mm(ARv))
                        if ARv  < MIN_AR_SIZE:
            #                print("AR violation at %s." % (pad.GetPosition() / mm_ius ))  Raw units, needs fixing
                            XYpair =  pad.GetPosition()
                            msg="AR PTH violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1]) 
                            rt.BeginTextColour('red')
                            writeTxt("AR PTH violation of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1])+'\n')
                            rt.EndTextColour()
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
                                rt.BeginTextColour('red')
                                writeTxt("AR NPTH warning of "+f_mm(ARv)+" at XY "+f_mm(XYpair[0])+","+f_mm(XYpair[1])+'\n')
                                rt.EndTextColour()
                                #print (msg)
                                LogMsg+=msg+'\n'
                                FailCN = FailCN+1
                            else:
                                PassCN = PassCN+1
                        else:
                            PassCN = PassCN+1
                        
            #if FailCV >0:
            #writeTxt('\n')
            msg = "TH PADS that Pass = "+repr(PassC)+"; Fails = "+repr(FailC)
            if FailC >0:
                rt.BeginBold()
            writeTxt("TH PADS that Pass = "+repr(PassC)+"; ")
            if FailC >0:
                rt.BeginTextColour('red')
            writeTxt("Fails = "+repr(FailC)+'\n')
            if FailC >0:
                rt.EndTextColour()
                rt.EndBold()
            print(msg)
            LogMsg+=msg+'\n'
            
            msg="NPTH PADS that Pass = "+repr(PassCN)+"; Fails = "+repr(FailCN)
            #writeTxt('\n')
            if FailCN >0:
                rt.BeginBold()
            writeTxt("NPTH PADS that Pass = "+repr(PassCN)+"; ")
            if FailCN >0:
                rt.BeginTextColour('red')
            writeTxt("Fails = "+repr(FailCN)+'\n')
            if FailC >0:
                rt.EndTextColour()
                rt.EndBold()
            print(msg)
            LogMsg+=msg+'\n'
            
            pcbName = (os.path.splitext(GetBoard().GetFileName())[0]) #filename no ext
            #wx.LogMessage(pcbName)#LogMsg)
            ##wx.LogMessage(LogMsg)
            FC=r"C:\FreeCAD\bin\freecad.exe"
            kSU=r"C:\Cad\Progetti_K\3D-FreeCad-tools\kicad-StepUp-tools.FCMacro"
            #subprocess.check_call([FC, kSU, pcbName])
            ##p = subprocess.Popen([FC, kSU, pcbName])
            
            #found_violations=False
            if (FailC+FailCN+FailCV)>0:
                found_violations=True
            
            if found_violations:
                #frame.m_staticTitle = wx.StaticText(frame, label=" Check result: (Violations found)")
                frame.m_staticTitle.SetLabel(" Check result: (Violations found)")
                #self.title.SetForegroundColour('#FF0000')
                frame.m_staticTitle.SetBackgroundColour('#FF0000')
                font = wx.Font(wx.DEFAULT, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
                frame.m_staticTitle.SetFont(font)
            else:
                #frame.m_staticTitle = wx.StaticText(frame, label=" Annular Check result: OK")
                frame.m_staticTitle.SetLabel(" Annular Check result: OK")
                frame.m_staticTitle.SetBackgroundColour('#00FF00')            
                font = wx.Font(wx.DEFAULT, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
                frame.m_staticTitle.SetFont(font)
            ##frame = displayDialog(None)
            #frame = wx.Frame(None)
            frame.Center()
            #frame.setMsg(LogMsg)
            frame.ShowModal()
            frame.Destroy()
            #frame = wx.wxFrame(None, 10110, 'T-Make', size=wx.wxSize(100,100),
            #           style=wx.wxSTAY_ON_TOP)
            #frame.show()
        
# annular_check().register()
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
            description='KiCad PCB Annular Checker')
    parser.add_argument('file', type=str, help="KiCad PCB file")
    args = parser.parse_args()
    print("Loading %s" % args.file)
    main(pcbnew.LoadBoard(args.file))

else:
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

