import wx
try:
    from .snap2grid import snap_to_grid
    snap_to_grid().register()
except Exception as e:
    wx.LogMessage('snap to grid plugin error\n'+str(e))
