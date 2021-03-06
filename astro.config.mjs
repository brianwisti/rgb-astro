// Full Astro Configuration API Documentation:
// https://docs.astro.build/reference/configuration-reference

// @type-check enabled!
// VSCode and other TypeScript-enabled text editors will provide auto-completion,
// helpful tooltips, and warnings if your exported object is invalid.
// You can disable this by removing "@ts-check" and `@type` comments below.


import { imagetools } from 'vite-imagetools';
import { builtinModules } from "node:module";


// @ts-check
export default /** @type {import('astro').AstroUserConfig} */ ({
  // Comment out "renderers: []" to enable Astro's default component support.
  buildOptions: {
    site: 'https://quirky-wozniak-e4e36f.netlify.app',
  },
  renderers: ['@astrojs/renderer-vue'],
  markdownOptions: {
    render: [
      '@astrojs/markdown-remark',
    ]
  },
  vite: {
    plugins: [imagetools()],
  },
});
