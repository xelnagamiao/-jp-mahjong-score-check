import time
start=time.time()

def majongdata(data):
    # 建立字牌匹配集
    savewordclass={"东", "南", "西", "北","发","白","中"}
    # 建立暂存不同牌组的字符串
    saves = ""
    savem = ""
    savep = ""
    # 输出值
    savenumber = ""
    saveword = ""
    for i in data:
        # 数字进入savenumber暂存字符串 字牌进入saveword暂存字符串
        if i.isdigit():
            savenumber+=i
        elif i in savewordclass:
            saveword+=i
        # 当遇到牌组标签s m p 时,将暂存的数据放入对应的标签集中
        elif i == "s":
            saves += savenumber
            savenumber= ""
        elif i == "m":
            savem += savenumber
            savenumber= ""
        elif i == "p":
            savep += savenumber
            savenumber = ""
        # 出现不匹配的值进行报错并且跳出
        else:
            print(f"请勿输入超出数字,字母's','m','p'以及东南西北白发中以外的字符")
            break
        # 获得 saves,savem,savep,saveword 下一步进行合并
    mjsave=Paizu()
    # 将四个集合中的数据存储于牌组mjsave中
    for i in saves:
        mjsave.append(Pai(int(i)+10))
    for i in savem:
        mjsave.append(Pai(int(i)+20))
    for i in savep:
        mjsave.append(Pai(int(i)+30))
    for char in saveword:
        match char:
            case "东":
                mjsave.append(Pai(41))
            case "南":
                mjsave.append(Pai(44))
            case "西":
                mjsave.append(Pai(47))
            case "北":
                mjsave.append(Pai(50))
            case "白":
                mjsave.append(Pai(53))
            case "发":
                mjsave.append(Pai(56))
            case "中":
                mjsave.append(Pai(59))
    return mjsave # 返回牌组mjsave
class Pai(int):
    def __init__(self, value):
        super().__init__()
        self.partner_group = 0
        self.samenr = 0
        self.highernr = 0
        self.smallernr = 0
        self.intnr = int(value)
        self.sign = False
    def reset(self):
        self.partner_group = 0
        self.samenr = 0
        self.highernr = 0
        self.smallernr = 0
        self.sign = False
class Paizu(list):
    def __init__(self, pais=None):
        super().__init__()
        if pais is None:
            pais = []
        self.extend(pais) # 继承list方法
        self.roundnr = 0 # 代表向听数
        self.duizi = 0 # 代表对子数
        self.dazi = 0 # 代表搭子数
        self.kezi = 0 # 代表刻子数
        self.dazicheck = False # 代表是否还可以产生搭子
        self.kezicheck = False # 代表是否还可以产生刻子
        self.duizicheck = False # 代表是否还可以产生对子
        self.combinations = [] # 存储牌组中已经成型的组合 其中d代表对 k代表刻 s代表顺 d12 代表在2索位置有一个对子
        self.combinations_MP = []
    def inherit(self,paizulist):
        self.roundnr = paizulist.roundnr # 继承向听数
        self.duizi = paizulist.duizi # 继承对子数
        self.dazi = paizulist.dazi # 继承搭子数
        self.kezi = paizulist.kezi # 继承刻子数
        self.combinations.extend(paizulist.combinations) # 继承牌组
        self.combinations_MP.extend(paizulist.combinations_MP)
    def check(self): # paizu中的check方法用以重置pai的属性
        nrlist = [item.intnr for item in self] # 生成一个数字列表供后续比对
        for i in self:
            i.reset() # 重置属性
            # 如果有更高,更低,相同的牌,则统计
            if i.intnr + 1 in nrlist:
                i.highernr = nrlist.count(i + 1)
            if i.intnr - 1 in nrlist:
                i.smallernr = nrlist.count(i - 1)
            if i.intnr in nrlist:
                i.samenr = nrlist.count(i) - 1 # 统计相同的牌时-1去掉自身
            # 高低牌选择更少的一边计算伙伴组合
            if i.highernr >= i.smallernr:
                i.partner_group = i.smallernr
            else:
                i.partner_group = i.highernr
            # 判断牌组是否已经达成了构成duizi,dazi和kezi的条件,并在牌组中记录
            if i.samenr >= 1:
                self.duizicheck = True
            if i.samenr >= 2:
                self.kezicheck = True
            if i.partner_group >= 1:
                self.dazicheck = True
