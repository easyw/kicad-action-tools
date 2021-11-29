# -*- coding: utf-8 -*-
#
# A script to generate POS file for kicad_pcb
# requirements: KiCAD pcbnew >= 4.0
# release "1.2.5"
# copyright Maurice easyw
# 
# main script from https://forum.kicad.info/t/pcba-wants-all-parts-in-the-pos-file-not-just-smd/10045/6
#

### plugins errors
#import pcbnew
#pcbnew.GetWizardsBackTrace()


___version___="1.2.8"
#wx.LogMessage("My message")
#mm_ius = 1000000.0

import sys, os
import pcbnew
import datetime
import wx
from pcbnew import *
import base64
from wx.lib.embeddedimage import PyEmbeddedImage

"""
execfile ("C:/kicad-wb-1602/msys64/home/userC/out3Dm/pack-x86_64/share/kicad/scripting/plugins/getpos.py")
"""

def find_pcbnew_w():
    windows = wx.GetTopLevelWindows()
    pcbneww = [w for w in windows if "pcbnew" in w.GetTitle().lower()]
    if len(pcbneww) != 1:
        return None
    return pcbneww[0]
#


def generate_POS(dir):
    import os
    mm_ius = 1000000.0
    
    my_board = pcbnew.GetBoard()

    fileName = pcbnew.GetBoard().GetFileName()
    
    dirpath = os.path.abspath(os.path.expanduser(fileName))
    path, fname = os.path.split(dirpath)
    ext = os.path.splitext(os.path.basename(fileName))[1]
    name = os.path.splitext(os.path.basename(fileName))[0]
    #wx.LogMessage(dir)
    #lsep=os.linesep
    lsep='\n'
    
    if len(dir)>0:
        dir = dir.rstrip('\\').rstrip('/')
        if not os.path.exists(path+os.sep+dir):
            #create dir
            os.mkdir(path+os.sep+dir)
        dir = dir+os.sep
        #wx.LogMessage(dir)
    else:
        dir = dir+os.sep
    #LogMsg1=lsep+"reading from:" + lsep + dirpath + lsep + lsep
    out_filename_top_SMD=path+os.sep+dir+name+"_POS_top_SMD.txt"
    out_filename_bot_SMD=path+os.sep+dir+name+"_POS_bot_SMD.txt"
    out_filename_top_THD=path+os.sep+dir+name+"_POS_top_THD.txt"
    out_filename_bot_THD=path+os.sep+dir+name+"_POS_bot_THD.txt"
    out_filename_top_VIRTUAL=path+os.sep+dir+name+"_POS_top_Virtual.txt"
    out_filename_bot_VIRTUAL=path+os.sep+dir+name+"_POS_bot_Virtual.txt"
    out_filename_ALL=path+os.sep+dir+name+"_POS_All.txt"

    Header_1="### Module positions - created on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+lsep
    Header_1+="### Printed by pcb_positions plugin"+lsep
    Header_1+="## Unit = mm, Angle = deg."+lsep
    #LogMsg+="## Side : All"+lsep
    if hasattr(my_board, 'GetAuxOrigin'):
        getAO = my_board.GetAuxOrigin()
    else:
        getAO = my_board.GetDesignSettings().GetAuxOrigin()
    Header_2="## Board Aux Origin: " + '{0:.3f}'.format( getAO.x / mm_ius)+'mm ,'+'{0:.3f}'.format(getAO.y / mm_ius)+'mm'+lsep
    Header_2+="{0:<14}".format("# Ref")+"{0:<20}".format("Val")+"{0:<30}".format("Package")+\
            "{0:<11}".format("PosX")+"{0:<11}".format("PosY")+"{0:<11}".format("Pin1_PosX")+"{0:<11}".format("Pin1_PosY")+"{0:<8}".format("  Rot")+\
            "{0:<10}".format("  Side")+"  Type"+lsep

    content_top_SMD=''
    content_bot_SMD=''
    content_top_THD=''
    content_bot_THD=''
    content_top_VIRTUAL=''
    content_bot_VIRTUAL=''
    content_ALL=''
    SMD_pads = 0
    TH_pads = 0
    Virt_pads = 0
    TH_top_cnt = 0
    TH_bot_cnt = 0
    SMD_top_cnt = 0
    SMD_bot_cnt = 0
    Virt_top_cnt = 0
    Virt_bot_cnt = 0
    
    bb = my_board.GetBoardEdgesBoundingBox()
    pcb_height = bb.GetHeight() / mm_ius
    pcb_width = bb.GetWidth() / mm_ius 
    
    Header_1+= '## Pcb Height ' +'{0:.3f}'.format( pcb_height ) + 'mm, Pcb Width ' + '{0:.3f}'.format( pcb_width ) + 'mm' +' [based on Edge bounding box]' +lsep
    
    #to add relative position to 
    #print ("Board Aux Origin: " + str(my_board.GetAuxOrigin()))
    
    #'{0:<10} {1:<10} {2:<10}'.format(1.0, 2.2, 4.4))
    
    tracks = my_board.GetTracks()
    vias = []
    if  hasattr(pcbnew,'VIA'):
        via_ = pcbnew.VIA
    else:
        via_ = pcbnew.PCB_VIA_T
    
    for via in tracks:
        if type(via) is via_:
            vias.append(via)
    vias_cnt = len(vias)
    
    if  hasattr(my_board,'GetModules'):
        footprints = my_board.GetModules()
        TH=0;SMD=1;Virt=2
    else:
        footprints = my_board.GetFootprints()
        TH=1;SMD=2;Virt=3
        
    for module in footprints: 
        #print ("%s \"%s\" %s %1.3f %1.3f %1.3f %s" % ( module.GetReference(), 
        #Nchars = 20
        # RefL = 10; ValL = 20
        
        md=""
        if module.GetAttributes() == TH:   # PTH=0, SMD=1, Virtual = 2
            md = "THD"
            TH_pads+=module.GetPadCount()
        elif module.GetAttributes() == SMD:
            md = "SMD"
            SMD_pads+=module.GetPadCount()
        else:
            md = "VIRTUAL"
            Virt_pads+=module.GetPadCount()
        
        #Reference=str(module.GetReference()).ljust(Nchars/2)
        #Value=str(module.GetValue()).ljust(Nchars)
        #Package=str(module.GetFPID().GetLibItemName()).ljust(Nchars)
        #X_POS=str(pcbnew.ToMM(module.GetPosition().x - my_board.GetAuxOrigin().x ))
        #Y_POS=str(-1*pcbnew.ToMM(module.GetPosition().y - my_board.GetAuxOrigin().y))
        #Rotation=str(module.GetOrientation()/10)
        #Layer="top".ljust(Nchars) if module.GetLayer() == 0 else "bottom".ljust(Nchars)
        #Type=md
        Reference="{0:<14}".format(str(module.GetReference()))
        Value = str(module.GetValue())
        Value=(Value[:17] + '..') if len(Value) > 19 else Value
        Value="{0:<20}".format(Value)
        Package = str(module.GetFPID().GetLibItemName())
        Package=(Package[:27] + '..') if len(Package) > 29 else Package
        Package="{0:<30}".format(Package)
        #Package="{0:<20}".format(str(module.GetFPID().GetLibItemName()))
        X_POS='{0:.4f}'.format(pcbnew.ToMM(module.GetPosition().x - getAO.x ))
        X_POS="{0:<11}".format(X_POS)
        Y_POS='{0:.4f}'.format(-1*pcbnew.ToMM(module.GetPosition().y - getAO.y))
        Y_POS="{0:<11}".format(Y_POS)

        PIN1 = None
        PIN1_XPOS = '{0:.4f}'.format(0)
        PIN1_XPOS="{0:<11}".format(PIN1_XPOS)
        PIN1_YPOS = '{0:.4f}'.format(0)
        PIN1_YPOS="{0:<11}".format(PIN1_YPOS)
        for pin in module.Pads():
            if pin.GetName() == "1":
                PIN1 = pin
                PIN1_XPOS='{0:.4f}'.format(pcbnew.ToMM(PIN1.GetCenter().x - getAO.x ))
                PIN1_XPOS="{0:<11}".format(PIN1_XPOS)
                PIN1_YPOS='{0:.4f}'.format(pcbnew.ToMM(-1*PIN1.GetCenter().y - getAO.y ))
                PIN1_YPOS="{0:<11}".format(PIN1_YPOS)
                break

        Rotation='{0:.1f}'.format((module.GetOrientation()/10))
        Rotation="{0:>6}".format(Rotation)+'  '
        if module.GetLayer() == 0:
            Layer="  top"
        else:
            Layer="  bottom"
        #Side="## Side :"+Layer+lsep
        Layer="{0:<10}".format(Layer)
        Type='  '+md
        content=Reference
        content+=Value
        content+=Package
        content+=X_POS
        content+=Y_POS
        content+=PIN1_XPOS
        content+=PIN1_YPOS
        content+=Rotation
        content+=Layer
        content+=Type+lsep
        if 'top' in Layer and 'SMD' in Type:
            content_top_SMD+=content
            SMD_top_cnt+=1
        elif 'bot' in Layer and 'SMD' in Type:
            content_bot_SMD+=content
            SMD_bot_cnt+=1
        elif 'top' in Layer and 'THD' in Type:
            content_top_THD+=content
            TH_top_cnt+=1
        elif 'bot' in Layer and 'THD' in Type:
            content_bot_THD+=content
            TH_bot_cnt+=1
        elif 'top' in Layer and 'VIRTUAL' in Type:
            content_top_VIRTUAL+=content
            Virt_top_cnt+=1
        elif 'bot' in Layer and 'VIRTUAL' in Type:
            content_bot_VIRTUAL+=content
            Virt_bot_cnt+=1
        content_ALL+=content
        #print ("%s %s %s %1.4f %1.4f %1.4f %s %s" % ( str(module.GetReference()).ljust(Nchars), 
        #                            str(module.GetValue()).ljust(Nchars),
        #                            str(module.GetFPID().GetLibItemName()).ljust(Nchars),
        #                            pcbnew.ToMM(module.GetPosition().x - my_board.GetAuxOrigin().x ),
        #                            -1*pcbnew.ToMM(module.GetPosition().y - my_board.GetAuxOrigin().y),
        #                            module.GetOrientation()/10,
        #                            "top".ljust(Nchars) if module.GetLayer() == 0 else "bottom".ljust(Nchars),
        #                            md
        #                            ))
    
