import { createApp } from "vue";
import App from "./App.vue";

// solstice bootstrap theme + component styles
import "bootstrap-icons/font/bootstrap-icons.css";
import "solstice-theme/dist/solstice.scss";
import "solstice-vue/dist/style.css";

const target = document.getElementById("supporttools-vue-nav");
const rawContext = document.getElementById("supporttools-vue-context");

if (target && rawContext) {
  const context = JSON.parse(rawContext.textContent || "{}");

  // Harvest any extra links already rendered by the server-side sidebar
  // template (e.g. custom_sidebar_links.html) that are not yet covered by
  // context.links.  This lets consuming apps get zero-config Vue nav on
  // step 1 of migration — just setting SUPPORTTOOLS_VUE_ENABLED = True is
  // enough; no settings registry changes are required.
  const knownUrls = new Set((context.links || []).map((l) => l.url));
  const domLinks = Array.from(target.querySelectorAll("a")).reduce(
    (acc, a) => {
      const url = a.getAttribute("href");
      if (url && !knownUrls.has(url)) {
        acc.push({
          id: url,
          section: "application",
          order: 100,
          label: a.textContent.trim(),
          url,
          url_args: [],
          url_kwargs: {},
        });
        knownUrls.add(url);
      }
      return acc;
    },
    []
  );

  const allLinks = [...(context.links || []), ...domLinks];

  // Only mount if there are links to render; otherwise leave the
  // server-rendered sidebar ({% sidebar_links %}) in place.
  if (allLinks.length > 0) {
    createApp(App, { context: { ...context, links: allLinks } }).mount(target);
  }
}
