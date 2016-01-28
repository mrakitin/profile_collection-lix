from ophyd import Device, Component as Cpt, EpicsMotor


class XYPitchMotor(Device):
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')
    p = Cpt(EpicsMotor, '-Ax:P}Mtr')

WBM = XYPitchMotor('XF:16IDA-OP{Mir:WBM', name='WBM')

# WBMx = EpicsMotor('XF:16IDA-OP{Mir:WBM-Ax:X}Mtr', name='WBMx')
# WBMy = EpicsMotor('XF:16IDA-OP{Mir:WBM-Ax:Y}Mtr', name='WBMy')
# WBMP = EpicsMotor('XF:16IDA-OP{Mir:WBM-Ax:P}Mtr', name='WBMP')

DCMBragg = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:Bragg}Mtr', name='DCMBragg')
DCMx = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:X}Mtr', name='DCMx')
DCMy2 = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:Of2}Mtr', name='DCMy2')
DCMP2 = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:P2}Mtr', name='DCMP2')
DCMP2 = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:R2}Mtr', name='DCMP2')
DCMfP2 = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:PF2}Mtr', name='DCMfP2')
CCMP2 = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:CCM_PF}Mtr', name='CCMP2')
DCMP2_rb = EpicsMotor('XF:16IDA-OP{Mono:DCM-Ax:PF_RDBK}Mtr', name='DCMP2_rb')
SCN3y = EpicsMotor('XF:16IDA-BI{FS:3-Ax:Y}Mtr', name='SCN3y')
MPSx1 = EpicsMotor('XF:16IDA-OP{Slt:1-Ax:I}Mtr', name='MPSx1')
MPSx2 = EpicsMotor('XF:16IDA-OP{Slt:1-Ax:O}Mtr', name='MPSx2')
MPSy2 = EpicsMotor('XF:16IDA-OP{Slt:1-Ax:T}Mtr', name='MPSy2')
MPSy1 = EpicsMotor('XF:16IDA-OP{Slt:1-Ax:B}Mtr', name='MPSy1')
HFMx1 = EpicsMotor('XF:16IDA-OP{Mir:KBH-Ax:XU}Mtr', name='HFMx1')
HFMx2 = EpicsMotor('XF:16IDA-OP{Mir:KBH-Ax:XD}Mtr', name='HFMx2')
HFMy1 = EpicsMotor('XF:16IDA-OP{Mir:KBH-Ax:YU}Mtr', name='HFMy1')
HFMy2 = EpicsMotor('XF:16IDA-OP{Mir:KBH-Ax:YD}Mtr', name='HFMy2')
VFMx = EpicsMotor('XF:16IDA-OP{Mir:KBV-Ax:X}Mtr', name='VFMx')
VFMy1 = EpicsMotor('XF:16IDA-OP{Mir:KBV-Ax:YU}Mtr', name='VFMy1')
VFMy2 = EpicsMotor('XF:16IDA-OP{Mir:KBV-Ax:YD}Mtr', name='VFMy2')
HFMfP_rb = EpicsMotor('XF:16IDA-OP{Mir:KBH-Ax:PF_RDBK}Mtr', name='HFMfP_rb')
HFMfP = EpicsMotor('XF:16IDA-OP{Mir:KBH-Ax:PF}Mtr', name='HFMfP')
VFMfP_rb = EpicsMotor('XF:16IDA-OP{Mir:KBV-Ax:PF_RDBK}Mtr', name='VFMfP_rb')
VFMfP = EpicsMotor('XF:16IDA-OP{Mir:KBV-Ax:PF}Mtr', name='VFMfP')
SCN4y = EpicsMotor('XF:16IDA-BI{FS:4-Ax:Y}Mtr', name='SCN4y')
BPMx = EpicsMotor('XF:16IDB-BI{BPM:1-Ax:X}Mtr', name='BPMx')
BPMy = EpicsMotor('XF:16IDB-BI{BPM:1-Ax:Y}Mtr', name='BPMy')
SSAdx = EpicsMotor('XF:16IDB-OP{Slt:SSA-Ax:X}Mtr', name='SSAdx')
SSAdy = EpicsMotor('XF:16IDB-OP{Slt:SSA-Ax:Y}Mtr', name='SSAdy')
ATN1x = EpicsMotor('XF:16IDB-OP{Fltr:Atn-Ax:X1}Mtr', name='ATN1x')
ATN2x = EpicsMotor('XF:16IDB-OP{Fltr:Atn-Ax:X2}Mtr', name='ATN2x')
ATN3x = EpicsMotor('XF:16IDB-OP{Fltr:Atn-Ax:X3}Mtr', name='ATN3x')
VBMfocus = EpicsMotor('XF:16IDB-BI{FS:VBM-Ax:F}Mtr', name='VBMfocus')
VBMzoom = EpicsMotor('XF:16IDB-BI{FS:VBM-Ax:Zm}Mtr', name='VBMzoom')
aSSAx = EpicsMotor('XF:16IDB-OP{Slt:aSSA-Ax:X}Mtr', name='aSSAx')
aSSAdx = EpicsMotor('XF:16IDB-OP{Slt:aSSA-Ax:dX}Mtr', name='aSSAdx')
aSSAy = EpicsMotor('XF:16IDB-OP{Slt:aSSA-Ax:Y}Mtr', name='aSSAy')
aSSAdy = EpicsMotor('XF:16IDB-OP{Slt:aSSA-Ax:dY}Mtr', name='aSSAdy')
SFza = EpicsMotor('XF:16IDC-OP{CRL-Ax:Z}Mtr', name='SFza')
SFzv = EpicsMotor('XF:16IDC-OP{CRL-Ax:Z1}Mtr', name='SFzv')
HRM1y = EpicsMotor('XF:16IDC-OP{Mir:HRM1-Ax:Y}Mtr', name='HRM1y')
HRM1P = EpicsMotor('XF:16IDC-OP{Mir:HRM1-Ax:Th}Mtr', name='HRM1P')
CRLx1 = EpicsMotor('XF:16IDC-OP{CRL-Ax:UX}Mtr', name='CRLx1')
CRLy1 = EpicsMotor('XF:16IDC-OP{CRL-Ax:UY}Mtr', name='CRLy1')
CRLx2 = EpicsMotor('XF:16IDC-OP{CRL-Ax:DX}Mtr', name='CRLx2')
CRLx2 = EpicsMotor('XF:16IDC-OP{CRL-Ax:DY}Mtr', name='CRLx2')
HRM2y = EpicsMotor('XF:16IDC-OP{Mir:HRM2-Ax:Y}Mtr', name='HRM2y')
HRM2P = EpicsMotor('XF:16IDC-OP{Mir:HRM2-Ax:Th}Mtr', name='HRM2P')
HRM2B1 = EpicsMotor('XF:16IDC-OP{Mir:HRM2-Ax:BU}Mtr', name='HRM2B1')
HRM2B2 = EpicsMotor('XF:16IDC-OP{Mir:HRM2-Ax:BD}Mtr', name='HRM2B2')
DDAx = EpicsMotor('XF:16IDC-OP{Slt:DDA-Ax:X}Mtr', name='DDAx')
DDAy = EpicsMotor('XF:16IDC-OP{Slt:DDA-Ax:Y}Mtr', name='DDAy')
DDAdx = EpicsMotor('XF:16IDC-OP{Slt:DDA-Ax:dX}Mtr', name='DDAdx')
DDAdy = EpicsMotor('XF:16IDC-OP{Slt:DDA-Ax:dY}Mtr', name='DDAdy')
BIMy = EpicsMotor('XF:16IDC-BI{BPM:2-Ax:Y}Mtr', name='BIMy')
SG1x = EpicsMotor('XF:16IDC-OP{Slt:G1-Ax:X}Mtr', name='SG1x')
SG1dx = EpicsMotor('XF:16IDC-OP{Slt:G1-Ax:dX}Mtr', name='SG1dx')
SG1y = EpicsMotor('XF:16IDC-OP{Slt:G1-Ax:Y}Mtr', name='SG1y')
SG1dy = EpicsMotor('XF:16IDC-OP{Slt:G1-Ax:dY}Mtr', name='SG1dy')
SMcx = EpicsMotor('XF:16IDC-ES:InAir{Stg:ScanC-Ax:X}Mtr', name='SMcx')
SMcy = EpicsMotor('XF:16IDC-ES:InAir{Stg:ScanC-Ax:Y}Mtr', name='SMcy')
SMfx = EpicsMotor('XF:16IDC-ES:InAir{Stg:ScanF-Ax:X}Mtr', name='SMfx')
SMfy = EpicsMotor('XF:16IDC-ES:InAir{Stg:ScanF-Ax:Y}Mtr', name='SMfy')
SMr = EpicsMotor('XF:16IDC-ES:InAir{Stg:ScanF-Ax:Rot}Mtr', name='SMr')
SG2x = EpicsMotor('XF:16IDC-ES:InAir{Mscp:1-Ax:X}Mtr', name='SG2x')
SG2y = EpicsMotor('XF:16IDC-ES:InAir{Mscp:1-Ax:Y}Mtr', name='SG2y')
SMz = EpicsMotor('XF:16IDC-ES:InAir{Mscp:1-Ax:F}Mtr', name='SMz')
POLr = EpicsMotor('XF:16IDC-ES:InAir{Mscp:1-Ax:Pol }Mtr', name='POLr')
MSzoom = EpicsMotor('XF:16IDC-ES:InAir{Mscp:1-Ax:Zm}Mtr', name='MSzoom')
SG2dx = EpicsMotor('XF:16IDC-ES:GI{Slt:G2-Ax:X}Mtr', name='SG2dx')
SG2dy = EpicsMotor('XF:16IDC-ES:GI{Slt:G2-Ax:dX}Mtr', name='SG2dy')
WAXS1x = EpicsMotor('XF:16IDC-ES{Stg:WAXS1-Ax:X}Mtr', name='WAXS1x')
WAXS1y = EpicsMotor('XF:16IDC-ES{Stg:WAXS1-Ax:Y}Mtr', name='WAXS1y')
WAXS1z = EpicsMotor('XF:16IDC-ES{Stg:WAXS1-Ax:Z}Mtr', name='WAXS1z')
WAXS2x = EpicsMotor('XF:16IDC-ES{Stg:WAXS2-Ax:X}Mtr', name='WAXS2x')
WAXS2y = EpicsMotor('XF:16IDC-ES{Stg:WAXS2-Ax:Y}Mtr', name='WAXS2y')
WAXS2z = EpicsMotor('XF:16IDC-ES{Stg:WAXS2-Ax:Z}Mtr', name='WAXS2z')
wBSx = EpicsMotor('XF:16IDC-ES{BS:WAXS-Ax:X}Mtr', name='wBSx')
wBSy = EpicsMotor('XF:16IDC-ES{BS:WAXS-Ax:Y}Mtr', name='wBSy')
wBSr = EpicsMotor('XF:16IDC-ES{BS:WAXS-Ax:Z}Mtr', name='wBSr')
SAXSx = EpicsMotor('XF:16IDC-ES{Stg:SAXS-Ax:X}Mtr', name='SAXSx')
SAXSy = EpicsMotor('XF:16IDC-ES{Stg:SAXS-Ax:Y}Mtr', name='SAXSy')
SAXSz = EpicsMotor('XF:16IDC-ES{Stg:SAXS-Ax:Z}Mtr', name='SAXSz')
sBSx = EpicsMotor('XF:16IDC-ES{BS:SAXS-Ax:X}Mtr', name='sBSx')
sBSy = EpicsMotor('XF:16IDC-ES{BS:SAXS-Ax:Y}Mtr', name='sBSy')
sBS1s = EpicsMotor('XF:16IDC-ES{BS:SAXS-Ax:R1}Mtr', name='sBS1s')
sBS2s = EpicsMotor('XF:16IDC-ES{BS:SAXS-Ax:R2}Mtr', name='sBS2s')
sBS3s = EpicsMotor('XF:16IDC-ES{BS:SAXS-Ax:R3}Mtr', name='sBS3s')
sBSP = EpicsMotor('XF:16IDC-ES{BS:SAXS-Ax:T1}Mtr', name='sBSP')
sBSY = EpicsMotor('XF:16IDC-ES{BS:SAXS-Ax:T2}Mtr', name='sBSY')
