import wx
try:
    from .model3d_list import checkMissing3DM
    checkMissing3DM().register()
except Exception as e:
    wx.LogMessage('3D missing models checker plugin error\n'+str(e))
