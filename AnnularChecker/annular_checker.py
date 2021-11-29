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
#

#### plugins errors
#import pcbnew;pcbnew.GetWizardsBackTrace()

global mm_ius, DRL_EXTRA, AR_SET, AR_SET_V, DRL_EXTRA_ius, MIN_AR_SIZE, MIN_AR_SIZE_V, found_violations, LogMsg, ___version___

___version___="1.7.2"

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
#import subprocess
import os
import pcbnew
from pcbnew import *
# import base64
# from wx.lib.embeddedimage import PyEmbeddedImage
import time

from . import AnnularDlg
from . import AnnularResultDlg

sys.path.append(os.path.dirname(__file__))

debug = False
def wxLogDebug(msg,dbg):
    """printing messages only if show is omitted or True"""
    if dbg == True:
        wx.LogMessage(msg)
#
def find_pcbnew_w():
    windows = wx.GetTopLevelWindows()
    pcbneww = [w for w in windows if "pcbnew" in w.GetTitle().lower()]
    if len(pcbneww) != 1:
        return None
    return pcbneww[0]
#

class AnnularResult_Dlg(AnnularResultDlg.AnnularResultDlg):
    # from https://github.com/MitjaNemec/Kicad_action_plugins
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        if wx.__version__ < '4.0':
            self.SetSizeHintsSz(sz1, sz2)
        else:
            super(AnnularResult_Dlg, self).SetSizeHints(sz1, sz2)

    def onOK(self, event):
        self.Destroy()
        #return self.EndModal(wx.ID_OK) # if modal_result == wx.ID_OK:
        
    def OnClickCopy(self, event):  
        self.m_richTextResult.SelectAll()
        self.m_richTextResult.Copy()
        #global LogMsg
        #copy2clip(LogMsg)
        self.copy_btn.SetLabel("Text Copied")

    # def onDeleteClick(self, event):
    #     return self.EndModal(wx.ID_DELETE)
    # 
    # def onConnectClick(self, event):
    #     return self.EndModal(wx.ID_REVERT)

    def __init__(self,  parent):
        import wx
        AnnularResultDlg.AnnularResultDlg.__init__(self, parent)
        #self.GetSizer().Fit(self)
        self.SetMinSize(self.GetSize())
                #### ----- connections
        # Connect Events
        self.Bind(wx.EVT_BUTTON, self.onOK, self.ok_btn)
        #self.ok_btn.Bind(wx.EVT_BUTTON, self.EndModal(wx.ID_OK))
        self.Bind(wx.EVT_BUTTON, self.OnClickCopy, self.copy_btn)
        self.ok_btn.SetFocus()
        # Tooltips
        self.copy_btn.SetToolTip( wx.ToolTip(u"Copy Text to Clipboard" ))
        self.ok_btn.SetToolTip( wx.ToolTip(u"Exit" ))

        #def onOK(self, event):
        #    return self.EndModal(wx.ID_OK) # if modal_result == wx.ID_OK:
        
        #def onConnectClick(self, event):
        #    return self.EndModal(wx.ID_REVERT)
            
        #self.m_buttonDelete.Bind(wx.EVT_BUTTON, self.onDeleteClick)
        #self.m_buttonReconnect.Bind(wx.EVT_BUTTON, self.onConnectClick)
        #if wx.__version__ < '4.0':
        #    self.m_buttonReconnect.SetToolTipString( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #    self.m_buttonRound.SetToolTipString( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
        #else:
        #    self.m_buttonReconnect.SetToolTip( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #    self.m_buttonRound.SetToolTip( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )

