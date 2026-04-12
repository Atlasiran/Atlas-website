<script>
    import Contact from "lucide-svelte/icons/contact";
    export let title;
    export let date;
    export let updated;
    export let headerBg = "";
</script>

<div class="w-full mx-auto max-w-[800px] pt-10 px-8">
    <div class="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-[#EDE3C7] text-[#1E3A6B] mb-4">
        <slot name="page-logo" />
    </div>
    <h1 class="text-4xl font-bold text-[#1E3A6B] mb-3">
        {title}
    </h1>
    <div class="flex flex-row gap-4 text-sm text-[rgba(30,58,107,0.56)]">
        <span><b>نوشته شده در:</b> {date}</span>
        <span><b>بروزرسانی شده در:</b> {updated}</span>
    </div>
    <div class="mt-6 border-b border-[rgba(30,58,107,0.08)]"></div>
</div>

<style>
</style>
