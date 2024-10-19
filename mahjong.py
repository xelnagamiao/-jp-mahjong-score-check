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
            savenumber += i
        elif i in savewordclass:
            saveword += i
        # 当遇到牌组标签s m p 时,将暂存的数据放入对应的标签集中
        elif i == "s":
            saves += savenumber
            savenumber = ""
        elif i == "m":
            savem += savenumber
            savenumber = ""
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
        mjsave.append(int(i)+10)
    for i in savem:
        mjsave.append(int(i)+20)
    for i in savep:
        mjsave.append(int(i)+30)
    for char in saveword:
        match char:
            case "东":
                mjsave.append(41)
            case "南":
                mjsave.append(44)
            case "西":
                mjsave.append(47)
            case "北":
                mjsave.append(50)
            case "白":
                mjsave.append(53)
            case "发":
                mjsave.append(56)
            case "中":
                mjsave.append(59)
    mjsave = sorted(mjsave)
    mjsavelist = Paizu()
    for i in mjsave:
        mjsavelist.append(Pai(i))
    return mjsavelist # 返回牌组mjsavelist
class Pai(int):

    def __init__(self, value):
        super().__init__()
        self.partner_group = 0 # 拥有±1两张伙伴牌,可以以自身为中心组成顺子的数量的标记
        self.samenr = 0 # 相同牌标记
        self.highernr = 0 # 比自己更高的牌的标记
        self.smallernr = 0 # 比自己更小的牌的标记
        self.intnr = int(value) # Pai类的整数值
        self.sign = False # 用以在duizicheck、dazicheck与kezicheck中标识自身是否被使用过

    def reset(self): # reset方法用以在paizu.check中重置pai类的属性
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
        self.combinations = [] # 存储牌组中已经成型的组合 其中d代表对 k代表刻 s代表顺 例如 d12则代表在2索位置有一个对子
        self.combinations_MP = [] # 存储牌组中副露的组合
        self.duizicheck_ = False # 出现了产生多个对子的七对检测进入主牌组遍历，造成出现4个对子2个顺子的结果的bug,
        # 该数值为True则代表该牌组包含2个以上的对子，不再参与主牌组遍历的过程
        self.combinations_count = [] # 在计分环节存储牌型番
        self.point_count = 0 # 在计分环节存储番数
    def inherit(self,paizulist): # inherit方法用以在牌组进行多次check对牌组进行归纳的过程中继承先前牌组的属性
        self.roundnr = paizulist.roundnr # 继承向听数
        self.duizi = paizulist.duizi # 继承对子数
        self.dazi = paizulist.dazi # 继承搭子数
        self.kezi = paizulist.kezi # 继承刻子数
        self.combinations.extend(paizulist.combinations) # 继承牌组
        self.combinations_MP.extend(paizulist.combinations_MP) # 继承副露牌组
        self.duizicheck_ = paizulist.duizicheck_

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
class Mjobject():
    def __init__(self):
        hand = ""
        inputMPdata1 = ""
        inputMPdata2 = ""
        inputMPdata3 = ""
        inputMPdata4 = ""
        way_to_hepai = []
        dora_num = ""
        deep_dora_num = ""
        position_select = ""
        public_position_select = ""
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
                    if i.samenr >=2: # 如果有三张一样的牌,可能会有产生2个对子的可能,以下循环完成全部标记
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
            # 判断牌组是否被标记，或是否是被标记牌的相邻牌，如不是则存储
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
        inputdata.roundnr += i.roundnr # 继承向听数
        inputdata.duizi += i.duizi # 继承对子数
        inputdata.dazi += i.dazi # 继承搭子数
        inputdata.kezi += i.kezi # 继承刻子数
        inputdata.combinations_MP.extend(i.combinations) # 继承牌组
        for item in i:
            print("检测到副露输入中包含未成搭，刻")
            break
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
            if savelist.roundnr > 2:
                savelist.duizicheck_ = True
            alllist.append(savelist)
            print("七对子遍历：向听数为",14-mjlist.roundnr,"包含的牌组包括",mjlist.combinations,"剩余的牌包括",mjlist)
            break
