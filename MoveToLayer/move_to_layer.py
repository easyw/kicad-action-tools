#  move_to_edge_cuts.py
#
# Copyright (C) 2017 KiCad Developers, see CHANGELOG.TXT for contributors.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

### plugins errors
#import pcbnew
#pcbnew.GetWizardsBackTrace()


import wx
import pcbnew
from pcbnew import *
import base64
from wx.lib.embeddedimage import PyEmbeddedImage
import os
___version___="1.2.5"

from . import Move2LayerDlg


def MoveToLayer(pcb,layerId):
    found_selected=False
    for drw in pcb.GetDrawings():
        if drw.IsSelected():
            drw.SetLayer(layerId)
            found_selected=True
    
    if found_selected!=True:
        LogMsg="select drawings to be moved to new layer\n"
        LogMsg+="use GAL for selecting lines"
        wx.LogMessage(LogMsg)
    else:
        pcbnew.Refresh()
        layerName = pcbnew.GetBoard().GetLayerName(layerId)
        LogMsg="selected drawings moved to "+layerName+" layer"
        wx.LogMessage(LogMsg)
#        
def find_pcbnew_w():
    windows = wx.GetTopLevelWindows()
    pcbneww = [w for w in windows if "pcbnew" in w.GetTitle().lower()]
    if len(pcbneww) != 1:
        return None
    return pcbneww[0]
#


# Python plugin stuff

class Move2Layer_Dlg(Move2LayerDlg.Move2LayerDlg):
    # from https://github.com/MitjaNemec/Kicad_action_plugins
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        if wx.__version__ < '4.0':
            self.SetSizeHintsSz(sz1, sz2)
        else:
            super(Move2Layer_Dlg, self).SetSizeHints(sz1, sz2)

    #def onApplyClick(self, event):
    #    return self.EndModal(wx.ID_OK)
    #
    #def onCancelClick(self, event):
    #    return self.EndModal(wx.ID_CANCEL)

    def __init__(self,  parent):
        import wx
        Move2LayerDlg.Move2LayerDlg.__init__(self, parent)
        #self.GetSizer().Fit(self)
        self.SetMinSize(self.GetSize())
        
        self.m_bitmapLayers.SetBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "./add_polygon.png")))
        self.m_bitmapDwgs.SetBitmap(wx.Bitmap(os.path.join(os.path.dirname(__file__), "./move2layer.png")))
        # self.m_buttonDelete.Bind(wx.EVT_BUTTON, self.onDeleteClick)
        # self.m_buttonReconnect.Bind(wx.EVT_BUTTON, self.onConnectClick)
        # if wx.__version__ < '4.0':
        #     self.m_buttonReconnect.SetToolTipString( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #     self.m_buttonRound.SetToolTipString( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
        # else:
        #     self.m_buttonReconnect.SetToolTip( u"Select two converging Tracks to re-connect them\nor Select tracks including one round corner to be straighten" )
        #     self.m_buttonRound.SetToolTip( u"Select two connected Tracks to round the corner\nThen choose distance from intersection and the number of segments" )
#
class move_to_draw_layer( pcbnew.ActionPlugin ):
    """
    A script to Move Selected Drawing(s) to chosen new Layer (available only in GAL) 
    How to use:
    - move to GAL
    - select some draw objects
    - call the plugin
    - select the new layer
    - selected draw objects will be moved to new layer
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        import os
        self.name = "Move Selected Drawings to chosen Layer \nversion "+___version___
        self.category = "Modify PCB"
        self.description = "Move Selected Drawings to chosen Layer on an existing PCB"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./move2layer.png")
        self.show_toolbar_button = True

    def Run( self ):
        found_selected=False
        
        board = pcbnew.GetBoard()
        fileName = GetBoard().GetFileName()
        # # dicts for converting layer name to id, used by _get_layer
        # _std_layer_dict = {pcbnew.BOARD_GetStandardLayerName(n): n
        #                 for n in range(pcbnew.PCB_LAYER_ID_COUNT)}
        # #_std_layer_names = {s: n for n, s in _std_layer_dict.iteritems()}
        # _std_layer_names = {s: n for n, s in _std_layer_dict.items()}
        # _brd_layer_dict = {pcbnew.GetBoard().GetLayerName(n): n
        #            for n in range(pcbnew.PCB_LAYER_ID_COUNT)}
        # #_std_layer_names = {s: n for n, s in _std_layer_dict.iteritems()}
        # _brd_layer_names = {s: n for n, s in _brd_layer_dict.items()}
        
        
        if 0: #len(fileName) == 0:
            wx.LogMessage("A board needs to be saved/loaded\nto run the plugin!")
        else:
            #from https://github.com/MitjaNemec/Kicad_action_plugins
            #hack wxFormBuilder py2/py3
            #_pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
            pcbnew_window = find_pcbnew_w()
            aParameters = Move2Layer_Dlg(pcbnew_window)
            aParameters.Show()
            for l in range(pcbnew.PCB_LAYER_ID_COUNT):
                aParameters.m_comboBoxLayer.Append(pcbnew.GetBoard().GetLayerName(l))
            aParameters.m_comboBoxLayer.Select(44)
            modal_result = aParameters.ShowModal()
            if modal_result == wx.ID_OK:
                LayerName = aParameters.m_comboBoxLayer.GetStringSelection()
                LayerIndex = aParameters.m_comboBoxLayer.FindString(LayerName)
                LayerStdName = pcbnew.BOARD_GetStandardLayerName(LayerIndex)
                #wx.LogMessage(LayerName+';'+str(LayerIndex)+';'+LayerStdName)
                MoveToLayer(board, LayerIndex)
            else:
                None  # Cancel

            LogMsg=''
            msg="'move to layer tool'\n"
            msg+="version = "+___version___


#move_to_draw_layer().register()

