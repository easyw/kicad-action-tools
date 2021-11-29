import wx
try:
    from .move_to_layer import move_to_draw_layer
    move_to_draw_layer().register()
except Exception as e:
    wx.LogMessage('move to layer plugin error\n'+str(e))