def handCheck(alllist):
    endlist = []
    while alllist:
        savelist = []
        r = 0
        residue_paizu = 0 # 监控savelist中一共有多少牌组
        endlist_paizu = 0
        for i in alllist:
            i.check() # 自检
            if i.duizicheck_ is not True:
                if i.kezicheck == True and i.dazicheck == True:  # 如果一个牌组又可以构成搭子又可以构成刻子
                    savelist.extend(dazicheck(i)) # 进行搭子运算
                    savelist.extend(kezicheck(i)) # 进行刻子运算 !如先进行刻子运算会导致 i(Pai).sign 未还原
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
    return endlist
def resultFilter(endlist):
    maxroundnr = 0
    mjlist = []
    for i in endlist:
        if i.roundnr >= maxroundnr :
             maxroundnr = i.roundnr
    for i in endlist:
        if i.roundnr == maxroundnr :
            mjlist.append(i)
            i.roundnr = 14-i.roundnr
    for i in mjlist:
        print("最低向听数为",i.roundnr,"包含的牌组包括",i.combinations,"副露牌组包括",i.combinations_MP,"剩余的牌包括",i)
    return mjlist
def distinctMjlist(mahjonglist):
    mjlist = []
    all_combinations = []
    all_combinations_list = []
    for i in mahjonglist:
        all_combinations = sorted(i.combinations + i.combinations_MP)
        if all_combinations not in all_combinations_list :
            mjlist.append(i)
            all_combinations_list.append(all_combinations)
            print(all_combinations)
    return mjlist

"""
duanyaoset={"d12","d13","d14","d15","d16","d17","d18",
            "d22","d23","d24","d25","d26","d27","d28",
            "d32","d33","d34","d35","d36","d37","d38",
            "s13","s14","s15","s16","s17",
            "s23","s24","s25","s26","s27",
            "k12", "k13", "k14", "k15", "k16", "k17", "k18",
            "k22", "k23", "k24", "k25", "k26", "k27", "k28",
            "k32", "k33", "k34", "k35", "k36", "k37", "k38",} # 断幺的牌组集合
"""

chunquanset={"s12","s18","s22","s28","s32","s38",
            "d11","d19","d21","d29","d31","d39",
            "k11","k19","k21","k29","k31","k39"} # 幺九的牌组集合

hunquanset={"s12","s18","s22","s28","s32","s38",
            "d11","d19","d21","d29","d31","d39",
            "k11","k19","k21","k29","k31","k39",
            "d41","d44","d47","d50","d53","d56","d59",
            "k41","k44","k47","k50","k53","k56","k59"} # 字牌、幺九的牌组集合

zipaiset={41,44,47,50,53,56,59} # 字牌集合
suoziset={11,12,13,14,15,16,17,18,19} # 索子集合
wanziset={21,22,23,24,25,26,27,28,29} # 万子集合
tongziset={31,32,33,34,35,36,37,38,39} # 筒子集合
yaojiuset={11,19,21,29,31,39} # 幺九集合
duanyaoset={12,13,14,15,16,17,18,21,22,23,24,25,26,27,28,32,33,34,35,36,37,38} # 断幺集合

