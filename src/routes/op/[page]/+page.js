import { error } from '@sveltejs/kit'

const mdModules = import.meta.glob('../../../content/org-pages/*.md');
const svxModules = import.meta.glob('../../../content/org-pages/*.svx');

export const prerender = true;

export const load = async ({ params }) => {
        if (!params || !params?.page) {
                return error(404, new Error('Post not found'));
        }

        const mdKey = `../../../content/org-pages/${params.page}.md`;
        const svxKey = `../../../content/org-pages/${params.page}.svx`;

        let post;
        let isSvx = false;

        if (mdModules[mdKey]) {
                post = await mdModules[mdKey]();
                isSvx = false;
        } else if (svxModules[svxKey]) {
                post = await svxModules[svxKey]();
                isSvx = true;
        } else {
                return error(404, new Error('Post not found'));
        }

        return {
                PostContent: post.default,
                meta: { 
                        isSvx,
                        ...post.metadata, 
                        slug: params.post, 
                }
        }
}
