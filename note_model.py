from datetime import datetime
from config import db, ma
from marshmallow import fields

class Note(db.Model):
    __tablename__ = 'note'

    note_id = db.Column(db.Integer, primary_key=True)
    person_id =  db.Column(db.Integer, db.ForeignKey("person.person_id"))
    content = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def update(self,update_content):
        self.content=update_content
        db.session.merge(self)
        db.session.commit()

class NotePersonSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    person_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.Str()

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        sqla_session = db.session 
    person = fields.Nested(NotePersonSchema,default=None)

