# 导入flask包 flask表单包 flask表单库包 sqlalchemy数据库操作包 pymysql数据库底层通信包
from flask import Flask,render_template,request,redirect,url_for # flask类,渲染模版,请求包,重定向,动态路由生成
from flask import make_response,json,jsonify,abort # 向前端发送信息,json数据格式,json处理包,abort抛错包,flask表单
from wtforms import StringField,PasswordField,SubmitField # 引入web表单库,包括字符串字段,秘钥字段,提交字段
from wtforms.validators import DataRequired,EqualTo # 验证数据不能为空,数据不能相同
from flask_wtf import FlaskForm # 引入flask_web表单库,flask表单
import secrets # 使用标准库生成session秘钥
from flask_sqlalchemy import SQLAlchemy # 引入flask sql包
import pymysql # python/sql通信包
from mahjong import mahjong_count # 调下处理牌的主程序

# 创建app变量 传参flask对象 __name__ = __main__  使用__name__参数 使flask类所调用的库的根目录确定为app.py本文件所在的目录
app = Flask(__name__)

# 配置web
app.config['DEBUG'] = True  # 开启调试模式
app.config['HOST'] = '127.0.0.2'  # 主机地址
app.config['PORT'] = 5000  # 端口号
app.config['JSON_AS_ASCII'] = False # 允许json直接输出,而非转译为Unicode转译序列
app.config['SECRET_KEY'] = secrets.token_hex(16) # session秘钥

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


@app.route("/",methods=["GET","POST","PUT"])
def index():
    return render_template("index.html")
    print(wayToHepai)

