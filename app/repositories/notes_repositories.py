from app.models import Note
from app.extensions import db


def create_note(note):
    db.session.add(note)
    db.session.commit()
    return note




def get_notes_by_id(note_id, user_id):
    return Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()


def get_all_users_notes(user_id):
    return Note.query.filter_by(
        user_id=user_id
    ).all()




def note_delete(note):
    db.session.delete(note)
    db.session.commit()