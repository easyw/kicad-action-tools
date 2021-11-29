# -*- coding: utf-8 -*-
#
# A script to Snap modules to selected Grid for kicad_pcb
# requirements: KiCAD pcbnew >= 4.0
# copyright Maurice easyw
# 
#

#import snaptogrid; import importlib; importlib.reload(snaptogrid)

### plugins errors
#import pcbnew;pcbnew.GetWizardsBackTrace()

__version__ = '1.2.2'
import sys, os
import pcbnew
import datetime
import wx
from pcbnew import *

use_grid_origin = True

gridReference = 0.1 #1.27 #mm pcbnew.FromMM(1.0) #0.1mm

gridSizeMM = gridReference

from . import Snap2GridDlg

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
 
class Snap2Grid_Dlg(Snap2GridDlg.Snap2GridDlg):
    # from https://github.com/MitjaNemec/Kicad_action_plugins
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        if wx.__version__ < '4.0':
            self.SetSizeHintsSz(sz1, sz2)
        else:
            super(Snap2Grid_Dlg, self).SetSizeHints(sz1, sz2)

    # def onDeleteClick(self, event):
    #     return self.EndModal(wx.ID_DELETE)
    # 
    # def onConnectClick(self, event):
    #     return self.EndModal(wx.ID_REVERT)

    def __init__(self,  parent):
        import wx
        Snap2GridDlg.Snap2GridDlg.__init__(self, parent)
        #self.GetSizer().Fit(self)
        self.SetMinSize(self.GetSize())
        self.m_bitmapS2G.SetBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "./snap2grid-help.png")))
        #self.SetIcon(wx.IconFromBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "./snap2grid.png"))))
        #self.m_buttonDelete.Bind(wx.EVT_BUTTON, self.onDeleteClick)
        #self.m_buttonReconnect.Bind(wx.EVT_BUTTON, self.onConnectClick)
        #if wx.__version__ < '4.0':
        #    self.m_buttonReconnect.SetToolTipString( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #    self.m_buttonRound.SetToolTipString( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
        #else:
        #    self.m_buttonReconnect.SetToolTip( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #    self.m_buttonRound.SetToolTip( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )

# Python plugin stuff
class snap_to_grid( pcbnew.ActionPlugin ):
    """
    A plugin to Snap modules to selected Grid for kicad_pcb
    requirements: KiCAD pcbnew >= 4.0
    
    """
    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Snap Selected Footprint(s) to Grid \nversion "+__version__
        self.category = "Modify PCB"
        self.description = "Automaticaly Snap Selected Footprint Module(s) to Grid on an existing PCB"
        #self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), './snap2grid.png')
    #

    def Run(self):
        #self.pcb = GetBoard()
        import sys,os
        #mm_ius = 1000000.0
        #_pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
        pcbnew_window = find_pcbnew_w()
        #aParameters = RoundTrackDlg(None)
        aParameters = Snap2Grid_Dlg(pcbnew_window)
        gridIndex = aParameters.m_comboBoxGrid.FindString('0.1mm     (3.94mils)')
        aParameters.m_comboBoxGrid.SetSelection(gridIndex)
        #aParameters.m_comboBoxGrid.Append('0.1mm (3.94mils)')
        aParameters.m_radioBtnGO.SetValue(True)
        aParameters.Show()
        
        modal_result = aParameters.ShowModal()
        if modal_result == wx.ID_OK:
            grid = aParameters.m_comboBoxGrid.GetStringSelection()
            gridSizeMM = float(grid.split('mm')[0])
            if aParameters.m_radioBtnGO.GetValue():
                use_grid = 'gridorigin'
            elif aParameters.m_radioBtnAO.GetValue():
                use_grid = 'auxorigin'
            else:
                use_grid = 'topleft'
            snap2grid(gridSizeMM,use_grid)
        else:
            None  # Cancel
##

