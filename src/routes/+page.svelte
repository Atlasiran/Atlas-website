<script>
    import { base, assets } from "$app/paths";
    import Logo from "$lib/icons/Logo.svelte";
    import ArrowLeft from "lucide-svelte/icons/arrow-left";
    import ChartNetwork from "lucide-svelte/icons/chart-network";
    import Handshake from "lucide-svelte/icons/handshake";
    import Users from "lucide-svelte/icons/users";

    const goals = [
        {
            title: "درک مسیر جنبش",
            desc: "تاریخچه‌ی توسعه‌ی جنبش را بررسی می‌کنیم و نقاط عطف و چالش‌های آن را شناسایی می‌کنیم.",
        },
        {
            title: "نقشه‌برداری شبکه‌ی ارتباطات",
            desc: "ساختارهای موجود در جنبش را تحلیل می‌کنیم تا نقاط قوت، ضعف و فرصت‌های همکاری را شناسایی کنیم.",
        },
        {
            title: "تعمیق درک",
            desc: "با انجام مطالعات عمیق، درک دقیق‌تری از دینامیک و نیازهای جنبش به دست می‌آوریم.",
        },
        {
            title: "ارزیابی منابع",
            desc: "منابع کیفی و کمی در دسترس جنبش را با هدف برنامه‌ریزی استراتژیک بررسی می‌کنیم.",
        },
        {
            title: "اندازه‌گیری تاثیر",
            desc: "پیشرفت‌ها و عقب‌گردها را پیگیری می‌کنیم تا استراتژی‌ها را به طور مداوم اصلاح کنیم.",
        },
        {
            title: "اطلاع‌رسانی برای آینده",
            desc: "برای جمع‌آوری بازخورد از شرکت‌کنندگان در جنبش و شکل‌دهی ابتکارات آینده، نظرسنجی انجام می‌دهیم.",
        },
    ];
</script>

<svelte:head>
    <title>اطلس جامعه مدنی ایران - صفحه‌ی اصلی</title>
    <meta property="og:image" content="{assets}/twitter_banner.png" />
</svelte:head>

<!-- ═══ HERO ═══ -->
<section class="hero dot-background">
    <div
        class="max-w-3xl mx-auto px-6 flex flex-col items-center text-center gap-8"
    >
        <div class="section-badge">
            <span class="badge-pulse"></span>
            پروژه‌ی نقشه‌برداری جامعه مدنی
        </div>

        <div class="w-20 h-20 hero-logo">
            <Logo />
        </div>

        <h1 class="hero-h1">اطلس جامعه مدنی ایران</h1>

        <p class="hero-sub">
            نقشه‌برداری، تحلیل و توانمندسازی شبکه‌ی جنبش‌های آزادی‌خواه ایران
        </p>

        <div class="flex flex-row flex-wrap gap-3 justify-center">
            <a href="{base}/groups" class="btn-primary">کاوش گروه‌ها</a>
            <a href="{base}/p/about-us" class="btn-outline">درباره اطلس</a>
        </div>
    </div>
</section>

<!-- ═══ QUICK NAV CARDS ═══ -->
<div
    class="nav-cards-strip border-t border-b"
    style="border-color: var(--atlas-navy-06)"
>
    <div class="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-3">
        <a href="{base}/groups" class="nav-strip-card">
            <Users class="nav-strip-icon" />
            <div>
                <div class="nav-strip-title">گروه‌ها</div>
                <p class="nav-strip-desc">سازمان‌های مدنی و اجتماعی</p>
            </div>
            <ArrowLeft class="nav-strip-arrow" />
        </a>

        <a
            href="{base}/parties"
            class="nav-strip-card border-y sm:border-y-0 sm:border-x"
            style="border-color: var(--atlas-navy-06)"
        >
            <Handshake class="nav-strip-icon" />
            <div>
                <div class="nav-strip-title">احزاب و سازمان‌های سیاسی</div>
                <p class="nav-strip-desc">طیف سیاسی ایران</p>
            </div>
            <ArrowLeft class="nav-strip-arrow" />
        </a>

        <a
            href="https://atlasiran.github.io/Atlas-website/graph"
            class="nav-strip-card"
        >
            <ChartNetwork class="nav-strip-icon" />
            <div>
                <div class="nav-strip-title">گراف ارتباطات</div>
                <p class="nav-strip-desc">شبکه‌ی بین سازمان‌ها</p>
            </div>
            <ArrowLeft class="nav-strip-arrow" />
        </a>
    </div>
</div>