if __name__ == "__main__" :
    # 牌组计算阶段
    Mj_input = Mjobject()
    # 模拟前端传回 Mjobject 类 其中包含十项数据 ：
    Mj_input.hand = "123123123s999s东东"
    Mj_input.inputMPdata1 = ""
    Mj_input.inputMPdata2 = ""
    Mj_input.inputMPdata3 = ""
    Mj_input.inputMPdata4 = ""
    Mj_input.way_to_hepai = ["wayToHepaiZi","wayToHepaiLi","wayToHepaiDoubleLi","wayToHepaiRo","wayToHepaiYi","wayToHepaiHe","wayToHepaiHai","wayToHepaiLin","wayToHepaiQG"]
    Mj_input.dora_num = "3"
    Mj_input.deep_dora_num = "2"
    Mj_input.position_select = "positionDong"
    Mj_input.public_position_select = "publicPositionDong"

    # 通过majongdata 处理 Mj_input.hand 和 Mj_input.inputMPdata* 数据
    inputdata = majongdata(Mj_input.hand)
    print("原始牌组",inputdata)
    inputMPdata1 = majongdata(Mj_input.inputMPdata1)
    inputMPdata2 = majongdata(Mj_input.inputMPdata2)
    inputMPdata3 = majongdata(Mj_input.inputMPdata3)
    inputMPdata4 = majongdata(Mj_input.inputMPdata4)

    # MPcheck 将传入的副露数据合并至 inputdata.combinations_MP
    MPcheck(inputMPdata1)  # 处理副露1
    MPcheck(inputMPdata2)  # 处理副露2
    MPcheck(inputMPdata3)  # 处理副露3
    MPcheck(inputMPdata4)  # 处理副露4

    # 遍历所有可能的雀头状态 存储于alllist当中
    alllist = []
    inputdata.check() # 牌组方法自检
    alllist.extend(duizicheck(inputdata))
    print("以下是几种雀头可能", alllist)

    # 如果主牌组的roundnr不为0 (没有副露) 就进行七对子和国士无双的检测 也将结果存储在alllist当中
    if inputdata.roundnr == 0:
        QDcheck(inputdata)
        GScheck(inputdata)

    # handCheck方法将所有alllist中的牌组进行搭子和刻子的判断 如果同时满足两个条件则均进行判断 保证得出所有和牌可能性 直到alllist内不再有可以迭代的对象
    endlist = handCheck(alllist)

    # resultFilter方法遍历endlist,只保留向听数最近/和牌的牌组
    mahjonglist = resultFilter(endlist)

    # 去重 mahjonglist 中重复的牌组 牌组操作结束
    mahjonglist = distinctMjlist(mahjonglist)

    # 牌组计分阶段
    # 通过 Mj_input.way_to_hepai 的前端传参判断全局变量 part1
    自摸 = False
    立直 = False
    双立直 = False
    荣和 = False
    一发 = False
    河底 = False
    海底 = False
    岭上 = False
    抢杠 = False
    for i in Mj_input.way_to_hepai:
        match i:
            case "wayToHepaiZi":
                自摸 = True
            case "wayToHepaiLi":
                立直 = True
            case "wayToHepaiDoubleLi":
                双立直 = True
            case "wayToHepaiRo":
                荣和 = True
            case "wayToHepaiYi":
                一发 = True
            case "wayToHepaiHe":
                河底 = True
            case "wayToHepaiHai":
                海底 = True
            case "wayToHepaiLin":
                岭上 = True
            case "wayToHepaiQG":
                抢杠 = True

    # 通过 手牌检测 判断全局变量 part2
    清一色 = False
    混一色 = False
    混老头 = False
    断幺 = False
    print(inputdata)
    if all(10 < element < 20 for element in inputdata):
        清一色 = True
    elif all(20 < element < 30 for element in inputdata):
        清一色 = True
    elif all(30 < element < 40 for element in inputdata):
        清一色 = True
    elif all(10 < element < 20 or 40 < element for element in inputdata):
        混一色 = True
    elif all(20 < element < 30 or 40 < element for element in inputdata):
        混一色 = True
    elif all(30 < element < 40 or 40 < element for element in inputdata):
        混一色 = True
    if all(element in yaojiuset for element in inputdata):
        混老头 = True
        print("混老头成立")
    if all(element in duanyaoset for element in inputdata):
        断幺 = True
        print("断幺成立")

    副露 = False
    自风 = ""
    场风 = ""
    宝牌 = int(Mj_input.dora_num)
    里宝牌 = int(Mj_input.deep_dora_num)
    # 通过 传值检测 获取全局变量 part3
    match Mj_input.position_select :
        case "positionDong":
            自风 = "东"
        case "positionNan":
            自风 = "南"
        case "positionXi":
            自风 = "西"
        case "positionBei":
            自风 = "北"
        case "positionOther":
            自风 = "闲家"
    match Mj_input.public_position_select :
        case "publicPositionDong":
            场风 = "东"
        case "publicPositionNan":
            场风 = "南"
        case "publicPositionXi":
            场风 = "西"
        case "publicPositionBei":
            场风 = "北"
    if Mj_input.inputMPdata1 + Mj_input.inputMPdata2 + Mj_input.inputMPdata3 + Mj_input.inputMPdata4 == True:
        副露 = True


    # 检测牌组
    for i in mahjonglist:
        all_combinations = sorted(i.combinations + i.combinations_MP)
        # 检测 断幺 （不成立）→ 混全 → 纯全
        if 断幺 == False :
            if all(element in hunquanset for element in all_combinations):
                if all(element in chunquanset for element in all_combinations):
                    i.combinations_count.append("纯全")
                else:
                    i.combinations_count.append("混全")
        # 检测刻子 对子 顺子的数量 以及 平和 对对 七对
        str_combinations = ""
        for item in all_combinations:
            match item:
                case "k53":
                    item.combinations_count.append("役牌白")
                case "k56":
                    item.combinations_count.append("役牌发")
                case "k59":
                    item.combinations_count.append("役牌中")
                case "k41":
                    if 自风 == "东" :
                        item.combinations_count.append("自风东")
                    if 场风 == "东" :
                        item.combinations_count.append("场风东")
                case "k44":
                    if 自风 == "南":
                        item.combinations_count.append("自风南")
                    if 场风 == "南":
                        item.combinations_count.append("场风南")
                case "k47":
                    if 自风 == "西":
                        item.combinations_count.append("自风西")
                    if 场风 == "西":
                        item.combinations_count.append("场风西")
                case "k50":
                    if 自风 == "北":
                        item.combinations_count.append("自风北")
                    if 场风 == "北":
                        item.combinations_count.append("场风北")
            str_combinations += item # 合并all_combinations 中的所有字符串
        # print(str_combinations)
        kezinr = 0
        dazinr = 0
        duizinr = 0
        for item in str_combinations:
            match item:
                case "d":
                    duizinr += 1
                case "k":
                    kezinr += 1
                case "s":
                    dazinr += 1
        # print(f"对子数量为{duizinr},搭子数量为{dazinr},刻子数量为{kezinr}")
        if dazinr == 4:
            i.combinations_count.append("平和")
        elif kezinr == 4:
            i.combinations_count.append("对对和")
        elif duizinr == 7:
            i.combinations_count.append("七对子")
        # 检测是否有一气
        if all(element in all_combinations for element in ["s12","s15","s18"]):
            print("一气成立")
            i.combinations_count.append("一气贯通")
        elif all(element in all_combinations for element in ["s22","s25","s28"]):
            print("一气成立")
            i.combinations_count.append("一气贯通")
        elif all(element in all_combinations for element in ["s22", "s25", "s28"]):
            print("一气成立")
            i.combinations_count.append("一气贯通")
        # 打印牌组及其番数
        print(all_combinations,i.combinations_count)



# 一杯口
# 三色同刻 三杠子 三暗刻 小三元
# 三色同顺 3.二杯口


"""
基础 = 20

根据前端传参决定的符数
荣和坎张 荣和单调 荣和两面 荣和双碰 荣和边张
自摸坎张 自摸单调 自摸两面 自摸双碰 自摸边张
门前荣和 += 10
自摸和 + 2
双碰两面 + 0
坎张 单骑 + 2

根据计算得出的符数
役牌雀头 +2 双役牌 +4 客风 +0
中张 明刻+2 暗刻+4 明杠+8 暗杠+16
幺九字牌 明刻+4 暗刻+8 明杠+16 暗杠+32

根据役决定的符数
七对25
平和自20
副露配合30
"""