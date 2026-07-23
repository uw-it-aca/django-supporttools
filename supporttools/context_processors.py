# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import NoReverseMatch, reverse
from userservice.user import UserService


def _resolve_url(url_name, url_args=None, url_kwargs=None):
    try:
        return reverse(url_name, args=url_args or (), kwargs=url_kwargs or {})
    except NoReverseMatch:
        return None


def _default_view_registry(request):
    entries = []
    defaults = [
        ("Support Home", "supporttools_home"),
        ("User Override", "userservice_override"),
        ("Status", "status_app.views.status"),
        ("Persistent Messages", "manage_persistent_messages"),
        ("Browse Student Web Service", "restclients_proxy",
         ("sws", "student/v5.json"), {}),
        ("Browse Person Web Service", "restclients_proxy",
         ("pws", "identity/v2.json"), {}),
    ]

    for row in defaults:
        if len(row) == 2:
            label, url_name = row
            url_args = ()
            url_kwargs = {}
        else:
            label, url_name, url_args, url_kwargs = row

        url = _resolve_url(url_name, url_args=url_args, url_kwargs=url_kwargs)
        if url:
            entries.append({
                "id": url_name,
                "section": "general",
                "order": 0,
                "label": label,
                "url_name": url_name,
                "url": url,
                "url_args": list(url_args),
                "url_kwargs": url_kwargs,
            })

    return entries


def _extra_views_registry(request):
    entries = []
    extra_views = getattr(settings, "SUPPORTTOOLS_EXTRA_VIEWS", {})

    for label, url_name in extra_views.items():
        url = _resolve_url(url_name)
        if not url:
            continue

        entries.append({
            "id": url_name,
            "section": "application",
            "order": 100,
            "label": label,
            "url_name": url_name,
            "url": url,
            "url_args": [],
            "url_kwargs": {},
        })

    return entries


def _settings_view_registry(request):
    entries = []
    raw_registry = getattr(settings, "SUPPORTTOOLS_VIEW_REGISTRY", [])

    for entry in raw_registry:
        if not isinstance(entry, dict):
            continue

        label = entry.get("label")
        url_name = entry.get("url_name")
        if not label or not url_name:
            continue

        url_args = entry.get("url_args", [])
        url_kwargs = entry.get("url_kwargs", {})
        url = _resolve_url(url_name, url_args=url_args, url_kwargs=url_kwargs)
        if not url:
            continue

        entries.append({
            "id": entry.get("id") or url_name,
            "section": entry.get("section") or "application",
            "order": int(entry.get("order", 100)),
            "label": label,
            "url_name": url_name,
            "url": url,
            "url_args": list(url_args),
            "url_kwargs": dict(url_kwargs),
        })

    return entries


def _effective_view_registry(request):
    # If registry is configured, prefer it. Otherwise adapt legacy extra views.
    configured = _settings_view_registry(request)
    if configured:
        extra_entries = configured
    else:
        extra_entries = _extra_views_registry(request)

    combined = _default_view_registry(request) + extra_entries
    return sorted(combined, key=lambda e: (e["section"], e["order"],
                                           e["label"].lower()))


def supportools_globals(request):
    view_registry = _effective_view_registry(request)
    user_agent = getattr(request, "user_agent", None)

    params = {
        "supporttools_user": UserService().get_original_user(),
        "supporttools_parent_app": getattr(settings,
                                           "SUPPORTTOOLS_PARENT_APP", ""),
        "supporttools_parent_app_url": getattr(settings,
                                               "SUPPORTTOOLS_PARENT_APP_URL",
                                               "/"),
        "supporttools_extra_views": getattr(settings,
                                            "SUPPORTTOOLS_EXTRA_VIEWS", {}),
        "supporttools_vue_enabled": getattr(settings,
                                             "SUPPORTTOOLS_VUE_ENABLED",
                                             False),
        "supporttools_view_registry": view_registry,
        "supporttools_vue_context": {
            "parent_app": getattr(settings, "SUPPORTTOOLS_PARENT_APP", ""),
            "parent_app_url": getattr(settings,
                                       "SUPPORTTOOLS_PARENT_APP_URL", "/"),
            "user": UserService().get_original_user(),
            "is_mobile": bool(getattr(user_agent, "is_mobile", False)),
            "is_tablet": bool(getattr(user_agent, "is_tablet", False)),
            "is_desktop": bool(getattr(user_agent, "is_pc", False)),
            "links": view_registry,
        },
    }
    return (params)


def has_less_compiled(request):
    """ See if django-compressor is being used to precompile less
    """
    key = getattr(settings, "COMPRESS_PRECOMPILERS", None)
    has_less_precompiler = False
    if key is not None and len(key) > 0:
        for entry in key:
            if entry[0] == "text/less":
                has_less_precompiler = True
    return {"has_less_compiled": has_less_precompiler}


def has_google_analytics(request):
    ga_key = getattr(settings, 'GOOGLE_ANALYTICS_KEY', False)
    return {
        'GOOGLE_ANALYTICS_KEY': ga_key,
        'has_google_analytics': ga_key
    }
