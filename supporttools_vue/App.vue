<template>
  <nav class="supporttools-nav" aria-label="Tool navigation">
    <template v-for="group in groupedLinks" :key="group.section">
      <h3 class="supporttools-nav-heading">
        {{ group.title }}
      </h3>
      <ul class="supporttools-nav-group">
        <li
          v-for="item in group.links"
          :key="item.id"
          class="supporttools-nav-item"
        >
          <a
            :href="item.url"
            class="supporttools-nav-link"
            :class="{ 'supporttools-nav-link--active': isActive(item) }"
            :aria-current="isActive(item) ? 'page' : null"
            @click="onToolClick($event, item)"
          >
            {{ item.label }}
          </a>
        </li>
      </ul>
    </template>
  </nav>
</template>

<script>
export default {
  name: "SupporttoolsNav",
  props: {
    context: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      currentPath: window.location.pathname,
    };
  },
  mounted() {
    this.onPathChange = () => {
      this.currentPath = window.location.pathname;
    };
    window.addEventListener("popstate", this.onPathChange);
    window.addEventListener("supporttools-spa:navigated", this.onPathChange);
  },
  beforeUnmount() {
    window.removeEventListener("popstate", this.onPathChange);
    window.removeEventListener("supporttools-spa:navigated", this.onPathChange);
  },
  computed: {
    groupedLinks() {
      const links = this.context.links || [];
      const sectionLabels = {
        general: "General Tools",
        application: "Application Tools",
      };

      const groups = links.reduce((acc, link) => {
        const section = link.section || "application";
        if (!acc[section]) {
          acc[section] = {
            title: link.section_label || sectionLabels[section] || section,
            links: [],
          };
        }
        acc[section].links.push(link);
        return acc;
      }, {});

      const sectionOrder = { general: 0, application: 1 };
      return Object.keys(groups)
        .sort(
          (a, b) =>
            (sectionOrder[a] ?? 99) - (sectionOrder[b] ?? 99)
        )
        .map((section) => ({
          section,
          title: groups[section].title,
          links: groups[section].links.slice().sort(
            (a, b) =>
              (a.order ?? 100) - (b.order ?? 100) ||
              a.label.localeCompare(b.label)
          ),
        }));
    },
  },
  methods: {
    isActive(item) {
      if (item.mode === "spa" && item.route) {
        return this.currentPath === item.route;
      }
      return this.currentPath === item.url;
    },
    onToolClick(event, item) {
      if (
        item.mode !== "spa" ||
        !item.route ||
        !item.component_key
      ) {
        return;
      }

      event.preventDefault();
      this.$emit("navigate-spa", item);
    },
  },
};
</script>
