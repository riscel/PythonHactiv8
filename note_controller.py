from note_model import Note, NoteSchema
from person_model import Person
from config import db

# GET /notes
def read_all():
    notes = Note.query.outerjoin(Person).all()
    # notes = Note.query.all()
    note_schema = NoteSchema(many=True)
    return note_schema.dump(notes)
    # GET /notes

def read_one(person_id, note_id):
    note = (Note.query #.outerjoin(Person).all()
                .filter(Note.note_id == note_id)
                .filter(Person.person_id == person_id)
                .one_or_none()
    )

    if note is None:
        abort (404, f"note with id {note_id} own by person {person_id} is not found")
    else:
        note_schema = NoteSchema()
        result=note_schema.dump(note)
        return result


    print(note, "<<<<<<<<")
    # notes = Note.query.all()
    
# POST /people/{person_id}/notes
# GET / people/{person_id}/notes/{note_id}
# PUT / people/{person_id}/notes/{note_id}
# DELETE / people/{person_id}/notes/{note_id}

def update(note_id, person_id, note):
    found_note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
                .filter(Note.note_id == note_id)
                # .filter(Person.person_id =person_id)
                .one_or_none()
    )
    print(note, "<<<<<<<<")

    if found_note is None:
        abort (404, f"note with id {note_id} own by person {person_id} is not found")
    
    content = note.get('content')
    found_note.update(content)

    # notes = Note.query.all()
    note_schema = NoteSchema()
    result = note_schema.dump(found_note)

    return result
    
def create(person_id,note):
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    if person is None:
        abort (404, f"Person with id {person_id} is not found")
    content = note.get('content')
    new_note = Note(content=content, person_id=person_id)
    
    person.notes.append(new_note)
    person.save()
    note_schema = NoteSchema()
    result = note_schema.dump(new_note)
    return result

# def delete(note_id):
#     del_note = Note.query.get(note_id)
#     if del_note is None:
#         abort(404,
#               f"Note with id {note_id} is not found!")
#     else:
#         schema = NoteSchema()
#         db.session.delete(del_note)
#         db.session.commit()
#         return schema.dump(del_note)