import { describe, expect, it } from "vitest";
import {
  buildNavigationLinks,
  getDirectPageData,
  loadSpaComponent,
  restoreServerDocumentTitle,
  setSpaDocumentTitle,
} from "./main.js";

describe("buildNavigationLinks", () => {
  it("preserves a custom sidebar's groups, labels, order, and visibility", () => {
    const target = document.createElement("div");
    target.innerHTML = `
      <h3>Overrides</h3>
      <div><a href="https://example.com/help">Override Help</a></div>
      <ul><li><a href="/support">User Override</a></li></ul>
      <h3>Content Management</h3>
      <ul><li><a href="/messages">Banner Messages</a></li></ul>
    `;
    const configured = [
      { id: "home", label: "Support Home", url: "/" },
      { id: "override", label: "Override", url: "/support", mode: "server" },
    ];

    expect(buildNavigationLinks(target, configured)).toEqual([
      expect.objectContaining({
        label: "Override Help",
        section: "rendered-0",
        section_label: "Overrides",
        order: 0,
      }),
      expect.objectContaining({
        id: "override",
        label: "User Override",
        section: "rendered-0",
        section_label: "Overrides",
        order: 1,
      }),
      expect.objectContaining({
        label: "Banner Messages",
        section: "rendered-1",
        section_label: "Content Management",
        order: 0,
      }),
    ]);
  });

  it("appends explicit registry entries missing from the rendered template", () => {
    const target = document.createElement("div");
    target.innerHTML = '<h3>Tools</h3><a href="/legacy">Legacy</a>';
    const configured = [{
      id: "new-tool",
      label: "New Tool",
      url: "/new",
      section: "application",
      explicit: true,
    }];

    expect(buildNavigationLinks(target, configured).map((link) => link.id)).toEqual([
      "/legacy",
      "new-tool",
    ]);
  });
});

describe("getDirectPageData", () => {
  it("returns page data serialized by the SPA template", () => {
    document.body.innerHTML = `
      <script id="supporttools-spa-page-data" type="application/json">
        {"items":[{"name":"Example"}]}
      </script>
    `;

    expect(getDirectPageData()).toEqual({
      items: [{ name: "Example" }],
    });
  });

  it("returns an empty object without page data", () => {
    document.body.innerHTML = "";

    expect(getDirectPageData()).toEqual({});
  });
});

describe("loadSpaComponent", () => {
  it("returns the default component export", async () => {
    const component = { name: "MyTool" };

    await expect(
      loadSpaComponent(() => Promise.resolve({ default: component }))
    ).resolves.toBe(component);
  });

  it("returns null when a component import fails", async () => {
    await expect(
      loadSpaComponent(() => Promise.reject(new Error("chunk unavailable")))
    ).resolves.toBeNull();
  });
});

describe("SPA document title", () => {
  it("updates and restores the server-rendered document title", () => {
    const serverTitle = document.title;

    setSpaDocumentTitle("Person Search");
    expect(document.title).toBe(
      serverTitle ? `Person Search - ${serverTitle}` : "Person Search"
    );

    restoreServerDocumentTitle();
    expect(document.title).toBe(serverTitle);
  });
});