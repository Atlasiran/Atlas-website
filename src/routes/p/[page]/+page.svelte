<script>
    import BlogPageLayout from "@/components/layout/BlogPageLayout.svelte";
    import Contact from "lucide-svelte/icons/contact";
    import Header from "@/components/layout/Header.svelte";
    import Footer from "@/components/layout/Footer.svelte";
    export let data;

    const { title, date, updated, isSvx } = data.meta;
    const { PostContent } = data;
</script>

{#if !isSvx}
    <BlogPageLayout>
        <article
            class="w-full mx-auto max-w-[800px] prose lg:prose-xl relative pt-10"
        >
        <div class="not-prose mb-8">
            <div class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] mb-3">
                <Contact class="w-5 h-5" />
            </div>
            <h1 class="text-4xl font-bold text-[#1E3A6B] mb-2 pb-4 border-b border-[rgba(30,58,107,0.08)]">{title}</h1>
            <div class="flex flex-row gap-4 text-sm text-[rgba(30,58,107,0.56)]">
                <span><b>نوشته شده در:</b> {date}</span>
                <span><b>بروزرسانی شده در:</b> {updated}</span>
            </div>
        </div>
            <svelte:component this={PostContent} dir="auto" />
        </article>
    </BlogPageLayout>
{:else}
    <Header />

    <div class="w-full mx-auto max-w-[800px] prose lg:prose-xl relative mb-24">
        <svelte:component this={PostContent} dir="auto" />
    </div>

    <Footer />
{/if}
