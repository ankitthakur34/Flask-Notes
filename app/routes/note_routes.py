
from app.services import create_note, get_all_notes, get_note_by_id, update_note, delete_note, get_notes_pagination, search_bytitle
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import NoteCreateSchema, NoteUpdateSchema
from app.exceptions import note_exception


note_bp = Blueprint('note_bp', __name__)

@note_bp.route('/')
def home():
    return "Welcome to the Note API"

@note_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note_route():
    user_id = get_jwt_identity()
    
    data = NoteCreateSchema().load(
        request.get_json()
    )

    note_data = {
       "title": data.get("title"),
        "content": data.get("content"),
        "category": data.get("category"),
        "priority": data.get("priority"),
        "is_completed": data.get("is_completed", False),
        "due_date": data.get("due_date"),

        # IMPORTANT
        "user_id": user_id
    }
   
    note = create_note(note_data)
    return {
        'message': 'Note created successfully',
        'note': note.to_dict()
    },201

@note_bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes_route():
    user_id = get_jwt_identity()
    notes = get_all_notes(user_id)
    return {
        'notes': [note.to_dict() for note in notes]
    }
@note_bp.route('/notes/pagination', methods=['GET'])
@jwt_required()
def get_notes_pagination_route():
    user_id = get_jwt_identity()
    s=request.args.get('s',default=1,type=int)
    l=request.args.get('l',default=5,type=int)
    notes = get_notes_pagination(user_id, s, l)
    return {
        'notes': [note.to_dict() for note in notes]
    }

@note_bp.route('/notes/search', methods=['GET'])
@jwt_required()
def search_notes_route():
    user_id = get_jwt_identity()
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400
    notes = search_bytitle(title, user_id)
    return {
        'notes': [note.to_dict() for note in notes]
    }

# Get Single Note
@note_bp.route("/notes/<int:note_id>", methods=["GET"])
@jwt_required()
def get_single_note(note_id):
    user_id = get_jwt_identity()
    note = get_note_by_id(note_id, user_id)
    if not note:

        raise note_exception.NoteNotFoundException()

    return note.to_dict()


# Update Note
@note_bp.route("/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def edit_note(note_id):
    user_id = get_jwt_identity()
    data = NoteUpdateSchema().load(request.get_json())

    note = update_note(note_id, data,user_id)

    if not note:

        raise note_exception.NoteNotFoundException()

    return {
        "message": "Note updated",
        "note": note.to_dict()
    }


# Delete Note
@note_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def remove_note(note_id):
    user_id = get_jwt_identity()
    deleted = delete_note(note_id,user_id)

    if not deleted:

        raise note_exception.NoteNotFoundException()

    return {
        "message": "Note deleted"
    }