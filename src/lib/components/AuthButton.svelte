<script>
    import LogoutModal from "$lib/components/LogoutModal.svelte";
    import { Button } from "$lib/components/ui/button";
    import { authStore } from "$lib/stores/authStore";
    import LogInIcon from "lucide-svelte/icons/log-in";
    import LogOutIcon from "lucide-svelte/icons/log-out";
    import { onMount } from "svelte";

    export let short = false;

    let openLogoutModal = false;
    let user = null;

    function onOpenChange(modal) {
        if (modal === "logout") {
            openLogoutModal = false;
        }
    }

    onMount(async () => {});
</script>

{#if $authStore.user}
    <LogoutModal bind:open={openLogoutModal} {onOpenChange} />

    <Button
        class="text-[rgba(30,58,107,0.56)]  mt-2"
        on:click={() => (openLogoutModal = true)}
        variant="secondary"
        size="sm"
    >
        <LogOutIcon class="w-4 h-4 {short ? '' : 'ml-2'}" />
        {#if !short}
            خروج از سیستم
        {/if}
    </Button>
{:else}
    <a
        href="https://atlasiran.org/admin"
        class="inline-flex items-center text-[rgba(30,58,107,0.56)] mt-2 px-3 py-1.5 rounded-md bg-secondary text-sm font-medium hover:bg-secondary/80 transition-colors"
    >
        <LogInIcon class="w-4 h-4  {short ? '' : 'ml-2'}" />
        {#if !short}
            ورود به سیستم
        {/if}
    </a>
{/if}
