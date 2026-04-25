from sqlalchemy import select , func
from routes import db
from models.article import Article
from datetime import datetime


class ArticleService:

    def get_article(self, article_id: int):
        return db.session.get(Article, article_id)

    def get_articles(self):
        query = db.select(Article)
        return db.session.execute(query).scalars().all()

    def create_article(self, article: Article):
        # todo: 添加同標題文章是否存在的檢查，如果存在則丟出異常
        existing_article = db.session.scalar(
            select(Article).where(Article.title == article.title)
        )
        if existing_article:
            raise ValueError("同標題文章已存在")

        db.session.add(article)
        db.session.commit()
        return article

    def update_article(self, article: Article):
        existing_article = db.session.get(Article, article.id)
        if not existing_article:
            raise ValueError("文章不存在")

        # todo: 添加同標題文章是否存在的檢查，如果存在則丟出異常
        another_article = db.session.scalar(
            select(Article)
            .where(Article.title == article.title)
            .where(Article.id != article.id)
        )
        if another_article:
            raise ValueError("同標題文章已存在")

        existing_article.title = article.title
        existing_article.content = article.content
        existing_article.update_time = func.now()

        db.session.commit()
        return existing_article
    
    def delete_article(self, article_id: int):
        article = db.session.get(Article, article_id)
        if not article:
            return False

        db.session.delete(article)
        db.session.commit()
        return True
