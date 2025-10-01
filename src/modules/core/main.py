import numpy as np
from src.modules.core.base import *

class Nonograms:
    """数织"""
    def __init__(self,overall_tips=[],size=(5,5)):
        # 全局数字提示，大小，内容，全局情况
        self.overall_tips=overall_tips if overall_tips else [[] for _ in range(sum(size))]
        self.size=size
        self.content=np.zeros(size)
        self.overall_cases=self.overall_enumerate()
        # 数织状态，是否允许
        self.condition=0
        self.permission=1

    def overall_enumerate(self):
        """全局枚举"""
        new_overall_cases=[]
        for index,tips in enumerate(self.overall_tips):
            length=self.size[1] if index+1<=self.size[0] else self.size[0]     #index小于等于行数时长度为列数，大于行数时长度为行数
            new_overall_cases.append(single_enumerate(tips,length))
        return new_overall_cases
       
    def find_overall_intersection(self):
        """根据全局情况取交集更新内容"""
        overall_content=[find_intersection(cases) for cases in self.overall_cases]
        for index,case in enumerate(overall_content):
            if index+1<=self.size[0]:
                self.content[index]=find_union(self.content[index],case)
            else:
                self.content[:,index-self.size[0]]=find_union(self.content[:,index-self.size[0]],case)
            

    def overall_filter(self):
        """根据内容筛选全局情况"""
        overall_content=list(self.content)+list(self.content.T)
        new_overall_cases=[]
        for cases,condition in zip(self.overall_cases,overall_content):
            new_overall_cases.append(condition_filter(cases,condition))
        self.overall_cases=new_overall_cases

    def judge(self):
        """判断数织是否解开"""
        overall_content=list(self.content)+list(self.content.T)
        unfold_content=[unfold_case(case) for case in overall_content]
        return self.overall_tips==unfold_content
    
    def simply_solve(self):
        """简易版解数织"""
        while self.content:
            sign=0
            self.overall_filter()
            old_content=self.content
            self.find_overall_intersection()
            # 如果内容无变化退出循环
            if np.array_equal(old_content,self.content):
                break
        self.condition=1 if self.judge else -1
        

