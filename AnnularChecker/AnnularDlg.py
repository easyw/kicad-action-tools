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
## Class AnnularDlg
###########################################################################

class AnnularDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Annular Ring Checker", pos = wx.DefaultPosition, size = wx.Size( 533,529 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_bitmapAR = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 180,114 ), 0 )
		bSizer3.Add( self.m_bitmapAR, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.m_LabelTitle = wx.StaticText( self, wx.ID_ANY, u"Check annular ring", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_LabelTitle.Wrap( -1 )

		bSizer3.Add( self.m_LabelTitle, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticTextARV = wx.StaticText( self, wx.ID_ANY, u"AR Vias (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextARV.Wrap( -1 )

		gSizer1.Add( self.m_staticTextARV, 0, wx.ALL, 5 )

		self.m_textCtrlARV = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_textCtrlARV, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticTextARP = wx.StaticText( self, wx.ID_ANY, u"AR Pads (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextARP.Wrap( -1 )

		gSizer1.Add( self.m_staticTextARP, 0, wx.ALL, 5 )

		self.m_textCtrlARP = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_textCtrlARP, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticTextPHD = wx.StaticText( self, wx.ID_ANY, u"PH Drill margin (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextPHD.Wrap( -1 )

		self.m_staticTextPHD.Enable( False )

		gSizer1.Add( self.m_staticTextPHD, 1, wx.ALL, 5 )

		self.m_textCtrlPHD = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlPHD.Enable( False )

		gSizer1.Add( self.m_textCtrlPHD, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_checkBoxPHD = wx.CheckBox( self, wx.ID_ANY, u"use drill size as finished hole size", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_checkBoxPHD, 0, wx.ALL, 5 )


		bSizer3.Add( gSizer1, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

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


