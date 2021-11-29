# -*- coding: utf-8 -*-
#
# A script to checking 3D models in kicad_pcb
# requirements: KiCAD pcbnew >= 4.0
# release "1.0.0"
# copyright https://github.com/MitjaNemec
# copyright Maurice easyw
# 
# main script from https://forum.kicad.info/t/report-that-lists-step-models/29594/5
# 
#

### plugins errors
#import pcbnew
#pcbnew.GetWizardsBackTrace()


___version___="1.1.4"
#wx.LogMessage("My message")
#mm_ius = 1000000.0

import sys, os
import pcbnew
import datetime
import wx
from pcbnew import *
# import base64
# from wx.lib.embeddedimage import PyEmbeddedImage
from sys import platform as _platform
import webbrowser

# execfile (r"C:\Users\userC\AppData\Roaming\kicad\scripting\plugins\model3d-list.py")

import pcbnew
import os.path

show = False

def check3D():
    import os
    
    # board = pcbnew.LoadBoard(r'C:\Cad\Project_K\testboard.kicad_pcb')
    my_board = pcbnew.GetBoard()
    fileName = pcbnew.GetBoard().GetFileName()

    dirpath = os.path.abspath(os.path.expanduser(fileName))
    path, fname = os.path.split(dirpath)
    ext = os.path.splitext(os.path.basename(fileName))[1]
    name = os.path.splitext(os.path.basename(fileName))[0]
    #wx.LogMessage(dir)
    #lsep=os.linesep
    lsep='\n'
    content_log = ''
    
    # if running standalone (outside of pcbnew)
    if os.getenv("KISYS3DMOD") is None:
        pt_lnx = False;pt_osx = False;pt_win = False;
        if _platform == "linux" or _platform == "linux2":
            # linux
            pt_lnx = True
            default_prefix3d = '/usr/share/kicad/modules/packages3d'
            #'/usr/share/kicad/modules/packages3d'
        elif _platform == "darwin":
            #osx
            pt_osx = True
            default_prefix3d = '/Library/Application Support/kicad/packages3d' 
            #/Library/Application Support/kicad/modules/packages3d/' wrong location
        else:
            # Windows
            pt_win = True
            #default_prefix3d = os.path.join(os.environ["ProgramFiles"],u'\\KiCad\\share\\kicad\\modules\\packages3d')
            default_prefix3d = (os.environ["ProgramFiles"]+u'\\KiCad\\share\\kicad\\modules\\packages3d')
            #print (default_prefix3d)
            default_prefix3d = re.sub("\\\\", "/", default_prefix3d) #default_prefix3d.replace('\\','/')
            #print (default_prefix3d)
            
            os.environ["KISYS3DMOD"] = os.path.normpath(default_prefix3d)
    if os.getenv("KIPRJMOD") is None:
        os.environ["KIPRJMOD"] = os.path.abspath(os.path.dirname(my_board.GetFileName()))
        
    # prepare folder for 3Dmodels
    proj_path = os.path.dirname(os.path.abspath(my_board.GetFileName()))
    out_filename_missing_3D_models=proj_path+os.sep+name+"_missing3Dmodels.txt"
    out_log_missing_3D_models=proj_path+os.sep+name+"_log_missing3Dmodels.txt"
    
    # get all footprints
    if  hasattr(my_board,'GetModules'):
        footprints = my_board.GetModules()
    else:
        footprints = my_board.GetFootprints()
    fp_without_models = []

    paths_to_check = []
    #get all os env variable with 3D in
    for k, v in sorted(os.environ.items()):
        if '3d' in k.lower():
            print(k+':', v)
            paths_to_check.append(v)

    # go through all the footprints
    for fp in footprints:
        fp_ref = fp.GetReference()
    
        # for each footprint get all 3D models
        fp_models = fp.Models()
    
        # for each 3D model find it's path
        for model in fp_models:
            model_path = model.m_Filename
            # check if path is encoded with variables
            if "${" in model_path or "$(" in model_path:
                # get environment variable name
                start_index = model_path.find("${") + 2 or model_path.find("$(") + 2
                end_index = model_path.find("}") or model_path.find(")")
                env_var = model_path[start_index:end_index]
    
                # check if variable is defined
                path = os.getenv(env_var)
    
                # if variable is defined, get absolute path
                if path is not None:
                    clean_model_path = os.path.normpath(path + model_path[end_index + 1:])
                # if variable is not defined, we can not find the model. Thus don't put it on the list
                else:
                    content_log+=("Can not find model defined with enviroment variable:\n" + model_path) + lsep
                    fp_without_models.append((fp_ref, model_path))
                    continue
            # check if path is absolute or relative
            elif model_path == os.path.basename(model_path):
                clean_model_path = os.path.normpath(proj_path + "//" + model_path)
            # check if model is given with absolute path
            elif os.path.exists(model_path):
                clean_model_path = model_path
            elif len(paths_to_check) > 0:
            # elif (os.getenv('KISYS3DMOD') is not None):
                found = False
                for path in paths_to_check:
                    # get 3D std path variable
                    #path = os.getenv('KISYS3DMOD')
                    # if variable is defined, get absolute path
                    #if path is not None:
                    clean_model_path = os.path.normpath(path + "//" + model_path)
                    if os.path.exists(clean_model_path):
                        found = True
                        break
                    # if variable is not defined, we can not find the model. Thus don't put it on the list
                if not found:
                    content_log+=("Can not find model defined with enviroment variable ("+path+" :\n" + model_path) + lsep
                    fp_without_models.append((fp_ref, model_path))
                    continue
            # otherwise we don't know how to parse the path
            else:
                content_log+=("Ambiguous path for the model: " + model_path) + lsep
                # test default 3D_library location "KISYS3DMOD"
                if os.path.exists(os.path.normpath(os.path.join(os.getenv("KISYS3DMOD"), model_path))):
                    clean_model_path = os.path.normpath(os.path.join(os.getenv("KISYS3DMOD"), model_path))
                    content_log+=("Going with: " + clean_model_path) + lsep
                # test in project folder location
                elif os.path.exists(os.path.normpath(os.path.join(proj_path, model_path))):
                    clean_model_path = os.path.normpath(os.path.join(proj_path, model_path))
                    content_log+=("Going with: " + clean_model_path) + lsep
                else:
                    content_log+=("Can not find model defined with path:\n" + model_path) + lsep
                    fp_without_models.append((fp_ref, model_path))
                    clean_model_path = None
                    continue
    
            model_path_without_extension = clean_model_path.rsplit('.', 1)[0]
    
            found_at_least_one = False
            if clean_model_path:
                model_without_extension = clean_model_path.rsplit('.', 1)[0]
                for ext in ['.stp', '.step', '.stpZ']:
                    if os.path.exists(model_without_extension + ext):
                        found_at_least_one = True
            if not found_at_least_one:
                fp_without_models.append((fp.GetReference(), clean_model_path))
    
            pass
        pass
    LogMsg=''
    # msg="'get_pos.py'"+os.linesep
    msg=  "Missing 3D models \nversion "+___version___+os.linesep
    msg+= "NUM of 3D missing models:" + str(len(fp_without_models)) + lsep
    
    #print(msg)
    LogMsg+=msg
    content_log+=(str(repr(fp_without_models))) + lsep
    Header_1="### Missing 3D models - created on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+lsep
    Header_1+="### Printed by checking_3D_models plugin"+lsep
    #LogMsg+="## Side : All"+lsep
    Header_2="Board file: " + str(fileName)+lsep
    Header_2+="3D missing models written to:" + lsep + out_filename_missing_3D_models + lsep
    Header_2+="-------" + lsep
    content=Header_1+Header_2
    for fp in fp_without_models:
        content+=str(fp)+lsep
    content += "-------" + lsep + "NUM of 3D missing models:" + str(len(fp_without_models)) + lsep
    content += "checked extensions ['.stp', '.step', '.stpZ']"
    Header_2+="NBR of 3D missing models:" + str(len(fp_without_models))+ lsep
    # new_content = "\n".join(content)
    with open(out_filename_missing_3D_models,'w') as f_out:
        f_out.write(content)
    with open(out_log_missing_3D_models,'w') as f_out:
        f_out.write(content_log)
    LogMsg+=Header_2
    wx.LogMessage(LogMsg)
    if len(fp_without_models) > 0 and show:
        webbrowser.open('file://' + os.path.realpath(out_filename_missing_3D_models))
        webbrowser.open('file://' + os.path.realpath(out_log_missing_3D_models))

