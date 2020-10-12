# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect,session

from dbSqlite3 import *

app = Flask(__name__)
app.secret_key = 'abcdefgh!@#$%'
def CheckLogin():
    if 'admin_name' not in session:
        return False
    else:
        return True

@app.route('/login', methods=['POST', 'GET'])
def login():  #验证登录身份
    if request.method=="GET":
        return render_template('login.html')
    session["nameka"] = request.form['admin_name']
    result, _ = GetSql2("select admin_name,Admin_pwd from admin_Info where admin_name='%s'" %request.form['admin_name'])
    print (result)

    if len(result) > 0 and result[0][1] == request.form['Admin_pwd']:
        session["admin_name"]=request.form['admin_name']
        return render_template('show_m.html')
    else:
        return render_template('login.html')
@app.route('/per', methods=['GET','post'])
def update5():   #修改密码
    if not CheckLogin():
        return redirect(url_for("login"))

    if request.method == "GET":
        name=session.get("nameka")
        result, _ = GetSql2("select * from admin_Info where admin_name='%s'" %name)
        print(result[0])
        print(type(result[0]))
        return render_template('code.html', data=result[0])
    else:
        data = dict(
            admin_id=request.form['admin_id'],
            admin_name=request.form['admin_name'],
            admin_pwd=request.form['admin_pwd']
        )
        UpdateData(data, "admin_Info")

        return render_template('show_m.html')

@app.route('/',methods=['GET'])
def index():   #学生信息维护
    if not CheckLogin():
        return redirect(url_for('login'))
    dataid, _ = GetSql2("select distinct Pro_id ,Pro_id as col2  from student_Info ")
    datad, _ = GetSql2("select distinct Class_id ,Class_id as col2  from student_Info ")
    # datada, _ = GetSql2("select distinct Stu_sex ,Stu_sex as col2  from student_Info ")
    strWhere = []
    if "name" in request.args:
        name = request.args["name"]
        if name != "":
            strWhere.append("Stu_name like '%%%s%%'" % name)

    if "Pro_id" in request.args:
        idd = request.args["Pro_id"]
        if idd != "":
            strWhere.append("Pro_id = '%s'" % idd)
    if "id" in request.args:
        id = request.args["id"]
        if id != "":
            strWhere.append("Stu_id = '%s'" % id)
    if "Stu_sex" in request.args:
        ida = request.args["Stu_sex"]
        if ida != "":
            strWhere.append("Stu_sex = '%s'" % ida)
    if "Class_id" in request.args:
        idc = request.args["Class_id"]
        if idc != "":
            strWhere.append("Class_id = '%s'" % idc)

    tablename = "student_Info"
    sql = "SELECT * FROM student_Info "

    if len(strWhere) > 0:
        sql = sql + " where " + " and ".join(strWhere)
        print(sql)

    result, fields = GetSql2(sql)
    return render_template('show.html', datas=result, fields=fields, dataid=dataid, datad=datad)

@app.route('/mama',methods=['GET'])
def index1():   #课程信息维护
    if not CheckLogin():
        return redirect(url_for('login'))
    dataid, _ = GetSql2("select distinct kind_id ,kind_id as col2  from course_Info ")
    datada, _ = GetSql2("select distinct teacher_id ,teacher_id as col2  from course_Info ")
    strWhere = []
    if "cname" in request.args:
        name = request.args["cname"]
        if name != "":
            strWhere.append("course_name like '%%%s%%'" % name)

    if "cid" in request.args:
        id = request.args["cid"]
        if id != "":
            strWhere.append("course_id = '%s'" % id)
    if "kind_id" in request.args:
        ida = request.args["kind_id"]
        if ida != "":
            strWhere.append("kind_id = '%s'" % ida)
    if "teacher_id" in request.args:
        idc = request.args["teacher_id"]
        if idc != "":
            strWhere.append("teacher_id = '%s'" % idc)
    tablename = "course_Info"
    sql = "SELECT * FROM course_Info "

    if len(strWhere) > 0:
        sql = sql + " where " + " and ".join(strWhere)
        print(sql)

    result, fields = GetSql2(sql)
    return render_template('show-t.html', datas=result, fields=fields,dataid=dataid,datada=datada)

