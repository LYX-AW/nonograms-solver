import numpy as np

def create_case(tips:list[int],positions:list[int],length:int):
    """根据某一行或某一列的数字提示新建一个case"""
    # 创建一个全是0的case，长度为length
    case=np.zeros(length)

    # 将数字提示与其位置一一对应，填色在case里
    for tip,position in zip(tips,positions):
        case[position:position+tip]=1

    return case

def single_enumerate(tips:list[int],length:int):
    """根据某一行或某一列的数字提示枚举出所有可能的情况"""
    # 先举出填色区域都靠近最左边的情况
    positions=[i+np.sum(tips[:i],dtype=np.int64) for i in range(len(tips))]
    case=create_case(tips,positions,length)
    cases=[case]
    
    # 开始枚举
    while True:
        sign=0
        # 先尝试挪动某片填色区域，从左往右试
        for i in range(len(positions)):
            # 检测该填色区域是否能往右挪动
            end_position=positions[i]+tips[i]
            if i==len(positions)-1:
                if end_position>length-1:
                    continue
            elif end_position+1>=positions[i+1]:
                continue

            # 能挪动就往右挪动一格
            positions[i]+=1

            # 同时前i-2片填色区域都挪到靠近最左边
            for j in range(len(positions[:i])):
                positions[j]=j+np.sum(tips[:j],dtype=np.int64)
                case=create_case(tips,positions,length)

            # 记录下这种情况
            case=create_case(tips,positions,length)
            cases.append(case)

            # 标示发生了挪动，并再从头开始试挪
            sign=1
            break
        # 如果试遍了没挪动一片填色区域，枚举就此结束
        if not sign:
            return cases

def find_intersection(cases:list):
    """在多种情况中求交集"""
    cases=np.array(cases)
    rows,cols=len(cases),len(cases[0])   # 获取行数和列数
    intersection=np.zeros(cols)
    for i in range(cols):
        sum_=np.sum(cases[:,i])
        match sum_:
            case x if x==rows:
                intersection[i] = 1 # 确定第i+1格一定填色
            case x if x==0:
                intersection[i] = -1 # 确定第i+1格一定不填色
    return intersection

def find_union(case_1,case_2):
    """求两种情况的并集"""
    union=[]
    for gird_1,grid_2 in zip(case_1,case_2):
        union.append(grid_2 if gird_1==0 else gird_1)
    return union

def condition_filter(cases:list,condition):
    """依据条件从多种情况中筛选"""
    filtered_cases=[]
    for case in cases:
        sign=0
        for grid,judgement in zip(case,condition):
            # 遇到一定要填色却没有填色或一定不填色却填了色的情况一律舍去
            if (judgement==-1 and grid==1) or (judgement==1 and grid==0):
                sign=1
                break
        
        # 符合条件的添加到列表
        if not sign:
            filtered_cases.append(case)
    
    return filtered_cases

def unfold_case(case):
    """折叠case"""
    new_case=[]
    num=0
    for index,grid in enumerate(case):
        if grid==1:
            num+=1
            if index+1==len(case):
                new_case.append(num)
        if grid!=1 and num!=0:
            new_case.append(num)
            num=0
    return new_case


if __name__=="__main__":
    """测试"""
    # tips=[1,1]
    # length=5
    # cases=single_enumerate(tips,length)
    # for case in cases:
    #     print(case)
    # filtered_cases=condition_filter(cases,[-1,0,1,0,0])
    # print('\n',filtered_cases[0])
    case=[-1,-1,-1,1,1,1,-1,1,1,1,1]
    print(unfold_case(case))