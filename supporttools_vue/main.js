import { createApp } from "vue";
import App from "./App.vue";

// solstice bootstrap theme + component styles
import "bootstrap-icons/font/bootstrap-icons.css";
import "solstice-theme/dist/solstice.scss";
import "solstice-vue/dist/style.css";
import "./supporttools-shell.scss";

// Expose a registration helper for SPA tool entry points.  Tool scripts call
// window.supporttoolsRegisterSpaTool(componentKey, importFn) which:
//   1. Registers the lazy component loader for SPA-nav use by this shell.
//   2. Bootstraps a direct-load mount when the page was server-rendered
//      (i.e. #spa-tool-app is present in the DOM).
//
// Load order is guaranteed: base.html loads this bundle first; tool scripts
// arrive via {% block extra_js %} which renders after the base scripts.
window.supporttoolsRegisterSpaTool = function (componentKey, importFn) {
  window.supporttoolsSpaComponents = window.supporttoolsSpaComponents || {};
  window.supporttoolsSpaComponents[componentKey] = importFn;

  const target = document.getElementById("spa-tool-app");
  if (target) {
    loadSpaComponent(importFn).then(function (component) {
      if (component) {
        createApp(component, { pageData: getDirectPageData() }).mount(target);
      }
    });
  }
};

export async function loadSpaComponent(loadComponent) {
  try {
    const mod = await loadComponent();
    return mod && (mod.default || mod);
  } catch {
    return null;
  }
}

export function getDirectPageData() {
  const pageData = document.getElementById("supporttools-spa-page-data");
  if (!pageData) {
    return {};
  }

  try {
    return JSON.parse(pageData.textContent || "{}");
  } catch {
    return {};
  }
}

const target = document.getElementById("supporttools-vue-nav");
const rawContext = document.getElementById("supporttools-vue-context");
const outlet = document.getElementById("supporttools-spa-outlet");
const outletTitle = document.getElementById("supporttools-spa-title");
const spaShell = document.getElementById("supporttools-spa-shell");
const pageContent = document.getElementById("supporttools-page-content");
const serverDocumentTitle = document.title;

const mountedApps = [];

function isValidSpaTool(tool) {
  return (
    tool &&
    tool.mode === "spa" &&
    Boolean(tool.route) &&
    Boolean(tool.component_key)
  );
}

function findSpaToolByPath(links, path) {
  return links.find((link) => isValidSpaTool(link) && link.route === path) || null;
}

export function buildNavigationLinks(target, configuredLinks = []) {
  const configuredByUrl = new Map(
    configuredLinks.map((link) => [link.url, link])
  );
  const renderedUrls = new Set();
  let sectionIndex = -1;
  let section = "application";
  let sectionLabel = "Application Tools";
  let order = 0;

  const renderedLinks = Array.from(target.querySelectorAll("h3, a")).reduce(
    (links, element) => {
      if (element.tagName === "H3") {
        sectionIndex += 1;
        section = `rendered-${sectionIndex}`;
        sectionLabel = element.textContent.trim();
        order = 0;
        return links;
      }

      const url = element.getAttribute("href");
      if (!url || renderedUrls.has(url)) {
        return links;
      }

      const configured = configuredByUrl.get(url) || {};
      links.push({
        ...configured,
        id: configured.id || url,
        section,
        section_label: sectionLabel,
        order: order++,
        label: element.textContent.trim(),
        url,
      });
      renderedUrls.add(url);
      return links;
    },
    []
  );

  const explicitAdditions = configuredLinks.filter(
    (link) => link.explicit && !renderedUrls.has(link.url)
  );
  return [...renderedLinks, ...explicitAdditions];
}

function setOutletTitle(tool) {
  if (!outletTitle) {
    return;
  }

  const title = tool.title || tool.label || "Tool";
  outletTitle.textContent = title;
  setSpaDocumentTitle(title);
  outletTitle.style.display = "block";
}

export function setSpaDocumentTitle(title) {
  document.title = serverDocumentTitle
    ? `${title} - ${serverDocumentTitle}`
    : title;
}

export function restoreServerDocumentTitle() {
  document.title = serverDocumentTitle;
}

async function renderSpaTool(tool, links) {
  if (!outlet || !isValidSpaTool(tool)) {
    return false;
  }

  const componentLoaders = window.supporttoolsSpaComponents || {};
  const loadComponent = componentLoaders[tool.component_key];
  if (typeof loadComponent !== "function") {
    return false;
  }

  const component = await loadSpaComponent(loadComponent);
  if (!component) {
    return false;
  }

  // Unmount any existing tool app before mounting the next one.
  while (mountedApps.length) {
    const app = mountedApps.pop();
    app.unmount();
  }

  outlet.innerHTML = "";
  setOutletTitle(tool);

  const app = createApp(component, {
    tool,
    links,
  });
  app.mount(outlet);
  mountedApps.push(app);

  if (spaShell) spaShell.style.display = "block";
  if (pageContent) pageContent.style.display = "none";
  return true;
}

function hideSpaOutlet() {
  if (!outlet) {
    return;
  }

  while (mountedApps.length) {
    const app = mountedApps.pop();
    app.unmount();
  }
  outlet.innerHTML = "";
  if (spaShell) spaShell.style.display = "none";
  if (pageContent) pageContent.style.display = "block";
  if (outletTitle) outletTitle.textContent = "";
  restoreServerDocumentTitle();
}

async function navigateSpa(item, links, push = true) {
  if (!isValidSpaTool(item)) {
    window.location.assign(item.url);
    return;
  }

  if (push && window.location.pathname !== item.route) {
    window.history.pushState({ supporttoolsSpa: true }, "", item.route);
  }

  window.dispatchEvent(new CustomEvent("supporttools-spa:navigated"));

  const rendered = await renderSpaTool(item, links);
  if (!rendered) {
    // When opening a server-rendered SPA route directly (push=false), avoid
    // reloading the exact same URL in a loop if a component loader isn't
    // registered yet. Leave server-rendered content in place.
    if (!push && window.location.pathname === item.route) {
      hideSpaOutlet();
      return;
    }

    // If a SPA tool cannot render (missing module, bad config), fall back
    // to the server URL to avoid trapping the user.
    window.location.assign(item.url);
  }
}

if (target && rawContext) {
  const context = JSON.parse(rawContext.textContent || "{}");
  const allLinks = buildNavigationLinks(target, context.links);

  const onNavigateSpa = (item) => {
    navigateSpa(item, allLinks, true);
  };

  window.addEventListener("popstate", () => {
    const match = findSpaToolByPath(allLinks, window.location.pathname);
    if (match) {
      navigateSpa(match, allLinks, false);
      return;
    }
    hideSpaOutlet();
  });

  // Only mount if there are links to render; otherwise leave the
  // server-rendered sidebar ({% sidebar_links %}) in place.
  if (allLinks.length > 0) {
    createApp(App, {
      context: { ...context, links: allLinks },
      onNavigateSpa,
    }).mount(target);

    // On direct page load, let the server-rendered content stand.
    // The outlet is only used for client-side (pushState) navigations.
    hideSpaOutlet();
  }
}
