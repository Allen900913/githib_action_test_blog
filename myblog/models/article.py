from datetime import datetime

from routes import db
from sqlalchemy import Integer, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Article(db.Model):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # 真正存在資料庫的欄位名是 "content"，在 Python 屬性上用 _content 保存 bytes
    _content: Mapped[bytes] = mapped_column(BLOB, name="content", nullable=False)

    create_time: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False , server_default=func.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True , server_default=func.now())

    @property
    def content(self) -> str:
        """讀取時把二進位內容解碼成 UTF-8 字串。"""
        return self._content.decode("utf-8")

    @content.setter
    def content(self, value: str) -> None:
        """寫入時把字串編碼回 bytes 存到 BLOB 欄位。"""
        self._content = value.encode("utf-8")
