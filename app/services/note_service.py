
from app.extensions import db
from app.models.note_model import Note
from datetime import datetime
from app.repositories import notes_repositories
from app.logging_config import logger
from app.exceptions import note_exception
from app.cache import get_cached_note, set_cached_note, delete_cached_note


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

# note_service.py



def get_notes_filter(
    user_id,
    page=1,
    limit=10,
    priority=None,
    search=None,
    sort="desc"
):

    query = notes_repositories.get_notes_query(user_id)

    # Filtering
    if priority:
        query = query.filter(
            Note.priority.ilike(priority)
        )

    # Search
    if search:
        query = query.filter(
            Note.title.ilike(f"%{search}%")
        )

    # Sorting
    if sort == "asc":
        query = query.order_by(
            Note.created_at.asc()
        )
    else:
        query = query.order_by(
            Note.created_at.desc()
        )

    return query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )

def get_notes_pagination(user_id, page, limit):

    return Note.query.filter_by(
        user_id=user_id
    ).paginate(
        page=page,
        per_page=limit,
        error_out=False
    ).items



def get_note_by_id(note_id, user_id):
        get_cached = get_cached_note(user_id, note_id)
        if get_cached:
            logger.info(f"Cache hit for note_id: {note_id} and user_id: {user_id}")
            return get_cached
        logger.info(f"Cache miss for note_id: {note_id} and user_id: {user_id}")
        note = notes_repositories.get_note_by_id(note_id, user_id)
        set_cached_note(user_id, note_id, note.to_dict())
        return note.to_dict()

def update_note(note_id, data, user_id):
    note = notes_repositories.get_note_by_id(note_id, user_id)
    
    note.title=data.get('title',note.title)
    note.content=data.get('content',note.content)
    note.category=data.get('category',note.category)
    note.priority=data.get('priority',note.priority)    
    note.is_completed=data.get('is_completed',note.is_completed)
    note.due_date=data.get('due_date',note.due_date)
    note.updated_by = user_id
    db.session.commit()
    delete_cached_note(user_id, note_id)
    return note
    

def delete_note(note_id, user_id):
    note = notes_repositories.get_note_by_id(note_id, user_id)
   
    notes_repositories.note_delete(note,user_id)
    delete_cached_note(user_id, note_id)
    return True

def restore_note_service(note_id, user_id):
    note = notes_repositories.restore_note(note_id, user_id)
    delete_cached_note(user_id, note_id)
    
    
    return note

def get_trashed_notes_service(user_id):
    return Note.query.filter_by(
        user_id=user_id,
        is_deleted=True
    ).all()
    