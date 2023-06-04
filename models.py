from typing import Any

import sqlalchemy as sq
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=255), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=255), nullable=False)
    publisher_id: Column[Any] = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)
    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return f'{self.id}: {self.title}, {self.publisher_id}'


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    shop = relationship(Shop, backref='stock')
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    book = relationship(Book, backref='stock')
    count = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'{self.id}: {self.shop_id}, {self.book_id}, {self.count}'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    stock = relationship(Stock, backref='sale')
    count = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'{self.id}: {self.price}, {self.date_sale}, {self.stock_id}, {self.count}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
