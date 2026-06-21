"""
Find-S
"""


def agree(h,e,elable):
    """
    d=<e,elable>
    样例d是否满足假设h
    e:样例的输入
    elable:样例标签(true/false)
    """
    ret=all([h[i]==e[i] or h[i]=='?' for i in range(len(h))])
    return ret if elable else not ret

def is_spacial_than(h1,h2,strict=False):
    if strict and h1==h2:return False
    return all([h1[i]==h2[i] or h2[i]=='?' for i in range(len(h1))])

def is_general_than(h1,h2,strict=False):
    if strict and h1==h2:return False
    return all([h1[i]==h2[i] or h1[i]=='?' for i in range(len(h1))])

def min_generalize(h,e):
    """
    极小一般化
    """
    if h==empty_h:
        return e.copy()
    else:
        return [h[i] if h[i] ==e[i] else '?' for i in range(len(h))]

def min_specialize(h):
    """
    极小特殊化
    """
    for i in range(len(h)):
        if h[i]=='?':
            for a in attributes[i]:
                new=h.copy()
                new[i]=a
                yield new

def generate_SG(examples):
    """
    生成极大特殊、一般边界:S,G
    """
    S,G=[empty_h],[full_h]

    i=0
    print('S%d:' % i,S)
    print('G%d' % i,G)

    for e in examples:
        if e[1]:
            #正例
            G=list(filter(lambda h:agree(h,e[0],e[1]),G))
            newS=[]
            for h in S:
                if agree(h,e[0],e[1]):
                    newS.append(h)
                else:
                    newS.extend(list(min_generalize(h,e[0])))
            S=list(filter(lambda hs:any([is_general_than(hg,hs,strict=True) for hg in G]),newS))
        else:
            #负例
            S=list(filter(lambda h:agree(h,e[0],e[1]),S))
            newG=[]
            for h in G:
                if agree(h,e[0],e[1]):
                    newG.append(h)
                else:
                    newG.extend(list(min_specialize(h)))
            newG=list(filter(lambda h:agree(h,e[0],e[1]),newG))
            G=list(filter(lambda hg:any([is_general_than(hg,hs,strict=True)for hs in S]),newG))
        i=i+1
        print('S%d:' % i,S)
        print('G%d:' % i,G)
    return S,G

def generate_VS(S,G):
    """
    生成除极大特殊、一般假设以外的所有和数据集保持一致的假设
    """
    VS=set()
    #VS.updata(['.'.join(h) for h in S])
    #VS.updata(['.'.join(h) for h in G])
    queue=[]
    queue.extend(G)
    while len(queue)>0:
        h=queue.pop()
        l=list(min_specialize(h))
        l=list(filter(lambda hg:any([is_general_than(hg,hs,strict=True)for hs in S]),l))
        VS.updata(['.'.join(h) for h in l])
        queue.extend(l)
    return [item.split('.') for item in VS]

def find_S(examples):
    h=empty_h
    for e in examples:
        if not e[1]:
            continue
        if agree(h,e[0],e[1]):
            continue
        h=min_generalize(h,e[0])
    return h

if __name__=="__main__":
    #train examples:
    examples=[
        [['Sunny','Warm','Normal','Strong','Warm','Same'],True],
        [['Sunny','Warm','High','Strong','Warm','Same'],True],
        [['Rainy','Cold','High','Strong','Warm','Change'],False],
        [['Sunny','Warm','High','Strong','Cool','Change'],True],
        #[['Sunny','Cold','Normal','Strong','Warm','Same'],False]
    ]

    #attributes and values:
    attributes=[
        ['Sunny','Rainy'],
        ['Warm','Cold'],
        ['Normal','High'],
        ['Strong','Light'],
        ['Warm','Cool'],
        ['Same','Change']
    ]
    #hypothesis:
    #['Sunny','?','?','Strong','Cool','?']

    #special hypothesises:
    empty_h=['$']*len(attributes)
    full_h=['?']*len(attributes)

    most_special_h=find_S(examples)
    print(most_special_h)
    
