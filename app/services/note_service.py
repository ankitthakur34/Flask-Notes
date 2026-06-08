
from app.extensions import db
from app.models.note_model import Note
from datetime import datetime

def create_note(data):

    due_date = None

    if data.get("due_date"):
        try:
            due_date = datetime.fromisoformat(
                data.get("due_date")
            )
        except ValueError:
            raise ValueError(
                "Invalid due_date format. Use YYYY-MM-DDTHH:MM:SS"
            )

    note = Note(
        title=data.get('title'),
        user_id=data.get('user_id'),
        content=data.get('content'),
        category=data.get('category'),
        priority=data.get('priority'),
        is_completed=data.get('is_completed', False),
        due_date=due_date
      
    )
    db.session.add(note)
    db.session.commit()
    
    return note

def get_all_notes(user_id):

    return Note.query.filter_by(
        user_id=user_id
    ).all()

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
        return Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()

def update_note(note_id, data, user_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()
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
    note = Note.query.filter_by(
        id=note_id,
        user_id=user_id
    ).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        return True
    return False