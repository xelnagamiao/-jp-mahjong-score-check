# 导入flask包 flask表单包 flask表单库包 sqlalchemy数据库操作包 pymysql数据库底层通信包
from flask import Flask,render_template,request,redirect,url_for # flask类,渲染模版,请求包,重定向,动态路由生成
from flask import make_response,json,jsonify,abort # 向前端发送信息,json数据格式,json处理包,abort抛错包,flask表单
from wtforms import StringField,PasswordField,SubmitField # 引入web表单库,包括字符串字段,秘钥字段,提交字段
from wtforms.validators import DataRequired,EqualTo # 验证数据不能为空,数据不能相同
from flask_wtf import FlaskForm # 引入flask_web表单库,flask表单
import secrets # 使用标准库生成session秘钥
from flask_sqlalchemy import SQLAlchemy # 引入flask sql包
import pymysql # python/sql通信包
import mahjong # 调下处理牌的主程序

# 创建app变量 传参flask对象 __name__ = __main__  使用__name__参数 使flask类所调用的库的根目录确定为app.py本文件所在的目录
app = Flask(__name__)

# 配置web
app.config['DEBUG'] = True  # 开启调试模式
app.config['HOST'] = '127.0.0.2'  # 主机地址
app.config['PORT'] = 443  # 端口号
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
    Mahjong_hand = Mjobject()
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
    print("收到信息：")
    print("手牌：",Mahjong_hand.hand)
    print("副露1：",Mahjong_hand.inputMPdata1)
    print("副露2：",Mahjong_hand.inputMPdata2)
    print("副露3：",Mahjong_hand.inputMPdata3)
    print("副露4：",Mahjong_hand.inputMPdata4)
    print("和牌手段",Mahjong_hand.way_to_hepai)
    print("宝牌数：",Mahjong_hand.dora_num)
    print("里宝牌数：",Mahjong_hand.deep_dora_num)
    print("自风：",Mahjong_hand.position_select)
    print("场风：",Mahjong_hand.public_position_select)

    Mj_count = "123s"
    print("返回信息:",Mj_count)
    return render_template("index.html",Mj_count=Mj_count)

if __name__ == "__main__" :
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
