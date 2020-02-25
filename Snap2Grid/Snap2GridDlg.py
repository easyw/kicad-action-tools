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
## Class Snap2GridDlg
###########################################################################

class Snap2GridDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Snap to Grid", pos = wx.DefaultPosition, size = wx.Size( 499,584 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_comment = wx.StaticText( self, wx.ID_ANY, u"Selected Model(s) to Snap\nto the Grid", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_comment.Wrap( -1 )

		bSizer3.Add( self.m_comment, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bitmapS2G = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 100,100 ), 0 )
		bSizer3.Add( self.m_bitmapS2G, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticTextGrid = wx.StaticText( self, wx.ID_ANY, u"Grid", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextGrid.Wrap( -1 )

		bSizer31.Add( self.m_staticTextGrid, 1, wx.ALL|wx.EXPAND, 5 )

		m_comboBoxGridChoices = [ u"1.0mm   (39.37mils)", u"0.5mm   (19.69mils)", u"0.25mm   (9.84mils)", u"0.1mm     (3.94mils)", u"2.54mm  (100mils)", u"1.27mm    (50mils)", u"0.635mm  (25mils)", u"0.508mm  (20mils)", u"0.254mm  (10mils)", u"0.127mm   (5mils)" ]
		self.m_comboBoxGrid = wx.ComboBox( self, wx.ID_ANY, u"1.0mm   (39.37mils)", wx.DefaultPosition, wx.Size( -1,-1 ), m_comboBoxGridChoices, 0 )
		self.m_comboBoxGrid.SetSelection( 0 )
		bSizer31.Add( self.m_comboBoxGrid, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer3.Add( bSizer31, 0, 0, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_radioBtnGO = wx.RadioButton( self, wx.ID_ANY, u"GridOrigin reference", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_radioBtnGO, 0, wx.ALL, 5 )

		self.m_radioBtnAO = wx.RadioButton( self, wx.ID_ANY, u"AuxOrigin reference", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_radioBtnAO, 0, wx.ALL, 5 )

		self.m_radioBtnZero = wx.RadioButton( self, wx.ID_ANY, u"Top Left (0,0)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_radioBtnZero, 0, wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

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


