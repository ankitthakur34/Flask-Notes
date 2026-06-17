
from app.services import create_note, get_all_notes, get_note_by_id, update_note, delete_note
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import NoteCreateSchema, NoteUpdateSchema
from app.exceptions import note_exception
from app.services.note_service import get_notes_filter,restore_note_service,get_trashed_notes_service
from app.utils import success_response, error_response
from app.logging_config import logger
from app.extensions import redis_client
from app.decoraters import rate_limit

note_bp = Blueprint('note_bp', __name__)


@note_bp.route('/')
def home():
    return "Welcome to the Note API"

@note_bp.route("/redis-test")
@jwt_required()
def redis_test():

    redis_client.set(
        "test",
        "Hello Redis"
    )

    value = redis_client.get("test")

    return {
        "value": value
    }

@note_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note_route():
    """
    Create Note
    ---
    tags:
      - Notes

    security:
      - Bearer: []

    parameters:
      - in: body
        name: body

        schema:
          type: object

          required:
            - title
            - content

          properties:

            title:
              type: string

            content:
              type: string

            category:
              type: string

            priority:
              type: string

            due_date:
              type: string
              format: date-time

    responses:
      201:
        description: Note created

      400:
        description: Validation error
    """
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
        "created_by": user_id,  # IMPORTANT
        "updated_by": user_id,  # IMPORTANT

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
@rate_limit(5,60)
@jwt_required()
def get_notes_pagination_route():
    """
    Get All Notes
    ---
    tags:
      - Notes

    security:
      - Bearer: []

    parameters:
      - name: page
        in: query
        type: integer
        required: false

      - name: limit
        in: query
        type: integer
        required: false

    responses:
      200:
        description: List of notes

      401:
        description: Unauthorized
    """
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
@rate_limit(3,60)
@jwt_required()
def get_single_note(note_id):
    user_id = get_jwt_identity()
    note = get_note_by_id(note_id, user_id)
    logger.info(f"Note retrieved: {note['title']} by user: {user_id}")

    
    return success_response(
        data=note,
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
@note_bp.route("/notes/<int:note_id>/restore", methods=["POST"])
@jwt_required()
def restore_note(note_id):
    user_id = get_jwt_identity()
    note = restore_note_service(note_id, user_id)


    

    return success_response(
        data=note.to_dict(),
        message="Note restored successfully",
        status_code=200
    )

@note_bp.route("/notes/trash", methods=["GET"])
@jwt_required()
def get_trashed_notes():
    user_id = get_jwt_identity()
    notes = get_trashed_notes_service(user_id)
    logger.info(f"Trashed notes retrieved for user: {user_id}")
    return success_response(
        data=[note.to_dict() for note in notes],
        message="Trashed notes retrieved successfully",
        status_code=200
    )