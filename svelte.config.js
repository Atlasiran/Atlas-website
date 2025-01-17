import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

// cloudflare 
import adapter from '@sveltejs/adapter-cloudflare';

import { mdsvex } from 'mdsvex';
import mdsvexConfig from './mdsvex.config.js';
import { getAllOPPaths } from './src/lib/server_utils.js';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: [
		'.svelte',
		...mdsvexConfig.extensions
	],

	preprocess: [
		mdsvex(mdsvexConfig),
		vitePreprocess(),
	],

	kit: {
		// --------------------------------------------------- static
		// adapter: adapter({
		// 	fallback: 'index.html'
		// }),

		// --------------------------------------------------- cloudflare 
		adapter: adapter({
			// See below for an explanation of these options
			routes: {
				include: [
					'/*'
				],
				exclude: [
					'<all>'
				]
			},
			platformProxy: {
				configPath: 'wrangler.toml',
				environment: undefined,
				experimentalJsonConfig: false,
				persist: false
			}
		}),

		alias: {
			"@/*": "./src/lib/*",
		},

		prerender: {
			entries: [
				'*',
				'/api/pages/page/*',
				'/api/posts/page/*',
				...getAllOPPaths()
			]
		},
		csp: { mode: 'auto' }

	},

};

export default config;
