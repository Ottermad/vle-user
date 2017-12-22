from flask import Blueprint, jsonify, g, request

from internal.decorators import permissions_required

from app.permissions.permission_functions import set_default_permissions, permission_create, permissions_list, \
    permission_detail, permission_delete, permission_update, \
    grant_permission, remove_permission, validate_permissions

permissions_blueprint = Blueprint('permissions', __name__, url_prefix='/permissions')


@permissions_blueprint.route('/set-defaults', methods=["POST"])
def set_defaults_view():
    return set_default_permissions(request)


@permissions_blueprint.route('/permission', methods=["POST", "GET"])
@permissions_required({'Administrator'})
def permission_listing_or_create_view():
    """Return a list of all permissions for a school or create a new one."""
    if request.method == "POST":
        return permission_create(request)
    else:
        return permissions_list(request)


@permissions_blueprint.route('/permission/<int:permission_id>', methods=["GET", "PUT", "DELETE"])
@permissions_required({'Administrator'})
def permission_detail_view(permission_id):
    if request.method == "GET":
        return permission_detail(request, permission_id)
    if request.method == "DELETE":
        return permission_delete(request, permission_id)
    if request.method == "PUT":
        return permission_update(request, permission_id)


@permissions_blueprint.route('/permission/grant', methods=["POST", "DELETE"])
@permissions_required({'Administrator'})
def grant_or_remove_permission_view():
    """Grant a permission to a user."""
    if request.method == "POST":
        return grant_permission(request)
    elif request.method == "DELETE":
        return remove_permission(request)


@permissions_blueprint.route('/validate', methods=("POST",))
def validate():
    return validate_permissions(request)
