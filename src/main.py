from modules.ui.elements import *
tips=[
        [2],
        [1,2],
        [2],
        [3,1],
        [2],
        [4],
        [3],
        [1],
        [2],
        [2,1]
        ]
size=(5,5)
nonograms=Nonograms(tips,size)
table=Table(nonograms,30,(-20,50))
table.draw_table()
tt.mainloop()