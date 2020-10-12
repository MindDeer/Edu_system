# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect,session

from dbSqlite3 import *

app = Flask(__name__)
app.secret_key = 'abcdefgh!@#$%'
def CheckLogin():
    if 'teacher_id' not in session:
        return False
    else:
        return True

@app.route('/login', methods=['POST', 'GET'])
def login():   #教师登录身份验证
    if request.method=="GET":
        return render_template('login_t.html')
    session["idka"] = request.form['teacher_id']
    result, _ = GetSql2("select teacher_id,teacher_pwd from teacher_Info where teacher_id='%s'" % request.form['teacher_id'])
    print(result)
    # sql="insert into stu_teacher(stu_id,stu_name,course_name) SELECT student_Info.stu_id,stu_name,course_name FROM stu_course,student_Info where student_Info.stu_id=stu_course.stu_id;"
    # print(sql)
    # ExeSql(sql)

    if len(result) > 0 and result[0][1] == request.form['teacher_pwd']:
        session["teacher_id"]=request.form['teacher_id']
        return render_template('teacher_m.html')
    else:
        return render_template('login_t.html')

@app.route('/per', methods=['GET','post'])
def update5():   #修改密码
    if not CheckLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        id=session.get("idka")
        result, _ = GetSql2("select * from teacher_Info where teacher_id='%s'" %id)
        print(result[0])
        print(type(result[0]))
        return render_template('code_t.html', data=result[0])
    else:
        data = dict(
            teacher_id=request.form['teacher_id'],
            teacher_name=request.form['teacher_name'],
            teacher_pwd=request.form['teacher_pwd']
        )
        UpdateData(data, "teacher_Info")

        return render_template('teacher_m.html')

@app.route('/',methods=['GET'])
def index():   #开课信息查看
    if not CheckLogin():
        return redirect(url_for('login'))
    id = session.get("idka")
    tablename = "course_Info"
    # sql = "SELECT course_id,course_order,course_name,kind_name,course_hours,course_credit,teacher_name,toplimit_num FROM course_Info,course_kind,teacher_Info where course_Info.kind_id=course_kind.kind_id and course_Info.teacher_id=teacher_Info.teacher_id "
    sql = "select * from course_Info where teacher_id='%s'" % id
    print(sql)

    result, fields = GetSql2(sql)
    return render_template('teacher.html', datas=result, fields=fields)

@app.route('/rar',methods=['GET'])
def index2():  #选课学生名单
    if not CheckLogin():
        return redirect(url_for('login'))
    id = session.get("idka")
    tablename = "course_Info"
    # sql = "SELECT course_id,course_order,course_name,kind_name,course_hours,course_credit,teacher_name,toplimit_num FROM course_Info,course_kind,teacher_Info where course_Info.kind_id=course_kind.kind_id and course_Info.teacher_id=teacher_Info.teacher_id "
    sql="select stu_course.stu_id,stu_name,course_name from stu_course,student_Info where stu_course.stu_id=student_Info.stu_id and teacher_id='%s'" % id
    print(sql)

    result, fields = GetSql2(sql)
    return render_template('add_t.html', datas=result, fields=fields)

@app.route('/shit',methods=['GET'])
def index3():  #成绩录入后返回界面
    if not CheckLogin():
        return redirect(url_for('login'))
    id = session.get("idka")
    sql="select stu_course.stu_id,stu_name,course_name,score from stu_course,student_Info where stu_course.stu_id=student_Info.stu_id and teacher_id='%s'" % id

    result, fields = GetSql2(sql)
    return render_template('add_z.html', datas=result, fields=fields)


@app.route('/update', methods=['GET','post'])
def upadte():   #录入（修改）学生成绩
    if not CheckLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        id = session.get("idka")
        sid = request.args['id']
        #name = request.args['cname']
        result, _ = GetSql2("select * from stu_course where teacher_id='%s' and stu_id='%s'" % (id, sid))
        print(result[0])
        print(type(result[0]))
        # for p in pro:
        #     print(p)
        return render_template('add_zz.html', data=result[0])
    else:
        data = dict(
            stu_id=request.form['stu_id'],
            course_name=request.form['course_name'],
            score=request.form['score']
        )
        UpdateData(data,'stu_course')

        # sql = "update stu_course set score='%s' where stu_id='%s' and course_name='%s'" % (data[list(data)[1:][2]], list(data)[1:][0], list(data)[1:][1])
        # print(sql)
        # ExeSql(sql)

        return redirect(url_for("index3"))




if __name__ == '__main__':

    app.run(port=5000,debug=True)

