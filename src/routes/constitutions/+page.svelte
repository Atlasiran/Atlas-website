<script>
    import { base } from "$app/paths";
    import { onDestroy, onMount } from "svelte";

    // The constitutions corpus (modules/constitutions) is built into
    // static/modules/constitutions/ before the Vite build; see "build:constitutions".
    const moduleUrl = `${base}/modules/constitutions/`;

    let container;
    let app;
    let failed = false;

    onMount(async () => {
        try {
            const { mount } = await import(/* @vite-ignore */ `${moduleUrl}app.js`);
            app = mount(container, {
                lang: "fa",
                embedded: true,
                theme: "atlas",
                dataUrl: `${moduleUrl}data/`,
            });
        } catch (e) {
            console.error(e);
            failed = true;
        }
    });

    onDestroy(() => app?.destroy());
</script>

<svelte:head>
    <title>اطلس جامعه مدنی ایران - اسناد بنیادین</title>
    <meta
        name="description"
        content="پیش‌نویس‌های قانون اساسی ایران، منشورها و اساسنامه‌ها: متن کامل، تفکیک‌شده به اصول و قابل مقایسه."
    />
    <link rel="stylesheet" href="{moduleUrl}app.css" />
    <link rel="stylesheet" href="{moduleUrl}atlas-theme.css" />
</svelte:head>

<div class="container mx-auto pt-8 pb-16">
    <div class="mb-8">
        <h1 class="text-4xl font-bold text-[#1E3A6B] dark:text-foreground mb-4">
            اسناد بنیادین
        </h1>
        <p class="text-justify text-[rgba(30,58,107,0.64)] dark:text-muted-foreground">
            قانون‌های اساسی، پیش‌نویس‌ها و منشورهای پیشنهادی برای ایران، با متن کامل
            و تفکیک‌شده به اصول. اسناد تنها با اسناد هم‌گونه مقایسه می‌شوند:
            قانون اساسی با قانون اساسی، اساسنامه با اساسنامه. متن‌ها همان‌گونه‌اند
            که نویسندگانشان نوشته‌اند و هیچ‌کدام رتبه‌بندی یا تأیید نشده‌اند.
        </p>
    </div>

    {#if failed}
        <p class="text-center text-muted-foreground py-16">
            بارگذاری اسناد ممکن نشد.
        </p>
    {/if}
    <div bind:this={container} dir="rtl"></div>
</div>