##

class checkMissing3DM( pcbnew.ActionPlugin ):
    """
    A script to checking 3D models in kicad_pcb
    requirements: KiCAD pcbnew >= 4.0
    release "1.0.0"
    """

    def defaults( self ):
        """
        Method defaults must be redefined
        self.name should be the menu label to use
        self.category should be the category (not yet used)
        self.description should be a comprehensive description
          of the plugin
        """
        self.name = "Missing 3D models \nversion "+___version___
        self.category = "Missing 3D models"
        self.description = "Missing 3D models\non kicad_pcb file"
        #self.SetIcon(PyEmbeddedImage(getPos_ico_b64_data).GetIcon())
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "./missing3dmodels.png")
        self.show_toolbar_button = True
        
    def Run( self ):
        #_pcbnew_frame = [x for x in wx.GetTopLevelWindows() if x.GetTitle().lower().startswith('pcbnew')][0]
        check3DMissing()

def check3DMissing():                
    
    board = pcbnew.GetBoard()
    
    #fileName = GetBoard().GetFileName()
    fileName = pcbnew.GetBoard().GetFileName()
    if len(fileName)==0:
        wx.MessageBox("a board needs to be saved/loaded!")
    else:
        #LogMsg=''
        # msg="'get_pos.py'"+os.linesep
        #msg="Missing 3D models \nversion "+___version___+os.linesep
        
        #print(msg)
        #LogMsg+=msg
        reply=check3D()
        #LogMsg+=reply
        #wx.LogMessage(LogMsg)
        
