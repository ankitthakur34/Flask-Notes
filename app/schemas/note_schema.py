from marshmallow import Schema, fields,validates, ValidationError
from datetime import datetime

class NoteCreateSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    @validates("title")
    def validate_title(self, value, **kwargs):
        if len(value.strip()) < 3:
            raise ValidationError(
                "Title must be at least 3 characters long"
            )
    content = fields.Str(required=True)
    category = fields.Str()
    priority = fields.Str()
    is_completed = fields.Bool()
    due_date = fields.DateTime()
    @validates("due_date")
    def validate_due_date(self, value, **kwargs):
        if value < datetime.utcnow():
            raise ValidationError(
                "Due date cannot be in the past"
            )
        


        
        

class NoteUpdateSchema(Schema):

    title = fields.String()

    content = fields.String()

    category = fields.String()

    priority = fields.String()

    is_completed = fields.Boolean()

    due_date = fields.DateTime()

    @validates("title")
    def validate_title(self, value, **kwargs):

        if len(value.strip()) < 3:
            raise ValidationError(
                "Title must be at least 3 characters"
            )    