# kicad-action-plugins
#### <font color='navy'><b>kicad action plugin tools</b></font>

- ### action_menu_annular_check.py
A script to check for annular ring violations  
for PTH, NPTH pads and vias  

- ### action_menu_pcb2dxf
A script to export technical layers of kicad PCB to DXF  
DXF generated file has single line draw as it should be for mechanical interchange (this option is missing in pcbnew plot)  
  

---
## action_menu_annular_check.py
A script to check for annular ring violations  
for PTH, NPTH pads and vias  

requirements: KiCAD pcbnew > 4.0 built with KICAD_SCRIPTING_ACTION_MENU option activated  
release "1.5.3"  

'action_menu_annular_check.py' checking PCB for Annular Ring in PTH, NPTH and Vias  
(SMD, Connector and NPTH are skipped)  
default Annular Ring >= 0.15 both for TH Pads and Vias  
to change values modify:  

    AR_SET = 0.150   #minimum annular accepted for pads  
    AR_SET_V = 0.150  #minimum annular accepted for vias  
    DRL_EXTRA = 0.100 #extra drill margin size for production  

Launch the Annular Check script in pcbnew from Tools menu:  
![Annular Check](screenshots/annular-checker.gif)

### todo (annular_check)
- [ ] add colors to output list  

---
## action_menu_pcb2dxf
**kicadpcb2dxf**  
_dxf exporter for mechanical layers of a kicad_pcb board_  
- "Dwgs", "Cmts", "Edge", "Eco1", "Eco2", "F.Fab", "B.Fab", "F.CrtYd", "B.CrtYd"  
- the dxf generated has single line draw as it should be for mechanical interchange (this option is missing in pcbnew plot)  

creates DXF file of technical layers of the selected kicad pcb board
  
![kicad pcb2dxf](screenshots/export-pcb2dxf.png)  

(this is a part of kicad StepUp tools; please refer to kicad StepUp tools for the full licence)

 kicadpcb2dxf: Copyright (c) 2015 Maurice easyw  
 dxf_parser="r12writer from ezdxf 0.7.6": Copyright (C) 2016, Manfred Moitzi with MIT License  
 
done:  
- [x] added line, circle, arc primitives  
- [x] added footprint support  
- [x] fixed negative arc case  
- [x] added text support (mirror & alignement not supported)  
- [x] added multiline text  
- [x] add quote support  
  
### todo (kicadpcb2dxf)
- [ ] tbd
---