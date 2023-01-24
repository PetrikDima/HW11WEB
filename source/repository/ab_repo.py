from source import db, models
from validation.get_value_ab import get_value_ab


def add_rec(name, phone='', birthday=None, email='', address=''):
    ab = models.AddressBook(name=name, phone=phone, birthday=birthday, email=email, address=address)
    db.session.add(ab)
    db.session.commit()


def show_rec():
    records = db.session.query(models.AddressBook).all()
    return records


def change_rec(_id, phone, birthday, email, address):
    ab = db.session.query(models.AddressBook).filter(models.AddressBook.id == int(_id)).one()
    get_value_ab(ab, phone, birthday, email, address)
    db.session.commit()


def del_rec(_id):
    db.session.query(models.AddressBook).filter(models.AddressBook.id == int(_id)).delete()
    db.session.commit()