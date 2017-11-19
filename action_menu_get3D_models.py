#!/usr/bin/python
# -*- coding: utf-8 -*-


# licence GPL 2
# copyright easyw

## todo:
# fix extra directory creation
# add force override as option check
# add OK-Cancel buttons
# add popen to elevate process

___version___="1.3.0"
#wx.LogMessage("My message")

import sys
import wx
import subprocess
import os
import pcbnew
from pcbnew import *
import base64
from wx.lib.embeddedimage import PyEmbeddedImage

import codecs
import re,os, sys

import urllib2
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


KISYS3DMOD=ur"C:\KiCad-stable\share\kicad\modules\packages3d"
KISYS3DMOD=ur"C:\Program Files (x86)\KiCad\share\kicad\modules\packages3d1"
KISYS3DMOD=KISYS3DMOD.replace('\\','/')

global fileOut

fileOut=ur"log-3Dmodels.txt"
fileOut=fileOut.replace('\\','/')

# filename=ur"C:\Temp\blinky-dev.kicad_pcb"
# filename=filename.replace('\\','/')

github_src=ur'https://github.com/KiCad/kicad-packages3D/raw/master/'
gh_base=ur'https://github.com/KiCad/kicad-packages3D/'


# import argparse
# 
# args=sys.argv
#for a in args:
#    print a

    
def collect_models(fn, kv, k3d, kprj, fupd):
    """collect models from GH for the present pcb"""
    
    global fileOut
    
    overwrite=False
    if fupd=='/u':
        overwrite=True
    filename=fn
    KISYS3DMOD=k3d
    kicad_version=kv
    KIPRJMOD=kprj
    
    txtFile = codecs.open(filename, mode='rb', encoding='utf-8', errors='replace', buffering=1)  #test maui utf-8
    content = txtFile.readlines()
    content.append(" ")
    txtFile.close()
    data=''.join(content)
    
    model_list = re.findall(r'\(model\s+(.+?)\.wrl',data)
    #model_list = re.findall(r'\(model\s+(.+?)\.wrl',data, re.MULTILINE|re.DOTALL)
    model_list2 = re.findall(r'\(model\s+(.+?)\.WRL',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.stp',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.step',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.STP',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.STEP',data)
    model_list=model_list+model_list2
    
    #print model_list
    fOut=codecs.open(fileOut, mode='wb', encoding='utf-8', errors='replace', buffering=1)
    
    parsed=[]
    fOut.write(u'parsed '+str(len(model_list))+u' model(s)'+ os.linesep)
    for d in model_list:        
        found=False
        d1=d.replace('\\','/')
        #d1=d1.rstrip('/') 
        if 'KISYS3DMOD' in d1:
            d1=d1.lstrip('${KISYS3DMOD}/')
            d1=d1.lstrip('/')
        d=d1
        local=False
        #print d1
        if 'KIPRJMOD' in d1:
            #print 'LOCAL'
            #stop
            local=True
            d1=d1.lstrip('${KIPRJMOD}')
            d1=d1.lstrip('/')
            print d1
        d=d1
        if d not in parsed:
            if local:
                fOut.write(d+u'.wrl'+ os.linesep)
                directory=d1
                prefix=KIPRJMOD
            else:
                fOut.write(KISYS3DMOD+os.sep+d+u'.wrl'+ os.linesep)
                directory=KISYS3DMOD+os.sep+d1
                prefix=KISYS3DMOD+os.sep
            #print d1
            ##stop
            #print d1.rfind('/')
            #stop
            if d1.rfind('/')!=-1:
                d1=d1[0:d1.rindex('/')]
            #else:
                
            #print 'd, d1, dir'
            #print d
            #print d1
            #print directory
            #stop
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except:
                    print 'you need Administrative rights'
                    continue
            if os.path.exists(prefix+d+u'.wrl'):
                found=True
                print u'exists '+d+u'.wrl'
                #fOut.write(d)
                #fOut.write('\n')
            if not found or overwrite:
                fileDest=prefix+d+u'.wrl'
                d1=d.replace('\\','/')
                try:
                    response = urllib2.urlopen(github_src+d1+u'.wrl', context=ctx)
                    myfile = response.read()
                    f_dest=codecs.open(fileDest, mode='wb', encoding='utf-8', errors='replace', buffering=1)
                    f_dest.write(myfile)
                    print fileDest + ur' written'
                except:
                    print 'error file not found'
                    print github_src+d1+u'.wrl'
                    print 'or you may need Administrative rights'
                #print myfile
                
            found=False
            if os.path.exists(prefix+d+u'.step') or os.path.exists(prefix+d+u'.STEP') or \
                                                os.path.exists(prefix+d+u'.stp') or os.path.exists(prefix+d+u'.STP'):
                print u'exists '+d+u'.step'
                #fOut.write(d)
                #fOut.write('\n')
                found=True
            if not found or overwrite:
                fileDest=prefix+d+u'.step'
                d1=d.replace('\\','/')
                #print github_src+d1+u'.step'
                try:
                    response = urllib2.urlopen(github_src+d1+u'.step', context=ctx)
                    myfile = response.read()
                    f_dest=codecs.open(fileDest, mode='wb', encoding='utf-8', errors='replace', buffering=1)
                    f_dest.write(myfile)
                    print fileDest + ur' written'
                except:
                    print 'error file not found'
                    print github_src+d1+u'.step'
                    print 'or you may need Administrative rights'
                #print myfile
                #fOut.write('\n')
            parsed.append(d)
        
    fOut.close()
    #print model_list2
    return parsed
