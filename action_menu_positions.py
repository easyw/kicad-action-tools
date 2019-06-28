# -*- coding: utf-8 -*-
#
# A script to generate POS file for kicad_pcb
# requirements: KiCAD pcbnew >= 4.0
# release "1.0.8"
# copyright Maurice easyw
# 
# main script from https://forum.kicad.info/t/pcba-wants-all-parts-in-the-pos-file-not-just-smd/10045/6
#

___version___="1.0.8"
#wx.LogMessage("My message")
#mm_ius = 1000000.0

import sys, os
import pcbnew
import datetime
import wx
from pcbnew import *
import base64
from wx.lib.embeddedimage import PyEmbeddedImage

"""
execfile ("C:/kicad-wb-1602/msys64/home/userC/out3Dm/pack-x86_64/share/kicad/scripting/plugins/getpos.py")
"""

def generate_POS():
    import os
    mm_ius = 1000000.0
    
    my_board = pcbnew.GetBoard()

    fileName = pcbnew.GetBoard().GetFileName()
    
    dirpath = os.path.abspath(os.path.expanduser(fileName))
    path, fname = os.path.split(dirpath)
    ext = os.path.splitext(os.path.basename(fileName))[1]
    name = os.path.splitext(os.path.basename(fileName))[0]
    
    #lsep=os.linesep
    lsep='\n'
    
    LogMsg1=lsep+"reading from:" + lsep + dirpath + lsep + lsep
    out_filename_top_SMD=path+os.sep+name+"_POS_top_SMD.txt"
    out_filename_bot_SMD=path+os.sep+name+"_POS_bot_SMD.txt"
    out_filename_top_THD=path+os.sep+name+"_POS_top_THD.txt"
    out_filename_bot_THD=path+os.sep+name+"_POS_bot_THD.txt"
    out_filename_top_VIRTUAL=path+os.sep+name+"_POS_top_Virtual.txt"
    out_filename_bot_VIRTUAL=path+os.sep+name+"_POS_bot_Virtual.txt"
    out_filename_ALL=path+os.sep+name+"_POS_All.txt"
    #out_filename=path+os.sep+name+"_POS.txt"
    LogMsg1+="written to:" + lsep + out_filename_top_SMD + lsep
    LogMsg1+= out_filename_bot_SMD + lsep
    LogMsg1+= out_filename_top_THD + lsep
    LogMsg1+= out_filename_bot_THD + lsep
    LogMsg1+= out_filename_top_VIRTUAL + lsep
    LogMsg1+= out_filename_bot_VIRTUAL + lsep
    LogMsg1+= out_filename_ALL + lsep
    # print (LogMsg)
    # 
    # print ("### Module positions - created on %s ###" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    # print ("### Printed by get_pos v1")
    # print ("## Unit = mm, Angle = deg.")
    # print ("## Side : All")
    # print ("# Ref     Val        Package       PosX       PosY       Rot  Side    Type")

    Header_1="### Module positions - created on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+lsep
    Header_1+="### Printed by get_pos v1"+lsep
    Header_1+="## Unit = mm, Angle = deg."+lsep
    #LogMsg+="## Side : All"+lsep
    Header_2="## Board Aux Origin: " + str(my_board.GetAuxOrigin())+lsep
    
    Header_2+="{0:<10}".format("# Ref")+"{0:<20}".format("Val")+"{0:<20}".format("Package")+\
            "{0:<11}".format("PosX")+"{0:<11}".format("PosY")+"{0:<8}".format("  Rot")+\
            "{0:<10}".format("  Side")+"  Type"+lsep
    content_top_SMD=''
    content_bot_SMD=''
    content_top_THD=''
    content_bot_THD=''
    content_top_VIRTUAL=''
    content_bot_VIRTUAL=''
    content_ALL=''
    SMD_pads = 0
    TH_pads = 0
    Virt_pads = 0
    TH_top_cnt = 0
    TH_bot_cnt = 0
    SMD_top_cnt = 0
    SMD_bot_cnt = 0
    Virt_top_cnt = 0
    Virt_bot_cnt = 0
    
    bb = my_board.GetBoardEdgesBoundingBox()
    pcb_height = bb.GetHeight() / mm_ius
    pcb_width = bb.GetWidth() / mm_ius 
    #to add relative position to 
    #print ("Board Aux Origin: " + str(my_board.GetAuxOrigin()))
    
    #'{0:<10} {1:<10} {2:<10}'.format(1.0, 2.2, 4.4))
    
    for module in my_board.GetModules(): 
        #print ("%s \"%s\" %s %1.3f %1.3f %1.3f %s" % ( module.GetReference(), 
        #Nchars = 20
        # RefL = 10; ValL = 20
        
        md=""
        if module.GetAttributes() == 0:   # PTH=0, SMD=1, Virtual = 2
            md = "THD"
            TH_pads+=module.GetPadCount()
        elif module.GetAttributes() == 1:
            md = "SMD"
            SMD_pads+=module.GetPadCount()
        else:
            md = "VIRTUAL"
            Virt_pads+=module.GetPadCount()
        
        #Reference=str(module.GetReference()).ljust(Nchars/2)
        #Value=str(module.GetValue()).ljust(Nchars)
        #Package=str(module.GetFPID().GetLibItemName()).ljust(Nchars)
        #X_POS=str(pcbnew.ToMM(module.GetPosition().x - my_board.GetAuxOrigin().x ))
        #Y_POS=str(-1*pcbnew.ToMM(module.GetPosition().y - my_board.GetAuxOrigin().y))
        #Rotation=str(module.GetOrientation()/10)
        #Layer="top".ljust(Nchars) if module.GetLayer() == 0 else "bottom".ljust(Nchars)
        #Type=md
        Reference="{0:<10}".format(str(module.GetReference()))
        Value = str(module.GetValue())
        Value=(Value[:17] + '..') if len(Value) > 19 else Value
        Value="{0:<20}".format(Value)
        Package = str(module.GetFPID().GetLibItemName())
        Package=(Package[:17] + '..') if len(Package) > 19 else Package
        Package="{0:<20}".format(Package)
        #Package="{0:<20}".format(str(module.GetFPID().GetLibItemName()))
        X_POS='{0:.4f}'.format(pcbnew.ToMM(module.GetPosition().x - my_board.GetAuxOrigin().x ))
        X_POS="{0:<11}".format(X_POS)
        Y_POS='{0:.4f}'.format(-1*pcbnew.ToMM(module.GetPosition().y - my_board.GetAuxOrigin().y))
        Y_POS="{0:<11}".format(Y_POS)
        Rotation='{0:.1f}'.format((module.GetOrientation()/10))
        Rotation="{0:>6}".format(Rotation)+'  '
        if module.GetLayer() == 0:
            Layer="  top"
        else:
            Layer="  bottom"
        #Side="## Side :"+Layer+lsep
        Layer="{0:<10}".format(Layer)
        Type='  '+md
        content=Reference
        content+=Value
        content+=Package
        content+=X_POS
        content+=Y_POS
        content+=Rotation
        content+=Layer
        content+=Type+lsep
        if 'top' in Layer and 'SMD' in Type:
            content_top_SMD+=content
            SMD_top_cnt+=1
        elif 'bot' in Layer and 'SMD' in Type:
            content_bot_SMD+=content
            SMD_bot_cnt+=1
        elif 'top' in Layer and 'THD' in Type:
            content_top_THD+=content
            TH_top_cnt+=1
        elif 'bot' in Layer and 'THD' in Type:
            content_bot_THD+=content
            TH_bot_cnt+=1
        elif 'top' in Layer and 'VIRTUAL' in Type:
            content_top_VIRTUAL+=content
            Virt_top_cnt+=1
        elif 'bot' in Layer and 'VIRTUAL' in Type:
            content_bot_VIRTUAL+=content
            Virt_bot_cnt+=1
        content_ALL+=content
        #print ("%s %s %s %1.4f %1.4f %1.4f %s %s" % ( str(module.GetReference()).ljust(Nchars), 
        #                            str(module.GetValue()).ljust(Nchars),
        #                            str(module.GetFPID().GetLibItemName()).ljust(Nchars),
        #                            pcbnew.ToMM(module.GetPosition().x - my_board.GetAuxOrigin().x ),
        #                            -1*pcbnew.ToMM(module.GetPosition().y - my_board.GetAuxOrigin().y),
        #                            module.GetOrientation()/10,
        #                            "top".ljust(Nchars) if module.GetLayer() == 0 else "bottom".ljust(Nchars),
        #                            md
        #                            ))
    
