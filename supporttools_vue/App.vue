<template>
  <nav>
    <template v-for="group in groupedLinks" :key="group.section">
      <h3 class="small text-uppercase text-white-50 px-2 mt-3 mb-1">
        {{ group.title }}
      </h3>
      <ul class="nav flex-column mb-2">
        <li v-for="item in group.links" :key="item.id" class="nav-item">
          <a :href="item.url" class="nav-link text-white py-1 px-2">
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
          acc[section] = [];
        }
        acc[section].push(link);
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
          title: sectionLabels[section] || section,
          links: groups[section].slice().sort(
            (a, b) =>
              (a.order ?? 100) - (b.order ?? 100) ||
              a.label.localeCompare(b.label)
          ),
        }));
    },
  },
};
</script>