##



class mod3D_check( pcbnew.ActionPlugin ):
    """
    A script to check for 3D models
    """
    
    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "3D models check"
        self.category = "Checking PCB"
        self.description = "Automatically check 3D models presence on an existing PCB"

    def Run( self ):
        
        #wx.MessageDialog(self.frame,"ciao")
        #subprocess.check_call(["C:\pathToYourProgram\yourProgram.exe", "your", "arguments", "comma", "separated"])
        #http://stackoverflow.com/questions/1811691/running-an-outside-program-executable-in-python
        class displayDialog(wx.Dialog):
            """
            The default frame
            http://stackoverflow.com/questions/3566603/how-do-i-make-wx-textctrl-multi-line-text-update-smoothly
            """
        
            #----------------------------------------------------------------------
            #def __init__(self):
            #    """Constructor"""
            #    wx.Frame.__init__(self, None, title="Display Frame", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)
            #    panel = wx.Panel(self)
            def __init__(self, parent):
                wx.Dialog.__init__(self, parent, id=-1, title="3D models Checker")#
                
                self.SetIcon(PyEmbeddedImage(annular_ico_b64_data).GetIcon())
                #wx.IconFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY)))
                self.panel = wx.Panel(self)     
                self.title = wx.StaticText(self.panel, label="3D models Check result:")
                self.editname = wx.TextCtrl(self.panel, size = (300, 400), style = wx.TE_MULTILINE|wx.TE_READONLY)
        
        
                # Set sizer for the frame, so we can change frame size to match widgets
                self.windowSizer = wx.BoxSizer()
                self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        
        
                # Set sizer for the panel content
                self.sizer = wx.GridBagSizer(5, 0)
                self.sizer.Add(self.title, (0, 0))
                #self.sizer.Add(self.result, (1, 0))
                #self.sizer.Add(self.lblname, (1, 0))
                self.sizer.Add(self.editname, (1, 0))
                #self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)
        
                # Set simple sizer for a nice border
                self.border = wx.BoxSizer()
                self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
        
                # Use the sizers
                self.panel.SetSizerAndFit(self.border)  
                self.SetSizerAndFit(self.windowSizer)  
                #self.result.SetLabel(msg)
                # Set event handlers
                #self.button.Bind(wx.EVT_BUTTON, self.OnButton)
                #self.Show()
                #self.Bind(wx.EVT_CLOSE,self.OnClose)
            
            #def OnClose(self,e):
            #    #wx.LogMessage("c")
            #    e.Skip()
                #self.Close()
            
            #def OnButton(self, e):
            #    self.result.SetLabel(self.editname.GetValue())
            def setMsg(self, t_msg):
                self.editname.SetValue(t_msg)
           
        def mod3D_presence(mpath):
            # checking 3d model existance
            p=mpath
            #print via.GetWidth()
            #print via.GetDrillValue()
            return p
            
        
        global fileOut
        board = pcbnew.GetBoard()
        
        fileName = GetBoard().GetFileName()
        if len(fileName)==0:
            wx.LogMessage("a board needs to be saved/loaded!")
        else:
            LogMsg=''
            msg="'action_menu_mod3D_check.py'\n"
            msg+="version = "+___version___
            msg+="\nTesting PCB for 3D models existence in\n"
            msg+=fileName+'\n'
            KISYS3DMOD = os.environ.get('KISYS3DMOD',None)
            if KISYS3DMOD is None:
                msg += 'Environment variable KISYS3DMOD is not set.\n\n'
            else:
                msg+='KISYS3DMOD='+KISYS3DMOD+'\n'
            pcbName = (os.path.splitext(GetBoard().GetFileName())[0]) #filename no ext
            KIPRJMOD = os.path.dirname(pcbName)
            msg += 'KIPRJMOD='+KIPRJMOD+'\n'
            home_user=os.path.expanduser('~')
            fileOut=os.path.join(home_user,fileOut) #writing log at user home folder
            #fileOut=os.path.join(KIPRJMOD,fileOut) #writing log at PRJ folder
            #print (msg)
            
            
            force_upd='/u'
            if force_upd is not None:
                msg+='\nforcing download and override all 3D models\n'
            #else:    
            #    msg+='\n'
            
            LogMsg+=msg+'\n'
            LogMsg+='Source 3D path: '+gh_base+'\n'
            
            kicad_ver='5'
            
            dir_path = os.path.dirname(os.path.realpath(__file__))
            LogMsg+='script dir='+dir_path+'\n'
            
            models_updated=collect_models(fileName, kicad_ver, KISYS3DMOD, KIPRJMOD, force_upd)
            
            for m in models_updated:
                LogMsg+=m+'\n'

            if 0:
                #determining platform
                from sys import platform as _platform
                pltf_linux=False;pltf_osx=False;pltf_win=False
                if _platform == "linux" or _platform == "linux2":
                    #print 'linux'
                    pltf_linux=True
                elif _platform == "darwin":
                    #print 'osx'
                    pltf_osx=True
                elif _platform == "win32":
                    #print 'win'            
                    pltf_win=True
                import subprocess
                cmd=os.path.join(dir_path,"test.cmd")
                # prm="C:\Windows\System32\catroot2\dberr.txt"
                prm = cmd
                param='@('+'\"'+prm+'\"'+')'
                
                ## p = subprocess.Popen([r'powershell.exe',
                ##                 'Start-Process '+cmd+' ',
                ##                 '-ArgumentList '+param+' ',
                ##                 '-Verb RunAs'])
                ## p.communicate()
                #SW_HIDE = 0
                #info = subprocess.STARTUPINFO()
                #info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                #info.wShowWindow = SW_HIDE
                #subprocess.Popen(r'C:\test.exe', startupinfo=info)
                SW_MINIMIZE = 6
                info = subprocess.STARTUPINFO()
                info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = SW_MINIMIZE
                #subprocess.Popen(r'C:\test.exe', startupinfo=info)
                p = subprocess.Popen([r'powershell.exe',
                                'Start-Process '+cmd+' ',
                                '-ArgumentList '+param+' ',
                                '-Verb RunAs'], startupinfo=info)
                p.communicate()    
    
            
            #wx.LogMessage(pcbName)#LogMsg)
            ##wx.LogMessage(LogMsg)
            #subprocess.check_call([FC, kSU, pcbName])
            ##p = subprocess.Popen([FC, kSU, pcbName])
            
            frame = displayDialog(None)
            #frame = wx.Frame(None)
            frame.Center()
            frame.setMsg(LogMsg)
            frame.ShowModal()
            frame.Destroy()
            #frame = wx.wxFrame(None, 10110, 'T-Make', size=wx.wxSize(100,100),
            #           style=wx.wxSTAY_ON_TOP)
            #frame.show()
        