class Annular_Dlg(AnnularDlg.AnnularDlg):
    # from https://github.com/MitjaNemec/Kicad_action_plugins
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        if wx.__version__ < '4.0':
            self.SetSizeHintsSz(sz1, sz2)
        else:
            super(Annular_Dlg, self).SetSizeHints(sz1, sz2)

    def __init__(self,  parent):
        import wx
        AnnularDlg.AnnularDlg.__init__(self, parent)
        #self.GetSizer().Fit(self)
        self.SetMinSize(self.GetSize())
        #c1.Bind(wx.EVT_CHECKBOX, self.OntextMetric, c1)
        #self.m_checkBoxPHD.Bind(wx.EVT_CHECKBOX, self.OnClickCheck, self.m_checkBoxPHD)
        self.m_checkBoxPHD.Bind(wx.EVT_CHECKBOX, self.OnClickCheck)
        self.m_bitmapAR.SetBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "./annular-help.png")))
        
        #self.Bind(wx.EVT_CHECKBOX, self.OnClickCheck)
        #self.m_buttonDelete.Bind(wx.EVT_BUTTON, self.onDeleteClick)
        #self.m_buttonReconnect.Bind(wx.EVT_BUTTON, self.onConnectClick)
        #if wx.__version__ < '4.0':
        #    self.m_buttonReconnect.SetToolTipString( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #    self.m_buttonRound.SetToolTipString( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
        #else:
        #    self.m_buttonReconnect.SetToolTip( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #    self.m_buttonRound.SetToolTip( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
    def OnClickCheck(self, event):  
        #self.Destroy()
        if self.m_checkBoxPHD.IsChecked():
            #self.Destroy()
            self.m_staticTextPHD.Enable()
            self.m_textCtrlPHD.Enable()
        else:
            self.m_staticTextPHD.Disable()
            self.m_textCtrlPHD.Disable()
            
    # def onDeleteClick(self, event):
    #     return self.EndModal(wx.ID_DELETE)
    # 
    # def onConnectClick(self, event):
    #     return self.EndModal(wx.ID_REVERT)


# Python plugin stuff
class annular_check( pcbnew.ActionPlugin ):
    """
    A script to check for annular ring violations
    both for TH pads and vias 
    requirements: KiCAD pcbnew >= 4.0
        AR_SET    minimum annular accepted for pads
        AR_SET_V  minimum annular accepted for vias
    """
    global ___version___
    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Annular checker \nversion "+___version___
        self.category = "Checking PCB"
        self.description = "Automaticaly check annular on an existing PCB"
        #self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'annular.png')

    def Run( self ):
        import sys,os
        #mm_ius = 1000000.0
        # _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]

        #while True:
        #    time.sleep(1)
        #    pcbnew_window = find_pcbnew_window()
        #    if not pcbnew_window:
        #        continue
        pcbnew_window = find_pcbnew_w()
        #aParameters = RoundTrackDlg(None)
        aParameters = Annular_Dlg(pcbnew_window) # _pcbnew_frame)
        aParameters.m_LabelTitle.SetLabel("version:  "+___version___)
        aParameters.m_textCtrlARP.SetToolTip( wx.ToolTip(u"Annular Ring for Pads (mm)" ))
        aParameters.m_staticTextPHD.SetToolTip( wx.ToolTip(u"Drill extra margin (mm)" ))
        aParameters.m_textCtrlARV.SetToolTip( wx.ToolTip(u"Annular Ring for Vias (mm)" ))
        aParameters.m_staticTextARV.SetToolTip( wx.ToolTip(u"Annular Ring for Vias (mm)" ))
        aParameters.m_textCtrlPHD.SetToolTip( wx.ToolTip(u"Drill extra margin (mm)" ))
        aParameters.m_staticTextARP.SetToolTip( wx.ToolTip(u"Annular Ring for Pads (mm)" ))
        aParameters.m_checkBoxPHD.SetToolTip( wx.ToolTip(u"use drill size as finished hole size\nadding an extra drill margin" ))
        aParameters.m_textCtrlPHD.SetValue('0.1')
        aParameters.m_textCtrlARP.SetValue('0.125')
        aParameters.m_textCtrlARV.SetValue('0.125')
        aParameters.Show()
        modal_result = aParameters.ShowModal()
        #import pcbnew;pcbnew.GetWizardsBackTrace()
        if modal_result == wx.ID_OK:
            global mm_ius, DRL_EXTRA, AR_SET, AR_SET_V, DRL_EXTRA_ius, MIN_AR_SIZE, MIN_AR_SIZE_V
            phd = float(aParameters.m_textCtrlPHD.GetValue().replace(',','.'))
            ar  = float(aParameters.m_textCtrlARP.GetValue().replace(',','.'))
            arv = float(aParameters.m_textCtrlARV.GetValue().replace(',','.'))
            if aParameters.m_checkBoxPHD.IsChecked():
                DRL_EXTRA=phd
                DRL_EXTRA_ius=DRL_EXTRA * mm_ius
            else:
                DRL_EXTRA=0
                DRL_EXTRA_ius=DRL_EXTRA * mm_ius
            AR_SET = ar   #minimum annular accepted for pads
            MIN_AR_SIZE = AR_SET * mm_ius
            
            AR_SET_V = arv  #minimum annular accepted for vias
            MIN_AR_SIZE_V = AR_SET_V * mm_ius
            #snap2grid(gridSizeMM,use_grid_origin)
            calculate_AR()
        else:
            None  # Cancel

    
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


