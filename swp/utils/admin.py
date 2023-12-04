from typing import Type

from django.contrib import admin
from django.db.models import Model
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html

DEFAULT_LINK_TEMPLATE = '<a href="{url}">{label}</a>'


def admin_url(model: Type[Model], view: str, *args, site=None, **kwargs) -> str:
    """
    Return an url to an admin view.
    """

    return reverse(admin_url_name(model, view, site=site), args=args, kwargs=kwargs)


def admin_redirect(model: Type[Model], view: str, *args, site=None, **kwargs) -> HttpResponseRedirect:
    return redirect(admin_url_name(model, view, site=site), *args, **kwargs)


def admin_url_name(model: Type[Model], view: str, *, site=None) -> str:
    namespace = (site or admin.site).name
    view_name = admin_view_name(model, view)

    return f'{namespace}:{view_name}'


def admin_view_name(model: Type[Model], view: str) -> str:
    return f'{model._meta.app_label}_{model._meta.model_name}_{view}'


def admin_path(model_admin: admin.ModelAdmin, route, view, name):
    name = admin_view_name(model_admin.model, name)
    view = model_admin.admin_site.admin_view(view)

    return path(route, view, name=name)


def admin_link(obj: Model, view='change', site=None, label=None, template=DEFAULT_LINK_TEMPLATE):
    url = admin_url(type(obj), view, obj.pk, site=site)

    return format_html(template, url=url, obj=obj, label=label or obj)
