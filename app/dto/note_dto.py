class NoteDTO:

    @staticmethod
    def to_response(note):
         return {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "category": note.category,
            "priority": note.priority,
            "is_completed": note.is_completed,
            "due_date": (
                note.due_date.isoformat()
                if note.due_date
                else None
            ),
            "created_at": (
                note.created_at.isoformat()
                if note.created_at
                else None
            )
        }