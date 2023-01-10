from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str()
    created_at = fields.DateTime()

class QuerySchema(Schema):
    userID = fields.Int()