#"top" if module.GetLayer() == 0 else "bottom"
                                    
    #LogMsg+="## End"+lsep
    
    Header=Header_1+"## Side : top"+lsep+Header_2
    content=Header+content_top_SMD+"## End"+lsep
    with open(out_filename_top_SMD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : bottom"+lsep+Header_2
    content=Header+content_bot_SMD+"## End"+lsep
    with open(out_filename_bot_SMD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : top"+lsep+Header_2
    content=Header+content_top_THD+"## End"+lsep
    with open(out_filename_top_THD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : bottom"+lsep+Header_2
    content=Header+content_bot_THD+"## End"+lsep
    with open(out_filename_bot_THD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : top"+lsep+Header_2
    content=Header+content_top_VIRTUAL+"## End"+lsep
    with open(out_filename_top_VIRTUAL,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : bottom"+lsep+Header_2
    content=Header+content_bot_VIRTUAL+"## End"+lsep
    with open(out_filename_bot_VIRTUAL,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : ALL"+lsep+Header_2
    content=Header+content_ALL+"## End"+lsep
    content = content + '## '+ str(SMD_pads) + ' SMD pads' +lsep
    content = content + '## '+ str(TH_pads) + ' TH pads' +lsep
    content = content + '## '+ str(Virt_pads) + ' Virtual pads' +lsep
    content = content + '## '+ str( TH_top_cnt) + ' Top TH modules' + lsep
    content = content + '## '+ str( TH_bot_cnt) + ' Bot TH modules' + lsep
    content = content + '## '+ str( SMD_top_cnt) + ' Top SMD modules' + lsep
    content = content + '## '+ str( SMD_bot_cnt) + ' Bot SMD modules' + lsep
    content = content + '## '+ str( Virt_top_cnt) + ' Top Virtual modules' + lsep
    content = content + '## '+ str( Virt_bot_cnt) + ' Bot Virtual modules' + lsep
    
    with open(out_filename_ALL,'w') as f_out:
        f_out.write(content)

    #with open(out_filename,'w') as f_out:
    #    f_out.write(LogMsg)
    #LogMsg=""
    #f = open(out_filename,'w')
    #f.write(LogMsg)
    #f.close()
    LogMsg1="reading from:" + lsep + dirpath + lsep
    LogMsg1+= lsep + 'Pads:' + lsep
    LogMsg1+= 'SMD pads ' + str(SMD_pads) + lsep
    LogMsg1+= 'TH pads ' + str(TH_pads) +lsep
    LogMsg1+= 'Virtual pads ' + str(Virt_pads) + lsep
    LogMsg1+= 'Vias ' + str( vias_cnt) + lsep
    LogMsg1+= lsep + 'Modules:' + lsep
    LogMsg1+= 'Top TH modules ' + str( TH_top_cnt) + lsep
    LogMsg1+= 'Bot TH modules ' + str( TH_bot_cnt) + lsep
    LogMsg1+= 'Top SMD modules ' + str( SMD_top_cnt) + lsep
    LogMsg1+= 'Bot SMD modules ' + str( SMD_bot_cnt) + lsep
    LogMsg1+= 'Top Virtual modules ' + str( Virt_top_cnt) + lsep
    LogMsg1+= 'Bot Virtual modules ' + str( Virt_bot_cnt) + lsep
    LogMsg1+= lsep + 'PCB Geometry:' + lsep
    LogMsg1+= 'Pcb Height ' +'{0:.3f}'.format( pcb_height ) + 'mm, Pcb Width ' + '{0:.3f}'.format( pcb_width ) + 'mm' +lsep+'[based on Edge bounding box]' +lsep
    LogMsg1+= lsep
    #LogMsg1+=lsep+"reading from:" + lsep + dirpath + lsep + lsep
    if 0:
        LogMsg1+="written to:" + lsep + out_filename_top_SMD + lsep
        LogMsg1+=out_filename_bot_SMD + lsep
        LogMsg1+=out_filename_top_THD + lsep
        LogMsg1+=out_filename_bot_THD + lsep
        LogMsg1+=out_filename_top_VIRTUAL + lsep
        LogMsg1+=out_filename_bot_VIRTUAL + lsep
        LogMsg1+=out_filename_ALL + lsep
    else:
        LogMsg1+="written to:" + lsep + path+os.sep+dir + lsep
    
    return LogMsg1
    #return LogMsg1+LogMsg


# Python plugin stuff
from . import PositionsDlg

class Positions_Dlg(PositionsDlg.PositionsDlg):
    # from https://github.com/MitjaNemec/Kicad_action_plugins
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        if wx.__version__ < '4.0':
            self.SetSizeHintsSz(sz1, sz2)
        else:
            super(Positions_Dlg, self).SetSizeHints(sz1, sz2)

    #def onApplyClick(self, event):
    #    return self.EndModal(wx.ID_OK)
    #
    #def onCancelClick(self, event):
    #    return self.EndModal(wx.ID_CANCEL)

    def __init__(self,  parent):
        import wx
        PositionsDlg.PositionsDlg.__init__(self, parent)
        #self.GetSizer().Fit(self)
        self.SetMinSize(self.GetSize())
        self.m_bitmapFab.SetBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "./fabrication-footprint-positions.png")))
        # self.m_buttonDelete.Bind(wx.EVT_BUTTON, self.onDeleteClick)
        # self.m_buttonReconnect.Bind(wx.EVT_BUTTON, self.onConnectClick)
        # if wx.__version__ < '4.0':
        #     self.m_buttonReconnect.SetToolTipString( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #     self.m_buttonRound.SetToolTipString( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
        # else:
        #     self.m_buttonReconnect.SetToolTip( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #     self.m_buttonRound.SetToolTip( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
#


class generatePOS( pcbnew.ActionPlugin ):
    """
    A script to generate POS file for kicad_pcb
    requirements: KiCAD pcbnew >= 4.0
    release "1.0.1"
   
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Fabrication Footprint Position \nversion "+___version___
        self.category = "Fabrication Output"
        self.description = "Generate POS output for SMD, THD, Virtual\nand Board Statistics"
        #self.SetIcon(PyEmbeddedImage(getPos_ico_b64_data).GetIcon())
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./fabricationPositions.png")
        self.show_toolbar_button = True
        
    def Run( self ):
        
        #wx.MessageDialog(self.frame,"ciao")
        #subprocess.check_call(["C:\pathToYourProgram\yourProgram.exe", "your", "arguments", "comma", "separated"])
        #http://stackoverflow.com/questions/1811691/running-an-outside-program-executable-in-python
        #from https://github.com/MitjaNemec/Kicad_action_plugins
        #hack wxFormBuilder py2/py3
        #_pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
        pcbnew_window = find_pcbnew_w()
        aParameters = Positions_Dlg(pcbnew_window)
        aParameters.Show()
        modal_result = aParameters.ShowModal()
        if modal_result == wx.ID_OK:
            DirName = aParameters.m_textCtrlDir.GetValue()
            #wx.LogMessage(DirName)
            #wx.LogMessage(LayerName+';'+str(LayerIndex)+';'+LayerStdName)
            GenPos(DirName)
        else:
            None  # Cancel


def GenPos(dir):                
    def f_mm(raw):
        return repr(raw/mm_ius)
    
    board = pcbnew.GetBoard()
    
    #fileName = GetBoard().GetFileName()
    fileName = pcbnew.GetBoard().GetFileName()
    if len(fileName)==0:
        wx.MessageBox("a board needs to be saved/loaded!")
    else:
        LogMsg=''
        # msg="'get_pos.py'"+os.linesep
        msg="Generate POS output: version = "+___version___+os.linesep
        #msg+="Generate POS output"+os.linesep
         #print (msg)
        #LogMsg=msg+'\n\n'
        
        #print(msg)
        LogMsg+=msg
        reply=generate_POS(dir)
        LogMsg+=reply
        wx.LogMessage(LogMsg)
        
        if 0:
            frame = displayDialog(None)
            #frame = wx.Frame(None)
            frame.Center()
            frame.setMsg(LogMsg)
            frame.ShowModal()
            frame.Destroy()
            #frame = wx.wxFrame(None, 10110, 'T-Make', size=wx.wxSize(100,100),
            #           style=wx.wxSTAY_ON_TOP)
            #frame.show()
            
#generatePOS().register()

#  execfile("round_tracks.py")

