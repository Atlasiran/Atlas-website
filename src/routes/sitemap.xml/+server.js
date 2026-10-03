import { siteUrl } from '../../content/configs';

export const prerender = true;

// The pages a search engine should find: the sections, the public content pages and every organisation.
// The blog is left out; it still holds the starter template's sample posts.
const SECTIONS = ['/', '/groups', '/parties', '/constitutions', '/graph'];
const pages = Object.keys(import.meta.glob('../../content/pages/*.md')).map((f) => '/p/' + f.split('/').pop().slice(0, -3));
const orgs = Object.keys(import.meta.glob('../../content/org-pages/*.md')).map((f) => '/op/' + f.split('/').pop().slice(0, -3));

const loc = (p) => siteUrl + p.split('/').map(encodeURIComponent).join('/');

export const GET = () =>
	new Response(
		'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
			[...SECTIONS, ...pages, ...orgs.sort()].map((p) => `<url><loc>${loc(p)}</loc></url>`).join('\n') +
			'\n</urlset>\n',
		{ headers: { 'Content-Type': 'application/xml' } }
	);
