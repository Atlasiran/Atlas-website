<script>
    import Button from "@/components/ui/button/button.svelte";
    import { onMount } from "svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import Link from "lucide-svelte/icons/link";
    import Scale from "lucide-svelte/icons/scale";
    import ScrollText from "lucide-svelte/icons/scroll-text";
    import Fullscreen from "lucide-svelte/icons/fullscreen";
    import MapPin from "lucide-svelte/icons/map-pin";
    import Users from "lucide-svelte/icons/users";
    import * as Tooltip from "$lib/components/ui/tooltip/index.js";
    import ListAllGroups from "@/components/ListAllGroups.svelte";
    import Header from "@/components/layout/Header.svelte";
    import Hash from "lucide-svelte/icons/hash";
    import EditModal from "@/components/EditModal.svelte";
    import CreateNewModal from "@/components/CreateNewModal.svelte"; // Import CreateNewModal
    import { authStore } from "$lib/stores/authStore";
    import { getEntities, fixNamesInDB, deleteEntity } from "$lib/api";
    import { base } from "$app/paths";

    let data = [];
    let editOpen = false;
    let editData;
    let createOpen = false;
    let suggestable = false;

    let _fetchDataState = "IDLE";
    let _initFist = false;

    let stats = [
        { title: "تعداد کل گروه‌های فعال", value: 0 },
        { title: "اخرین بروزرسانی", value: "۱۴۰۳/۰۸/۱۰" },
    ];

    let menuActions = [];

    function edit(e) {
        editOpen = false;
        editData = data.find((item) => item.id === e.detail.id);
        setTimeout(() => {
            editOpen = true;
        }, 100);
    }

    async function deleteItem(item) {
        const elementToDelete = data.find((el) => el.id === item.id);
        if (!elementToDelete) {
            return;
        }
        elementToDelete.loading = true;
        console.log("delete", elementToDelete.id);
        await deleteEntity(elementToDelete.id)
            .then(() => {
                data = data.filter((el) => el.id !== elementToDelete.id);
            })
            .catch((e) => {
                console.error(e);
            })
            .finally(() => {
                elementToDelete.loading = false;
            });
    }

    function likeItem(id) {
        data = data.map((item) => {
            if (item.id === id) {
                item.liked = !item.liked;
            }
            return item;
        });
    }

    function addNewItem() {
        createOpen = true;
    }

    function modalClose() {
        editOpen = false;
        createOpen = false;
        data = [...data];
    }

    function fetchData(isAuth = false) {
        _fetchDataState = "LOADING";

        if (isAuth) {
            getEntities()
                .then((res) => {
                    data = res;
                    stats[0].value = data.length;
                    _fetchDataState = "SUCCESS";
                })
                .catch((e) => {
                    _fetchDataState = "ERROR";
                    setTimeout(() => {
                        fetchData(isAuth);
                    }, 5000);
                });
        }

        if (!isAuth) {
            fetch(`${base}/data/data.json`)
                .then((response) => response.json())
                .then((json) => {
                    data = json;
                    stats[0].value = data.length;
                    _fetchDataState = "SUCCESS";
                })
                .catch((e) => {
                    _fetchDataState = "ERROR";
                    setTimeout(() => {
                        fetchData(isAuth);
                    }, 5000);
                });
            return;
        }
    }

    function updateMenuActions(isAuth = false) {
        const _menuActions = [
            {
                title: "دانلود json",
                action: () => {
                    const element = document.createElement("a");
                    const file = new Blob([JSON.stringify(data)], {
                        type: "text/plain",
                    });
                    element.href = URL.createObjectURL(file);
                    element.download = `data-${new Date().toISOString().split("T")[0]}.json`;
                    document.body.appendChild(element); // Required for this to work in FireFox
                    element.click();
                },
            },
        ];

        const _authMenuActions = [
            {
                title: "درست کردن اسم‌ها",
                action: () => {
                    fixNamesInDB().then(() => {
                        fetchData(true);
                    });
                },
            },
        ];

        if (isAuth) {
            _menuActions.push(..._authMenuActions);
        }

        menuActions = _menuActions;
    }

    onMount(() => {
        _fetchDataState = "IDLE";
        fetchData($authStore.isAuthenticated);
        _initFist = true;
    });

    $: _initFist && fetchData($authStore.isAuthenticated);
    $: updateMenuActions($authStore.isAuthenticated);
</script>

<svelte:head>
    <title>اطلس جامعه مدنی ایران - گروه‌ها</title>
</svelte:head>

<EditModal
    id={editData?.id}
    bind:open={editOpen}
    on:close={modalClose}
    {suggestable}
/>

<CreateNewModal bind:open={createOpen} on:close={modalClose} {suggestable} />

<div class="container mx-auto pt-8">
    <div class="mb-32">
        <h1 class="text-4xl font-bold text-indigo-400 mb-4">گروه‌ها</h1>
        <p class="text-justify text-gray-600">
            در این بخش می‌توانید اطلاعات مربوط به نهادهای مدنی را
            مشاهده کنید. این نهادها بر اساس مستندات عمومی جمع‌آوری شده‌اند. اگر اطلاعاتی در این
            اطلس ناقص یا نادرست است، لطفن به ما
            اطلاع بدهید. برای اطلاعات بیشتر
            به بخش «همکاری» مراجعه کنید.
        </p>
    </div>

    <div class="flex flex-row my-16 gap-4">
        {#if $authStore.isAuthenticated}
            <button class="w-[250px] h-[110px]" on:click={addNewItem}>
                <Card.Root
                    class=" h-full flex flex-col items-center justify-center cursor-pointer"
                >
                    <div class="text-4xl text-indigo-400">+</div>
                    <span> افزودن گروه جدید </span>
                </Card.Root>
            </button>
        {/if}
        {#each stats as { title, value }}
            <Card.Root class="w-[250px]">
                <Card.Header
                    class="flex flex-row items-center justify-between space-y-0 pb-2"
                >
                    <Card.Title class="text-sm font-medium">
                        {title}
                    </Card.Title>
                </Card.Header>
                <Card.Content>
                    <div class="text-2xl font-bold">
                        {value}
                    </div>
                    <p class="text-muted-foreground text-xs"></p>
                </Card.Content>
            </Card.Root>
        {/each}
    </div>

    <ListAllGroups
        {menuActions}
        {data}
        on:edit={edit}
        on:delete={deleteItem}
        on:like={likeItem}
        editable={!!$authStore.user}
    />
</div>
