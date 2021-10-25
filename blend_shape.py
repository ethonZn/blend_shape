# -*- coding: utf-8 -*- 
# Fusion deformation link tool, by Zn 2021-10-14
'''先选模型再选控制器 '方向'_'位置'_'名称'
例如：眉毛 L_eb_sad 眼睛 L_eye_sad 口型 M_mouth_i'''
import maya.cmds as cmds
class BslinkClass():
    def __init__(self):
        self.window_id = 'BslinkWindow'
        if cmds.window (self.window_id, ex=True):
            cmds.deleteUI (self.window_id)    
        cmds.window (self.window_id, t='BslinkTool', h=75, w=150, sizeable=False, mxb= False, mnb=False)
        cmds.columnLayout (adj=True)   
        cmds.button (l='Associate', c='Bslink.BslinkDef()')                                            
    def show_win (self):
        cmds.showWindow (self.window_id)
        cmds.window (self.window_id, e=True, h=30, w=250)   
    def BslinkDef(self):
        bs_name,L_eb,R_eb,L_eye,R_eye,M_Mouth=[],[],[],[],[],[]#设置变量的列表为控制器名字   
        lisths=[L_eb,R_eb,L_eye,R_eye,M_Mouth]#设置变量名的列表
        for i in cmds.ls(sl=1):#吧选择的物理进行筛选
            for ai in ['L_eb','R_eb','L_eye','R_eye','M_Mouth']:
                if ai in i:#如果以上字符存在
                    eval(ai).append(i)#把字符串更改成变量后添加到变量的列表里 
        selblend= cmds.ls(sl=1)[0]#设置融合变形名称
        endv=len(cmds.listAnimatable(selblend))-2#搜索融合变形的属性_bs_name=cmds.blendShape(selblend,q=True,target=True)#返回融合变形的名称 必须不能删除原有融合变形，不能有重复名字
        for i in cmds.listAnimatable(selblend)[0:endv]:#切片保留有用的
            bs_name.append(i.split('.',1)[1])#添加融合变形名称到列表中
        for seqz,i in enumerate(['L_eb','R_eb','L_eye','R_eye','M_Mouth']):#开始判断链接控制器
            for n in bs_name:#返回融合变形名字
                if i in n:#如果定义的名字在融合变形里  
                    if lisths[seqz]:#并且选择的控制器为真
                        facename=n.split('_',2)[2]#提取表情名字   
                        cmds.addAttr(lisths[seqz][0],ln=facename,at='double',min=0,max=10,dv=0,k=True)#给相应的控制器添加属性                          
                        cmds.setDrivenKeyframe('%s.%s'%(selblend,n),dv=0,v=0,cd='%s.%s'%(lisths[seqz][0],facename))#驱动关键帧       
                        cmds.setDrivenKeyframe('%s.%s'%(selblend,n),dv=10,v=1,cd='%s.%s'%(lisths[seqz][0],facename))#驱动关键帧
                        cmds.warning('%s is OK'%('%s.%s'%(selblend,n)))#输出结果                      	        
Bslink = BslinkClass()
Bslink.show_win()