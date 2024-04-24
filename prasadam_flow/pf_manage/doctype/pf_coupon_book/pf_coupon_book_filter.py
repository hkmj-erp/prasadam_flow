import frappe
from prasadam_flow.constants import FILTER_EXCLUDE_ROLES


def list_filter(user):
    if not user:
        user = frappe.session.user

    user_roles = frappe.get_roles(user)

    full_access = any(role in FILTER_EXCLUDE_ROLES for role in user_roles)

    if full_access:
        return "( 1 )"

    return f" ( custodian = '{user}' ) "


def single(doc, user=None, permission_type=None):
    if not user:
        user = frappe.session.user

    user_roles = frappe.get_roles(user)

    full_access = any(role in FILTER_EXCLUDE_ROLES for role in user_roles)

    if full_access or doc.custodian == user:
        return True

    return False
