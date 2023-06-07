import json
import os
from operator import or_

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale


def loading_data():
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'book': Book,
            'shop': Shop,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def search(req):
    author_id = None
    author_name = None
    if req.isdigit():
        author_id = req
    else:
        author_name = req

    res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale). \
        join(Publisher).join(Stock).join(Sale).join(Shop). \
        filter(or_(Publisher.id == author_id, Publisher.name == author_name))

    return res


if __name__ == '__main__':
    load_dotenv()
    engine = sqlalchemy.create_engine(os.getenv("DSN"))
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    loading_data()
    inp = input("Введите имя или идентификатор издателя: ")

    for book, shop, price, count, date in search(inp):
        print(f'{book: <40} | {shop: <10} | {price * count: <8} | {date.strftime("%d-%m-%Y")}')

    session.close()
