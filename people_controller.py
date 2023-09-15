from flask import make_response, abort
from config import db
from person_model import Person, PersonSchema
from note_model import Note

def read_all():
    people = Person.query.all()
    person_schema = PersonSchema(many=True)
    return person_schema.dump(people)

def read_one(person_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {person_id}")

def update(person_id, person_data):
    updated_person = Person.query.get(person_id)
    if updated_person is None:
        abort(404,
              f"Person with id {person_id} is not found!")
    else:
        schema = PersonSchema()
        updated_person.fname = person_data['fname']
        updated_person.lname = person_data['lname']
        db.session.merge(updated_person)
        db.session.commit()
        return schema.dump(updated_person)
        

def create(person):
    # new_person = Person.query.get(person_data['person_id'])
    # person = Person.query.add(person_id, lname, fname)
    # if new_person is None:
        schema = PersonSchema()
        new_person = Person (
            fname = person['fname'],
            lname = person['lname']
        )
        db.session.add(new_person)
        db.session.commit()
        return schema.dump(new_person)
    # else:
    #     abort(404,
    #           f"Person with id {person_id} already exist!")


def delete(person_id):
    del_person = Person.query.get(person_id)
    if del_person is None:
        abort(404,
              f"Person with id {person_id} is not found!")
    else:
        schema = PersonSchema()
        db.session.delete(del_person)
        db.session.commit()
        return schema.dump(del_person)
        