mod3D_check().register()



# "b64_data" is a variable containing your base64 encoded jpeg
annular_ico_b64_data =\
"""
iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAIQQAACEEB+v+u9gAAABl0RVh0U29mdHdhcmUAd3d
3Lmlua3NjYXBlLm9yZ5vuPBoAAAJ5SURBVDiNdZRNSFRRFMd/976ZJjeBn2PUoiLaiMFkFkHIQ0NBdBUlJuIqiixmIYjQRgiJYKAMXRRSi6TCD5gaWiSFsy
gixOyDpDAog8wn9SISapz33m0x82bmzcOzO/97/r973nn3XqGUojjCybIm4BhQD9Rl5XlgDnhi6ObTYo8oBIWTZeXAMNDlalW/FJYmMLd5fONA1NBN0wcKJ
8sagftAZWRJcWHS5vCiouJ3pnClUvC8VnDtpOTTDgGwCpwydHM2Bwony8LAe6koH7hjc37aQXN8XwzAv5DgUo9krF0C/ABqDN1ck9n1G0D54C2H6OTmEICt
KcXQTZvTCQegAhgFEFWzpW1A4uAHRaLfQhbPXgD+/8HfkKBhNMDXMACtEmgC6L/reCBWKGAzMmLxbQWWl2Fw0FJavqIkpYhO2m7aHADqNQcOLXq3DcSuKnp
6Ajmhry8g1tfTxGJBVzryLuepl0Bk16qiJJUHKU0qOjryEDe6u4OF6e7vitCGAohIAFk0XCWEQkp8oWmeVAAiu78EFj5vF6S2iFyBtGxJPJ72gSYmPNpyOH
McgAUJzFkazO/zetLRc4J43MayIJWCsTHLuTzkaellTa7rOVE1W9oOPDz6VjF90fI14QQ1RzhKCNsRhfpGEBqvB1jaKQDapKGbCeDBs/2C8Rb/XGTalsUQg
Fin5kKmDN185DrPAD8HzmrcbpUony0flgZXujSGT+SuSC94L20LcA8obXiduSp1H8kdiz8l8KJWEOvUeLNXuJAuQzdnPKAsrBoYAY4DaA7sWck8I1+qKex0
Cug1dHPNFcQmD1sL0AwcACJZeQF4BcwYuvm42PMfVgD11Y9MUIEAAAAASUVORK5CYII=
""" 


#  execfile("annular.py")
# annular.py Testing PCB for Annular Ring >= 0.15
# AR violation of 0.1 at XY 172.974,110.744
# VIAS that Pass = 100 Fails = 1
# AR violation of 0.1 at XY 172.212,110.744
# AR violation of 0.0 at XY 154.813,96.52
# PADS that Pass = 49 Fails = 2

