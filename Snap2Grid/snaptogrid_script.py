# -*- coding: utf-8 -*-
#
# A script to Snap modules to selected Grid for kicad_pcb
# requirements: KiCAD pcbnew >= 4.0
# copyright Maurice easyw
# 
#

#import snaptogrid; import importlib; importlib.reload(snaptogrid)
import sys, os
import pcbnew
import datetime
import wx
from pcbnew import *

use_grid_origin = True
gridReference = 0.127 #1.27 #mm pcbnew.FromMM(1.0) #0.1mm


# def PutOnGridMM(value, gridSizeMM):
#     thresh = FromMM(gridSizeMM)
#     return round(value/thresh)*thresh
# 
# def PutOnGridMils(value, gridSizeMils):
#     thresh = FromMils(gridSizeMils)
#     return round(value/thresh)*thresh
#def SetPosition(self, p):
#    """SetPosition(wxRect self, wxPoint p)"""
#    return _pcbnew.wxRect_SetPosition(self, p)


def Snap2Grid(gridSizeMM,use_grid_origin):
    import sys,os
    #mm_ius = 1000000.0
    
    pcb = pcbnew.GetBoard()
    gridOrigin = pcb.GetGridOrigin()
    auxOrigin = pcb.GetAuxOrigin()
    content=''
    #wxPoint(77470000, 135890000)
    for module in pcb.GetModules(): 
        if module.IsSelected():
            if use_grid_origin:
                mpx = module.GetPosition().x - gridOrigin.x
                mpy = module.GetPosition().y - gridOrigin.y
                print(mpx,mpy)
                mpxOnG = int(mpx/FromMM(gridSizeMM))*FromMM(gridSizeMM)+ gridOrigin.x
                mpyOnG = int(mpy/FromMM(gridSizeMM))*FromMM(gridSizeMM)+ gridOrigin.y
                print(mpxOnG,mpyOnG)
                module.SetPosition(wxPoint(mpxOnG,mpyOnG))
                X_POS=str(module.GetPosition().x) # - gridOrigin.x)
                #X_POS='{0:.4f}'.format(pcbnew.ToMM(module.GetPosition().x - gridOrigin.x ))
                X_POS="{0:<11}".format(X_POS)
                Y_POS=str(module.GetPosition().y) # - gridOrigin.y)
                Y_POS="{0:<11}".format(Y_POS)
                ## mpOnGx = PutOnGridMM(module.GetPosition().x, gridSizeMM)
                ## mpOnGy = PutOnGridMM(module.GetPosition().y, gridSizeMM)
                ## module.SetPosition(wxPoint(mpOnGx,mpOnGy))
                #module.SetPosition(wxPoint(mpOnGx+FromMM(100.0),mpOnGy+FromMM(2.0)))
                #module.SetOrientation(10)
                #Y_POS='{0:.4f}'.format(-1*pcbnew.ToMM(module.GetPosition().y - gridOrigin.y))
            # else:
            #     mpx = module.GetPosition().x - auxOrigin().x
            #     mpy = module.GetPosition().y - auxOrigin().y
            #     X_POS='{0:.4f}'.format(pcbnew.ToMM(module.GetPosition().x - auxOrigin().x ))
            #     X_POS="{0:<11}".format(X_POS)
            #     Y_POS='{0:.4f}'.format(-1*pcbnew.ToMM(module.GetPosition().y - auxOrigin().y))
            #     Y_POS="{0:<11}".format(Y_POS)
            Reference="{0:<10}".format(str(module.GetReference()))
            Value = str(module.GetValue())
            Value=(Value[:17] + '..') if len(Value) > 19 else Value
            Value="{0:<20}".format(Value)
            Rotation='{0:.1f}'.format((module.GetOrientation()/10))
            Rotation="{0:>6}".format(Rotation)+'  '
            if module.GetLayer() == 0:
                Layer="  top"
            else:
                Layer="  bottom"
            #Side="## Side :"+Layer+lsep
            Layer="{0:<10}".format(Layer)
            content+=Reference
            #content+=Value
            content+=X_POS
            content+=Y_POS
            #content+=str(mpOnGx)
            #content+=str(mpOnGy)
            content+=str(mpxOnG)
            content+=str(mpyOnG)
            content+=Layer+os.linesep
    content+=str(pcbnew.FromMM(gridReference))
    Refresh()
    return content

reply=Snap2Grid(gridReference,use_grid_origin)
#LogMsg=reply
wx.LogMessage(reply)
