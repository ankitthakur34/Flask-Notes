

from app.services import get_note_by_id
from flask import Blueprint,request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.note_service import get_notes_filter
from app.utils import success_response
from app.logging import logger
from app.decoraters import rate_limit


note_v2_bp = Blueprint(
    "notes_v2",
    __name__,
    url_prefix="/api/v2"
)

@note_v2_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return "Welcome to the Notes Dashboard API v2"

@note_v2_bp.route("/notes/<int:note_id>", methods=["GET"])
@rate_limit(3,60)
@jwt_required()
def get_single_note(note_id):
    user_id = get_jwt_identity()
    note = get_note_by_id(note_id, user_id)
    logger.info(f"Note retrieved: {note['title']} by user: {user_id}")

    return success_response(
        data=note,
        message="Note retrieved successfully with API v2",
        status_code=200
    )

@note_v2_bp.route('/notes', methods=['GET'])
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
            "notes_v2": [
                note.to_dict()
                for note in notes.items
            ]
        },
        message="Notes retrieved successfully with API v2",
        status_code=200
    )