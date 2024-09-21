# 导入flask包 flask表单包 flask表单库包 sqlalchemy数据库操作包 pymysql数据库底层通信包
from flask import Flask,render_template,request,redirect,url_for # flask类,渲染模版,请求包,重定向,动态路由生成
from flask import make_response,json,jsonify,abort # 向前端发送信息,json数据格式,json处理包,abort抛错包,flask表单
from wtforms import StringField,PasswordField,SubmitField # 引入web表单库,包括字符串字段,秘钥字段,提交字段
from wtforms.validators import DataRequired,EqualTo # 验证数据不能为空,数据不能相同
from flask_wtf import FlaskForm # 引入flask_web表单库,flask表单
import secrets # 使用标准库生成session秘钥
from flask_sqlalchemy import SQLAlchemy # 引入flask sql包
import pymysql # python/sql通信包

# 创建app变量 传参flask对象 __name__ = __main__  使用__name__参数 使flask类所调用的库的根目录确定为app.py本文件所在的目录
app = Flask(__name__)

# 配置web
app.config['DEBUG'] = True  # 开启调试模式
app.config['HOST'] = '127.0.0.2'  # 主机地址
app.config['PORT'] = 443  # 端口号
app.config['JSON_AS_ASCII'] = False # 允许json直接输出,而非转译为Unicode转译序列
app.config['SECRET_KEY'] = secrets.token_hex(16) # session秘钥

# 配置数据库
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qwe123@127.0.0.1:3306/database_mj'
    # 配置数据库用户名root 密码qwe123 host：127.0.0.1 端口3306 数据库名database_mj
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 关闭跟踪变化
app.config.from_object(Config) # 传入数据库配置至web配置
db = SQLAlchemy(app) # 复制db一个sqlalchemy类,传参配置好的app配置,此时可以使用db进行数据库操作.

# 创建数据库模型类
class Role(db.Model): # 角色表
    __tablename__ = "role"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)
class User(db.Model): # 用户表
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)  # 修复拼写错误
    password = db.Column(db.String(128))
    # 表关系
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


@app.route('/index',methods=["GET","POST","PUT"])
def index():
    if request.method == "GET":
        name,password = False,False
        return render_template("index.html",name=name,password=password)
    # "GET /?name=xelnaga&password=qwe123&submit=提交 HTTP/1.1" 200 - 一个GET请求通过url传参
    if request.method == "POST":
        name = request.form.get("name") # post请求通过request请求传参
        password = request.form.get("password")
        if name == "xelnaga" and password == "qwe123":
            return render_template("index.html",name=name,password=password)
        else:
            abort(404)
            #return "未注册的账号，请联系网站管理员"

@app.errorhandler(404)
def handle_404_error(err):
    #return "未注册的账号，请联系网站管理员"
    return render_template("404.html")

@app.route("/response")
def response(): #
    data = {
        "name":"Xe"
    }
    #res = make_response(json.dumps(data,ensure_ascii=False)) # 将XML数据转换为json字符串
    #res.mimetype = "application/json" # 将MIME 类型标识分类/响应体数据 改为 application/json 以供接收方解析
    return jsonify(data) # 自动化以上步骤并 return

@app.route("/")
def redirect_index():
    return redirect(url_for("index",_external=True)) # url_for 一个路由方法也是可以的
    # 重定向一个url ← url_for 生成一个url 使用index 生成完整路由=True

@app.route("/error")
def error():
    abort(404) # 直接输出错误码

# 自定义过滤器 |add_weiba 添加尾巴
def remove(input):
    output = str(input)+"尾巴"
    return output
app.add_template_filter(remove,'add_weiba') # 自定义函数名+过滤器名

# 表单模版类
class Register(FlaskForm): # 命名一个Register类 继承父类FlaskForm方法
    user_name = StringField(label='用户名',validators=[DataRequired("用户名不得为空")])
    # 赋值user_name 一个 StringField类 标签=str关联 //点击用户名会跳转文本框 验证器=DataRequired //确保字段在提交时必须有值 如非 返回'用...'
    password = PasswordField(label='密码',validators=[DataRequired("密码不得为空")])
    password_reinfusion = PasswordField(label='再次确认密码',validators=[DataRequired("密码不得为空"),EqualTo('password',message="两次输入的密码不一致")])
    submit = SubmitField(label='提交')

@app.route('/register',methods=['GET','POST'])
def register():
    # 创建表单对象
    form = Register()
    if request.method == "GET":
        return render_template('register.html',form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.user_name.data
            password = form.password.data
            password = form.password_reinfusion.data
        else:
            return "输入格式有误"
        return render_template('register.html',form=form)

if __name__ == "__main__" :
    with app.app_context(): # 在应用上下文中执行数据库操作
        # 清除所有表
        db.drop_all()
        # 创建所有表
        db.create_all()
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG']) # app.run会阻塞主线程 需要最后执行
    """
    # 创建对象 插入数据
    role1 = Role(name='admin')
    # session记录到对象任务中
    db.session.add(role1)
    # 提交任务
    """





"""
class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
# 传参渲染
@app.route('/') 
def index():
    # 将User类赋值给user变量名
    user = User(username="Xe",password="1448826180")
    age = 17
    person = {
        "username":"Xe",
        "password":"1448826180"
    }
    return render_template("index.html",user=user,person=person,age=age)
    # 可以在html中正常使用python的字典和类方法，说明flask是将html文本的双括号内容进行渲染以后返回的

@app.route('/blog/<int:blog_id>') # app收到了blog/<> 括号中的整数值传参
def bolg(blog_id):
    return render_template("blog_detail.html",blog_id=blog_id,username="Xe")

# Get传参 /book/list?page=2 在访问book/list时传参page=2
@app.route('/book/list')
def book_list():
    # arg argument参数
    # request.args:类字典类型
    page = request.args.get("page",default=1,type=int) # 获得?page=2 page=空则为0
    return f"您获取的是第{page}的图书列表"
"""