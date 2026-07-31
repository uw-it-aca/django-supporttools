import { describe, it, expect, vi, afterEach } from "vitest";
import { mount } from "@vue/test-utils";
import App from "./App.vue";

afterEach(() => {
  vi.restoreAllMocks();
});

const makeLink = (overrides = {}) => ({
  id: "tool-a",
  label: "Tool A",
  url: "/tools/a",
  section: "application",
  order: 10,
  mode: "server",
  route: null,
  component_key: null,
  ...overrides,
});

describe("groupedLinks", () => {
  it("returns empty array when context has no links", () => {
    const wrapper = mount(App, { props: { context: {} } });
    expect(wrapper.vm.groupedLinks).toEqual([]);
  });

  it("groups links by section with correct titles", () => {
    const links = [
      makeLink({ id: "g", section: "general", label: "G Tool", order: 1 }),
      makeLink({ id: "a", section: "application", label: "A Tool", order: 1 }),
    ];
    const wrapper = mount(App, { props: { context: { links } } });
    const groups = wrapper.vm.groupedLinks;
    expect(groups[0].section).toBe("general");
    expect(groups[0].title).toBe("General Tools");
    expect(groups[1].section).toBe("application");
    expect(groups[1].title).toBe("Application Tools");
  });

  it("orders general section before application section", () => {
    const links = [
      makeLink({ id: "app", section: "application", label: "App", order: 1 }),
      makeLink({ id: "gen", section: "general", label: "Gen", order: 1 }),
    ];
    const wrapper = mount(App, { props: { context: { links } } });
    expect(wrapper.vm.groupedLinks[0].section).toBe("general");
  });

  it("sorts links within section by order then label", () => {
    const links = [
      makeLink({ id: "b", label: "B Tool", order: 10 }),
      makeLink({ id: "a", label: "A Tool", order: 10 }),
      makeLink({ id: "c", label: "C Tool", order: 5 }),
    ];
    const wrapper = mount(App, { props: { context: { links } } });
    const sorted = wrapper.vm.groupedLinks[0].links;
    expect(sorted[0].id).toBe("c"); // order 5 wins
    expect(sorted[1].id).toBe("a"); // order 10, "A" < "B"
    expect(sorted[2].id).toBe("b");
  });

  it("defaults to application section when section is absent", () => {
    const link = { id: "x", label: "X", url: "/x", mode: "server" };
    const wrapper = mount(App, { props: { context: { links: [link] } } });
    expect(wrapper.vm.groupedLinks[0].section).toBe("application");
  });
});

describe("isActive", () => {
  it("matches SPA route against currentPath", () => {
    const item = makeLink({
      mode: "spa",
      route: "/tools/spa",
      component_key: "spa_key",
    });
    const wrapper = mount(App, { props: { context: {} } });
    wrapper.vm.currentPath = "/tools/spa";
    expect(wrapper.vm.isActive(item)).toBe(true);
  });

  it("returns false for SPA item when path does not match", () => {
    const item = makeLink({ mode: "spa", route: "/tools/spa", component_key: "k" });
    const wrapper = mount(App, { props: { context: {} } });
    wrapper.vm.currentPath = "/other";
    expect(wrapper.vm.isActive(item)).toBe(false);
  });

  it("matches server url against currentPath", () => {
    const item = makeLink({ url: "/server-tool" });
    const wrapper = mount(App, { props: { context: {} } });
    wrapper.vm.currentPath = "/server-tool";
    expect(wrapper.vm.isActive(item)).toBe(true);
  });

  it("returns false for server item when path does not match", () => {
    const item = makeLink({ url: "/server-tool" });
    const wrapper = mount(App, { props: { context: {} } });
    wrapper.vm.currentPath = "/other";
    expect(wrapper.vm.isActive(item)).toBe(false);
  });
});

describe("onToolClick", () => {
  it("emits navigate-spa and calls preventDefault for valid SPA item", () => {
    const item = makeLink({ mode: "spa", route: "/tools/spa", component_key: "k" });
    const wrapper = mount(App, { props: { context: { links: [item] } } });
    const event = { preventDefault: vi.fn() };
    wrapper.vm.onToolClick(event, item);
    expect(event.preventDefault).toHaveBeenCalled();
    expect(wrapper.emitted("navigate-spa")).toBeTruthy();
    expect(wrapper.emitted("navigate-spa")[0][0]).toEqual(item);
  });

  it("does not emit or prevent default for server item", () => {
    const item = makeLink(); // mode: "server"
    const wrapper = mount(App, { props: { context: {} } });
    const event = { preventDefault: vi.fn() };
    wrapper.vm.onToolClick(event, item);
    expect(event.preventDefault).not.toHaveBeenCalled();
    expect(wrapper.emitted("navigate-spa")).toBeFalsy();
  });

  it("does not emit for SPA item missing route", () => {
    const item = makeLink({ mode: "spa", route: null, component_key: "k" });
    const wrapper = mount(App, { props: { context: {} } });
    const event = { preventDefault: vi.fn() };
    wrapper.vm.onToolClick(event, item);
    expect(event.preventDefault).not.toHaveBeenCalled();
  });

  it("does not emit for SPA item missing component_key", () => {
    const item = makeLink({ mode: "spa", route: "/tools/spa", component_key: null });
    const wrapper = mount(App, { props: { context: {} } });
    const event = { preventDefault: vi.fn() };
    wrapper.vm.onToolClick(event, item);
    expect(event.preventDefault).not.toHaveBeenCalled();
  });
});

describe("lifecycle event listeners", () => {
  it("registers popstate and spa:navigated listeners on mount", () => {
    const addSpy = vi.spyOn(window, "addEventListener");
    mount(App, { props: { context: {} } });
    expect(addSpy).toHaveBeenCalledWith("popstate", expect.any(Function));
    expect(addSpy).toHaveBeenCalledWith(
      "supporttools-spa:navigated",
      expect.any(Function)
    );
  });

  it("removes both listeners on unmount", () => {
    const removeSpy = vi.spyOn(window, "removeEventListener");
    const wrapper = mount(App, { props: { context: {} } });
    wrapper.unmount();
    expect(removeSpy).toHaveBeenCalledWith("popstate", expect.any(Function));
    expect(removeSpy).toHaveBeenCalledWith(
      "supporttools-spa:navigated",
      expect.any(Function)
    );
  });
});
