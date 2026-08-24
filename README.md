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
# Example A — simple server-rendered tool:
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

# Example B — SPA tool (use one definition, not both):
# Optional: mixed navigation support for incremental migration.
# Legacy tools can stay server-rendered; converted Vue tools are SPA-only.
# mode defaults to "server" only for legacy entries.
# Entries with SPA marker fields (route/component_key/vite_entry)
# are treated as "spa" even if mode is omitted.
#
# SPA-mode fields:
#   route          – URL path the component is served at (must match a Django URL pattern)
#   component_key  – key used to look up the component in window.supporttoolsSpaComponents
#   vite_entry     – Vite asset path; passed to {% vite_scripts %} in the generic SPA template
#   view           – dotted import path to the Django view class (optional; see SUPPORTTOOLS_DEFAULT_SPA_VIEW)
SUPPORTTOOLS_VIEW_REGISTRY = [
  {
    "id": "retention-admin",
    "section": "application",
    "order": 20,
    "label": "Retention Admin",
    "url_name": "retention_admin",
    "mode": "spa",
    "route": "/support/retention_admin/",
    "component_key": "retention_admin",
    "vite_entry": "myapp_vue/support/retention-admin.js",
    "view": "myapp.views.support.retention.RetentionAdminView",  # omit to use the default SPA view
  }
]

# Optional: default view class for auto-registered SPA tools.
# Used when a registry entry omits the "view" key.
# Typically a project-specific subclass of SpaToolView that adds authentication.
SUPPORTTOOLS_DEFAULT_SPA_VIEW = "myapp.views.support.base.MySpaToolView"
```

### Migrating to Vue

Apps can migrate incrementally across four phases. Each phase is independently
testable and reversible before moving to the next.

| Phase | What changes | Minimum required |
|---|---|---|
| 0 | Nothing — existing server-rendered nav keeps working | No changes required |
| 1 | Enable the Vue nav shell | One settings flag: `SUPPORTTOOLS_VUE_ENABLED = True` |
| 2 | Register tools explicitly | Add entries to `SUPPORTTOOLS_VIEW_REGISTRY` (or keep using `SUPPORTTOOLS_EXTRA_VIEWS`) |
| 3 | Set up shared SPA infrastructure | One base view class, one settings entry, one `urls.py` line, one Vite config snippet |
| 4 | Convert individual pages to Vue | One registry entry + one JS entry point + one Vue component per tool |

Phases 0–2 require no Node.js and no frontend changes. Phase 3 is a
one-time project setup. Phase 4 is per-tool and fully incremental — legacy
tools can remain server-rendered indefinitely.

---

#### Phase 1 — Enable the Vue nav shell (zero-config)

Set the feature flag in your settings file:

```python
SUPPORTTOOLS_VUE_ENABLED = True
```

That is the only required change. When the flag is on, the Vue nav shell
mounts on `#supporttools-vue-nav` and automatically harvests links from the
server-rendered `{% sidebar_links %}` output already present in the DOM — so
your existing `custom_sidebar_links.html` override (if any) keeps its section
headings, link labels, ordering, and visibility rules with no changes.

**Verify**: the sidebar renders the same links as before, the hamburger toggle
works on mobile viewports, and there are no JS errors in the browser console.

---

#### Phase 2 — Register your tools explicitly (optional but recommended)

The rendered sidebar remains the presentation source of truth while an app is
migrating. Registering tools in settings adds navigation behavior such as SPA
routing; explicit registry entries that are not in the rendered sidebar are
also appended, so tools can be converted incrementally.

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

#### Phase 3 — Set up shared SPA infrastructure (once per project)

Complete this once before converting any individual tool in Phase 4.

**1. Create a project-level SPA view base** that adds your auth decorator:

```python
# myapp/views/support/base.py
from django.conf import settings
from django.utils.decorators import method_decorator
from uw_saml.decorators import group_required
from supporttools.views import SpaToolView

@method_decorator(group_required(settings.MY_SUPPORT_GROUP), name='dispatch')
class MySpaToolView(SpaToolView):
    pass
```

**2. Add the default view and auto-register URLs** in your settings and `urls.py`:

```python
# settings.py
SUPPORTTOOLS_DEFAULT_SPA_VIEW = "myapp.views.support.base.MySpaToolView"
```

