import { base } from '$app/paths';

export const load = async ({ url, fetch }) => {
    const postRes = await fetch(`${url.origin}${base}/api/pages.json`)
    const posts = await postRes.json()

    const totalRes = await fetch(`${url.origin}${base}/api/pages/count`)
    const total = await totalRes.json()

    return { posts, total }
}
