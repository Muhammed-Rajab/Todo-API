from bson import ObjectId as BSONObjectID

# ObjectID Class
class ObjectId(BSONObjectID):
    """
        Class to get ObjectID and validate it using pydantic
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not BSONObjectID.is_valid(v):
            raise ValueError("Invalid objectid")
        return BSONObjectID(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")