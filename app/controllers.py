# -*- coding: utf-8 -*-
import os
from werkzeug import secure_filename
from app.database import init_db, db_session
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from models import User, Post
from app import app

UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif', 'bmp'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#메인 페이지
@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', users = users)

#프로필
@app.route('/profile/<int:userId>')
def profile(userId):
    #사용자 정보
    user = User.query.filter_by(id = userId).first()
    #컨텐츠 리스트
    posts = Post.query.filter(Post.userid == User.id).order_by(Post.id.desc()).all()
    #app.logger.debug(len(posts))
    return render_template('profile.html', user = user, posts = posts, userId = userId)

#회원가입 화면
@app.route('/register-form')
def registerForm():
    return render_template('register.html')





#로그인 화면
@app.route('/login-form')
def loginForm():
    return render_template('login.html')

#로그인
@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).filter_by(password = password).first()
        if (user):
            session['logged_in'] = True
            session['id'] = user.id
            session['email'] = user.email
            session['name'] = user.name
            session['image'] = user.image
            return redirect("/profile/" + str(user.id))
        else:
            return '로그인 정보가 맞지 않습니다.'
    else:
        return '잘못된 접근입니다.'

#로그아웃
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))

#컨텐츠 등록
@app.route('/add/<int:userId>', methods = ['POST'])
def add(userId):
    if request.method == 'POST':
        if (session['logged_in']):
            post = Post(request.form['contents'], userId, session['id'])
            db_session.add(post)
            db_session.commit()
            return redirect("/profile/" + str(userId))
        else:
            return "로그인이 필요합니다"
    else:
        return "잘못된 접근입니다"

#회원가입
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        email =  request.form['email']
        if(request.form['password'] == request.form['repassword']):
            if(User.query.filter_by(email = email).first()):
                return "이메일이 중복됩니다."
            else:
                file = request.files['image']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user = User(request.form['name'], request.form['email'], request.form['password'], 'img/' +filename)
                db_session.add(user)
                db_session.commit()
                return redirect('/index')
        else:
            return "비밀번호가 일치하지 않습니다"
    else:
        return "잘못된 접근입니다"



#컨텐츠 삭제
@app.route('/delete/<int:userId>/<int:postId>')
def delete(userId, postId):
    if(session['logged_in']):
        Post.query.filter_by(id = postId).delete()
        return redirect("/profile/" + str(userId))
    else:
        return "잘못된 접근입니다"



