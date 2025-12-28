import { error } from '@sveltejs/kit'
export const prerender = true;

export const load = async ({ params }) => {
	let post;
	let isSvx = true;

	if (!params || !params?.page) {
		return error(404, new Error('Post not found'));
	}


	try {
		post = await import(`../../../content/org-pages/${params.page}.md`);
		isSvx = false;
	} catch (err) {
		console.log(err);
		try {
			post = await import(`../../../content/org-pages/${params.page}.svx`);
		} catch (err) {
			console.log(err);
			return error(404, err);
		}
	}

	if(!post) {
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
