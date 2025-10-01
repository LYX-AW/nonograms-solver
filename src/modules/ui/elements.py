import turtle as tt
import numpy as np
from src.modules.ui.shapes import *
from src.modules.core.main import *

def corner_position():
    """获取画布右上角的坐标"""
    # 获取画布的宽与高
    screen=tt.Screen()
    window_width=screen.window_width()
    window_height=screen.window_height()
    return [window_width//2,window_height//2]

class Element:
    """元件"""
    elements=[]
    def __init__(self,quadrant=1,spacing=[0,0]):
        # 所在象限，间距
        self.elements.append(self)
        self.quadrant=quadrant
        self.spacing=spacing
        # 位置，尺寸
        self.position:tuple[float,float]
        self.size:tuple[float,float]

    def update_position(self):
        """更新位置"""
        corner_x,corner_y=corner_position()
        spacing_x,spacing_y=self.spacing
        width,height=self.size
        match self.quadrant:
            case 1|2:
                y=corner_y-spacing_y
            case 3|4:
                y=-corner_y+spacing_y+height
        match self.quadrant:
            case 1|4:
                x=corner_x-spacing_x-width
            case 2|3:
                x=corner_x+spacing_x
        self.position=[x,y]
    def update_size(self):
        """更新尺寸"""
        self.size=self.size

    def load(self):
        """从无到有或者重新加载"""
        pass
    def update(self):
        """更新"""
        pass

class InteractiveElement(Element):
    """可交互的元件（比如按钮和选择框）"""
    int_elements=[]
    def __init__(self,quadrant=1,spacing=[0,0]):
        super().__init__(quadrant,spacing)
        self.int_elements.append(self)

    def onclick(self,x,y):
        """鼠标按下时执行的函数"""
        x_0,y_0=self.position
        width,height=self.size
        if not (x_0<=x<=x_0+width and y_0-height<=y<=y_0) :
            return False
        return True

class Table(InteractiveElement):
    """表格(包含数字提示框)"""
    def __init__(self,nonograms:Nonograms,grid_size:float,quadrant=2,spacing=[10,10]):
        super().__init__(quadrant,spacing)
        self.nonograms=nonograms
        self.grid_size=grid_size

        self.turtle_table=tt.Turtle(shape="blank")
        self.turtle_tips=tt.Turtle(shape='blank')
        self.turtle_content=tt.Turtle(shape='blank')

        self.turtle_table.penup()
        self.turtle_tips.penup()
        self.turtle_content.penup()
        self.turtle_content.pensize(bold)

    def update_size(self):
        """修改尺寸"""
        content_width,content_height=self.get_data('content_size')      # 内容的宽和高
        row_tips_length,col_tips_length=self.get_data('tips_width')    # 提示框的长
        # 宽和高
        width=content_width+row_tips_length
        height=content_height+col_tips_length

        self.size=[width,height]

    def load(self):
        """加载表格"""
        self.update_size()
        self.update_position()
        self.draw_table()
        self.draw_tips()
        self.update()
    def update(self):
        """更新内容"""
        self.draw_content()
        self.draw_condition()   
    def onclick(self, x, y):
        """鼠标点击触发事件"""
        if not(super().onclick(x,y)):return None
        # 处理数字提示
        tips_box_position=self._judge_which_tips_box(x,y)
        self.change_tips(tips_box_position)
        # 处理内容
        grid_position=self._judge_which_grid(x,y)
        self.change_content(grid_position)

    def get_data(self,name:str):
        """获取数据"""
        rows,cols=self.nonograms.size   # 行数 列数
        match name:
            case 'content_size':
                return self.grid_size*cols,self.grid_size*rows
            case 'tips_width':
                row_tips_length=len(max(self.nonograms.overall_tips[:rows],key=len))*self.grid_size  # 行提示框的长
                col_tips_width=len(max(self.nonograms.overall_tips[rows:],key=len))*self.grid_size   # 列提示框的长
                if row_tips_length<self.grid_size*2:
                    row_tips_length=self.grid_size*2
                if col_tips_width==0:
                    col_tips_width=self.grid_size
                return row_tips_length,col_tips_width

    def draw_content(self):
        """填色"""
        x_0,y_0=self.position   # 表格的位置
        rows,cols=self.nonograms.size   # 行数 列数        
        row_tips_length,col_tips_width=self.get_data('tips_width')    # 提示框的长
        # 表格内容的位置
        x_0+=row_tips_length
        y_0-=col_tips_width
        self.turtle_content.clear()
        for i,row in enumerate(self.nonograms.content):
            for j,grid in enumerate(row):
                if grid==0: continue
                grid_x=x_0+j*self.grid_size
                grid_y=y_0-i*self.grid_size
                self.turtle_content.setposition(grid_x,grid_y)
                if grid==1:
                    self.turtle_content.pencolor('black')
                    filled_grid(self.turtle_content,self.grid_size)
                elif grid==-1:
                    self.turtle_content.pencolor('red')
                    cross(self.turtle_content,self.grid_size)
    def draw_table(self):
        """画出表格"""
        rows,cols=self.nonograms.size   # 行数 列数        

        content_width,content_height=self.get_data('content_size')      # 内容的宽和高
        row_tips_length,col_tips_width=self.get_data('tips_width')    # 提示框的长

        x_0,y_0=self.position

        # 画出行
        self.turtle_table.setheading(0)
        self.turtle_table.color('black')
        self.turtle_table.clear()
        for i in range(rows+1):
            # 每隔五行或到最后一行加粗线条
            pensize=bold if i%5==0 or i==rows else light   
            self.turtle_table.pensize(pensize)
            line(self.turtle_table,[x_0,y_0-col_tips_width-i*self.grid_size],row_tips_length+content_width)
        # 画出列
        self.turtle_table.setheading(-90)
        for i in range(cols+1):
            pensize=bold if i%5==0 or i==cols else light   
            self.turtle_table.pensize(pensize)
            line(self.turtle_table,[x_0+row_tips_length+i*self.grid_size,y_0],col_tips_width+content_height)
        # 最后封上
        self.turtle_table.pensize(bold)
        self.turtle_table.setheading(-90)
        line(self.turtle_table,[x_0,y_0],content_height+col_tips_width)
        self.turtle_table.setheading(0)
        line(self.turtle_table,[x_0,y_0],content_width+row_tips_length)
        # 标明数织规格
        self.turtle_table.setposition(x_0+row_tips_length/2,y_0-col_tips_width/2-24*scale)
        self.turtle_table.write(f'{rows}×{cols}',align='center',font=(font,int(self.grid_size*scale*0.8)))   
    def draw_tips(self):
        """写出数字提示"""
        rows,cols=self.nonograms.size   # 行数 列数     
        x_0,y_0=self.position
        row_tips_length,col_tips_width=self.get_data('tips_width')    # 提示框的长


        # 行数字提示
        x_1=x_0+row_tips_length-self.grid_size/2
        y_1=y_0-col_tips_width-self.grid_size/2-self.grid_size*scale
        self.turtle_tips.clear()
        for i,tips in enumerate(self.nonograms.overall_tips[:rows]):
            y_2=y_1-i*self.grid_size
            for j,num in enumerate(tips[::-1]):
                x_2=x_1-j*self.grid_size
                self.turtle_tips.setposition(x_2,y_2)
                self.turtle_tips.write(arg=num,align='center',font=(font,int(self.grid_size*scale)))
        # 列数字提示
        x_1=x_0+row_tips_length+self.grid_size/2
        y_1=y_0-col_tips_width+self.grid_size/2-self.grid_size*scale
        for i,tips in enumerate(self.nonograms.overall_tips[rows:]):
            x_2=x_1+i*self.grid_size
            for j,num in enumerate(tips[::-1]):
                y_2=y_1+j*self.grid_size
                self.turtle_tips.setposition(x_2,y_2)
                self.turtle_tips.write(arg=num,align='center',font=(font,int(self.grid_size*scale)))
    def draw_condition(self):
        """描绘数织状态"""
        x_0,y_0=self.position
        width,height=self.size
        match self.nonograms.condition:
            case 0:
                return None
            case 1:
                color='green'
            case -1:
                color='red'
        self.turtle_table.pensize(bold*2)
        self.turtle_table.color(color)
        rect(self.turtle_table,[x_0,y_0],[width,height])

    def change_tips(self,tips_box_position:int):
        """更改数字提示"""
        rows=self.nonograms.size[0]
        if tips_box_position>=0:
            num=f'[{tips_box_position+1}]行' if tips_box_position<rows else f'[{tips_box_position-rows+1}]列'
            input_=tt.textinput(title=f'修改第{num}的数字提示',prompt='数字之间用逗号隔开，例如：1,2,3')
            if input_:
                new_tips=list(map(int, input_.split(',')))
                self.nonograms.overall_tips[tips_box_position]=new_tips
                self.load()
        elif tips_box_position==-1:
            input_=tt.textinput(title='修改规格',prompt='输入两个数字，数字之间用*隔开，例如：5*5')
            if input_:
                new_size=list(map(int, input_.split('*')))
                self.nonograms.__init__(size=new_size)
                self.load()
    def change_content(self,grid_position):
        """更改内容"""
        if grid_position:
            grid_row,grid_col=grid_position
            grid=self.nonograms.content[grid_row,grid_col]
            if grid==0:
                # 填色
                self.nonograms.content[grid_row,grid_col]=1
            elif grid==1:
                # 标记
                self.nonograms.content[grid_row,grid_col]=-1
            elif grid==-1:
                # 清空
                self.nonograms.content[grid_row,grid_col]=0
            self.draw_content()

    def _judge_which_tips_box(self,x,y):
        """判断一个坐标落在哪个提示框内"""
        x_0,y_0=self.position   #表格的位置
        rows,cols=self.nonograms.size   # 行数 列数        
        row_tips_length,col_tips_width=self.get_data('tips_width')    # 提示框的长

        if x_0<=x<=x_0+row_tips_length and y_0-col_tips_width-self.grid_size*rows<=y<=y_0:
            if y_0-col_tips_width<=y<=y_0:
                return -1   #落在规格框里
            for i in range(rows):
                y_max=y_0-col_tips_width-i*self.grid_size
                y_min=y_max-self.grid_size
                if y_min<=y<=y_max:
                    return i
        elif y_0-col_tips_width<=y<=y_0 and x_0+row_tips_length<=x<=x_0+row_tips_length+self.grid_size*cols:
            for i in range(cols):
                x_min=x_0+row_tips_length+i*self.grid_size
                x_max=x_min+self.grid_size
                if x_min<=x<=x_max:
                    return rows+i
        return -2
    def _judge_which_grid(self,x,y):
        """判断一个坐标落在哪个格子里"""
        x_0,y_0=self.position   # 表格的位置
        rows,cols=self.nonograms.size   # 行数 列数        
        row_tips_length,col_tips_width=self.get_data('tips_width')    # 提示框的长
        # 表格内容的位置
        x_0+=row_tips_length
        y_0-=col_tips_width
        if not (x_0<=x<=x_0+self.grid_size*cols and y_0-self.grid_size*rows<=y_0):
            # 不落在内容范围内的直接返回-1
            return None
        for i in range(rows):
            if not(y_0-(i+1)*self.grid_size<=y<=y_0-i*self.grid_size):
                # 不落在第i+1行范围内的直接continue
                continue
            for j in range(cols):
                if x_0+j*self.grid_size<=x<x_0+(j+1)*self.grid_size:
                    return i,j

class TextBox(Element):
    def __init__(self, text:str,variable=True,box=True,setup_width=100,grid_size=40,align='left',quadrant=4, spacing=[10, 10]):
        super().__init__(quadrant, spacing)
        self.text=text
        self.variable=variable
        self.setup_width=setup_width
        self.grid_size=grid_size
        self.box=box
        self.align=align

        self.turtle_text=tt.Turtle(shape='blank')
        self.turtle_box=tt.Turtle(shape='blank')

        self.turtle_text.penup()
        self.turtle_box.penup()
        self.turtle_box.pensize(bold)

    def update_size(self):
        strings=self.text.split('\n')
        if self.variable:
            width=self.grid_size*len(max(strings,key=len))*0.75
        else:
            width=self.setup_width
        height=self.grid_size*len(strings)*0.75
        self.size=[width,height]
    def load(self):
        self.update_size()
        self.update_position()
        if not(self.variable):
            self.draw_box()
    def update(self):
        if self.variable:
            self.load()
            self.draw_text()
            self.draw_box()
        else:
            self.draw_text()

    def draw_box(self):
        """画框"""
        if not(self.box):
            return None
        if self.variable:
            width=self.turtle_text.position()[0]-self.position[0]
            height=self.size[1]
            self.turtle_box.clear()
            rect(self.turtle_box,self.turtle_text.position(),[-width,-height])
        else:
            self.turtle_box.clear()
            rect(self.turtle_box,self.position,self.size)
    
    def draw_text(self):
        """显示文字"""
        x_0,y_0=self.position
        self.turtle_text.clear()
        strings=self.text
        x_1=x_0+self.size[0]/2 if self.align=='center' else x_0
        y_1=y_0-self.size[1]
                    
        self.turtle_text.setposition(x_1,y_1)
        self.turtle_text.write(strings,move=True,align=self.align,font=(font,int(self.grid_size*scale),'normal'))


class Button(InteractiveElement):
    """按钮""" 
    styles={
        'play or pause':('⏯',False),
        'stop':('⏹',False),
        'plus':('＋',True),
        'sub':('－',True)
    }
    def __init__(self, fun,style='play or pause',grid_size=30,quadrant=1, spacing=[0, 0]):
        super().__init__(quadrant, spacing)
        self.fun=fun
        self.style=self.styles[style]
        self.size=(grid_size,grid_size)
        self.text_box=TextBox(
            text=self.style[0],
            variable=False,
            box=self.style[1],
            setup_width=grid_size*0.75,
            grid_size=grid_size,
            quadrant=quadrant,
            spacing=spacing,
            align='center'
        )
    def load(self):
        self.update_position()
        self.text_box.load()
    def update(self):
        self.text_box.update()
    def onclick(self, x, y):
        if not(super().onclick(x,y)):return None
        self.fun(x,y)

class AdjustStrip(InteractiveElement):
    """调节条"""
    def __init__(self, variable_name:str,main_fun,sub_fun,plus_fun,
                 size=30,width=120,quadrant=1, spacing=[0, 0]):
        super().__init__(quadrant, spacing)
        self.button_sub=Button(
            fun=sub_fun,
            style='sub',
            grid_size=size,
            quadrant=quadrant,
            spacing=spacing
        )
        spacing_2=[spacing[0]+size*0.75,spacing[1]]
        self.text_box=TextBox(
            text=eval(variable_name),
            variable=True,
            box=True,
            setup_width=width,
            grid_size=size,
            align='center',
            quadrant=quadrant,
            spacing=spacing_2,
        )
        

if __name__=='__main__':
    tt.tracer(0)
    # tips=[
    #     [2],
    #     [1,2],
    #     [2],
    #     [3,1],
    #     [2],
    #     [4],
    #     [3],
    #     [1],
    #     [2],
    #     [2,1]
    #     ]
    # size=(5,5)
    # nonograms=Nonograms(tips,size)
    # table=Table(nonograms,20)
    # table.load()
    # table.update()
    # tt.onscreenclick(table.onclick)
    # tt.listen()
    a=TextBox('+-')
    a.load()
    a.update()
    tt.listen()
    tt.mainloop()
    