```python
# your ROOT_URLCONF module (for example: project/urls.py or docker/urls.py)
from supporttools.urls import get_registry_urlpatterns

urlpatterns += get_registry_urlpatterns()  # reads SUPPORTTOOLS_VIEW_REGISTRY
```

**3. Auto-discover Vite entry points** by editing your existing `vite.config.js`
so new tools are picked up automatically:

Add/merge the snippet below into your current Vite config. Do not replace the
entire file.

```javascript
// vite.config.js
import { readdirSync } from "fs";

const supportEntries = readdirSync("./myapp_vue/support")
  .filter((f) => f.endsWith(".js"))
  .map((f) => `./myapp_vue/support/${f}`);

export default defineConfig({
  build: {
    rollupOptions: {
      input: ["./myapp_vue/main.js", ...supportEntries],
    },
  },
});
```

---

#### Phase 4 — Convert individual pages to Vue

Each page can be converted independently without affecting other tools.
Legacy tools can remain server-rendered while converted tools use SPA nav.

- `mode: "server"` (default for legacy entries): normal full-page navigation.
- `mode: "spa"`: client-side navigation — no full-page reload when the sidebar
  link is clicked.
- Converted Vue tools are SPA-only. If `route`, `component_key`, or
  `vite_entry` is present, the entry is normalized to `mode: "spa"`.

Data access is owned by the tool component. A tool can pre-load data from
the server on direct URL navigation, and fetch from API endpoints when
mounted via SPA navigation. This direct-URL bootstrap uses the SPA view
template; it is not a fallback to server-navigation mode.

---

##### Adding a new SPA tool

**1. Register the tool in `SUPPORTTOOLS_VIEW_REGISTRY`**

```python
{
    "id": "my-tool",
    "section": "application",
    "order": 10,
    "label": "My Tool",
    "url_name": "my_tool",
    "mode": "spa",
    "route": "/support/my_tool/",
    "component_key": "my_tool",
    "vite_entry": "myapp_vue/support/my-tool.js",
    # "view": "myapp.views.support.my_tool.MyToolView"  # only needed for custom server data
}
```

The URL is auto-registered by `get_registry_urlpatterns()`. No `urls.py` edit needed.

**2. Create the Vue entry point** (the entire file):

```javascript
// myapp_vue/support/my-tool.js
window.supporttoolsRegisterSpaTool("my_tool", () => import("./MyTool.vue"));
```

`window.supporttoolsRegisterSpaTool` is provided by the supporttools bundle
already loaded in `base.html`. It handles both SPA-nav mounting (via the
sidebar) and direct-URL mounting (via server-rendered JSON). No imports needed.

**3. Create the Vue component**

The component receives a `pageData` prop on direct-URL load (populated from
server-rendered JSON), and a `tool` prop when mounted via SPA navigation:

```vue
<template>
  <div>
    <h1>My Tool</h1>
    <!-- your UI -->
  </div>
</template>

<script>
export default {
  name: "MyTool",
  props: {
    pageData: { type: Object, default: () => ({}) },
    tool: { type: Object, default: null },
  },
  async mounted() {
    // When mounted via SPA nav, pageData is empty — fetch fresh data from API.
    if (this.tool && this.tool.mode === "spa") {
      await this.loadData();
    }
  },
  methods: {
    async loadData() { /* fetch from your API endpoint */ },
  },
};
</script>
```

**That's all that's needed for a tool with no server-side bootstrap data.**

---

##### Adding server-side bootstrap data (optional)

If the tool needs data pre-loaded on direct URL navigation, create a
Django view that inherits from your project's SPA view base and overrides
`get_page_data()`. The data is serialised to JSON and passed as the
`pageData` prop automatically by the generic `spa_tool.html` template.

```python
# myapp/views/support/my_tool.py
from myapp.views.support.base import MySpaToolView

class MyToolView(MySpaToolView):
    def get_page_data(self):
        return {
            'items': [
                {'id': obj.id, 'name': obj.name}
                for obj in MyModel.objects.all()
            ]
        }
```

Then add `"view": "myapp.views.support.my_tool.MyToolView"` to the registry
entry. No template file needed — `spa_tool.html` is used automatically.

---

#### CI/CD note

The compiled bundle at `supporttools/static/supporttools/js/main.js` is built
at publish time by CI and distributed inside the PyPI wheel. Consuming apps do
not need Node.js. See `.github/workflows/cicd.yml` for the build step in the
`publish` job.


