<script>
    import GroupCardItem from "./GroupCardItem.svelte";
    import { createEventDispatcher, onMount } from "svelte";
    import Button from "@/components/ui/button/button.svelte";
    import GroupTable from "./GroupTable.svelte";
    import Input from "$lib/components/ui/input/input.svelte";
    import Ellipsis from "lucide-svelte/icons/ellipsis";
    import * as Menubar from "$lib/components/ui/menubar";

    const dispatch = createEventDispatcher();

    export let data = [];
    export let editable = true;
    export let menuActions = [];

    let _data = [];
    let filters = [
        { title: "همه", value: "all" },
        { title: "دارای اینستاگرام", value: "social_instagram" },
        { title: "دارای تلگرام", value: "social_telegram" },
        { title: "دارای x", value: "social_x" },
        { title: "دارای وبسایت", value: "internetAddress" },
        { title: "دارای مرامنامه", value: "codeOfConduct" },
        { title: "دارای منیفست", value: "manifest" },
        { title: "دارای چارت سازمانی", value: "constitution" },
    ];
    let selectedFilter = [];

    let searchText = "";

    function truncateString(str, length) {
        if (!str) return "";
        return str.length > length ? `${str.substring(0, length)}...` : str;
    }

    function edit(e) {
        dispatch("edit", e.detail);
    }

    function deleteItem(idx) {
        _data = _data.filter((_, i) => i !== idx);
        dispatch("delete", idx);
    }

    function likeItem(idx) {
        _data = _data.map((item, i) => {
            if (i === idx) {
                item.liked = !item.liked;
            }
            return item;
        });
        dispatch("like", idx);
    }

    function addNewItem() {
        const newItem = { name: "New Group", about: "Description", liked: false };
        _data = [newItem, ..._data];
        dispatch("add", newItem);
    }

    function dataSourceChanged(d) {
        _data = d;
    }

    function addFilter(filter) {
        if (filter === "all") {
            if (selectedFilter.includes("all")) {
                selectedFilter = [];
            }
            return (selectedFilter = ["all"]);
        }
        if (selectedFilter.includes(filter)) {
            selectedFilter = selectedFilter.filter((v) => v !== filter);
        } else {
            selectedFilter = [...selectedFilter, filter];
        }
    }

    function applyFilters(data, filter, search) {
        if (selectedFilter.includes("all") || selectedFilter.length === 0) {
            _data = data;
        } else {
            _data = data.filter((item) => {
                return selectedFilter.some((filter) => item[filter]);
            });
        }

        if (search) {
            _data = _data.filter((item) => {
                const lowerCaseSearch = search.toLowerCase();
    
                return (
                    item?.name?.toLowerCase().includes(lowerCaseSearch) ||
                    item?.name_fa?.toLowerCase().includes(lowerCaseSearch) ||
                    item?.name_en?.toLowerCase().includes(lowerCaseSearch) ||
                    item?.about?.toLowerCase().includes(lowerCaseSearch) ||
                    item?.manifest?.toLowerCase().includes(lowerCaseSearch) ||  
                    item?.codeOfConduct?.toLowerCase().includes(lowerCaseSearch)
                );
            });
        }
    }

    function downloadJson() {
        const dataStr =
            "data:text/json;charset=utf-8," +
            encodeURIComponent(JSON.stringify(data));
        const downloadAnchorNode = document.createElement("a");
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "data.json");
        document.body.appendChild(downloadAnchorNode); // required for firefox
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    }

    $: dataSourceChanged(data);
    $: applyFilters(data, selectedFilter, searchText);

    onMount(() => {
        // all fields
        const fields = data.map((item) => {
            return Object.keys(item);
        });
        // remove duplicates
        const uniqueFields = [...new Set(fields.flat())];
    });
</script>

<div
    class="w-full flex flex-row flex-wrap justify-between items-center my-4 gap-4"
>
    <div class="min-w-[300px] max-w-full">
        <Input bind:value={searchText} placeholder="جستجو" />
    </div>

    <div
        class="flex flex-row gap-2 flex-wrap sm:justify-start justify-between items-center"
    >
        {#each filters as { title, value } (value)}
            <Button
                class="text-sm {selectedFilter.includes(value)
                    ? 'text-blue-800 border-blue-800'
                    : ''}"
                variant="outline"
                size="sm"
                on:click={() => addFilter(value)}
            >
                {title}
            </Button>
        {/each}

        {#if editable}
            <Menubar.Root>
                <Menubar.Menu>
                    <Menubar.Trigger>
                        <Ellipsis class="h-4 w-4" />
                    </Menubar.Trigger>
                    <Menubar.Content>
                        {#each menuActions as { title, action } (title)}
                            <Menubar.Item on:click={action}>
                                {title}
                            </Menubar.Item>
                        {/each}
                    </Menubar.Content>
                </Menubar.Menu>
            </Menubar.Root>
        {/if}
    </div>
</div>

{#if _data.length === 0}
    <span class="h-40 w-full flex flex-row justify-center items-center">
        گروهی یافت نشد
    </span>
{:else}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each _data as item, idx (idx)}
            <GroupCardItem 
                {...item} 
                on:edit={edit} 
                on:delete={() => deleteItem(idx)} 
                on:like={() => likeItem(idx)} 
                {editable} 
            />
        {/each}
    </div>
{/if}

<!-- <GroupTable {data}/> -->

<style>
</style>