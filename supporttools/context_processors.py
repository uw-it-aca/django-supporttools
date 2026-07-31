# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging

from django.conf import settings
from django.urls import NoReverseMatch, reverse
from userservice.user import UserService

logger = logging.getLogger(__name__)


def _normalize_mode_fields(entry):
    # Treat entries with SPA markers as converted tools, even if mode is
    # omitted. Legacy server tools do not include these fields.
    is_converted = any(
        entry.get(key) for key in ("route", "component_key", "vite_entry")
    )
    mode = entry.get("mode", "server")
    if mode not in {"server", "spa"}:
        mode = "server"
    if is_converted:
        mode = "spa"

    route = entry.get("route")
    component_key = entry.get("component_key")
    # Converted tools are SPA-only; full reload is not supported for them.
    requires_full_reload = False

    # A SPA entry must declare both route and component_key. Converted tools
    # that fail this contract are dropped from the Vue registry.
    if mode == "spa" and not (route and component_key):
        logger.warning(
            "Skipping invalid SPA supporttools registry entry %r: "
            "route and component_key are required for converted tools.",
            entry.get("id") or entry.get("url_name") or entry.get("label"),
        )
        return None

    return {
        "mode": mode,
        "route": route,
        "component_key": component_key,
        "requires_full_reload": requires_full_reload,
    }


def _resolve_url(url_name, url_args=None, url_kwargs=None):
    try:
        return reverse(url_name, args=url_args or (), kwargs=url_kwargs or {})
    except NoReverseMatch:
        return None


def _default_view_registry(request):
    entries = []
    defaults = [
        (10, "Support Home", "supporttools_home"),
        (20, "User Override", "userservice_override"),
        (30, "Status", "status_app.views.status"),
        (40, "Persistent Messages", "manage_persistent_messages"),
        (50, "Browse Student Web Service", "restclients_proxy",
         ("sws", "student/v5.json"), {}),
        (60, "Browse Person Web Service", "restclients_proxy",
         ("pws", "identity/v2.json"), {}),
    ]

    for row in defaults:
        if len(row) == 3:
            order, label, url_name = row
            url_args = ()
            url_kwargs = {}
        else:
            order, label, url_name, url_args, url_kwargs = row

        url = _resolve_url(url_name, url_args=url_args, url_kwargs=url_kwargs)
        if url:
            entries.append({
                "id": url_name,
                "section": "general",
                "order": order,
                "label": label,
                "url_name": url_name,
                "url": url,
                "url_args": list(url_args),
                "url_kwargs": url_kwargs,
                "mode": "server",
                "route": None,
                "component_key": None,
                "requires_full_reload": False,
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
            "mode": "server",
            "route": None,
            "component_key": None,
            "requires_full_reload": False,
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

        mode_fields = _normalize_mode_fields(entry)
        if not mode_fields:
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
            **mode_fields,
        })

    return entries


def _effective_view_registry(request):
    # Structured VIEW_REGISTRY (preferred) and legacy EXTRA_VIEWS are both
    # always included so that enabling SUPPORTTOOLS_VUE_ENABLED alone is
    # sufficient for apps that already have SUPPORTTOOLS_EXTRA_VIEWS set.
    # VIEW_REGISTRY entries take precedence; duplicates are dropped by url_name.
    structured = _settings_view_registry(request)
    legacy = _extra_views_registry(request)

    seen = {e["url_name"] for e in structured}
    merged = structured + [e for e in legacy if e["url_name"] not in seen]

    seen.update(e["url_name"] for e in merged)
    defaults = _default_view_registry(request)
    combined = [e for e in defaults if e["url_name"] not in seen] + merged
    return sorted(combined, key=lambda e: (e["section"], e["order"],
                                           e["label"].lower()))


def supportools_globals(request):
    user = UserService().get_original_user()
    view_registry = _effective_view_registry(request)
    user_agent = getattr(request, "user_agent", None)

    params = {
        "supporttools_user": user,
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
            "user": user,
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
