
from app.services import create_note, get_all_notes, get_note_by_id, update_note, delete_note
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import NoteCreateSchema, NoteUpdateSchema
from app.exceptions import note_exception
from app.services.note_service import get_notes_filter
from app.utils import success_response, error_response
from app.logging_config import logger


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
   
    logger.info(f"Note created: {note.title} by user: {user_id}")
    return success_response(
        data=note.to_dict(),
        message="Note created successfully",
        status_code=201
    )

# @note_bp.route('/notes', methods=['GET'])
# @jwt_required()
# def get_notes_route():
#     user_id = get_jwt_identity()
#     notes = get_all_notes(user_id)
#     return {
#         'notes': [note.to_dict() for note in notes]
#     }
@note_bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes_pagination_route():
    user_id = get_jwt_identity()

    page=request.args.get('page',default=1,type=int)
    limit=request.args.get('limit',default=10,type=int)

    priority = request.args.get("priority")

    search = request.args.get("search")

    sort = request.args.get(
        "sort",
        default="desc"
    )


    notes = get_notes_filter(
        user_id=user_id,
        page=page,
        limit=limit,
        priority=priority,
        search=search,
        sort=sort
    )
    logger.info(f"Notes retrieved for user: {user_id} - Page: {page}, Limit: {limit}, Priority: {priority}, Search: {search}, Sort: {sort}")
    return success_response(
        data={
            "page": page,
            "limit": limit,
            "total": notes.total,
            "pages": notes.pages,
            "notes": [
                note.to_dict()
                for note in notes.items
            ]
        },
        message="Notes retrieved successfully",
        status_code=200
    )


# Get Single Note
@note_bp.route("/notes/<int:note_id>", methods=["GET"])
@jwt_required()
def get_single_note(note_id):
    user_id = get_jwt_identity()
    note = get_note_by_id(note_id, user_id)
    logger.info(f"Note retrieved: {note.title} by user: {user_id}")

    
    return success_response(
        data=note.to_dict(),
        message="Note retrieved successfully",
        status_code=200
    )


# Update Note
@note_bp.route("/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def edit_note(note_id):
    user_id = get_jwt_identity()
    data = NoteUpdateSchema().load(request.get_json())

    note = update_note(note_id, data,user_id)

    logger.info(f"Note updated: {note.title} by user: {user_id}")

    return success_response(
        data=note.to_dict(),
        message="Note updated",
        status_code=200
    )


# Delete Note
@note_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def remove_note(note_id):
    user_id = get_jwt_identity()
    deleted = delete_note(note_id,user_id)
    logger.info(f"Note deleted: ID {note_id} by user: {user_id}")
    return success_response(
        data=None,
        message="Note deleted",
        status_code=200
    )