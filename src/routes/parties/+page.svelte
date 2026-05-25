<script>
    import { base } from "$app/paths";
    import * as Card from "$lib/components/ui/card/index.js";
    import ListAllGroups from "@/components/ListAllGroups.svelte";
    import { onMount } from "svelte";

    let data = [];

    let stats = [
        { title: "تعداد کل گروه‌های فعال", value: 0 },
        { title: "اخرین بروزرسانی", value: "۱۴۰۵/۰۲/۲۷" },
    ];

    onMount(() => {
        fetch(`${base}/data/political_parties.json`)
            .then((response) => response.json())
            .then((json) => {
                data = json;
                stats[0].value = data.length;
            });
    });
</script>

<svelte:head>
    <title>اطلس جامعه مدنی ایران - احزاب و سازمان‌های سیاسی</title>
</svelte:head>

<div class="container mx-auto pt-8">
    <div class="mb-32">
        <h1 class="text-4xl font-bold text-[#1E3A6B] mb-4">
            احزاب و سازمان‌های سیاسی
        </h1>
        <p class="text-justify text-[rgba(30,58,107,0.64)]">
            در این بخش می‌توانید اطلاعات مربوط به احزاب و سازمان‌های سیاسی را
            مشاهده کنید. این نهادها بر اساس مستندات عمومی جمع‌آوری شده‌اند. اگر
            اطلاعاتی در این اطلس ناقص یا نادرست است، لطفن به ما اطلاع بدهید.
            برای اطلاعات بیشتر به بخش «همکاری» مراجعه کنید.
        </p>
    </div>

    <div class="flex flex-row my-16 gap-4">
        {#each stats as { title, value }}
            <Card.Root class="w-[250px]">
                <Card.Header
                    class="flex flex-row items-center justify-between space-y-0 pb-2"
                >
                    <Card.Title class="text-sm font-medium">
                        {title}
                    </Card.Title>
                </Card.Header>
                <Card.Content>
                    <div class="text-2xl font-bold">
                        {value}
                    </div>
                    <p class="text-muted-foreground text-xs"></p>
                </Card.Content>
            </Card.Root>
        {/each}
    </div>

    <ListAllGroups {data} />
</div>
