from models.article import Article
from forms.image_upload_form import ImageUploadForm
from commom.profile import Profile
from services.image_service import ImageService
from . import app
from flask import render_template , redirect, url_for , flash , request
from services.article_service import ArticleService
from forms.article_form import ArticleForm
from flask_login import login_required
from werkzeug.utils import secure_filename
from commom import utils


@app.route('/create_article.html' , methods=['GET', 'POST'])
@login_required
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article()
        new_article.title = form.title.data
        new_article.content = form.content.data

        try:
            ArticleService().create_article(new_article)
            flash(f'文章已成功发布', category='success')
            return redirect(url_for('home_page'))
        except Exception as e:
            flash(f'发布文章失败: {e}', category='danger')

    return render_template('editarticle.html', form=form, is_edit=False)

@app.route('/editarticle/<article_id>.html' , methods=['GET', 'POST'])
@login_required
def edit_article_users(article_id : int):
    form = ArticleForm()
    if request.method == 'GET':
        try:
            article = ArticleService().get_article(article_id)
            if not article:
                flash('文章不存在', category='warning')
                return redirect(url_for('home_page'))
            else:
                form.title.data = article.title
                form.content.data = article.content
        except Exception as e:
            flash(f'獲取文章失敗: {e}', category='danger')
            return redirect(url_for('home_page'))

    if form.validate_on_submit():
        update_article = Article()
        update_article.id = article_id
        update_article.title = form.title.data
        update_article.content = form.content.data

        try:
            ArticleService().update_article(update_article)
            flash(f'文章已成功更新', category='success')
            return redirect(url_for('home_page'))
        except Exception as e:
            flash(f'文章更新失败: {e}', category='danger')

    return render_template('editarticle.html', form=form , is_edit=True)

@app.route('/images.html', methods=['GET', 'POST'])
@login_required
def image_upload():
    form = ImageUploadForm()

    if form.validate_on_submit():
        image_file = form.image_file.data

        image_path = Profile.get_image_path()
        image_filename = secure_filename(image_file.filename)
        image_fullpath = utils.get_save_filepath(image_path, image_filename) # 處理相同檔案上傳，使用不同名稱在上傳

        image_file.save(image_fullpath)
        flash('图片上传成功', category='success')
        
    image_filenames = ImageService().get_image_filename_list()
    return render_template('images.html', form=form, image_filenames=image_filenames)
