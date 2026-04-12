<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog";
    export let isOpen;
    export let onOpenChange = () => {
        isOpen = false;
    };
</script>

<Dialog.Root bind:open={isOpen} {onOpenChange}>
    <Dialog.Content>
        <Dialog.Header>
            <slot />
        </Dialog.Header>
    </Dialog.Content>
</Dialog.Root>

<style>
    .modal {
        position: fixed;
        top: 0;
        bottom: 0;
        right: 0;
        left: 0;
        display: flex;
        justify-content: center;
        align-items: center;

        /* allow click-through to backdrop */
        pointer-events: none;
        @apply text-[#1E3A6B];
    }

    .contents {
        min-width: 240px;
        border-radius: 6px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        pointer-events: auto;
        max-height: calc(100vh - 200px);
        overflow-y: auto;
        @apply bg-[#EDE3C7];
    }
</style>
