# Django Support Tools

[![Build Status](https://github.com/uw-it-aca/django-supporttools/workflows/tests/badge.svg)](https://github.com/uw-it-aca/django-supporttools/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/django-supporttools/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/django-supporttools?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/django-supporttools.svg)](https://pypi.python.org/pypi/django-supporttools)
![Python versions](https://img.shields.io/badge/python-3.12-blue.svg)


A Django application used for theming and wrapping support tools.

### Installation

This should be installed as a dependency in your project.  You should not install this manually.

### Configuration

Add these values to your project's settings.py:

```
MIDDLEWARE = [
    ...
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

INSTALLED_APPS = [
    ...
    'supporttools',
    'userservice',
    'compressor',
    'django_user_agents',
]

TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                ...
                'django.template.context_processors.request',
                'supporttools.context_processors.supportools_globals',
                'supporttools.context_processors.has_less_compiled',
            ],
        },
    },
]

# Where the back link should go, and how it's labeled.
SUPPORTTOOLS_PARENT_APP = "TestApp"
SUPPORTTOOLS_PARENT_APP_URL = "/"

# Optional: enable Vue-powered supporttools navigation shell.
# Keep False during migration to preserve legacy behavior.
SUPPORTTOOLS_VUE_ENABLED = False

# Optional: Vite manifest location for Vue bundle assets.
VITE_MANIFEST_PATH = '/static/manifest.json'

# Optional: new structured link registry (preferred over EXTRA_VIEWS
# when configured).
SUPPORTTOOLS_VIEW_REGISTRY = [
    {
        "id": "app-tool-1",
        "section": "application",
        "order": 10,
        "label": "Example Tool",
        "url_name": "example_tool",
        "url_args": [],
        "url_kwargs": {},
    }
]
```

### Migrating jQuery-Based Tools to Vue

Apps that use `django-supporttools` can migrate gradually. The intent is to
avoid a large rewrite and keep existing tool URLs and wrappers working while
you move page logic from jQuery to Vue.

#### Recommended Migration Strategy

1. **Keep supporttools in legacy mode first**
     - Leave `SUPPORTTOOLS_VUE_ENABLED = False`.
     - Keep your existing jQuery tool templates/views unchanged.

2. **Adopt structured navigation data**
     - Add `SUPPORTTOOLS_VIEW_REGISTRY` entries for your tools.
     - Keep existing `SUPPORTTOOLS_EXTRA_VIEWS` during transition if needed.
     - When both are present, `SUPPORTTOOLS_VIEW_REGISTRY` is preferred.

3. **Convert one tool at a time**
     - Keep the same Django URL/view contract for each tool where possible.
     - Render a page-level mount element (for example, `<div id="tool-app"></div>`)
         from your existing Django template.
     - Move behavior from jQuery handlers to Vue components/composables in small
         slices (form state, table actions, filters, then remaining UI logic).

4. **Introduce Vue assets for the converted tool**
     - Build the new tool bundle with Vite and include it from your template.
     - Keep non-migrated tools on legacy scripts until they are converted.

5. **Enable Vue supporttools shell when ready**
     - Set `SUPPORTTOOLS_VUE_ENABLED = True` after validating the new nav shell
         in your environment.
     - Keep this feature flag available for rollback during rollout.

#### Compatibility Notes

- Existing `supporttools` wrappers and URL routes can remain in place.
- You do not need to migrate all tools at once.
- Server-rendered Django views remain valid; Vue can be layered on top of
    existing templates.
- Prefer preserving URL names and response shapes so external integrations and
    tests require minimal change.

#### Suggested Rollout Checklist

- Add one pilot tool to `SUPPORTTOOLS_VIEW_REGISTRY`.
- Verify navigation, permissions, and URL resolution in supporttools pages.
- Run frontend checks (`lint`, unit tests, build) and backend tests in CI.
- Migrate additional tools incrementally after the pilot is stable.

#### Example: Migrating an Existing Admin Tool

You can migrate an existing admin tool to Vue without changing its public URL
or supporttools link label.

1. Keep the same Django route name and path:

```python
# project/urls.py
from django.urls import path
from project.views.tools import custom_support_tool

urlpatterns = [
    path(
        "custom-support-tool/",
        custom_support_tool,
        name="custom_support_tool",
    ),
]
```

2. Register the same URL in supporttools navigation:

```python
# settings.py
SUPPORTTOOLS_VIEW_REGISTRY = [
    {
        "id": "custom-support-tool",
        "section": "application",
        "order": 20,
        "label": "Custom Support Tool",
        "url_name": "custom_support_tool",
    },
]
```

3. Keep the Django view, but switch template internals to a Vue mount:

```python
# project/views/tools.py
from django.shortcuts import render


def custom_support_tool(request):
    page_context = {
        "initial_filters": {},
        "api_base": "/api/custom-tool/",
    }
    return render(
        request,
        "project/custom_support_tool.html",
        {"tool_page_context": page_context},
    )
```

```django
{# project/templates/project/custom_support_tool.html #}
{% extends "supporttools/base.html" %}
{% load static %}

{% block content %}
    {{ tool_page_context|json_script:"tool-page-context" }}
    <div id="custom-support-tool-app"></div>
{% endblock %}

{% block extra_js %}
        <script type="module" src="{% static 'project/assets/custom-support-tool.js' %}"></script>
{% endblock %}
```

4. Bootstrap Vue from that mount point:

```javascript
// frontend/custom-support-tool/main.js
import { createApp } from "vue";
import CustomSupportToolApp from "./App.vue";

const target = document.getElementById("custom-support-tool-app");
const raw = document.getElementById("tool-page-context");

if (target && raw) {
  const context = JSON.parse(raw.textContent || "{}");
    createApp(CustomSupportToolApp, { context }).mount(target);
}
```

5. Move jQuery logic incrementally:
   - First migrate page state and filters.
   - Then migrate async table actions and inline edits.
   - Keep existing backend APIs and payload shapes during transition.

This pattern lets any app import the new Vue tool through the same
supporttools wrapper and route name, minimizing changes for users,
permissions, and integration tests.