def calculate_AR():
    global mm_ius, DRL_EXTRA, AR_SET, AR_SET_V, DRL_EXTRA_ius, MIN_AR_SIZE, MIN_AR_SIZE_V
    board = pcbnew.GetBoard()
    PassC=FailC=0
    PassCV=FailCV=0
    
    PassCN=FailCN=0
    PassCVN=FailCVN=0
    
    fileName = GetBoard().GetFileName()
    dirpath = os.path.abspath(os.path.expanduser(fileName))
    path, fname = os.path.split(dirpath)
    ext = os.path.splitext(os.path.basename(fileName))[1]
    name = os.path.splitext(os.path.basename(fileName))[0]
    #wx.LogMessage(dir)
    #lsep=os.linesep
    lsep='\n'
    proj_path = os.path.dirname(os.path.abspath(fileName))
    out_filename_AR_checking=proj_path+os.sep+name+"_AR-Check.txt"
    
    if len(fileName)==0:
        wx.LogMessage("a board needs to be saved/loaded!")
    else:
        found_violations=False
        pcbnew_window = find_pcbnew_w()
        # _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
        aResult = AnnularResult_Dlg(pcbnew_window)
        #import pcbnew;pcbnew.GetWizardsBackTrace()
        writeTxt= aResult.m_richTextResult.WriteText
        rt = aResult.m_richTextResult
        rt.BeginItalic()
        writeTxt("AR checking written on:\n'"+out_filename_AR_checking+"'\n")
        writeTxt("'action_menu_annular_check.py'\n")
        #frame.m_richText1.WriteText("'action_menu_annular_check.py'\n")
        LogMsg=""
        msg="AR checking written on:\n'"+out_filename_AR_checking+"'\n"
        msg+="'action_menu_annular_check.py'\n"
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
            if  hasattr(pcbnew,'VIA'):
                via = pcbnew.VIA
                testing = type(item)
            else:
                via = pcbnew.PCB_VIA  #'PCB_VIA'
                item = pcbnew.Cast_to_PCB_VIA(item)
                testing = type(item) #item.GetClass()

            #writeTxt(str(testing))
            if testing is via: # or via in testing:
                #writeTxt(str(testing)+"here")
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
        
        if  hasattr(board,'GetModules'):
            footprints = board.GetModules()
            PAD_ATTR_STANDARD = PAD_ATTRIB_STANDARD
            PAD_ATTR_HOLE_NOT_PLATED = PAD_ATTRIB_HOLE_NOT_PLATED
        else:
            footprints = board.GetFootprints()
            PAD_ATTR_STANDARD = PAD_ATTRIB_PTH # HOLE_ATTRIBUTE_HOLE_PAD
            PAD_ATTR_HOLE_NOT_PLATED = HOLE_ATTRIBUTE_HOLE_MECHANICAL
        for module in footprints:
            try:
                module_Pads=module.PadsList()
            except:
                module_Pads=module.Pads()
            for pad in module_Pads:                    #print(pad.GetAttribute())
                if pad.GetAttribute() == PAD_ATTR_STANDARD: #TH pad
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
                if pad.GetAttribute() == PAD_ATTR_HOLE_NOT_PLATED:
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
            aResult.m_staticTitle.SetLabel(" Check result: (Violations found)")
            #self.title.SetForegroundColour('#FF0000')
            aResult.m_staticTitle.SetBackgroundColour('#FF0000')
            font = wx.Font(wx.DEFAULT, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
            aResult.m_staticTitle.SetFont(font)
        else:
            #frame.m_staticTitle = wx.StaticText(frame, label=" Annular Check result: OK")
            aResult.m_staticTitle.SetLabel(" Annular Check result: OK")
            aResult.m_staticTitle.SetBackgroundColour('#00FF00')            
            font = wx.Font(wx.DEFAULT, wx.DECORATIVE, wx.ITALIC, wx.BOLD)
            aResult.m_staticTitle.SetFont(font)
        
        with open(out_filename_AR_checking,'w') as f_out:
            f_out.write(LogMsg)
    
        aResult.Show()
        #modal_result = aResult.ShowModal()
        #if modal_result == wx.ID_OK:
        #    aResult.Destroy()
        #if modal_result == wx.ID_OK:
        #    aResult.Destroy()
        
        
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


#  execfile("annular.py")
# annular.py Testing PCB for Annular Ring >= 0.15
# AR violation of 0.1 at XY 172.974,110.744
# VIAS that Pass = 100 Fails = 1
# AR violation of 0.1 at XY 172.212,110.744
# AR violation of 0.0 at XY 154.813,96.52
# PADS that Pass = 49 Fails = 2

