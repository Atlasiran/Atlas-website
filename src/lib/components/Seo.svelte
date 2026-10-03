<script>
    // One complete set of title, description and share tags for a page. Crawlers keep the first
    // og:title they see, so the layout sets none and every page renders this instead.
    import { page } from "$app/stores";
    import { siteName, siteDescription, siteUrl } from "../../content/configs";

    export let title = "";
    export let description = siteDescription;
    export let image = `${siteUrl}/og-image.jpg`;
    export let type = "website";

    $: fullTitle = title ? `${title} | ${siteName}` : siteName;
    $: url = siteUrl + $page.url.pathname.split("/").map((s) => encodeURIComponent(decodeURIComponent(s))).join("/");
</script>

<svelte:head>
    <title>{fullTitle}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={url} />
    <meta property="og:type" content={type} />
    <meta property="og:title" content={fullTitle} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={image} />
    <meta property="og:url" content={url} />
    <meta name="twitter:title" content={fullTitle} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={image} />
</svelte:head>