@app.route("/count",methods=["POST"])
def get_count():
    Mj_count = "通信中"
    Mahjong_hand = Mjobject() # 获取数据
    Mahjong_hand.hand = request.form.get('hand')
    Mahjong_hand.inputMPdata1 = request.form.get('fulu1')
    Mahjong_hand.inputMPdata2 = request.form.get('fulu2')
    Mahjong_hand.inputMPdata3 = request.form.get('fulu3')
    Mahjong_hand.inputMPdata4 = request.form.get('fulu4')
    Mahjong_hand.way_to_hepai = request.form.getlist('wayToHepai')
    Mahjong_hand.dora_num = request.form.get('doraNum')
    Mahjong_hand.deep_dora_num = request.form.get('deepDoraNum')
    Mahjong_hand.position_select = request.form.get("positionSelect")
    Mahjong_hand.public_position_select = request.form.get("publicPositionSelect")
    # 如果和牌方式是河底或抢杠 属于荣和型 如果和牌方式属于海底或岭上 属于自摸型
    if "wayToHepaiHe" or "wayToHepaiQG" in Mahjong_hand.way_to_hepai:
        Mahjong_hand.way_to_hepai.append("wayToHePaiRo")
    if "wayToHepaiHai" or "wayToHepaiLin" in Mahjong_hand.way_to_hepai:
        Mahjong_hand.way_to_hepai.append("wayToHePaiZi")

    print("收到信息：") # 显示数据
    print("手牌：",Mahjong_hand.hand)
    print("副露1：",Mahjong_hand.inputMPdata1)
    print("副露2：",Mahjong_hand.inputMPdata2)
    print("副露3：",Mahjong_hand.inputMPdata3)
    print("副露4：",Mahjong_hand.inputMPdata4)
    print("和牌手段",Mahjong_hand.way_to_hepai) # 可以为空
    print("宝牌数：",Mahjong_hand.dora_num) # 可以为空
    print("里宝牌数：",Mahjong_hand.deep_dora_num) # 可以为空
    print("自风：",Mahjong_hand.position_select) # 无限制
    print("场风：",Mahjong_hand.public_position_select) # 无限制

    # 检测输入
    # 四种报错 1.超出规定字符串集合限制 2.超出副露组合限制 3.牌组超出或不足规定长度限制 4.宝牌和里宝牌不为阿拉伯数字 如牌组未听牌或无役则按正常结果返回
    error_message = "" # 报错信息
    allow_character = {"0","1","2","3","4","5","6","7","8","9","0","s","m","p","东","南","西","北","中","白","发"} # 输入字符串限制
    count_character = {"0","1","2","3","4","5","6","7","8","9","0","东","南","西","北","中","白","发"} # 被计入麻将牌的各字符
    count_tiles = 0 # 麻将牌数量 应当满足14
    allow_MP = {"123s","123m","123p","234s","234m","234p","345s","345m","345p", # 副露组合限制
                "456s","456m","456p","567s","567m","567p","678s","678m","678p","789s","789m","789p",
                "340s", "340m", "340p","406s", "406m", "406p", "067s", "067m", "067p",
                "111s","1111s","11111s","111m","1111m","11111m","111p","1111p","11111p",
                "222s","2222s","22222s","222m","2222m","22222m","222p","2222p","22222p",
                "333s","3333s","33333s","333m","3333m","33333m","333p","3333p","33333p",
                "444s","4444s","44444s","444m","4444m","44444m","444p","4444p","44444p",
                "555s","5555s","55555s","555m","5555m","55555m","555p","5555p","55555p",
                "666s","6666s","66666s","666m","6666m","66666m","666p","6666p","66666p",
                "777s","7777s","77777s","777m","7777m","77777m","777p","7777p","77777p",
                "888s","8888s","88888s","888m","8888m","88888m","888p","8888p","88888p",
                "999s","9999s","99999s","999m","9999m","99999m","999p","9999p","99999p",
                "东东东","东东东东","东东东东东","南南南","南南南南","南南南南南","西西西","西西西西","西西西西西","北北北","北北北北","北北北北北",
                "中中中","中中中中","中中中中中","发发发","发发发发","发发发发发","白白白","白白白白","白白白白白",}

    # 1.如果传入手牌以及副露的手牌不符合规则即报错
    for i in Mahjong_hand.hand + Mahjong_hand.inputMPdata1 + Mahjong_hand.inputMPdata2 + Mahjong_hand.inputMPdata3 + Mahjong_hand.inputMPdata4:
        if i not in allow_character:
            error_message = "格式错误:手牌与副露中不得出现超出0,1,2,3,4,5,6,7,8,9,0,s,m,p,东,南,西,北的字符"
            return render_template("index.html", Mj_count=Mj_count, output = error_message)

    # 2.如果传入的副露不为空并且不符合allow_MP:中的组合即报错
    MP_list = [Mahjong_hand.inputMPdata1,Mahjong_hand.inputMPdata2,Mahjong_hand.inputMPdata3,Mahjong_hand.inputMPdata4]
    for i in MP_list:
        if i :
            count_tiles += 3
            if i not in allow_MP:
                error_message = f"格式错误:副露中只能出现{allow_MP}内的组合"
                return render_template("index.html", Mj_count=Mj_count, output=error_message)

    # 3.如果传入的副露加上手牌超出不足14枚则报错
    for i in Mahjong_hand.hand:
        if i in count_character:
            count_tiles += 1
    if count_tiles != 14:
        if count_tiles > 14: # 大于14
            error_message = "格式错误:传入麻将牌数量大于14"
            return render_template("index.html", Mj_count=Mj_count, output=error_message)
        else: # 小于14
            error_message = "格式错误:传入麻将牌数量小于14"
            return render_template("index.html", Mj_count=Mj_count, output=error_message)

    # 4.如果宝牌和里宝牌的输入不为阿拉伯数字则报错
    if Mahjong_hand.deep_dora_num:
        if not Mahjong_hand.deep_dora_num.isdigit():
            error_message = "格式错误:宝牌和里宝牌应当为阿拉伯数字"
            return render_template("index.html", Mj_count=Mj_count, output=error_message)
    if Mahjong_hand.dora_num:
        if not Mahjong_hand.dora_num.isdigit():
            error_message = "格式错误:宝牌和里宝牌应当为阿拉伯数字"
            return render_template("index.html", Mj_count=Mj_count, output=error_message)

    # 计算输出
    try:
        output = mahjong_count(Mahjong_hand) # mahjong_count 主程序
    except Exception as count_error: #
        error_message = f"计算错误:主程序运算出错,error_name = {count_error},请联系网站管理员q1448826180"
        return render_template("index.html", Mj_count=Mj_count, output=error_message)

    print("返回信息:",Mj_count)
    return render_template("index.html",Mj_count = Mj_count,output = output)

if __name__ == "__main__" :
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])

