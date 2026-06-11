from app.exceptions import note_exception
from app.models import Note
from app.extensions import db
from app.logging_config import logger


def create_note(note):
    db.session.add(note)
    db.session.commit()
    return note




def get_note_by_id(note_id, user_id):
    note= Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()
    if not note:
        logger.warning(f"Note not found: ID {note_id} for user: {user_id}")
        raise note_exception.NoteNotFoundException()
    return note


def get_all_users_notes(user_id):
    return Note.query.filter_by(
        user_id=user_id
    ).all()

def get_notes_query(user_id):
    return Note.query.filter_by(user_id=user_id)




def note_delete(note):
    db.session.delete(note)
    db.session.commit()