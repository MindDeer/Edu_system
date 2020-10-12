# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect,session

from dbSqlite3 import *

app = Flask(__name__)
app.secret_key = 'abcdefgh!@#$%'
def CheckLogin():
    if 'stu_id' not in session:
        return False
    else:
        return True

@app.route('/login', methods=['POST', 'GET'])
def login():   #学生登录身份验证
    if request.method=="GET":
        return render_template('login_s.html')
    session["idka"] = request.form['stu_id']
    result, _ = GetSql2("select stu_id,stu_pwd from student_Info where stu_id='%s'" % request.form['stu_id'])
    print(result)

    if len(result) > 0 and result[0][1] == request.form['stu_pwd']:
        session["stu_id"]=request.form['stu_id']
        return render_template('stu_m.html')
    else:
        return render_template('login_s.html')

@app.route('/per', methods=['GET','post'])
def update5():  #学生密码修改、个人信息
    if not CheckLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        id=session.get("idka")
        result, _ = GetSql2("select * from student_Info where stu_id='%s'" % id)
        print(result[0])
        print(type(result[0]))
        return render_template('code_s.html', data=result[0])
    else:
        data = dict(
            stu_id=request.form['stu_id'],
            stu_name=request.form['stu_name'],
            pro_id=request.form['pro_id'],
            stu_sex=request.form['stu_sex'],
            stu_birth=request.form['stu_birth'],
            class_id=request.form['class_id'],
            stu_pwd=request.form['stu_pwd']
        )
        UpdateData(data, "student_Info")

        return render_template('stu_m.html')

@app.route('/',methods=['GET'])
def index():   #课程信息查看
    if not CheckLogin():
        return redirect(url_for('login'))
    # dataid, _ = GetSql2("select distinct Pro_id ,Pro_id as col2  from student_Info ")
    # datad, _ = GetSql2("select distinct Class_id ,Class_id as col2  from student_Info ")
    # datada, _ = GetSql2("select distinct Stu_sex ,Stu_sex as col2  from student_Info ")
    strWhere = []
    if "cname" in request.args:
        name = request.args["cname"]
        if name != "":
            strWhere.append(" course_name like '%%%s%%' " % name)

    if "cid" in request.args:
        id = request.args["cid"]
        if id != "":
            strWhere.append(" course_id = '%s' " % id)

    tablename = "course_Info"
    # sql = "SELECT course_id,course_order,course_name,kind_name,course_hours,course_credit,teacher_name,toplimit_num FROM course_Info,course_kind,teacher_Info where course_Info.kind_id=course_kind.kind_id and course_Info.teacher_id=teacher_Info.teacher_id "
    sql="select * from course_Info "
    print(sql)
    if len(strWhere) > 0:
        sql = sql + " where " + " and ".join(strWhere)
        print(sql)

    result, fields = GetSql2(sql)
    return render_template('stu.html', datas=result, fields=fields)

@app.route('/rar',methods=['GET'])
def index2():  #已选课查看
    if not CheckLogin():
        return redirect(url_for('login'))
    id = session.get("idka")
    tablename = "course_Info"
    sql = "SELECT * FROM stu_course where stu_id='%s'" % id

    result, fields = GetSql2(sql)
    return render_template('add_s.html', datas=result, fields=fields)

@app.route('/fen',methods=['GET'])
def index3():  #查看个人成绩
    if not CheckLogin():
        return redirect(url_for('login'))
    id = session.get("idka")
    tablename = "course_Info"
    sql = "SELECT course_name,score FROM stu_course where stu_id='%s'" % id

    result, fields = GetSql2(sql)
    return render_template('add_ss.html', datas=result, fields=fields)

@app.route('/del-t/<id>', methods=['GET'])
def delete1(id):  #学生退课
    if not CheckLogin():
        return redirect(url_for("login"))
    DelDataById("course_id", id, "stu_course")
    return redirect(url_for("index2"))

@app.route('/add-t/<id>', methods=['GET'])
def add(id):  #所选的课加入到个人课程表
    if not CheckLogin():
        return redirect(url_for("login"))
    flag = session.get("idka")
    tablename = "course_Info"
    sql = "insert into stu_course(course_id,course_order,course_name,kind_id,course_hours,course_credit,teacher_id,toplimit_num,stu_id) SELECT course_id,course_order,course_name,kind_id,course_hours,course_credit,teacher_id,toplimit_num,'%s' FROM course_Info WHERE course_id='%s'" % (flag,id)

    print(sql)
    ExeSql(sql)
    return render_template(url_for("index"))

@app.route('/update-t', methods=['GET', 'post'])
def update():
        if not CheckLogin():
            return redirect(url_for("login"))
        if request.method == "GET":
            id = request.args['id']
            result, _ = GetSql2("select * from course_Info where course_id='%s'" % id)
            print(result[0])
            print(type(result[0]))
            pro, _ = GetSql2("select distinct kind_id from course_Info ")
            # for p in pro:
            #     print(p)
            return render_template('add_s.html', data=result[0], pro=pro)
        else:

            data = dict(
                course_id=request.form['course_id'],
                course_order=request.form['course_order'],
                course_name=request.form['course_name'],
                kind_id=request.form['kind_id'],
                course_hours=request.form['course_hours'],
                course_credit=request.form['course_credit'],
                teacher_id = request.form['teacher_id']
            )
            UpdateData(data, "stu_course")

            return redirect(url_for("index"))


if __name__ == '__main__':

    app.run(port=3000,debug=True)

