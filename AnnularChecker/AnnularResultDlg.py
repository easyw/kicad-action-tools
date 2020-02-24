# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class AnnularResultDlg
###########################################################################

class AnnularResultDlg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Annular Checker", pos = wx.DefaultPosition, size = wx.Size( 539,659 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticTitle = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTitle.Wrap( -1 )

		bSizer2.Add( self.m_staticTitle, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_richTextResult = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.m_richTextResult.SetMinSize( wx.Size( -1,400 ) )

		bSizer2.Add( self.m_richTextResult, 1, wx.EXPAND |wx.ALL, 5 )

		gSizer3 = wx.GridSizer( 0, 2, 0, 0 )

		self.ok_btn = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.ok_btn, 0, wx.ALL, 5 )

		self.copy_btn = wx.Button( self, wx.ID_ANY, u"Copy Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.copy_btn, 0, wx.ALL, 5 )


		bSizer2.Add( gSizer3, 1, wx.ALIGN_TOP|wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


