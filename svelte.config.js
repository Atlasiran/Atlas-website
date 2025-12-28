import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import cloudflareAdapter from '@sveltejs/adapter-cloudflare';
import staticAdapter from '@sveltejs/adapter-static';

import { mdsvex } from 'mdsvex';
import mdsvexConfig from './mdsvex.config.js';
import { getAllOPPaths } from './src/lib/server_utils.js';

const useStatic = process.env.ADAPTER === 'static';
const dev = process.env.NODE_ENV === 'development';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  extensions: ['.svelte', ...mdsvexConfig.extensions],

  preprocess: [mdsvex(mdsvexConfig), vitePreprocess()],

  kit: {
    adapter: useStatic
      ? staticAdapter({
          pages: 'build',
          assets: 'build',
          fallback: '404.html'
        })
      : cloudflareAdapter({
          routes: {
            include: ['/*'],
            exclude: ['<all>']
          },
          platformProxy: {
            configPath: 'wrangler.toml',
            environment: undefined,
            experimentalJsonConfig: false,
            persist: false
          }
        }),

    alias: {
      '@/*': './src/lib/*'
    },

    paths: {
      base: useStatic && !dev ? '/Atlas-website' : ''
    },

    prerender: {
      entries: ['*', '/parties', '/groups', '/graph', '/api/pages/page/*', '/api/posts/page/*', ...getAllOPPaths()],
      handleHttpError: 'warn'
    },

    csp: { mode: 'auto' }
  }
};

export default config;
