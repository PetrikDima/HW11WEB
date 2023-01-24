from flask import render_template, request, redirect, url_for, flash

from source.models import Note, Tag
from source import db

from . import app

from validation.validation_ab import DateIsNotValid, Birthday, Phone, Name, Email, Address
from .repository.ab_repo import add_rec, show_rec, change_rec, del_rec
from .repository.note_repo import create_note, create_tag, show_notes


@app.route('/')
@app.route('/main')
def main_page():
    return render_template('pages/main.html')


@app.route('/addressbook', strict_slashes=False, methods=['GET', 'POST'])
def addressbook():
    if request.method == 'POST':
        name = Name(request.form.get('name')).value
        try:
            phone = Phone(request.form.get('phone')).value
            birthday = Birthday(request.form.get('birthday')).value
            email = Email(request.form.get('email')).value
        except ValueError:
            flash('Invalid phone try 10 or 12 numbers')
            return redirect(url_for('addressbook'))
        except DateIsNotValid:
            flash('Invalid birthday, try: year-month-day')
            return redirect(url_for('addressbook'))
        except AttributeError:
            flash('Invalid email, try: symbols(,.@ a-z 0-9)')
            return redirect(url_for('addressbook'))
        address = Address(request.form.get('address')).value
        add_rec(name=name, phone=phone, email=email, birthday=birthday, address=address)
        return redirect('/show_ab')
    else:
        return render_template('pages/addressbook.html', back='/show_ab')


@app.route('/note', strict_slashes=False, methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        description = request.form.get('description')
        tags = request.form.getlist("tags")
        create_note(desc=description, tags=tags)
        return redirect('/show_note')
    else:
        tags = db.session.query(Tag).all()
    return render_template('pages/note.html', back='/show_note', tags=tags)


@app.route('/tag', methods=['POST', 'GET'])
def tag():
    if request.method == 'POST':
        tags = request.form.get('tags')
        create_tag(tags=tags)
        return redirect(url_for('note'))
    return render_template('pages/tag.html', back='/show_note')


@app.route('/show_ab')
def show_ab():
    return render_template('pages/show_ab.html', back='/', addressbooks=show_rec())


@app.route('/show_note')
def show_note():
    return render_template('pages/show_note.html', back='/main', notes=show_notes())


@app.route('/done/<id>')
def done(id):
    note = db.session.query(Note).filter(Note.id == id).one()
    note.done = True
    db.session.commit()
    return redirect('/show_note')


@app.route('/change_ab/', methods=['POST', 'GET'])
def change_ab():
    phone = ''
    birthday = None
    email = ''
    if request.method == 'POST':
        _id = request.form.get('id')
        try:
            phone = Phone(request.form.get('phone')).value
            birthday = Birthday(request.form.get('birthday')).value
            email = Email(request.form.get('email')).value
        except ValueError:
            print('Incorrect phone')
        except DateIsNotValid:
            print('Incorrect birthday')
        except AttributeError:
            print('Incorrect email')
        address = Address(request.form.get('address')).value
        change_rec(_id=_id, phone=phone, birthday=birthday, email=email, address=address)
        return redirect('/show_ab')
    return render_template('pages/change_ab.html', back='/show_ab')


@app.route('/delete_ab/', methods=['POST', 'GET'])
def delete_ab():
    if request.method == 'POST':
        _id = request.form.get('id')
        del_rec(_id=_id)
        return redirect('/show_ab')
    return render_template('pages/delete_ab.html', back='/show_ab')


@app.route('/change_note/', methods=['POST', 'GET'])
def change_note():
    if request.method == 'POST':
        id = request.form.get('id')
        description = request.form.get('description')
        tags = request.form.getlist("tags")
        tags_obj = []
        for tag in tags:
            tags_obj.append(db.session.query(Tag).filter(Tag.tag == tag).first())
        note = db.session.query(Note).filter(Note.id == int(id)).one()
        if note.done is not True:
            note.tags = tags_obj
            note.description = description
            db.session.commit()
            return redirect('/show_note')
    else:
        tags = db.session.query(Tag).all()
    return render_template('pages/change_note.html', back='/show_note', tags=tags)


@app.route('/delete_note/', methods=['POST', 'GET'])
def delete_note():
    if request.method == 'POST':
        id_ = request.form.get('id')
        db.session.query(Note).filter(Note.id == int(id_)).delete()
        db.session.commit()
        return redirect('/show_note')

    return render_template('pages/delete_note.html', back='/show_note')


@app.route('/delete_tag/', methods=['POST', 'GET'])
def delete_tag():
    if request.method == 'POST':
        tag = request.form.getlist('tags')
        for i in tag:
            db.session.query(Tag).filter(Tag.tag == i).delete()
        db.session.commit()
        return redirect('/show_note')
    else:
        tags = db.session.query(Tag).all()
    return render_template('pages/delete_tag.html', back='/show_note', tags=tags)
