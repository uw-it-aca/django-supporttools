import { createApp } from "vue";
import App from "./App.vue";

const target = document.getElementById("supporttools-vue-nav");
const rawContext = document.getElementById("supporttools-vue-context");

if (target && rawContext) {
  const context = JSON.parse(rawContext.textContent || "{}");
  createApp(App, { context }).mount(target);
}
