# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PositionsDlg
###########################################################################

class PositionsDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Generating Fab Positions", pos = wx.DefaultPosition, size = wx.Size( 499,377 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_comment = wx.StaticText( self, wx.ID_ANY, u"Generating Modules Fab Positions", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_comment.Wrap( -1 )

		bSizer3.Add( self.m_comment, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bitmapFab = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 180,90 ), 0 )
		bSizer3.Add( self.m_bitmapFab, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Output DIR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer31.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_textCtrlDir = wx.TextCtrl( self, wx.ID_ANY, u"grb", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_textCtrlDir, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer3.Add( bSizer31, 0, 0, 5 )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_buttonOK = wx.Button( self, wx.ID_OK, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonOK.SetDefault()
		bSizer1.Add( self.m_buttonOK, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_buttonCancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_buttonCancel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer3.Add( bSizer1, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )


		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


