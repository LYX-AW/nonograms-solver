import turtle as tt

bold=2    
light=1
font='arial'
scale=0.5

def line(turtle:tt.Turtle,position:tuple[float,float],length:float):
    """一条直线"""
    turtle.penup()
    turtle.setposition(position)
    turtle.pendown()
    turtle.forward(length)   
    turtle.penup()

def rect(turtle:tt.Turtle,position:tuple[float,float],size:tuple[float,float]):
    """一个矩形"""
    width,height=size
    turtle.penup()
    turtle.setposition(position)
    turtle.pendown()
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(height)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(height)
    turtle.penup()
    turtle.right(90)


def filled_grid(turtle:tt.Turtle,size:float):
    """已填色的格子"""
    # 画边框
    x_0,y_0=turtle.position()
    turtle.penup()
    turtle.setposition(x_0,y_0)
    turtle.pendown()
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)  
    turtle.penup()

    real_size=size*0.8
    x_0+=(size-real_size)/2
    y_0-=(size-real_size)/2
    turtle.setposition(x_0,y_0)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(real_size)
        turtle.right(90)
    turtle.end_fill()

def cross(turtle:tt.Turtle,size:float):
    scale=0.5
    real_size=size*scale
    x_0,y_0=turtle.position()
    x_0+=(size-real_size)/2
    y_0-=(size-real_size)/2
    turtle.penup()
    turtle.setposition(x_0,y_0)
    turtle.pensize(bold)
    turtle.pendown()
    turtle.setposition(x_0+real_size,y_0-real_size)
    turtle.penup()
    turtle.setposition(x_0+real_size,y_0)
    turtle.pendown()
    turtle.setposition(x_0,y_0-real_size)
    turtle.penup()

