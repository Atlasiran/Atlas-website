<script>
    import { base } from "$app/paths";
    import Footer from "@/components/layout/Footer.svelte";
    import Header from "@/components/layout/Header.svelte";
    import OrgPageLayout from "@/components/layout/OrgPageLayout.svelte";
    import Building2 from "lucide-svelte/icons/building-2";
    import Link from "lucide-svelte/icons/link";
    export let data;

    const m = data.meta;
    const { PostContent } = data;

    // Relations with other organisations; each one carries its public source and a status
    const REL_OUT = {
        member_of: "عضو",
        affiliated_with: "وابسته به",
        coalition_partner: "هم‌پیمان با",
        split_from: "منشعب از",
        merged_into: "ادغام‌شده در",
        successor_of: "جانشین",
    };
    const REL_IN = {
        member_of: "اعضا",
        affiliated_with: "نهادهای وابسته",
        coalition_partner: "هم‌پیمان با",
        split_from: "انشعاب‌ها",
        merged_into: "ادغام‌شده در این نهاد",
        successor_of: "جانشینان",
    };
    const REL_STATUS = {
        self_declared: "به اعلام خود نهاد",
        documented: "مستند",
        disputed: "مورد مناقشه",
    };
    const relationGroups = (() => {
        const groups = new Map();
        const add = (key, label, r) => {
            if (!groups.has(key)) groups.set(key, { label, items: [] });
            groups.get(key).items.push(r);
        };
        for (const r of data.relations?.out || [])
            add(r.type === "coalition_partner" ? r.type : `out:${r.type}`, REL_OUT[r.type], r);
        for (const r of data.relations?.in || [])
            add(r.type === "coalition_partner" ? r.type : `in:${r.type}`, REL_IN[r.type], r);
        return [...groups.values()];
    })();
    const relationDates = (r) =>
        [r.since, r.until].some(defined) ? `${r.since || "?"} – ${r.until || "اکنون"}` : "";

    const orgName = [m.name_fa, m.name_en, m.name_short, m.title].find(defined);

    const ORG_TYPE_LABELS = {
        ORG: "سازمان مدنی",
        P_ORG: "سازمان سیاسی",
        H_ORG: "سازمان حقوق بشری",
        NGO: "سازمان غیردولتی (NGO)",
        PARTY: "حزب سیاسی",
        رسانه: "رسانه",
        پروژه: "پروژه",
        گوناگون: "گوناگون",
        "سازمان سیاسی - بسته شده": "سازمان سیاسی - بسته شده",
    };
    const orgTypeLabel =
        (m.org_type && ORG_TYPE_LABELS[m.org_type]) || m.org_type || null;

    // Normalize a social field value to a full URL, or return null if unusable.
    // Handles: full URLs, @handle, plain handle, Python list literals ['handle'].
    function socialUrl(value, base) {
        if (!defined(value)) return null;
        // Strip Python list literal: ['handle'] or ["handle"]
        const listMatch = value.match(/^\[['"](.+?)['"]\]$/);
        if (listMatch) value = listMatch[1];
        if (!defined(value)) return null;
        if (value.startsWith("http://") || value.startsWith("https://"))
            return value;
        const handle = value.startsWith("@") ? value.slice(1) : value;
        return `${base}${handle}`;
    }

    const links = {
        telegram: socialUrl(m.social_telegram, "https://t.me/"),
        instagram: socialUrl(m.social_instagram, "https://instagram.com/"),
        x: socialUrl(m.social_x, "https://x.com/"),
        facebook: socialUrl(m.social_facebook, "https://facebook.com/"),
        youtube: socialUrl(m.social_youtube, "https://youtube.com/"),
        bluesky: socialUrl(m.social_bluesky, "https://bsky.app/profile/"),
        linkedin: socialUrl(m.social_linkedin, "https://linkedin.com/"),
        tiktok: socialUrl(m.social_tiktok, "https://tiktok.com/@"),
        web:
            defined(m.internetAddress) && m.internetAddress.startsWith("http")
                ? m.internetAddress
                : null,
    };

    function isDocumentLink(value) {
        if (!defined(value)) return false;
        return (
            value.startsWith("http://") ||
            value.startsWith("https://") ||
            value.startsWith("/") ||
            value.includes(".pdf") ||
            value.includes(".doc") ||
            value.includes(".docx")
        );
    }

    function documentLink(value) {
        if (value.startsWith("http://") || value.startsWith("https://")) {
            return value;
        }
        const normalized = value.startsWith("/") ? value : `/${value}`;
        return `${base}${normalized}`;
    }

    function defined(v) {
        return v && v !== "None" && v.trim() !== "";
    }

    const SITE_URL = "https://AtlasIran.org";
    const DEFAULT_OG_IMAGE = `${SITE_URL}/og-image.jpg`;
    const REPORT_EMAIL = "hi@AtlasIran.org";

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
        ? `${SITE_URL}/og/op/${encodeURIComponent(slug)}.jpg`
        : DEFAULT_OG_IMAGE;
    const ogUrl = m.pageLink
        ? `${SITE_URL}${m.pageLink.split("/").map(encodeURIComponent).join("/")}`
        : SITE_URL;

    const reportSubject = encodeURIComponent(
        `درخواست ویرایش نهاد ${orgName || ""}`,
    );
    const reportBody = encodeURIComponent(`آدرس صفحه: ${ogUrl}`);
    const reportLink = `mailto:${REPORT_EMAIL}?subject=${reportSubject}&body=${reportBody}`;
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
        <article class="w-full mx-auto max-w-[960px] pt-10 pb-16">
            <!-- Header -->
            <div class="mb-8 flex items-start gap-5">
                {#if defined(m.logo)}
                    <img
                        src="{base}/{m.logo}"
                        alt={orgName}
                        class="w-20 h-20 rounded-xl object-contain bg-white border border-[rgba(30,58,107,0.1)] p-1 shrink-0"
                    />
                {:else}
                    <div
                        class="inline-flex items-center justify-center w-20 h-20 rounded-xl bg-[#EDE3C7] text-[#1E3A6B] shrink-0"
                    >
                        <Building2 class="w-8 h-8" />
                    </div>
                {/if}
                <h1
                    class="text-4xl font-bold text-[#1E3A6B] mb-2 pb-4 border-b border-[rgba(30,58,107,0.08)] w-full"
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
                        {orgTypeLabel || "—"}
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
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        نام محلی
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.name_local || "—"}
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
                        <span
                            class="font-normal text-[rgba(30,58,107,0.5)] text-xs"
                            >(این برداشت ماست)</span
                        >
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.political_orientation || "—"}
                    </dd>
                </div>
                <div>
                    <dt class="font-semibold text-[#1E3A6B] mb-0.5">
                        ایمیل یا راه تماس
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {#if defined(m.contact)}
                            <a
                                href="mailto:{m.contact}"
                                class="underline hover:text-[#1E3A6B]"
                                >{m.contact}</a
                            >
                        {:else}
                            —
                        {/if}
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
                        بروزرسانی
                    </dt>
                    <dd class="text-[rgba(30,58,107,0.72)]">
                        {m.updated_at || "—"}
                    </dd>
                </div>
            </dl>

            <!-- Main content + links sidebar (flex-row-reverse puts aside on the left visually) -->
            <div
                class="mt-6 flex flex-col lg:flex-row-reverse gap-8 items-start"
            >
                <!-- Main content -->
                <div class="flex-1 min-w-0">
                    <!-- تخصص‌ها -->
                    <div class="mb-4">
                        <h2 class="font-semibold text-[#1E3A6B] mb-0.5 text-sm">
                            تخصص‌ها
                        </h2>
                        <p
                            class="text-[rgba(30,58,107,0.72)] text-sm leading-relaxed break-words"
                        >
                            {m.expertise || "—"}
                        </p>
                    </div>

                    <!-- مرامنامه یا مانیفست -->
                    <div class="mb-4">
                        <h2 class="font-semibold text-[#1E3A6B] mb-0.5 text-sm">
                            مرامنامه یا مانیفست
                        </h2>
                        <p
                            class="text-[rgba(30,58,107,0.72)] text-sm leading-relaxed break-words"
                        >
                            {#if defined(m.coc) || defined(m.manifest)}
                                {#if defined(m.coc)}
                                    {#if isDocumentLink(m.coc)}
                                        <a
                                            href={documentLink(m.coc)}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            class="inline-flex items-center gap-1 text-[#1E3A6B] underline hover:opacity-70"
                                            >مشاهده سند ↗</a
                                        >
                                    {:else}
                                        {m.coc}
                                    {/if}
                                {/if}
                                {#if defined(m.coc) && defined(m.manifest)}<br
                                    />{/if}
                                {#if defined(m.manifest)}
                                    {#if isDocumentLink(m.manifest)}
                                        <a
                                            href={documentLink(m.manifest)}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            class="inline-flex items-center gap-1 text-[#1E3A6B] underline hover:opacity-70"
                                            >مشاهده سند ↗</a
                                        >
                                    {:else}
                                        {m.manifest}
                                    {/if}
                                {/if}
                            {:else}
                                —
                            {/if}
                        </p>
                    </div>

                    <!-- پیوندها و وابستگی‌ها -->
                    {#if relationGroups.length}
                        <div class="mb-4">
                            <h2 class="font-semibold text-[#1E3A6B] mb-0.5 text-sm">
                                پیوندها و وابستگی‌ها
                            </h2>
                            {#each relationGroups as g}
                                <h3 class="text-[rgba(30,58,107,0.72)] text-xs font-medium mt-2 mb-1">
                                    {g.label}
                                </h3>
                                <ul class="text-sm leading-relaxed space-y-1">
                                    {#each g.items as r}
                                        <li class="text-[rgba(30,58,107,0.72)] break-words">
                                            <a
                                                href="{base}{r.org.pageLink}"
                                                class="text-[#1E3A6B] underline hover:opacity-70"
                                                >{r.org.name_fa || r.org.name_en}</a
                                            >
                                            {#if relationDates(r)}<span class="text-xs"> ({relationDates(r)})</span>{/if}
                                            <span
                                                class="text-xs px-1.5 py-0.5 rounded {r.status === 'disputed'
                                                    ? 'bg-[#EDE3C7] text-[#1E3A6B]'
                                                    : 'bg-[rgba(30,58,107,0.07)]'}"
                                                >{REL_STATUS[r.status]}</span
                                            >
                                            <a
                                                href={r.source}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                class="text-xs underline hover:opacity-70"
                                                >منبع ↗</a
                                            >
                                        </li>
                                    {/each}
                                </ul>
                            {/each}
                        </div>
                    {/if}

                    <!-- درباره -->
                    <div class="mb-4">
                        <h2 class="font-semibold text-[#1E3A6B] mb-0.5 text-sm">
                            درباره
                        </h2>
                        <p
                            class="text-[rgba(30,58,107,0.72)] text-sm leading-relaxed break-words"
                        >
                            {#if m.about && m.about.startsWith("http")}
                                <a
                                    href={m.about}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-1 text-[#1E3A6B] underline hover:opacity-70"
                                    >مشاهده ↗</a
                                >
                            {:else}
                                {m.about || "—"}
                            {/if}
                        </p>
                    </div>

                    <!-- تاریخچه -->
                    <div class="mb-4">
                        <h2 class="font-semibold text-[#1E3A6B] mb-0.5 text-sm">
                            تاریخچه
                        </h2>
                        <p
                            class="text-[rgba(30,58,107,0.72)] text-sm leading-relaxed break-words"
                        >
                            {m.history || "—"}
                        </p>
                    </div>

                    <!-- Markdown body (if any) -->
                    <div class="prose lg:prose-xl mt-8">
                        <svelte:component this={PostContent} dir="auto" />
                    </div>

                    <!-- Report error -->
                    <div
                        class="mt-10 pt-6 border-t border-[rgba(30,58,107,0.12)] flex flex-col sm:flex-row sm:items-center gap-3"
                    >
                        <p class="text-sm text-[rgba(30,58,107,0.55)] flex-1">
                            آیا اطلاعاتی در این صفحه نادرست یا ناکامل است؟
                            می‌توانید درخواست ویرایش ارسال کنید.
                        </p>
                        <a
                            href={reportLink}
                            class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-[rgba(30,58,107,0.07)] text-[#1E3A6B] text-sm font-medium hover:bg-[rgba(30,58,107,0.14)] transition-colors shrink-0"
                        >
                            درخواست ویرایش اطلاعات
                        </a>
                    </div>
                </div>

                <!-- Links sidebar (appears on the left in RTL flex-row-reverse layout) -->
                <aside class="w-full lg:w-52 lg:shrink-0">
                    <div
                        class="lg:sticky lg:top-6 rounded-xl border border-[rgba(30,58,107,0.1)] bg-[rgba(30,58,107,0.02)] p-4"
                    >
                        <h2 class="font-semibold text-[#1E3A6B] mb-3 text-sm">
                            پیوندها
                        </h2>
                        <div class="flex flex-wrap lg:flex-col gap-2">
                            {#if links.web}
                                <a
                                    href={links.web}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    ><Link class="w-3.5 h-3.5 shrink-0" /> وب‌سایت</a
                                >
                            {/if}
                            {#if links.telegram}
                                <a
                                    href={links.telegram}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >تلگرام</a
                                >
                            {/if}
                            {#if links.instagram}
                                <a
                                    href={links.instagram}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >اینستاگرام</a
                                >
                            {/if}
                            {#if links.x}
                                <a
                                    href={links.x}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >X</a
                                >
                            {/if}
                            {#if links.facebook}
                                <a
                                    href={links.facebook}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >فیس‌بوک</a
                                >
                            {/if}
                            {#if links.youtube}
                                <a
                                    href={links.youtube}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >یوتیوب</a
                                >
                            {/if}
                            {#if links.bluesky}
                                <a
                                    href={links.bluesky}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >بلواسکای</a
                                >
                            {/if}
                            {#if links.linkedin}
                                <a
                                    href={links.linkedin}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >لینکدین</a
                                >
                            {/if}
                            {#if links.tiktok}
                                <a
                                    href={links.tiktok}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] text-xs font-medium hover:bg-[#d6cdb0] transition-colors"
                                    >تیک‌تاک</a
                                >
                            {/if}
                            {#if !links.web && !links.telegram && !links.instagram && !links.x && !links.facebook && !links.youtube && !links.bluesky && !links.linkedin && !links.tiktok}
                                <span class="text-xs text-[rgba(30,58,107,0.4)]"
                                    >—</span
                                >
                            {/if}
                        </div>
                    </div>
                </aside>
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
