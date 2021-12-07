"""
Source: https://djangosnippets.org/snippets/1703/
"""
from django.conf import settings
from django.core.cache import caches

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _


def get_allowed_groups(groups_required):
    """
    Builds a list of all groups equal or higher to the provided groups
    This means checking for guest will also allow admins to access
    :param groups_required: list or tuple of groups
    :return: tuple of groups
    """
    groups_allowed = tuple(groups_required)
    if 'guest' in groups_required:
        groups_allowed = groups_allowed + ('user', 'admin')
    if 'user' in groups_required:
        groups_allowed = groups_allowed + ('admin',)
    return groups_allowed


def has_group_permission(user, groups):
    """
    Tests if a given user is member of a certain group (or any higher group)
    Superusers always bypass permission checks.
    Unauthenticated users cant be member of any group thus always return false.
    :param user: django auth user object
    :param groups: list or tuple of groups the user should be checked for
    :return: True if user is in allowed groups, false otherwise
    """
    if not user.is_authenticated:
        return False
    groups_allowed = get_allowed_groups(groups)
    if user.is_authenticated:
        if bool(user.groups.filter(name__in=groups_allowed)):
            return True
    return False


def group_required(*groups_required):
    """
    Decorator that tests the requesting user to be member
    of at least one of the provided groups or higher level groups
    :param groups_required: list of required groups
    :return: true if member of group, false otherwise
    """

    def in_groups(u):
        return has_group_permission(u, groups_required)

    return user_passes_test(in_groups, login_url='view_no_perm')
