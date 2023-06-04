import json
import os

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


def search(request):
    query = session.query(
            Book.title, Shop.name, Sale.price, Sale.date_sale
        ).filter(
            Stock.id == Sale.stock_id
        ).filter(
            Book.id == Stock.book_id
        ).filter(
            Publisher.id == Book.publisher_id
        ).filter(
            Shop.id == Stock.shop_id
        )

    return query.filter(Publisher.name == request or Publisher.id == request)


if __name__ == '__main__':
    load_dotenv()
    engine = sqlalchemy.create_engine(os.getenv("DSN"))
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    loading_data()
    req = input("Введите имя или идентификатор издателя: ")
    for datas in search(req):
        print()
        for _ in datas:
            print(_, end=' | ')
    session.close()
