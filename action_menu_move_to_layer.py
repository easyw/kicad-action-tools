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
___version___="1.1.1"


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
        self.name = "Move Selected drawings to chosen Layer"
        self.category = "Modify Drawing PCB"
        self.description = "Move Selected drawings to chosen Layer on an existing PCB"

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
                wx.Dialog.__init__(self, parent, id=-1, title="Move to Layer")#
                #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION) 
                #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION)
                #, pos=DefaultPosition, size=DefaultSize, style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX), name="fname")
                #, wx.ICON_INFORMATION) #, title="Annular Check", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)    
                #
                
                self.SetIcon(PyEmbeddedImage(move_to_layer_ico_b64_data).GetIcon())
                #wx.IconFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY)))
                self.panel = wx.Panel(self)     
                
                self.ct = 0
                self.layerSelection = "Edge_Cuts"
                layerList = ["Edge_Cuts", "Eco1_User", "Eco2_User", "Dwgs_User", "Cmts_User", "Margin", "F_CrtYd", "B_CrtYd", "F_Fab", "B_Fab", "F_SilkS", "B_SilkS"]
                self.combo = wx.ComboBox(self.panel, choices=layerList)
                self.combo.SetSelection(0)
                
                self.combo.Bind(wx.EVT_COMBOBOX, self.onCombo)
                
                self.title = wx.StaticText(self.panel, label="Move to Layer:")
                #self.result = wx.StaticText(self.panel, label="")
                #self.result.SetForegroundColour('#FF0000')
                #self.button = wx.Button(self.panel, label="Save")
                #self.lblname = wx.StaticText(self.panel, label="Your name:")
                #self.editname = wx.TextCtrl(self.panel, size=(140, -1))
                ##self.editname = wx.TextCtrl(self.panel, size = (300, 400), style = wx.TE_MULTILINE|wx.TE_READONLY)
        
        
                # Set sizer for the frame, so we can change frame size to match widgets
                self.windowSizer = wx.BoxSizer()
                self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        
        
                # Set sizer for the panel content
                self.sizer = wx.GridBagSizer(5, 0)
                self.sizer.Add(self.title, (0, 0))
                #self.sizer.Add(self.result, (1, 0))
                #self.sizer.Add(self.lblname, (1, 0))
                ##self.sizer.Add(self.editname, (1, 0))
                self.sizer.Add(self.combo, (1, 0))
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
            #----------------------------------------------------------------------
            def onCombo(self, event):
                """
                """
                self.layerSelection = self.combo.GetValue()
        
            #def OnClose(self,e):
            #    #wx.LogMessage("c")
            #    e.Skip()
                #self.Close()
            
            #def OnButton(self, e):
            #    self.result.SetLabel(self.editname.GetValue())
            #def setMsg(self, t_msg):
            #    self.editname.SetValue(t_msg)
        
        board = pcbnew.GetBoard()
        #wx.MessageDialog(None, 'This is a message box.', 'Test', wx.OK | wx.ICON_INFORMATION).ShowModal()
        fileName = GetBoard().GetFileName()
        if len(fileName)==0:
            wx.LogMessage("a board needs to be saved/loaded!")
        else:
            LogMsg=''
            msg="'move to layer tool'\n"
            msg+="version = "+___version___
        frame = displayDialog(None)
        #frame = wx.Frame(None)
        frame.Center()
        #frame.setMsg(LogMsg)
        frame.ShowModal()
        frame.Destroy()
        
        #dlg=wx.MessageBox( 'Changing Layer for Selected?', 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION )
        dlg=wx.MessageBox( 'Changing Layer for Selected '+frame.layerSelection+ '?', 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING )
        if dlg == wx.YES:
            #wx.LogMessage("YES")
            #wx.LogMessage(str(board.IsModified()))
            #board.SetModified()
            #wx.LogMessage(str(board.IsModified()))
            for drw in board.GetDrawings():
                if drw.IsSelected():
                    drw.SetLayer(switch(frame.layerSelection))
                    found_selected=True
    
            if found_selected!=True:
                LogMsg="select lines to be moved to new layer\n"
                LogMsg+="use GAL for selecting lines"
                wx.LogMessage(LogMsg)
            else:
                pcbnew.Refresh()
                LogMsg="selected drawings moved to "+frame.layerSelection+" layer"
                wx.LogMessage(LogMsg)
        


move_to_draw_layer().register()


# "b64_data" is a variable containing your base64 encoded jpeg
move_to_layer_ico_b64_data =\
"""
iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAKYQAACmEB/MxKJQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAJrSURBVDiNnZRRSFNxFMa/s3vlLje3y0bpdKkwrcTCxbChQUIPUWBJ0IvQy3STCIkgoehFJIKCHkSCkLRBVNJT0EPQQ4W9bFmJDS0TSmwbc65ku7ZrY96dHsQ1yQfnB+flcPj9/985h0O+iz5nVtJGwGwjprEHg6N92IHErKSNTB9fcKmmDPa9qb3gdt9dmJg48hIQIswudaOwt7fXmhZXbzOhTdDgr7ZW3+rv78/lQWC2qaYMQIBSnjasrBqGAAawBqJ3ywDCACInzlod2dOT+xO1CtUFbVeFcHQawPM8iJjGGt7aPakK1Vg1Y02FYnu8AMkA7IVRJqfqv9YqlBNzWHIkTXLc0F4IImZGT09Pa06CU/udfeL3+5Nb9aD7Uvf1ZVv62pIjWbY3aP9jTgtHh4eHJzeBtqOBgQFdNB5t/x6xD4aCLksiUbGb2ZXNFzBzUQEEO4AgA8GOwrxuW9/ZJPEFgGUA5wuzRYPW7dBTAO1EH807Bq1LewRAD2jnCl4orkcbIUnj887me3M+n6+Vmbc/tUJ5PB45q9eHY01xo5zYlTT/0o8WZY1oSiYKnJybP/Q45lw0LDYmMNv2Q2biThHAlgtJBB3wvgHQWgBqAdAC4ACgo2+zdVl3JKSh4adYqkgAUUzsutx9R6lWPakK1Vg5VX7DaHx1P502HgbgBmAGCACiAAIAjwC6QDxeMmldEW5antV3gihWkhG8IhN3fjkWsYCA3JpgqXEsXPkcavwAwA9wABACzM3h/42e6gOQPzkiiGKlilSpmjIwL5UqVU1TZ2Y+dY0XOwCxJCN4D76u+XfYHg4VDQGAvyJXT3w3dEsJAAAAAElFTkSuQmCC""" 

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
