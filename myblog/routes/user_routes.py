from services.user_service import UserService
from . import app
from flask import render_template , abort, redirect, url_for, flash , send_from_directory
from services.article_service import ArticleService
from datetime import datetime
from forms.login_form import LoginForm
from forms.delete_article_form import DeleteArticleForm
from flask_login import login_user, logout_user, current_user
from commom.profile import Profile

@app.route('/' , methods=['GET', 'POST'])
@app.route('/index.html' , methods=['GET', 'POST'])
def home_page():
    if current_user.is_authenticated:
        delete_article_form = DeleteArticleForm()
        if delete_article_form.validate_on_submit():
            try:
                article_id = delete_article_form.article_id.data
                result = ArticleService().delete_article(article_id)
                if result:
                    flash('文章刪除成功', category='success')
                    return redirect(url_for('home_page'))
                else:
                    flash('文章刪除失敗', category='danger')
            except Exception as e:
                flash('發生錯誤，請稍後再試', category='danger')

        
    articles = ArticleService().get_articles()
    if current_user.is_authenticated:
        return render_template('index.html', articles=articles , delete_article_form=delete_article_form)
    
    return render_template('index.html', articles=articles)

@app.route('/about.html')
def about_page():
    return render_template('about.html')

@app.route('/login.html' , methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            result = UserService().do_login(login_form.username.data, login_form.password.data)
            if result:
                flash(f'歡迎 {login_form.username.data} 回來', category='success')
                return redirect(url_for('home_page'))
            else:
                flash('用戶名或密碼錯誤', category='danger')
        except Exception as e:
            # 記錄錯誤日誌（在實際應用中建議使用 logging 模組）
            print(f"登入過程發生錯誤: {str(e)}")
            flash('系統暫時無法處理您的請求，請稍後再試', category='danger')
    return render_template('login.html', form=login_form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('你已成功登出', category='info')
    return redirect(url_for('home_page'))

@app.route('/article/<article_id>.html')
def article_page(article_id: int):
    
    article = ArticleService().get_article(article_id)
    if article:
        return render_template('article.html', article=article)
    abort(404)

@app.route('/image/<image_filename>')
def image_page(image_filename: str):
    image_path = Profile.get_image_path()
    image_filepath = image_path.joinpath(image_filename)
    if not image_filepath.exists():
        return abort(404)
    
    return send_from_directory(image_path, image_filename)