def snap2grid(gridSizeMM,use_grid):
        
    pcb = pcbnew.GetBoard()
    if hasattr(pcb, 'GetAuxOrigin'):
        auxOrigin  = pcb.GetAuxOrigin()
        gridOrigin = pcb.GetGridOrigin()
    else:
        auxOrigin  = pcb.GetDesignSettings().GetAuxOrigin()
        gridOrigin = pcb.GetDesignSettings().GetGridOrigin()
    if  hasattr(pcb,'GetModules'):
        footprints = pcb.GetModules()
    else:
        footprints = pcb.GetFootprints()
    
    content=''
    locked_fp=''
    #wxPoint(77470000, 135890000)
    for module in footprints: 
        if module.IsSelected():
            if 'grid' in use_grid:
                mpx = module.GetPosition().x - gridOrigin.x
                mpy = module.GetPosition().y - gridOrigin.y
                #print(mpx,mpy)
                mpxOnG = int(mpx/FromMM(gridSizeMM))*FromMM(gridSizeMM)+ gridOrigin.x
                mpyOnG = int(mpy/FromMM(gridSizeMM))*FromMM(gridSizeMM)+ gridOrigin.y
                #print(mpxOnG,mpyOnG)
                locked=''
                if not module.IsLocked():
                    module.SetPosition(wxPoint(mpxOnG,mpyOnG))
                else:
                    locked='LOCKED'
                X_POS=str(module.GetPosition().x) # - gridOrigin.x)
                #X_POS='{0:.4f}'.format(pcbnew.ToMM(module.GetPosition().x - gridOrigin.x ))
                X_POS="{0:<11}".format(X_POS)
                Y_POS=str(module.GetPosition().y) # - gridOrigin.y)
                Y_POS="{0:<11}".format(Y_POS)
                ## mpOnGx = PutOnGridMM(module.GetPosition().x, gridSizeMM)
                ## mpOnGy = PutOnGridMM(module.GetPosition().y, gridSizeMM)
                ## module.SetPosition(wxPoint(mpOnGx,mpOnGy))
                #module.SetPosition(wxPoint(mpOnGx+FromMM(100.0),mpOnGy+FromMM(2.0)))
                #module.SetOrientation(10)
                #Y_POS='{0:.4f}'.format(-1*pcbnew.ToMM(module.GetPosition().y - gridOrigin.y))
            elif 'aux' in use_grid:  # AuxOrigin
                mpx = module.GetPosition().x - auxOrigin.x
                mpy = module.GetPosition().y - auxOrigin.y
                #print(mpx,mpy)
                mpxOnG = int(mpx/FromMM(gridSizeMM))*FromMM(gridSizeMM)+ auxOrigin.x
                mpyOnG = int(mpy/FromMM(gridSizeMM))*FromMM(gridSizeMM)+ auxOrigin.y
                #print(mpxOnG,mpyOnG)
                locked=''
                if not module.IsLocked():
                    module.SetPosition(wxPoint(mpxOnG,mpyOnG))
                else:
                    locked='LOCKED'
                X_POS=str(module.GetPosition().x) # - gridOrigin.x)
                #X_POS='{0:.4f}'.format(pcbnew.ToMM(module.GetPosition().x - gridOrigin.x ))
                X_POS="{0:<11}".format(X_POS)
                Y_POS=str(module.GetPosition().y) # - gridOrigin.y)
                Y_POS="{0:<11}".format(Y_POS)
                ## mpOnGx = PutOnGridMM(module.GetPosition().x, gridSizeMM)
                ## mpOnGy = PutOnGridMM(module.GetPosition().y, gridSizeMM)
                ## module.SetPosition(wxPoint(mpOnGx,mpOnGy))
                #module.SetPosition(wxPoint(mpOnGx+FromMM(100.0),mpOnGy+FromMM(2.0)))
                #module.SetOrientation(10)
                #Y_POS='{0:.4f}'.format(-1*pcbnew.ToMM(module.GetPosition().y - gridOrigin.y))
            else:
                mpx = module.GetPosition().x #- auxOrigin.x
                mpy = module.GetPosition().y #- auxOrigin.y
                mpxOnG = int(mpx/FromMM(gridSizeMM))*FromMM(gridSizeMM) #+ auxOrigin.x
                mpyOnG = int(mpy/FromMM(gridSizeMM))*FromMM(gridSizeMM) #+ auxOrigin.y
                locked=''
                if not module.IsLocked():
                    module.SetPosition(wxPoint(mpxOnG,mpyOnG))
                else:
                    locked='LOCKED'
                X_POS=str(module.GetPosition().x) # - gridOrigin.x)
                X_POS="{0:<11}".format(X_POS)
                Y_POS=str(module.GetPosition().y) # - gridOrigin.y)
                Y_POS="{0:<11}".format(Y_POS)            
            Reference="{0:<10}".format(str(module.GetReference()))
            Value = str(module.GetValue())
            Value=(Value[:17] + '..') if len(Value) > 19 else Value
            Value="{0:<20}".format(Value)
            Rotation='{0:.1f}'.format((module.GetOrientation()/10))
            Rotation="{0:>6}".format(Rotation)+'  '
            if module.GetLayer() == 0:
                Layer="  top"
            else:
                Layer="  bottom"
            #Side="## Side :"+Layer+lsep
            Layer="{0:<10}".format(Layer)
            content+=Reference
            if 'LOCKED' in locked:
                locked_fp+=Reference + ' LOCKED'+'\n' #os.linesep
            #content+=Value
            content+=X_POS
            content+=Y_POS
            #content+=str(mpOnGx)
            #content+=str(mpOnGy)
            content+=str(mpxOnG)
            content+=str(mpyOnG)
            content+=Layer+'\n' #os.linesep
    if len(content)>0:
        content+=str(pcbnew.FromMM(gridSizeMM))+'\n'
        info='Snapped to grid: '+str(gridSizeMM)+'mm\n'
        if 'grid' in use_grid:
            content+="Using GridOrigin as Ref"+'\n'
            info+="Using GridOrigin as Ref"+'\n'
        elif 'aux' in use_grid:
            content+="Using AuxOrigin as Ref"+'\n'
            info+="Using AuxOrigin as Ref"+'\n'
        else:
            content+="Using Top Left Origin as Ref"+'\n'
            info+="Using Top Left Origin as Ref"+'\n'
        if debug:
            wxLogDebug(content,debug)
        #else:
            wxLogDebug(info,True)
        if len (locked_fp)>0:
            locked_fp+='\n'+'NOT Moved (Locked fp)'
            locked_fp+='\n'+info
            wxLogDebug(locked_fp,True)
        else:
            wxLogDebug(info,True)
    else:
        wxLogDebug('No Modules Selected',True)
    Refresh()
    #return content

        # wxLogDebug('showing Selected Tracks',debug)
        # wx.LogMessage('Select Tracks to calculate the Length\nor One Pad to select connected Tracks')
#
 