def duizicheck(duizilist):
    outputlist = []
    while True: # 执行循环直到 break
        signnr = 2 # 控制标记牌数的变量 对子为2
        mjlist = Paizu()
        mjlist.inherit(duizilist) # 继承牌组属性
        for i in duizilist:
            # 如果有一张相同的牌 并且signnr大于1 没有被其他牌组使用过
            if i.samenr >= 1 and signnr >= 1 and i.sign == False:
                i.sign = True
                signnr -= 1
                if signnr == 0: # 如果标记牌数归零
                    mjlist.duizi += 1 # 对子数+1
                    mjlist.roundnr += 2  # 向听数+2
                    mjlist.combinations.append(f"d{i}") # 添加牌组标记
                    # 判断组2 用以改变周边牌类的标记
                    if i.samenr >=3: # 如果有三张一样的牌,可能会有产生2个对子的可能,以下循环完成全部标记
                        for item in duizilist:
                            if item.intnr == i.intnr:
                                item.sign = True
            else: # 如果没有被标记则存储
                mjlist.append(i)
        # 存储mjlist 如果标记牌数没有归零 说明没有更多的对子组合 结束while循环
        outputlist.append(mjlist)
        if signnr == 2:
            return outputlist
def kezicheck(kezilist):
    outputlist = []
    while True:
        mjlist=Paizu()
        mjlist.inherit(kezilist) # 同步牌组属性
        signnr = 3  # 控制标记牌数的变量 刻子为3
        for i in kezilist:
            # 判断一张牌是否构成刻子可能,并且将该牌进行标记
            if i.samenr >= 2 and signnr >= 1 and i.sign == False: # 如果breaknr尚未被清空 且done未被标记
                i.sign = True
                signnr -= 1
                if signnr == 0:
                    mjlist.kezi += 1  # 刻子数+1
                    mjlist.roundnr += 3  # 向听数+3
                    mjlist.combinations.append(f"k{i}")  # 添加牌组标记
                    # 判断组2 用以改变周边牌类的标记
                    for item in kezilist:
                        if item.intnr == i.intnr:
                            item.sign = True
            # 操作组 将未被标记的牌组进行添加
            else:
                mjlist.append(i)
        if signnr == 3:
            return outputlist
        outputlist.append(mjlist)
def dazicheck(dazilist):
    outputlist = []
    while True:
        mjlist=Paizu()
        mjlist.inherit(dazilist)
        signnr = 3
        samenr = 0
        for i in dazilist:
            # 判断一张牌是否构成搭子可能,并且将该牌进行标记
            if i.partner_group >= 1 and signnr == 3 and i.sign == False:
                mjlist.dazi += 1
                mjlist.roundnr += 3
                mjlist.combinations.append(f"s{i}")
                samenr = i.intnr
                for item in dazilist:
                    if item.intnr == samenr:
                        item.sign = True
                break
        for item in dazilist:
            if item.intnr == samenr - 1 and signnr == 3:
                signnr -= 1
            elif item.intnr == samenr and signnr == 2:
                signnr -= 1
            elif item.intnr == samenr + 1 and signnr == 1:
                signnr -= 1
            else:
                mjlist.append(item)
        if signnr == 3:
            return outputlist
        outputlist.append(mjlist)

# 初始化变量
alllist = []
savelist = []
endlist = []
maxroundnr = 0
r = 0
majonglist=[]

# 引入数据
#inputdata = majongdata("12233444456789s")
inputdata = majongdata("23444456789s")
inputMPdata1 = majongdata("123s")

# 副露处理
def MPcheck(mplist):
    MPlist = []
    savelist = []
    MPlistoutput = []
    MPlist.append(mplist)
    while MPlist:
        for i in MPlist:
            i.check() # 自检
            if i.kezicheck == True and i.dazicheck == False:  # 如果一个牌可以构成刻子
                savelist.extend(kezicheck(i)) # 进行刻子运算
            elif i.dazicheck == True and i.kezicheck == False:
                savelist.extend(dazicheck(i)) # 进行搭子运算
            elif i.dazicheck == False and i.kezicheck == False:
                MPlistoutput.append(i)
        MPlist = savelist
        savelist = []
    for i in MPlistoutput:
        inputdata.roundnr = i.roundnr # 继承向听数
        inputdata.duizi = i.duizi # 继承对子数
        inputdata.dazi = i.dazi # 继承搭子数
        inputdata.kezi = i.kezi # 继承刻子数
        inputdata.combinations_MP.extend(i.combinations) # 继承牌组
        for item in i:
            print("检测到副露输入中包含未成搭，刻")
            break
MPcheck(inputMPdata1)

# 对子处理
inputdata.check()
print("原始牌组",inputdata)
alllist.extend(duizicheck(inputdata))
print("以下是几种雀头可能",alllist)

# 十三幺与七对子遍历
def GScheck(yaojiulist):
    yaojiu = {11, 19, 21, 29, 31, 39, 41, 44, 47, 50, 53, 56, 59}
    mjlist = Paizu()
    samenr = 0
    keynr = 0
    for i in yaojiulist:
        if i.intnr in yaojiu and samenr != i.intnr or keynr == 0:
            if i.samenr != i.intnr:
                keynr += 1
            samenr = i.intnr
            mjlist.roundnr += 1
        else:
            mjlist.append(i)
    if mjlist.roundnr == 14:
        mjlist.combinations.append("y13")
    else:
        mjlist.combinations.append("?y13")
    alllist.append(mjlist)
    print("十三幺遍历：向听数为",14-mjlist.roundnr,"包含的牌组包括",mjlist.combinations,"剩余的牌包括",mjlist)
