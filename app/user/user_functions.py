from app import db
from internal.exceptions import FieldInUseError, CustomError
from internal.helper import get_boolean_query_param, json_from_request, check_keys, get_record_by_id, check_values_not_blank
from app.user.models import Form
from flask import jsonify, g
from .models import User
from flask_bcrypt import check_password_hash


def authenticate(request):
    #  Decode the JSON data
    data = json_from_request(request)

    # Validate data
    expected_keys = ["username", "password"]
    check_keys(expected_keys, data)
    check_values_not_blank(expected_keys, data)
    username = data['username']
    password = data['password']

    # Check username
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise CustomError(401, message='Username or password were not found.')

    # Check password
    if not check_password_hash(user.password, password):
        raise CustomError(401, message='Username or password were not found.')

    return jsonify({'success': True, 'user': user.to_dict(nest_permissions=True)})


def user_listing(request):
    # Get parameters from query string
    nest_permissions = get_boolean_query_param(request, 'nest-permissions')
    nest_forms = get_boolean_query_param(request, 'nest-forms')

    # Query database and get users in same school
    users = User.query.filter_by(school_id=g.user.school_id)

    # Create a list containing each user as a dictionary
    users_list = [
        u.to_dict(
            nest_permissions=nest_permissions,
            nest_form=nest_forms
        ) for u in users
        ]

    # Return as JSON
    return jsonify({'success': True, 'users': users_list})


def user_create(request):
    #  Decode the JSON data
    data = json_from_request(request)

    # Validate data
    expected_keys = ["first_name", "last_name", "password", "username", "email"] # List of keys which need to in JSON
    check_keys(expected_keys, data) # Checks keys are in JSON
    check_values_not_blank(expected_keys, data) # Check that values for the keys are not blank

    # Check email is not in use.
    if User.query.filter_by(email=data['email']).first() is not None:
        raise FieldInUseError("email")

    # Check username is not in use in that school.
    if User.query.filter_by(username=data['username'], school_id=g.user.school_id).first() is not None:
        raise FieldInUseError("username")

    # Create user
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        username=data['username'],
        school_id=g.user.school_id
    )

    if "form_id" in data.keys():
        # Validate form id
        form = get_record_by_id(data["form_id"], Form, custom_not_found_error=CustomError(409, message="Invalid form_id."))
        # Set user's form_id
        user.form_id = form.id

    # Add user to db
    db.session.add(user)
    db.session.commit()

    # Return JSON
    return jsonify({"success": True, "user": user.to_dict()}), 201


def user_update(request, user_id):
    # Get JSON data
    data = json_from_request(request)

    # Get User object from id in url
    user = get_record_by_id(user_id, User)

    # Check that
    check_values_not_blank(data.keys(), data)

    if "first_name" in data.keys():
        user.first_name = data['first_name']

    if "last_name" in data.keys():
        user.first_name = data['first_name']

    if "password" in data.keys():
        user.password = user.generate_password_hash(data['password'])

    if "email" in data.keys():
        if user.email != data['email'] and User.query.filter_by(email=data['email']).first() is not None:
            raise FieldInUseError("email")
        user.email = data['email']

    if "username" in data.keys():
        if user.username != data['username'] and User.query.filter_by(username=data['username'], school_id=g.user.school_id).first() is not None:
            raise FieldInUseError("username")
        user.username = data['username']

    if "form_id" in data.keys():
        # Validate form id
        form = get_record_by_id(data["form_id"], Form,
                                custom_not_found_error=CustomError(409, message="Invalid form_id."))
        user.form_id = form.id

    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Updated.'})


def user_delete(request, user_id):
    # Get user object using id from URL
    user = get_record_by_id(user_id, User)

    # Delete user
    db.session.delete(user)
    db.session.commit()

    # Return success message
    return jsonify({'success': True, 'message': 'Deleted.'})


def user_detail(request, user_id):
    # Get user by id
    user = get_record_by_id(user_id, User)

    # Get query params
    nest_permissions = get_boolean_query_param(request, 'nest-permissions')

    # Return user
    return jsonify({
        'success': True,
        "user": user.to_dict(
            nest_permissions=nest_permissions
        )
    })


def current_user_details(request):
    nest_permissions = get_boolean_query_param(request, 'nest-permissions')

    user = get_record_by_id(g.user.id, User)

    user_dict = user.to_dict(
        nest_permissions=nest_permissions
    )
    return jsonify({'success': True, 'user': user_dict})
