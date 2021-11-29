import wx
try:
    from .fabrication_positions import generatePOS
    generatePOS().register()
except Exception as e:
    wx.LogMessage('fabrication positions plugin error\n'+str(e))
