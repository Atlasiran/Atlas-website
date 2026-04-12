<script>
    import { cn } from "$lib/utils.js";
    export let loading = false;
    export let size = 34;
    let className = undefined;

    export { className as class };

</script>

<div class={cn("relative p-0 m-0", className)} {...$$restProps}>
    <slot></slot>
    {#if loading}
        <div
            class="absolute inset-0 flex items-center justify-center bg-[#F4F6F7] bg-opacity-80"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width={size}
                height={size}
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                class="animate-spin"
            >
                <path d="M21 12a9 9 0 1 1-6.219-8.56" />
            </svg>
        </div>
    {/if}
</div>

<style>
</style>