#"top" if module.GetLayer() == 0 else "bottom"
                                    
    #LogMsg+="## End"+lsep
    
    Header=Header_1+"## Side : top"+lsep+Header_2
    content=Header+content_top_SMD+"## End"+lsep
    with open(out_filename_top_SMD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : bottom"+lsep+Header_2
    content=Header+content_bot_SMD+"## End"+lsep
    with open(out_filename_bot_SMD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : top"+lsep+Header_2
    content=Header+content_top_THD+"## End"+lsep
    with open(out_filename_top_THD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : bottom"+lsep+Header_2
    content=Header+content_bot_THD+"## End"+lsep
    with open(out_filename_bot_THD,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : top"+lsep+Header_2
    content=Header+content_top_VIRTUAL+"## End"+lsep
    with open(out_filename_top_VIRTUAL,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : bottom"+lsep+Header_2
    content=Header+content_bot_VIRTUAL+"## End"+lsep
    with open(out_filename_bot_VIRTUAL,'w') as f_out:
        f_out.write(content)
    Header=Header_1+"## Side : ALL"+lsep+Header_2
    content=Header+content_ALL+"## End"+lsep
    content = content + '## '+ str(SMD_pads) + ' SMD pads' +lsep
    content = content + '## '+ str(TH_pads) + ' TH pads' +lsep
    content = content + '## '+ str(Virt_pads) + ' Virtual pads' +lsep
    content = content + '## '+ str( TH_top_cnt) + ' Top TH modules' + lsep
    content = content + '## '+ str( TH_bot_cnt) + ' Bot TH modules' + lsep
    content = content + '## '+ str( SMD_top_cnt) + ' Top SMD modules' + lsep
    content = content + '## '+ str( SMD_bot_cnt) + ' Bot SMD modules' + lsep
    content = content + '## '+ str( Virt_top_cnt) + ' Top Virtual modules' + lsep
    content = content + '## '+ str( Virt_bot_cnt) + ' Bot Virtual modules' + lsep
    
    with open(out_filename_ALL,'w') as f_out:
        f_out.write(content)

    #with open(out_filename,'w') as f_out:
    #    f_out.write(LogMsg)
    #LogMsg=""
    #f = open(out_filename,'w')
    #f.write(LogMsg)
    #f.close()
    LogMsg1+= lsep + str(SMD_pads) + ' SMD pads' +lsep
    LogMsg1+= str(TH_pads) + ' TH pads' +lsep
    LogMsg1+= str(Virt_pads) + ' Virtual pads' +lsep
    LogMsg1+= str( TH_top_cnt) + ' Top TH modules' + lsep
    LogMsg1+= str( TH_bot_cnt) + ' Bot TH modules' + lsep
    LogMsg1+= str( SMD_top_cnt) + ' Top SMD modules' + lsep
    LogMsg1+= str( SMD_bot_cnt) + ' Bot SMD modules' + lsep
    LogMsg1+= str( Virt_top_cnt) + ' Top Virtual modules' + lsep
    LogMsg1+= str( Virt_bot_cnt) + ' Bot Virtual modules' + lsep
    LogMsg1+= '{0:.3f}'.format( pcb_height ) + 'mm Pcb Height, ' + '{0:.3f}'.format( pcb_width ) + 'mm Pcb Width [based on Edge bounding box]' +lsep
    
    return LogMsg1
    #return LogMsg1+LogMsg




class generatePOS( pcbnew.ActionPlugin ):
    """
    A script to generate POS file for kicad_pcb
    requirements: KiCAD pcbnew >= 4.0
    release "1.0.1"
   
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Generate POS output"
        self.category = "Fabrication Output"
        self.description = "Generate POS output for SMD, THD, Virtual"

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
                wx.Dialog.__init__(self, parent, id=-1, title="Generate POS output")#
                #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION) 
                #, style=wx.DEFAULT_DIALOG_STYLE, wx.ICON_INFORMATION)
                #, pos=DefaultPosition, size=DefaultSize, style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX), name="fname")
                #, wx.ICON_INFORMATION) #, title="Annular Check", style=wx.DEFAULT_FRAME_STYLE, wx.ICON_INFORMATION)    
                #
                
                self.SetIcon(PyEmbeddedImage(round_ico_b64_data).GetIcon())
                #wx.IconFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY)))
                self.panel = wx.Panel(self)     
                self.title = wx.StaticText(self.panel, label="Generate POS debug:")
                #self.result = wx.StaticText(self.panel, label="")
                #self.result.SetForegroundColour('#FF0000')
                self.button = wx.Button(self.panel, label="Close")
                #self.lblname = wx.StaticText(self.panel, label="Your name:")
                #self.editname = wx.TextCtrl(self.panel, size=(140, -1))
                self.editname = wx.TextCtrl(self.panel, size = (600, 500), style = wx.TE_MULTILINE|wx.TE_READONLY)
        
        
                # Set sizer for the frame, so we can change frame size to match widgets
                self.windowSizer = wx.BoxSizer()
                self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)        
        
                # Set sizer for the panel content
                self.sizer = wx.GridBagSizer(5, 0)
                self.sizer.Add(self.title, (0, 0))
                #self.sizer.Add(self.result, (1, 0))
                #self.sizer.Add(self.lblname, (1, 0))
                self.sizer.Add(self.editname, (1, 0))
                self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)
        
                # Set simple sizer for a nice border
                self.border = wx.BoxSizer()
                self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)
                
                # Use the sizers
                self.panel.SetSizerAndFit(self.border)  
                self.SetSizerAndFit(self.windowSizer)  
                #self.result.SetLabel(msg)
                # Set event handlers
                #self.Show()
                self.button.Bind(wx.EVT_BUTTON, self.OnClose)
                self.Bind(wx.EVT_CLOSE,self.OnClose)
            
            def OnClose(self,e):
                #wx.LogMessage("c")
                e.Skip()
                #self.Close()
                self.Destroy()
            
            #def OnButton(self, e):
            #    self.result.SetLabel(self.editname.GetValue())
            def setMsg(self, t_msg):
                self.editname.SetValue(t_msg)


                
        def f_mm(raw):
            return repr(raw/mm_ius)
        
        board = pcbnew.GetBoard()
        
        #fileName = GetBoard().GetFileName()
        fileName = pcbnew.GetBoard().GetFileName()
        if len(fileName)==0:
            wx.LogMessage("a board needs to be saved/loaded!")
        else:
            LogMsg=''
            # msg="'get_pos.py'"+os.linesep
            msg="Generate POS output: version = "+___version___+os.linesep
            #msg+="Generate POS output"+os.linesep
             #print (msg)
            #LogMsg=msg+'\n\n'
            
            print(msg)
            LogMsg+=msg
            reply=generate_POS()
            LogMsg+=reply
            
            frame = displayDialog(None)
            #frame = wx.Frame(None)
            frame.Center()
            frame.setMsg(LogMsg)
            frame.ShowModal()
            frame.Destroy()
            #frame = wx.wxFrame(None, 10110, 'T-Make', size=wx.wxSize(100,100),
            #           style=wx.wxSTAY_ON_TOP)
            #frame.show()
            
generatePOS().register()

# "b64_data" is a variable containing your base64 encoded jpeg
round_ico_b64_data =\
"""
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
gg==
""" 



#  execfile("round_tracks.py")

