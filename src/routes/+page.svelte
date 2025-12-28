<script>   
    import Button from "@/components/ui/button/button.svelte";
    import { onMount } from "svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import Link from "lucide-svelte/icons/link";
    import Scale from "lucide-svelte/icons/scale";
    import ScrollText from "lucide-svelte/icons/scroll-text";
    import Fullscreen from "lucide-svelte/icons/fullscreen";
    import MapPin from "lucide-svelte/icons/map-pin";
    import Users from "lucide-svelte/icons/users";
    import * as Tooltip from "$lib/components/ui/tooltip/index.js";
    import ListAllGroups from "@/components/ListAllGroups.svelte";
    import Header from "@/components/layout/Header.svelte";
    import Hash from "lucide-svelte/icons/hash";
    import Globe from "lucide-svelte/icons/globe";
    import Logo from "$lib/icons/Logo.svelte";
    import Handshake from "lucide-svelte/icons/handshake";
    import ChartNetwork from "lucide-svelte/icons/chart-network";
    import { base } from "$app/paths";

    let data = [];

    onMount(() => {});
</script>

<svelte:head>
    <title>اطلس جامعه مدنی ایران - صفحه‌ی اصلی</title>
</svelte:head>

<div class="container mx-auto">
    <section
        class="flex flex-col justify-center items-center gap-8 dot-background"
    >
        <div class="w-[200px] h-[200px]">
            <Logo />
        </div>
        <h1 class="text-3xl sm:text-5xl text-gray-600">
            اطلس جامعه مدنی ایران
        </h1>
    </section>

    <section class="p-2 sm:p-8 flex flex-col gap-16">
        <div class="card">
            <h2 class="text-4xl font-extralight text-center flex-grow">
                اطلس جامعه مدنی ایران چیست؟
            </h2>
            <p class="w-96 text-gray-600 flex-grow">
                <br />
                اطلس جامعه مدنی ایرانیان پروژه‌ای است که با هدف توانمندسازی سازمان‌های مدنی ایران از راه همکاری هدایت می‌شود. اطلس با هدف ایجاد یک جبهه‌ی متحد برای <a href="جنبش">جنبش زن، زندگی، آزادی</a> میان سازمان‌های ایرانیان پل می‌زند.
                <br />
                <br />
                <strong>هدف‌ها</strong>
               
                <br />
                <br />
                <strong>درک مسیر جنبش:</strong> ما تاریخچه‌ی توسعه‌ی جنبش را بررسی می‌کنیم و نقاط عطف و چالش‌های آن را شناسایی می‌کنیم.
                <br />
                <br />
                <strong>نقشه برداری از شبکه‌ی ارتباطات:</strong> ما ساختارهای موجود در جنبش را تحلیل می‌کنیم تا نقاط قوت، ضعف و فرصت‌های همکاری را شناسایی کنیم.
                <br />
                <br />
                <strong>تعمیق درک:</strong> ما با انجام مطالعات عمیق، درک دقیق‌تری از دینامیک و نیازهای جنبش به دست می‌آوریم.
                <br />
                <br />
                <strong>ارزیابی منابع:</strong> ما منابع کیفی و کمی در دسترس جنبش را با هدف برنامه‌ریزی استراتژیک بررسی می‌کنیم.
                <br />
                <br />
                <strong>اندازه‌گیری تاثیر:</strong> ما پیشرفت‌ها و عقب‌گردها را پیگیری می‌کنیم تا استراتژی‌ها را به طور مداوم اصلاح کنیم و اثربخشی تلاش‌های مشترک را اندازه‌گیری کنیم.
                <br />
                <br />
                <strong>اطلاع‌رسانی برای آینده:</strong> ما برای جمع‌آوری بازخورد از شرکت‌کنندگان در جنبش، و شکل‌دهی ابتکارات آینده، نظرسنجی انجام می‌دهیم.
            </p>
        </div>

        <div class="py-32 flex flex-col justify-center gap-32 items-center justify-between">
            <div class="flex flex-row flex-wrap gap-8 justify-center">
            <a href="{base}/groups">
                <Card.Root
                class="w-[200px] h-[200px] flex flex-col justify-center items-center gap-4
                hover:border-yellow-600 transition-colors text-gray-700 hover:text-yellow-600"
                >
                <Users class="h-20 w-20 " />
                <span class="text-3xl"> گروه ها </span>
                </Card.Root>
            </a>

            <a href="{base}/parties">
                <Card.Root
                class="w-[200px] h-[200px] flex flex-col justify-center items-center gap-4
                hover:border-yellow-600 transition-colors text-gray-700 hover:text-yellow-600"
                >
                <Handshake class="h-20 w-20 " />
                <span class="text-3xl text-center">احزاب و سازمان‌های سیاسی</span>
                </Card.Root>
            </a>

            <a href="https://graphcommons.com/graphs/7cac498a-d3a1-4a8f-b993-e8c8bdf13ae7">
                <Card.Root
                class="w-[200px] h-[200px] flex flex-col justify-center items-center gap-4
                hover:border-yellow-600 transition-colors text-gray-700 hover:text-yellow-600"
                >
                <ChartNetwork class="h-20 w-20 " />
                <span class="text-3xl"> گراف</span>
                </Card.Root>
            </a>
            </div>

        </div>

        <div class="card-2">
            <h2 class="text-2xl font-extralight text-center flex-grow">
                چگونه همکاری کنیم؟
            </h2>
            <p class="w-96 text-gray-600 flex-grow">
                پروژه اطلس بر همکاری استوار است. اگر شما نیز به توانمندسازی جنبش زن، زندگی، آزادی علاقه دارید، شما را به همکاری دعوت می‌کنیم. شما می‌توانید:
                <br />
                <br />
                - آخرین اخبار پروژه را در این وبسایت دنبال کنید.<br />
                - دانش خود را به اشتراک بگذارید.<br />
                - با ما <a href="mailto:hi@atlasiran.org" class="underline">تماس بگیرید</a>.<br />
            </p>
        </div>
    </section>
</div>

<style>
    .card {
        @apply w-full text-justify  bg-gradient-to-tr from-gray-50 to-gray-100 px-2 sm:p-8 rounded-md flex flex-row flex-wrap justify-between items-center;
        @apply border-[1px] border-gray-200;
    }
    .card-2 {
        @apply w-full text-justify  bg-gradient-to-bl from-gray-50 to-gray-100 px-2 sm:p-8 rounded-md flex flex-row flex-wrap justify-between items-center;
        @apply border-[1px] border-gray-200;
    }
    section {
        min-height: calc(100vh - 50px);
    }

    @keyframes wave {
        0%,
        100% {
            background-position: 0 0;
        }
        50% {
            background-position: 50px 50px;
        }
    }

    .dot-background {
        background-image: radial-gradient(
            circle,
            rgba(0, 0, 0, 0.2) 1px,
            transparent 1px
        );
        background-size: 20px 20px;
        animation: wave 50s linear infinite;
    }
</style>
