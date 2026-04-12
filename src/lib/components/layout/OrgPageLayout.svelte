<script>
    import Header from "@/components/layout/Header.svelte";
    import Footer from "@/components/layout/Footer.svelte";
    import { onMount } from "svelte";

    export let name_fa;

    onMount(() => {});
</script>

<div class="container mx-auto" dir="auto">
    <slot />
</div>