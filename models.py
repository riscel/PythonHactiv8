
from config import db
from person_model import Person

class PersonSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Person
        sqla_session = db.session

    notes = fields.Nested('PersonNoteSchema', default=[], many=True)


class NoteSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Note
        sqla_session = db.session

    person = fields.Nested("NotePersonSchema", default=None)

