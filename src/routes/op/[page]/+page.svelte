<script>
    import Footer from "@/components/layout/Footer.svelte";
    import Header from "@/components/layout/Header.svelte";
    import OrgPageLayout from "@/components/layout/OrgPageLayout.svelte";
    import Building2 from "lucide-svelte/icons/building-2";
    import Link from "lucide-svelte/icons/link";
    export let data;

    const m = data.meta;
    const { PostContent } = data;

    const orgName = [m.name_fa, m.name_en, m.name_short, m.title].find(defined);

    function defined(v) {
        return v && v !== "None" && v.trim() !== "";
    }

    const SITE_URL = "https://atlasiran.org";
    const DEFAULT_OG_IMAGE = `${SITE_URL}/og-image.jpg`;

    const ogTitle = [orgName, "اطلس جامعه مدنی ایران"]
        .filter(Boolean)
        .join(" | ");
    const ogDescription = (() => {
        if (defined(m.about)) return m.about;
        const parts = [
            defined(m.expertise) ? m.expertise : null,
            defined(m.political_orientation) ? m.political_orientation : null,
            defined(m.location) ? m.location : null,
        ].filter(Boolean);
        return parts.length ? parts.join(" · ") : "اطلس جامعه مدنی ایران";
    })();
    const slug = m.pageLink ? m.pageLink.replace(/^\/op\//, "") : null;
    const ogImage = slug
        ? `${SITE_URL}/og/op/${slug}.jpg`
        : DEFAULT_OG_IMAGE;
    const ogUrl = `${SITE_URL}${m.pageLink || ""}`;
</script>

<svelte:head>
    <title>{ogTitle}</title>
    <meta property="og:type" content="profile" />
    <meta property="og:title" content={ogTitle} />
    <meta property="og:description" content={ogDescription} />
    <meta property="og:image" content={ogImage} />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:url" content={ogUrl} />
    <meta property="og:site_name" content="اطلس جامعه مدنی ایران" />
    <meta name="description" content={ogDescription} />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={ogTitle} />
    <meta name="twitter:description" content={ogDescription} />
    <meta name="twitter:image" content={ogImage} />
</svelte:head>

{#if !m.isSvx}
    <OrgPageLayout {...m}>
        <article class="w-full mx-auto max-w-[800px] pt-10 pb-16">
            <!-- Header -->
            <div class="mb-8">
                <div
                    class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] mb-3"
                >
                    <Building2 class="w-5 h-5" />
                </div>
                <h1
                    class="text-4xl font-bold text-[#1E3A6B] mb-2 pb-4 border-b border-[rgba(30,58,107,0.08)]"
                >
                    {orgName}
                </h1>
            </div>

            <!-- Info grid -->
            <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4 text-sm">
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        نوع نهاد
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.org_type || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        نام فارسی
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.name_fa || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        نام لاتین
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        <bdi>{m.name_en || "—"}</bdi>
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        نام کوتاه
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.name_short || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">مکان</dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.location || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        نشانی پستی
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.post_location || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        تعداد تخمینی اعضا
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.estimation_of_members || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        گرایش سیاسی
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.political_orientation || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">ایمیل</dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.email || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">تلفن</dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.phone || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        ثبت شده در
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.created_at || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        بروزرسانی
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.updated_at || "—"}
                    </dd>
                </div>
            </dl>

            <!-- About -->
            <div class="mt-6">
                <h2 class="font-semibold text-[#1E3A6B] mb-2">درباره</h2>
                <p class="text-[rgba(30,58,107,0.72)] text-sm leading-relaxed">
                    {m.about || "—"}
                </p>
            </div>

            <!-- Detail fields -->
            <dl class="mt-6 grid grid-cols-1 gap-y-4 text-sm">
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">تخصص‌ها</dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.expertise || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        تاریخ‌چه
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.history || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">منیفست</dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.manifest || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        مرام‌نامه
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">{m.coc || "—"}</dd>
                </div>
            </dl>

            <!-- Social links -->
            <div class="mt-6">
                <h2 class="font-semibold text-[#1E3A6B] mb-3 text-sm">
                    پیوندها
                </h2>
                <div class="flex flex-wrap gap-2">
                    {#if defined(m.internetAddress)}
                        <a
                            href={m.internetAddress}
                            target="_blank"
                            rel="noopener"
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0]"
                            ><Link class="w-3 h-3" /> وب‌سایت</a
                        >
                    {:else}
                        <span
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[rgba(30,58,107,0.06)] text-[rgba(30,58,107,0.36)] text-xs"
                            ><Link class="w-3 h-3" /> وب‌سایت</span
                        >
                    {/if}
                    {#if defined(m.social_telegram)}
                        <a
                            href={m.social_telegram}
                            target="_blank"
                            rel="noopener"
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0]"
                            >تلگرام</a
                        >
                    {:else}
                        <span
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[rgba(30,58,107,0.06)] text-[rgba(30,58,107,0.36)] text-xs"
                            >تلگرام</span
                        >
                    {/if}
                    {#if defined(m.social_instagram)}
                        <a
                            href={m.social_instagram}
                            target="_blank"
                            rel="noopener"
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0]"
                            >اینستاگرام</a
                        >
                    {:else}
                        <span
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[rgba(30,58,107,0.06)] text-[rgba(30,58,107,0.36)] text-xs"
                            >اینستاگرام</span
                        >
                    {/if}
                    {#if defined(m.social_x)}
                        <a
                            href={m.social_x}
                            target="_blank"
                            rel="noopener"
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0]"
                            >X</a
                        >
                    {:else}
                        <span
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[rgba(30,58,107,0.06)] text-[rgba(30,58,107,0.36)] text-xs"
                            >X</span
                        >
                    {/if}
                    {#if defined(m.social_facebook)}
                        <a
                            href={m.social_facebook}
                            target="_blank"
                            rel="noopener"
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0]"
                            >فیس‌بوک</a
                        >
                    {:else}
                        <span
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[rgba(30,58,107,0.06)] text-[rgba(30,58,107,0.36)] text-xs"
                            >فیس‌بوک</span
                        >
                    {/if}
                    {#if defined(m.social_youtube)}
                        <a
                            href={m.social_youtube}
                            target="_blank"
                            rel="noopener"
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0]"
                            >یوتیوب</a
                        >
                    {:else}
                        <span
                            class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-[rgba(30,58,107,0.06)] text-[rgba(30,58,107,0.36)] text-xs"
                            >یوتیوب</span
                        >
                    {/if}
                </div>
            </div>

            <!-- Markdown body (if any) -->
            <div class="prose lg:prose-xl mt-8">
                <svelte:component this={PostContent} dir="auto" />
            </div>
        </article>
    </OrgPageLayout>
{:else}
    <Header />
    <div class="w-full mx-auto max-w-[800px] prose lg:prose-xl relative mb-24">
        <svelte:component this={PostContent} dir="auto" />
    </div>
    <Footer />
{/if}