@app.route('/del/<id>', methods=['GET'])
def delete(id):   #删除学生信息
    if not CheckLogin():
        return redirect(url_for("login"))
    DelDataById("Stu_id", id, "student_Info")
    return redirect(url_for("index"))
@app.route('/del-t/<id>', methods=['GET'])
def delete1(id):   #删除课程信息
    if not CheckLogin():
        return redirect(url_for("login"))
    DelDataById("course_id", id, "course_Info")
    return redirect(url_for("index1"))

@app.route('/add', methods=['GET','post'])
def add():   #添加学生信息
    if not CheckLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        datas, _ = GetSql2("select distinct Pro_id ,Pro_id as col2  from student_Info ")
        data, _ = GetSql2("select distinct Class_id ,Class_id as col2  from student_Info ")
        return render_template('add.html', datas=datas,data=data)

    else:
        data = dict(
            Stu_id=request.form['Stu_id'],
            Stu_name=request.form['Stu_name'],
            Pro_id=request.form['Pro_id'],
            Stu_sex=request.form['Stu_sex'],
            Stu_birth=request.form['Stu_birth'],
            Class_id=request.form['Class_id'],
            Stu_pwd=request.form['Stu_pwd']
        )

        InsertData(data, "student_Info")
        return redirect(url_for("index"))
@app.route('/add-t', methods=['GET','post'])
def add1():   #添加课程信息
    if not CheckLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        datas, _ = GetSql2("select distinct kind_id ,kind_id as col2  from course_Info ")
        return render_template('add-t.html', datas=datas)

    else:
        data = dict(
            course_id=request.form['course_id'],
            course_order=request.form['course_order'],
            course_name=request.form['course_name'],
            kind_id=request.form['kind_id'],
            course_hours=request.form['course_hours'],
            course_credit=request.form['course_credit'],
            teacher_id=request.form['teacher_id'],
            class_id=request.form['class_id'],
            toplimit_num=request.form['toplimit_num'],
            class_date=request.form['class_date']
        )

        InsertData(data, "course_Info")
        return redirect(url_for("index1"))



@app.route('/update', methods=['GET','post'])
def upadte():   #修改学生信息
    if not CheckLogin():
        return redirect(url_for("login"))
    if request.method == "GET":
        id = request.args['id']
        result, _ = GetSql2("select * from student_Info where Stu_id='%s'" % id)
        print(result[0])
        print(type(result[0]))
        pro, _ = GetSql2("select distinct Pro_id from student_Info ")
        proo, _ = GetSql2("select distinct Class_id from student_Info ")
        # for p in pro:
        #     print(p)
        return render_template('updata.html', data=result[0], pro=pro,proo=proo)
    else:

        data = dict(
            Stu_id=request.form['Stu_id'],
            Stu_name=request.form['Stu_name'],
            Pro_id=request.form['Pro_id'],
            Stu_sex=request.form['Stu_sex'],
            Stu_birth=request.form['stu_birth'],
            Class_id=request.form['Class_id'],
            Stu_pwd=request.form['stu_pwd']
        )
        UpdateData(data, "student_Info")

        return redirect(url_for("index"))

@app.route('/update-t', methods=['GET', 'post'])
def upadte1():   #修改课程信息
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
            return render_template('update-t.html', data=result[0], pro=pro)
        else:

            data = dict(
                course_id=request.form['course_id'],
                course_order=request.form['course_order'],
                course_name=request.form['course_name'],
                kind_id_id=request.form['kind_id'],
                course_hours=request.form['course_hours'],
                course_credit=request.form['course_credit'],
                teacher_id = request.form['teacher_id'],
                class_id = request.form['class_id'],
                toplimit_num = request.form['toplimit_num'],
                class_date = request.form['class_date']

            )
            UpdateData(data, "course_Info")

            return redirect(url_for("index1"))


if __name__ == '__main__':

    app.run(port=4000,debug=True)

