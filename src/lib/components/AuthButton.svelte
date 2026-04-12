<script>
    import { Button } from "$lib/components/ui/button";
    import LogInIcon from "lucide-svelte/icons/log-in";
    import LogOutIcon from "lucide-svelte/icons/log-out";
    import LoginModal from "$lib/components/LoginModal.svelte";
    import LogoutModal from "$lib/components/LogoutModal.svelte";
    import { supabase } from "$lib/supabaseClient";
    import { onMount } from "svelte";
    import { authStore } from "$lib/stores/authStore";

    export let short = false;
    
    let openLoginModal = false;
    let openLogoutModal = false;
    let user = null;
    

    function onOpenChange(modal) {
        if (modal === "login") {
            openLoginModal = false;
        } else if (modal === "logout") {
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
    <LoginModal bind:open={openLoginModal} {onOpenChange} />

    <Button
        class="text-[rgba(30,58,107,0.56)] mt-2"
        on:click={() => (openLoginModal = true)}
        variant="secondary"
        size="sm"
    >
        <LogInIcon class="w-4 h-4  {short ? '' : 'ml-2'}" />
        {#if !short}
            ورود به سیستم
        {/if}
    </Button>
{/if}
