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

import wx
import pcbnew
from pcbnew import *
import base64
from wx.lib.embeddedimage import PyEmbeddedImage
import os
___version___="1.2.1"

from . import Move2LayerDlg

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
        self.name = "Move Selected drawings to chosen Layer\nversion "+___version___
        self.category = "Modify PCB"
        self.description = "Move Selected drawings to chosen Layer on an existing PCB"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./move2layer.png")
        self.show_toolbar_button = True

    def Run( self ):
        found_selected=False
        #wx.MessageDialog(self.frame,"ciao")
        #subprocess.check_call(["C:\pathToYourProgram\yourProgram.exe", "your", "arguments", "comma", "separated"])
        #http://stackoverflow.com/questions/1811691/running-an-outside-program-executable-in-python
        def switch(x):
            return {
                'Edge_Cuts': pcbnew.Edge_Cuts,
                'Eco1_User': pcbnew.Eco1_User,
                'Eco2_User': pcbnew.Eco2_User,
                'Dwgs_User': pcbnew.Dwgs_User,
                'Cmts_User': pcbnew.Cmts_User,
                'Margin'   : pcbnew.Margin,
                'F_CrtYd'  : pcbnew.F_CrtYd,
                'B_CrtYd'  : pcbnew.B_CrtYd,
                'F_Fab'    : pcbnew.F_Fab,
                'B_Fab'    : pcbnew.B_Fab,
                'F_SilkS'    : pcbnew.F_SilkS,
                'B_SilkS'    : pcbnew.B_SilkS,
            }[x]
        
        # class displayDialog(wx.Dialog):
        #     """
        #     The default frame
        #     http://stackoverflow.com/questions/3566603/how-do-i-make-wx-textctrl-multi-line-text-update-smoothly
        #     """
        # 
        #     #----------------------------------------------------------------------
        #     #def __init__(self):
        #     #    """Constructor"""
        #     #    wx.Frame.__init__(self, None, title="Display Frame", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)
        #     #    panel = wx.Panel(self)
        #     def __init__(self, parent):
        #         wx.Dialog.__init__(self, parent, id=-1, title="Move to Layer")#
        #         #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION) 
        #         #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION)
        #         #, pos=DefaultPosition, size=DefaultSize, style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX), name="fname")
        #         #, wx.ICON_INFORMATION) #, title="Annular Check", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)    
        #         #
        #         
        #         self.SetIcon(PyEmbeddedImage(move_to_layer_ico_b64_data).GetIcon())
        #         #wx.IconFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY)))
        #         self.panel = wx.Panel(self)     
        #         
        #         self.ct = 0
        #         self.layerSelection = "Edge_Cuts"
        #         layerList = ["Edge_Cuts", "Eco1_User", "Eco2_User", "Dwgs_User", "Cmts_User", "Margin", "F_CrtYd", "B_CrtYd", "F_Fab", "B_Fab", "F_SilkS", "B_SilkS"]
        #         self.combo = wx.ComboBox(self.panel, choices=layerList)
        #         self.combo.SetSelection(0)
        #         
        #         self.combo.Bind(wx.EVT_COMBOBOX, self.onCombo)
        #         
        #         self.title = wx.StaticText(self.panel, label="Move to Layer:")
        #         #self.result = wx.StaticText(self.panel, label="")
        #         #self.result.SetForegroundColour('#FF0000')
        #         #self.button = wx.Button(self.panel, label="Save")
        #         #self.lblname = wx.StaticText(self.panel, label="Your name:")
        #         #self.editname = wx.TextCtrl(self.panel, size=(140, -1))
        #         ##self.editname = wx.TextCtrl(self.panel, size = (300, 400), style = wx.TE_MULTILINE|wx.TE_READONLY)
        # 
        # 
        #         # Set sizer for the frame, so we can change frame size to match widgets
        #         self.windowSizer = wx.BoxSizer()
        #         self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        
        # 
        #         # Set sizer for the panel content
        #         self.sizer = wx.GridBagSizer(5, 0)
        #         self.sizer.Add(self.title, (0, 0))
        #         self.button = wx.Button(self.panel, label="OK")
        #         self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)
        #         #self.sizer.Add(self.result, (1, 0))
        #         #self.sizer.Add(self.lblname, (1, 0))
        #         ##self.sizer.Add(self.editname, (1, 0))
        #         self.sizer.Add(self.combo, (1, 0))
        #         #self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)
        # 
        #         # Set simple sizer for a nice border
        #         self.border = wx.BoxSizer()
        #         self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
        # 
        #         # Use the sizers
        #         self.panel.SetSizerAndFit(self.border)  
        #         self.SetSizerAndFit(self.windowSizer)  
        #         
        #         #self.button = wx.Button(self.panel, label="Close")
        #         self.button.Bind(wx.EVT_BUTTON, self.OnClose)
        #         self.Bind(wx.EVT_CLOSE,self.OnClose)
        #     
        #     #----------------------------------------------------------------------
        #     def OnClose(self,e):
        #         #wx.LogMessage("c")
        #         e.Skip()
        #         self.Close()
        #         #self.result.SetLabel(msg)
        #         # Set event handlers
        #         #self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        #         #self.Show()
        #         #self.Bind(wx.EVT_CLOSE,self.OnClose)
        #     def onCombo(self, event):
        #         """
        #         """
        #         self.layerSelection = self.combo.GetValue()
        # 
        #     #def OnClose(self,e):
        #     #    #wx.LogMessage("c")
        #     #    e.Skip()
        #         #self.Close()
        #     
        #     #def OnButton(self, e):
        #     #    self.result.SetLabel(self.editname.GetValue())
        #     #def setMsg(self, t_msg):
        #     #    self.editname.SetValue(t_msg)
        
        board = pcbnew.GetBoard()
        #wx.MessageDialog(None, 'This is a message box.', 'Test', wx.OK | wx.ICON_INFORMATION).ShowModal()
        fileName = GetBoard().GetFileName()
        if 0: #len(fileName) == 0:
            wx.LogMessage("A board needs to be saved/loaded\nto run the plugin!")
        else:
            #from https://github.com/MitjaNemec/Kicad_action_plugins
            #hack wxFormBuilder py2/py3
            _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
            aParameters = Move2Layer_Dlg(_pcbnew_frame)
            aParameters.Show()
            modal_result = aParameters.ShowModal()
            if modal_result == wx.ID_OK:
                MoveToLayer(pcb, Layer)
            else:
                None  # Cancel

            LogMsg=''
            msg="'move to layer tool'\n"
            msg+="version = "+___version___
            #wx.LogMessage(LogMsg)
            
            # frame = displayDialog(None)
            # #frame = wx.Frame(None)
            # frame.Center()
            # #frame.setMsg(LogMsg)
            # frame.ShowModal()
            # #dlg.Destroy()
            # frame.Destroy()
        
            #dlg=wx.MessageBox( 'Changing Layer for Selected?', 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION )
            #dlg=wx.MessageBox( 'Changing Layer for Selected '+frame.layerSelection+ '?', 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING )
            #if dlg == wx.YES:
            #    #wx.LogMessage("YES")
            #    #wx.LogMessage(str(board.IsModified()))
            #    #board.SetModified()
            #    #wx.LogMessage(str(board.IsModified()))
            #    #try:
            #    #    board_drawings=board.GetDrawings()
            #    #except:
            #    #    board_drawings=board.DrawingsList()
            #    #
            #    #for drw in board_drawings:
            #    for drw in board.GetDrawings():
            #        if drw.IsSelected():
            #            drw.SetLayer(switch(frame.layerSelection))
            #            found_selected=True
            #
            #    if found_selected!=True:
            #        LogMsg="select lines to be moved to new layer\n"
            #        LogMsg+="use GAL for selecting lines"
            #        wx.LogMessage(LogMsg)
            #    else:
            #        pcbnew.Refresh()
            #        LogMsg="selected drawings moved to "+frame.layerSelection+" layer"
            
                
        


#move_to_draw_layer().register()

# pcbnew.F_Cu
# pcbnew.In1_Cu
# pcbnew.In2_Cu
#..
# pcbnew.In30_Cu
# pcbnew.B_Cu
# pcbnew.B_Adhes
# pcbnew.F_Adhes
# pcbnew.B_Paste
# pcbnew.F_Paste
# pcbnew.B_SilkS
# pcbnew.F_SilkS
# pcbnew.B_Mask
# pcbnew.F_Mask
# pcbnew.Dwgs_User
# pcbnew.Cmts_User
# pcbnew.Eco1_User
# pcbnew.Eco2_User
# pcbnew.Edge_Cuts
# pcbnew.Margin
# pcbnew.B_CrtYd
# pcbnew.F_CrtYd
# pcbnew.B_Fab
# pcbnew.F_Fab
