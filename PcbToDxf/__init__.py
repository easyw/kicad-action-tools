import wx
try:
    from .action_menu_pcb2dxf import pcb2dxf
    pcb2dxf().register()
except Exception as e:
    wx.LogMessage('pcb to dxf plugin error\n'+str(e))
