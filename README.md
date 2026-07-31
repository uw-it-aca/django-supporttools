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

### Migrating to Vue

Apps can migrate incrementally across three phases. Each phase is independently
testable and reversible before moving to the next.

---

#### Phase 1 — Enable the Vue nav shell (zero-config)

Set the feature flag in your settings file:

```python
SUPPORTTOOLS_VUE_ENABLED = True
```

That is the only required change. When the flag is on, the Vue nav shell
mounts on `#supporttools-vue-nav` and automatically harvests links from the
server-rendered `{% sidebar_links %}` output already present in the DOM — so
your existing `custom_sidebar_links.html` override (if any) keeps working with
no changes.

**Verify**: the sidebar renders the same links as before, the hamburger toggle
works on mobile viewports, and there are no JS errors in the browser console.

---

#### Phase 2 — Register your tools explicitly (optional but recommended)

DOM harvesting from Phase 1 works but provides no control over labels,
ordering, or section grouping. Registering tools in settings gives Vue the
structured data it needs.

**Option A — simple dict (lowest friction first step):**

```python
# settings.py
SUPPORTTOOLS_EXTRA_VIEWS = {
    "My Tool": "my_tool_url_name",
    "Another Tool": "another_tool_url_name",
}
```

**Option B — structured registry (preferred for new work):**

```python
# settings.py
SUPPORTTOOLS_VIEW_REGISTRY = [
    {
        "id": "my-tool",
        "section": "application",
        "order": 10,
        "label": "My Tool",
        "url_name": "my_tool_url_name",
    },
    {
        "id": "another-tool",
        "section": "application",
        "order": 20,
        "label": "Another Tool",
        "url_name": "another_tool_url_name",
    },
]
```

When `SUPPORTTOOLS_VIEW_REGISTRY` is set it takes precedence; entries from
`SUPPORTTOOLS_EXTRA_VIEWS` are merged in as a supplement. Once your tools are
registered here the `custom_sidebar_links.html` template override is redundant
and can be removed.

---

#### Phase 3 — Convert individual pages to Vue

Each page can be converted independently without affecting other tools.

**1. Serialize the page data in the Django view**

Replace queryset context variables with JSON-serialisable dicts. `DateTimeField`
values must be converted with `.isoformat()`:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_data'] = [
        {
            'id': obj.id,
            'created': obj.created.isoformat() if obj.created else None,
            'name': obj.name,
        }
        for obj in MyModel.objects.all()
    ]
    return context
```

**2. Replace the template with a mount point**

```django
{% extends 'supporttools/base.html' %}
{% load vite %}

{% block content %}
  {{ page_data|json_script:"my-tool-data" }}
  <div id="my-tool-app"></div>
{% endblock content %}

{% block extra_js %}
  {% vite_scripts 'myapp_vue/support/my-tool.js' %}
{% endblock %}
```

**3. Create the Vue entry point**

```javascript
// myapp_vue/support/my-tool.js
import { createApp } from "vue";
import MyTool from "./MyTool.vue";

const target = document.getElementById("my-tool-app");
const raw = document.getElementById("my-tool-data");

if (target && raw) {
  const items = JSON.parse(raw.textContent || "[]");
  createApp(MyTool, { items }).mount(target);
}
```

**4. Create the Vue component**

Use Bootstrap 3 table classes — the supporttools base template loads Bootstrap 3:

```vue
<template>
  <div>
    <h1>My Tool</h1>
    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>Created</th><th>Name</th></tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.created }}</td>
          <td>{{ item.name }}</td>
        </tr>
        <tr v-if="items.length === 0">
          <td colspan="3">No items found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "MyTool",
  props: {
    items: { type: Array, default: () => [] },
  },
};
</script>
```

**5. Register the entry point in vite.config.js**

```javascript
rollupOptions: {
  input: [
    "./myapp_vue/main.js",
    "./myapp_vue/support/my-tool.js",  // add this
  ],
},
```

---

#### CI/CD note

The compiled bundle at `supporttools/static/supporttools/js/main.js` is built
at publish time by CI and distributed inside the PyPI wheel. Consuming apps do
not need Node.js. See `.github/workflows/cicd.yml` for the build step in the
`publish` job.


