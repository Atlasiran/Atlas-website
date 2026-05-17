<script>
    import { cubicIn, cubicOut } from "svelte/easing";
    import { fly } from "svelte/transition";

    import Footer from "$lib/components/layout/Footer.svelte";
    import Header from "$lib/components/layout/Header.svelte";
    import { Toaster } from "$lib/components/ui/sonner";
    import { authStore } from "$lib/stores/authStore";
    import { supabase } from "$lib/supabaseClient";
    import { onMount } from "svelte";
    import { siteDescription, siteName, siteTitle } from "../content/configs";

    import "../app.css";
    export let data = {};

    onMount(async () => {
        const {
            data: { session },
        } = await supabase.auth.getSession();
        const user = session?.user ?? null;

        if (user) {
            const { email, email_confirmed_at, last_sign_in_at } = user;
            authStore.update((state) => {
                return {
                    ...state,
                    user: {
                        email,
                        email_confirmed_at,
                        last_sign_in_at,
                    },
                };
            });
        }

        supabase.auth.onAuthStateChange((event, session) => {
            const user = session?.user ?? null;
            if (user) {
                const { email, email_confirmed_at, last_sign_in_at } = user;
                authStore.update((state) => {
                    return {
                        ...state,
                        isAuthenticated: !!user,
                        user: {
                            email,
                            email_confirmed_at,
                            last_sign_in_at,
                        },
                    };
                });
            } else {
                authStore.update((state) => {
                    return {
                        ...state,
                        isAuthenticated: !!user,
                        user: null,
                    };
                });
            }
        });
    });
</script>

<svelte:head>
    <meta property="og:title" content={siteTitle} />
    <meta property="og:site_name" content={siteName} />
    <meta property="og:description" content={siteDescription} />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@AtlasIranOrg" />
    <meta name="twitter:creator" content="@AtlasIranOrg" />
</svelte:head>
<Toaster />

<div class="flex h-screen flex-col justify-between pt-[56px]">
    <Header />

    <!-- Review banner -->
    <div
        class="w-full bg-[#EDE3C7] text-[#1E3A6B] text-sm text-center py-2 px-4 leading-relaxed"
        dir="rtl"
    >
        داده‌های نسخه‌ی تازه‌ی اطلس (۰.۲.۰) برای مدت یک‌ماه برای بازبینی در
        دسترس همگان قرار دارند. لطفن ایرادات را از راهی که در برگه‌ی هر نهاد
        آمده برای ما بفرستید.
    </div>

    <main class="mb-auto">
        {#key data?.pathname}
            <div
                in:fly={{ easing: cubicOut, y: 10, duration: 300, delay: 400 }}
                out:fly={{ easing: cubicIn, y: -10, duration: 300 }}
            >
                <slot />
            </div>
        {/key}
    </main>
    <div class="w-full">
        <Footer />
    </div>
</div>
