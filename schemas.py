from marshmallow import Schema, fields, validate


class StudentSchema(Schema):
    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    last_name = fields.Str(required=True)

    email = fields.Email(required=True)

    age = fields.Int(
        required=True,
        validate=validate.Range(min=10, max=100)
    )