def QDcheck(duizilist):
    savelist = duizilist
    savelist.check()
    while True :
        signnr = 2
        mjlist = Paizu()
        mjlist.inherit(savelist) # 继承牌组属性
        for i in savelist:
            # 如果有一张相同的牌 并且signnr大于1 没有被其他牌组使用过
            if i.samenr >= 1 and signnr >= 1 and i.sign == False:
                i.sign = True
                signnr -= 1
                if signnr == 0:  # 如果标记牌数归零
                    mjlist.duizi += 1  # 对子数+1
                    mjlist.roundnr += 2  # 向听数+2
                    if (f"d{i}") in mjlist.combinations:
                        mjlist.append(i)
                        mjlist.append(i)
                        mjlist.duizi -= 1
                        mjlist.roundnr -= 2
                        signnr = 2
                    else:
                        mjlist.combinations.append(f"d{i}")  # 添加牌组标记
                    # 判断组2 用以改变周边牌类的标记
                    if i.samenr >= 3:  # 如果有三张一样的牌,可能会有产生2个对子的可能,以下循环完成全部标记
                        for item in duizilist:
                            if item.intnr == i.intnr:
                                item.sign = True
            else:  # 如果没有被标记则存储
                mjlist.append(i)
            # 存储mjlist 如果标记牌数没有归零 说明没有更多的对子组合 结束while循环
        savelist = mjlist
        savelist.check()
        if signnr == 2:
            alllist.append(savelist)
            print("七对子遍历：向听数为",14-mjlist.roundnr,"包含的牌组包括",mjlist.combinations,"剩余的牌包括",mjlist)
            break
QDcheck(inputdata)
GScheck(inputdata)

# 一般型遍历
while alllist:
    residue_paizu = 0 # 监控savelist中一共有多少牌组
    endlist_paizu = 0
    for i in alllist:
        i.check() # 自检
        if i.kezicheck == True and i.dazicheck == True:  # 如果一个牌组又可以构成搭子又可以构成刻子
            savelist.extend(kezicheck(i)) # 进行刻子运算
            savelist.extend(dazicheck(i)) # 进行搭子运算
            residue_paizu += 2
        elif i.kezicheck == True and i.dazicheck == False:  # 如果一个牌可以构成刻子
            savelist.extend(kezicheck(i)) # 进行刻子运算
            residue_paizu += 1
        elif i.dazicheck == True and i.kezicheck == False:
            savelist.extend(dazicheck(i)) # 进行搭子运算
            residue_paizu += 1
        elif i.dazicheck == False and i.kezicheck == False:
            endlist.append(i)
            endlist_paizu += 1
    alllist = savelist
    savelist = []
    r += 1
    print(f"第{r}轮遍历剩余牌组还有", residue_paizu)
    print("完成牌组总共", endlist_paizu)

# 保留向听最近牌组
for i in endlist:
    if i.roundnr >= maxroundnr :
         maxroundnr = i.roundnr
for i in endlist:
    if i.roundnr == maxroundnr :
        majonglist.append(i)
        i.roundnr = 14-i.roundnr
for i in majonglist:
    print("最低向听数为",i.roundnr,"包含的牌组包括",i.combinations,"副露牌组包括",i.combinations_MP,"剩余的牌包括",i)

# 计算符数
def fu_count(fulist):
    keziset={}

# 计算役数
def yi_count(yilist):
    duanyaoset={"d12","d13","d14","d15","d16","d17","d18",
                "d22","d23","d24","d25","d26","d27","d28",
                "d32","d33","d34","d35","d36","d37","d38",
                "s13","s14","s15","s16","s17",
                "s23","s24","s25","s26","s27"
                "k12", "k13", "k14", "k15", "k16", "k17", "k18",
                "k22", "k23", "k24", "k25", "k26", "k27", "k28",
                "k32", "k33", "k34", "k35", "k36", "k37", "k38",}

    chunquanset={"s12","s18","s22","s28","s32","s38"
                 "d11","d19","d21","d29","d31","d39"
                 "k11","k19","k21","k29","k31","k39"}

    hunquanset={"s12","s18","s22","s28","s32","s38"
                "d11","d19","d21","d29","d31","d39"
                "k11","k19","k21","k29","k31","k39"
                "d41","d44","d47","d50","d53","d56","d59"
                "k41","k44","k47","k50","k53","k56","k59"}

# 计算


# 显示用时

print("用时",time.time()-start,"s")