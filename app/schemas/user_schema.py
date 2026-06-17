from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    ValidationError
)


class RegisterSchema(Schema):

    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=50)
    )

    email = fields.Email(
        required=True
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=8)
    )
    

    @validates("username")
    def validate_username(self, value, **kwargs):

        if " " in value:
            raise ValidationError(
                "Username cannot contain spaces"
            )


class LoginSchema(Schema):

    email = fields.Email(
        required=True
    )

    password = fields.String(
        required=True
    )