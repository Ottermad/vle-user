from app import db
from internal.exceptions import FieldInUseError, BlankValueError
from internal.helper import get_record_by_id, json_from_request, check_keys, check_values_not_blank
from app.user.models import Form
from flask import g, jsonify


def create_form(request):
    expected_keys = ["name"] # Keys expected to be in JSON
    data = json_from_request(request) # Fetch JSON from request
    check_keys(expected_keys, data) # Check keys are in JSON
    check_values_not_blank(expected_keys, data) # Check values are not blank

    # Create Form object
    form = Form(name=data['name'], school_id=g.user.school_id)

    # Add form to db
    db.session.add(form)
    db.session.commit()

    # Return JSON
    return jsonify({'success': True, 'form': form.to_dict()}), 201


def list_forms(request):
    # Query all forms which are in user's school
    forms = Form.query.filter_by(school_id=g.user.school_id).all()

    # Covert Query object into list of dictionaries so it is JSON serialisable
    form_list = [f.to_dict() for f in forms]

    # Return JSON
    return jsonify({'success': True, 'forms': form_list})


def edit_form(request, form_id):
    data = json_from_request(request) # Get data from request
    form = get_record_by_id(form_id, Form) # Get form by id (this automatically checks school_id is the same as the g.user)

    # Check name key is in JSON
    if "name" in data.keys():
        # Check name is not blank
        if data['name'].strip() == "":
            raise BlankValueError("name")

        # Update form data
        form.name = data['name']

    # Update DB
    db.session.add(form)
    db.session.commit()

    # Return JSON
    return jsonify({'success': True, 'message': 'Updated.'})


def form_detail(request, form_id):
    # Get form by id from URL
    # this function will throw a 404 error if id not found and a 409 error if form.school_id != g.user.school_id
    form = get_record_by_id(form_id, Form)

    # Return JSON
    return jsonify({'success': True, 'form': form.to_dict()})


def delete_form(request, form_id):
    # Get Form using id
    form = get_record_by_id(form_id, Form)

    # Delete from DB
    db.session.delete(form)
    db.session.commit()

    # Return JSON
    return jsonify({'success': True, 'message': 'Deleted.'})
