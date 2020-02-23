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
## Class Move2LayerDlg
###########################################################################

class Move2LayerDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Move to Layer", pos = wx.DefaultPosition, size = wx.Size( 568,263 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_comment = wx.StaticText( self, wx.ID_ANY, u"Selected Objects will be Moved to chosen Layer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_comment.Wrap( -1 )

		bSizer3.Add( self.m_comment, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticTextLayer = wx.StaticText( self, wx.ID_ANY, u"Layer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextLayer.Wrap( -1 )

		bSizer31.Add( self.m_staticTextLayer, 1, wx.ALL|wx.EXPAND, 5 )

		m_comboBoxLayerChoices = []
		self.m_comboBoxLayer = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.Size( 250,-1 ), m_comboBoxLayerChoices, 0 )
		bSizer31.Add( self.m_comboBoxLayer, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bitmapLayers = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_bitmapLayers, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_bitmapDwgs = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer31.Add( self.m_bitmapDwgs, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer3.Add( bSizer31, 0, 0, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText101 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText101.Wrap( -1 )

		bSizer1.Add( self.m_staticText101, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_buttonOK = wx.Button( self, wx.ID_OK, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonOK.SetDefault()
		bSizer1.Add( self.m_buttonOK, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_buttonCancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_buttonCancel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer3.Add( bSizer1, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )


		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