<!-- ═══ ABOUT SECTION ═══ -->
<section class="about-section">
    <div
        class="max-w-5xl mx-auto px-6 py-24 sm:py-32 grid grid-cols-1 lg:grid-cols-2 gap-16 items-start"
    >
        <div class="flex flex-col gap-5">
            <div class="section-label">درباره اطلس</div>
            <h2 class="section-title">اطلس جامعه مدنی ایران چیست؟</h2>
            <p class="section-body">
                اطلس جامعه مدنی ایرانیان پروژه‌ای است که با هدف توانمندسازی
                سازمان‌های مدنی ایران از راه همکاری هدایت می‌شود. اطلس با هدف
                ایجاد یک جبهه‌ی متحد برای جنبش‌های آزادی‌خواه میان سازمان‌های
                ایرانیان پل می‌زند.
            </p>
        </div>

        <!-- Goals grid -->
        <div class="goals-grid">
            {#each goals as { title, desc }}
                <div class="goal-card">
                    <div class="goal-card-title">{title}</div>
                    <p class="goal-card-desc">{desc}</p>
                </div>
            {/each}
        </div>
    </div>
</section>

<!-- ═══ COLLABORATE SECTION ═══ -->
<section
    class="collab-section border-t"
    style="border-color: var(--atlas-navy-06)"
>
    <div
        class="max-w-5xl mx-auto px-6 py-24 sm:py-32 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center"
    >
        <div class="flex flex-col gap-5">
            <div class="section-label">همکاری</div>
            <h2 class="section-title">چگونه همکاری کنیم؟</h2>
            <p class="section-body">
                پروژه اطلس بر همکاری استوار است. اگر شما نیز به توانمندسازی
                جنبش‌های آزادی‌خواهی ایران علاقه دارید، شما را به همکاری دعوت
                می‌کنیم.
            </p>
        </div>

        <div class="collab-steps">
            <div class="collab-step">
                <span class="step-num">۱</span>
                <p>آخرین اخبار پروژه را در این وبسایت دنبال کنید.</p>
            </div>
            <div class="collab-step">
                <span class="step-num">۲</span>
                <p>دانش خود را به اشتراک بگذارید.</p>
            </div>
            <div class="collab-step last">
                <span class="step-num">۳</span>
                <p>
                    با ما
                    <a href="mailto:hi@atlasiran.org" class="collab-link"
                        >تماس بگیرید</a
                    >.
                </p>
            </div>
        </div>
    </div>
</section>

<style>
    /* ── Hero ── */
    .hero {
        min-height: calc(100vh - 56px);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 80px 0 60px;
    }

    .hero-logo {
        opacity: 0.9;
    }

    .hero-h1 {
        font-size: clamp(2rem, 6vw, 3.5rem);
        font-weight: 900;
        line-height: 1.3;
        color: #1e3a6b;
        letter-spacing: -0.01em;
    }

    .hero-sub {
        font-size: 1.0625rem;
        font-weight: 300;
        color: rgba(30, 58, 107, 0.64);
        max-width: 520px;
        line-height: 2;
    }

    /* ── Hero badge ── */
    .section-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 16px;
        border: 1px solid rgba(30, 58, 107, 0.12);
        border-radius: 999px;
        font-size: 0.8125rem;
        font-weight: 400;
        color: rgba(30, 58, 107, 0.56);
    }

    .badge-pulse {
        width: 6px;
        height: 6px;
        background: #0ebb90;
        border-radius: 50%;
        flex-shrink: 0;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.3;
        }
    }

    /* ── Dot background ── */
    .dot-background {
        /* inherits dot pattern from body */
    }

    /* ── Quick nav strip ── */
    .nav-cards-strip {
        background: #f4f6f7;
    }

    .nav-strip-card {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 16px;
        padding: 28px 32px;
        text-decoration: none;
        transition: background 0.18s ease;
        color: #1e3a6b;
        background: #f4f6f7;
    }

    .nav-strip-card:hover {
        background: #ede3c7;
    }

    .nav-strip-icon {
        width: 28px;
        height: 28px;
        flex-shrink: 0;
        opacity: 0.5;
        color: #1e3a6b;
    }

    .nav-strip-title {
        font-size: 0.9375rem;
        font-weight: 700;
        color: #1e3a6b;
        margin-bottom: 2px;
    }

    .nav-strip-desc {
        font-size: 0.8125rem;
        font-weight: 300;
        color: rgba(30, 58, 107, 0.56);
    }

    .nav-strip-arrow {
        width: 16px;
        height: 16px;
        color: rgba(30, 58, 107, 0.3);
        margin-right: auto;
        /* Flip for RTL: arrow points left (toward destination) */
        transform: rotate(180deg);
        transition:
            transform 0.18s ease,
            color 0.18s ease;
    }

    .nav-strip-card:hover .nav-strip-arrow {
        color: #1e3a6b;
        transform: rotate(180deg) translateX(-4px);
    }

    /* ── About section ── */
    .about-section {
        background: #ede3c7;
    }

    /* ── Goals grid ── */
    .goals-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1px;
        background-color: rgba(30, 58, 107, 0.08);
        border: 1px solid rgba(30, 58, 107, 0.08);
        border-radius: 12px;
        overflow: hidden;
    }

    .goal-card {
        background: #ede3c7;
        padding: 20px;
        transition: background 0.18s ease;
    }

    .goal-card:hover {
        background: #e4d7b3;
    }

    .goal-card-title {
        font-size: 0.875rem;
        font-weight: 700;
        color: #1e3a6b;
        margin-bottom: 6px;
    }

    .goal-card-desc {
        font-size: 0.8125rem;
        color: rgba(30, 58, 107, 0.64);
        line-height: 1.7;
        font-weight: 300;
    }

    /* ── Collab section ── */
    .collab-section {
        background: #f4f6f7;
    }

    .collab-steps {
        display: flex;
        flex-direction: column;
    }

    .collab-step {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding-bottom: 24px;
        border-bottom: 1px solid rgba(30, 58, 107, 0.06);
        margin-bottom: 24px;
        font-size: 0.9375rem;
        color: rgba(30, 58, 107, 0.72);
        font-weight: 300;
        line-height: 1.8;
    }

    .collab-step.last {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }

    .step-num {
        flex-shrink: 0;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(30, 58, 107, 0.12);
        border-radius: 50%;
        font-weight: 600;
        font-size: 0.8125rem;
        color: #1e3a6b;
    }

    .collab-link {
        font-weight: 600;
        color: #1e3a6b;
        text-decoration: underline;
        text-underline-offset: 3px;
    }

    /* ── Responsive ── */
    @media (max-width: 640px) {
        .goals-grid {
            grid-template-columns: 1fr;
        }

        .nav-strip-arrow {
            display: none;
        }
    }
</style>
