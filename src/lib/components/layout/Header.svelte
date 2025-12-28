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
        if (scrollY > 657) {
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
    <div class="bg-gray-700 border-b w-full sticky-header h-[50px] t-0">
        <div class="container mx-auto flex flex-row justify-between">
            <div class="inline-flex items-center flex-row gap-4">
                <div class="w-4 h-4">
                    <Logo />
                </div>
                <h1 class="font-extralight text-md">
                    <a href="{base}">
                        {siteTitle}
                    </a>
                </h1>
            </div>

            <Sheet.Root>
                <Sheet.Trigger>
                    <Button variant="ghost" class="inline-flex lg:hidden ">
                        <Menu class="w-6 h-6 text-gray-400" />
                    </Button>
                </Sheet.Trigger>
                <Sheet.Content side="left">
                        <div class="flex flex-col justify-between h-full">
                            <div
                                class="inline-flex flex-col text-right justify-start gap-4 mt-8"
                            >
                                {#each haederLinks as { name, link }, idx (idx)}
                                    <SheetClose>
                                        <a href="{base}{link}" class="text-md">
                                            {name}
                                        </a>
                                    </SheetClose>
                                {/each}
                            </div>

                            <div
                                class=" flex-col text-center justify-center gap-4 mt-8"
                            >
                                <AuthButton />
                            </div>
                        </div>
                </Sheet.Content>
            </Sheet.Root>
            <div class="hidden lg:inline-flex flex-row justify-start gap-5">
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
                <div class="" style="padding-bottom: 50px;">
                    <AuthButton short={true} />
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    header {
        @apply bg-gray-50 mb-4 border-b flex flex-col;
        height: calc(100vh + 3px);
    }
    /* .sticky {
        position: sticky;
    } */

    .sticky-header {
        display: flex;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 20;
        @apply bg-white;
        @apply border-b;
    }
    .sticky-header .active-link {
        @apply text-indigo-500;
    }

    .sticky-header .not-active-link {
        @apply text-gray-500;
    }

    .active-link {
        @apply font-bold text-white;
    }

    .not-active-link {
        @apply text-gray-300;
    }
</style>
