<template>
  <div>
    <template v-for="group in groupedLinks" :key="group.section">
      <h3>{{ group.title }}</h3>
      <ul>
        <li v-for="item in group.links" :key="item.id">
          <a :href="item.url">{{ item.label }}</a>
        </li>
      </ul>
    </template>
  </div>
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

      return Object.keys(groups)
        .sort()
        .map((section) => ({
          section,
          title: sectionLabels[section] || section,
          links: groups[section],
        }));
    },
  },
};
</script>
