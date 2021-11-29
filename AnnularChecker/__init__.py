import wx
try:
    from .annular_checker import annular_check
    annular_check().register()
except Exception as e:
    wx.LogMessage('annular checker plugin error\n'+str(e))
