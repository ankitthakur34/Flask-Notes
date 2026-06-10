
from app.extensions import db
from app.models.note_model import Note
from datetime import datetime
from app.repositories import notes_repositories
from app.logging_config import logger


def create_note(data):

    
    note = Note(
        title=data.get('title'),
        user_id=data.get('user_id'),
        content=data.get('content'),
        category=data.get('category'),
        priority=data.get('priority'),
        is_completed=data.get('is_completed', False),
        due_date=data.get('due_date')
      
    )
    logger.info(f"Creating note with title: {note.title} for user_id: {note.user_id}")
    return notes_repositories.create_note(note)

def get_all_notes(user_id):

    return notes_repositories.get_all_users_notes(user_id)

def get_notes_pagination(user_id, page, limit):

    return Note.query.filter_by(
        user_id=user_id
    ).paginate(
        page=page,
        per_page=limit,
        error_out=False
    ).items

def search_bytitle(title, user_id):

    return Note.query.filter(
        Note.user_id == user_id,
        Note.title.ilike(f"%{title}%")
    ).all()

def get_note_by_id(note_id, user_id):
        return notes_repositories.get_notes_by_id(note_id, user_id)

def update_note(note_id, data, user_id):
    note = notes_repositories.get_notes_by_id(note_id, user_id)
    if note:  
        note.title=data.get('title',note.title)
        note.content=data.get('content',note.content)
        note.category=data.get('category',note.category)
        note.priority=data.get('priority',note.priority)    
        note.is_completed=data.get('is_completed',note.is_completed)
        note.due_date=data.get('due_date',note.due_date)
        db.session.commit()
        return note
    return None

def delete_note(note_id, user_id):
    note = notes_repositories.get_notes_by_id(note_id, user_id)
    if note:
        notes_repositories.note_delete(note)
        return True
    return False