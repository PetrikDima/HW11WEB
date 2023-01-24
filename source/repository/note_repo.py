from source.models import Note, Tag
from source import db


def create_note(desc, tags):
    tags_obj = []
    for tag in tags:
        tags_obj.append(db.session.query(Tag).filter(Tag.tag == tag).first())
    note = Note(description=desc, tags=tags_obj)
    db.session.add(note)
    db.session.commit()


def create_tag(tags):
    tag_ = Tag(tag=tags)
    db.session.add(tag_)
    db.session.commit()


def show_notes():
    return db.session.query(Note).all()
