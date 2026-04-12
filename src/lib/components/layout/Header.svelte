<script>
    import { onMount } from "svelte";
    import Button from "@/components/ui/button/button.svelte";
    import Globe from "lucide-svelte/icons/globe";
    import { page } from "$app/stores";
    import * as Sheet from "$lib/components/ui/sheet";
    import { SheetClose } from "$lib/components/ui/sheet";
    import Menu from "lucide-svelte/icons/menu";
    import { defaultHeaderLinks, siteTitle } from "../../../content/configs";
    import Logo from "$lib/icons/Logo.svelte";
    import AuthButton from "$lib/components/AuthButton.svelte";
    import { base } from "$app/paths";

    export let haederLinks = defaultHeaderLinks;
    export let style = 2;

    let isSticky = false;
    let scrollY;

    $: {
        if (scrollY > 20) {
            isSticky = true;
        } else {
            isSticky = false;
        }
    }

    onMount(() => {});
</script>

<svelte:window bind:scrollY />

{#if style == 1}
    <header>
        <div
            class="container flex-grow flex flex-col mr-auto justify-center items-center gap-4"
        >
            <Globe class="w-[200px] h-[200px] text-indigo-300 " />
            <a href="{base}">
                <h1 class="font-extralight text-4xl text-gray-600">
                    {siteTitle}
                </h1>
            </a>
        </div>

        <div class="bg-gray-700 border-b container rounded-t-md">
            <div class="flex flex-row justify-start gap-5">
                {#each haederLinks as { name, link }, idx (idx)}
                    <a
                        href="{base}{link}"
                        class:active-link={$page.url.pathname === link}
                        class:not-active-link={$page.url.pathname !== link}
                        class="my-4 text-lg"
                    >
                        {name}
                    </a>
                {/each}
            </div>
            <div>
                <AuthButton />
            </div>
        </div>
    </header>
    <div
        class:sticky-header={isSticky}
        class="hidden bg-gray-700 border-b container rounded-t-md flex-row justify-between"
    >
        <div class="inline-flex items-center flex-row gap-4">
            <Globe class="w-4 h-4 text-indigo-300 " />
            <h1 class="font-extralight text-md">اطلس جامعه مدنی ایران</h1>
        </div>
        <div class="inline-flex flex-row justify-start gap-5">
            {#each haederLinks as { name, link }, idx (idx)}
                <a
                    href="{base}{link}"
                    class:active-link={$page.url.pathname === link}
                    class:not-active-link={$page.url.pathname !== link}
                    class="my-4 text-sm"
                >
                    {name}
                </a>
            {/each}
        </div>
        <div class="">
            <AuthButton />
        </div>
    </div>
{:else if style == 2}
    <div class="nav-bar w-full sticky-header h-[56px] t-0" class:nav-scrolled={isSticky}>
        <div class="container mx-auto flex flex-row justify-between items-center h-full px-4 lg:px-8">
            <a href="{base}/" class="inline-flex items-center flex-row gap-3 nav-logo-text" style="text-decoration:none">
                <div class="w-5 h-5 logo-icon">
                    <Logo />
                </div>
                <span class="font-semibold text-sm tracking-tight">
                    {siteTitle}
                </span>
            </a>

            <Sheet.Root>
                <Sheet.Trigger>
                    <Button variant="ghost" class="inline-flex lg:hidden p-2 text-[var(--atlas-navy-64)] hover:text-[var(--atlas-navy)]">
                        <Menu class="w-5 h-5" />
                    </Button>
                </Sheet.Trigger>
                <Sheet.Content side="left" class="bg-[#F4F6F7]">
                        <div class="flex flex-col justify-between h-full">
                            <div
                                class="inline-flex flex-col text-right justify-start gap-1 mt-8"
                            >
                                {#each haederLinks as { name, link }, idx (idx)}
                                    <SheetClose>
                                        <a href="{base}{link}" class="mobile-nav-link">
                                            {name}
                                        </a>
                                    </SheetClose>
                                {/each}
                            </div>
                            <div class="flex-col text-center justify-center gap-4 mt-8">
                                <AuthButton />
                            </div>
                        </div>
                </Sheet.Content>
            </Sheet.Root>

            <div class="hidden lg:inline-flex flex-row items-center justify-start gap-1">
                {#each haederLinks as { name, link }, idx (idx)}
                    <a
                        href="{base}{link}"
                        class:desktop-nav-active={$page.url.pathname === link}
                        class="desktop-nav-link"
                    >
                        {name}
                    </a>
                {/each}
                <div class="mr-2">
                    <AuthButton short={true} />
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    header {
        @apply bg-[#F4F6F7] mb-4 border-b flex flex-col;
        height: calc(100vh + 3px);
    }

    .sticky-header {
        display: flex;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
    }

    /* Nav bar default state */
    .nav-bar {
        background: rgba(244, 246, 247, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid transparent;
        transition: border-color 0.18s ease, background 0.18s ease;
    }

    .nav-scrolled {
        background: rgba(244, 246, 247, 0.95);
        border-bottom: 1px solid rgba(30, 58, 107, 0.08);
    }

    .nav-logo-text {
        color: #1E3A6B;
        cursor: pointer;
    }

    .nav-logo-text:hover {
        opacity: 0.8;
    }

    .logo-icon {
        opacity: 0.85;
    }

    /* Desktop nav links */
    .desktop-nav-link {
        font-size: 0.8125rem;
        font-weight: 400;
        color: rgba(30, 58, 107, 0.64);
        padding: 6px 10px;
        border-radius: 6px;
        text-decoration: none;
        transition: color 0.18s ease, background 0.18s ease;
        white-space: nowrap;
    }

    .desktop-nav-link:hover {
        color: #1E3A6B;
        background: rgba(30, 58, 107, 0.05);
    }

    .desktop-nav-active {
        color: #1E3A6B !important;
        font-weight: 600;
    }

    /* Mobile nav links */
    .mobile-nav-link {
        display: block;
        font-size: 1rem;
        color: rgba(30, 58, 107, 0.72);
        padding: 10px 16px;
        border-radius: 8px;
        text-decoration: none;
        transition: color 0.18s ease, background 0.18s ease;
        text-align: right;
    }

    .mobile-nav-link:hover {
        color: #1E3A6B;
        background: rgba(30, 58, 107, 0.06);
    }

    /* Style 1 legacy links */
    header .active-link {
        @apply text-[#8CDAF5];
    }
    header .not-active-link {
        @apply text-[rgba(30,58,107,0.64)];
    }
</style>
