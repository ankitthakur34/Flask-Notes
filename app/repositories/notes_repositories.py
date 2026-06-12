from datetime import datetime

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
        user_id=user_id,
        is_deleted=False
    ).first()
    if not note:
        logger.warning(f"Note not found: ID {note_id} for user: {user_id}")
        raise note_exception.NoteNotFoundException()
    return note

def restore_note(note_id, user_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id,
        is_deleted=True
    ).first()
    if not note:
        logger.warning(f"Note not found for restoration: ID {note_id} for user: {user_id}")
        raise note_exception.NoteNotFoundException()
    
    note.is_deleted = False
    note.deleted_at = None
    db.session.commit()
    
    return note


def get_all_users_notes(user_id):
    return Note.query.filter_by(
        user_id=user_id,
        is_deleted=False
    ).all()

def get_notes_query(user_id):
    return Note.query.filter_by(user_id=user_id, is_deleted=False)




def note_delete(note, user_id):
    note.is_deleted = True
    note.deleted_at = datetime.utcnow()
    note.deleted_by = user_id
    db.session.commit()