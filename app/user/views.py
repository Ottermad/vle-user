from internal.decorators import permissions_required
from internal.exceptions import UnauthorizedError
from app.user.form_functions import create_form, list_forms, edit_form, \
    delete_form, form_detail
from app.user.user_functions import user_listing, user_create, \
    current_user_details, user_update, user_detail, user_delete, authenticate
from flask import Blueprint, request, g
from app import services

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


@user_blueprint.route("/")
def index_view():
    return "User Index"


@user_blueprint.route("/test")
def test():
    response = services.user.get('user')
    return 'forwarding: {}'.format(str(response))


@user_blueprint.route("/user", methods=["GET", "POST"])
def user_listing_or_create_view():
    """Route to create User from a POST request."""
    if request.method == "GET":
        return user_listing(request)

    if request.method == "POST":
        if g.user.has_permissions({'Administrator'}):
            return user_create(request)
        raise UnauthorizedError()


@user_blueprint.route("/user/<int:user_id>", methods=["PUT", "GET", "DELETE"])
def user_update_or_delete(user_id):
    if request.method == "PUT":
        return user_update(request, user_id)

    if request.method == "GET":
        return user_detail(request, user_id)

    if request.method == "DELETE":
        return user_delete(request, user_id)


@user_blueprint.route("/me")
def current_user_detail_view():
    return current_user_details(request)


@user_blueprint.route("/form", methods=("POST", "GET"))
@permissions_required({'Administrator'})
def form_listing_or_create():
    if request.method == "POST":
        return create_form(request)
    return list_forms(request)


@user_blueprint.route("/form/<int:form_id>", methods=("GET", "PUT", "DELETE"))
@permissions_required({"Administrator"})
def form_detail_update_delete(form_id):
    if request.method == "GET":
        return form_detail(request, form_id)

    if request.method == "PUT":
        return edit_form(request, form_id)

    if request.method == "DELETE":
        return delete_form(request, form_id)


@user_blueprint.route("/authenticate", methods=("POST",))
def authenticate_view():
    return authenticate(request)
