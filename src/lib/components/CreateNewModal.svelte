<script lang="ts">
  import { createEntity, uploadLogo } from "$lib/api";
  import { Button } from "$lib/components/ui/button";
  import CountrySelect from "$lib/components/ui/CountrySelect.svelte";
  import * as Dialog from "$lib/components/ui/dialog";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import * as Tabs from "$lib/components/ui/tabs";
  import { createEventDispatcher } from "svelte";
  import Textarea from "./ui/textarea/textarea.svelte";

  const dispatch = createEventDispatcher();

  export let open = false;
  export let data = {};
  export let suggestable = false;

  let createState = "INIT";

  let forms = [
    {
      name: "اطلاعات کلی",
      value: "info",
      selected: true,
      fields: [
        {
          id: "name_fa",
          displayName: "نام فارسی",
          value: "",
          type: "text",
        },
        {
          id: "name_en",
          displayName: "نام اینگلیسی",
          value: "",
          type: "text",
        },
        {
          id: "location",
          displayName: "پایگاه فعالیت",
          value: "",
          type: "countrySelect",
        },
      ],
    },
    {
      name: "لوگو",
      value: "logo",
      fields: [
        {
          id: "logo",
          displayName: "لوگو",
          value: "",
          type: "image_upload",
        },
      ],
    },
    {
      name: "اطلاعات ارتباطی",
      value: "contact",
      fields: [],
    },
    {
      name: "اطلاعات سازمانی",
      value: "organization",
      fields: [
        {
          id: "expertise",
          displayName: "تخصص‌ها",
          value: "",
          type: "text",
        },
        {
          id: "estimationOfMembers",
          displayName: "تخمین تعداد اعضا",
          value: "",
          type: "number",
        },
        {
          id: "manifest",
          displayName: "بیانیه",
          value: "",
          type: "text",
        },
        {
          id: "political_orientation",
          displayName: "گرایش سیاسی",
          value: "",
          type: "text",
        },
      ],
    },
    {
      name: "اطلاعات تکمیلی",
      value: "additional",
      fields: [
        {
          id: "history",
          displayName: "تاریخچه",
          value: "",
          type: "text",
        },
        {
          id: "about",
          displayName: "توضیحات",
          value: "",
          type: "textarea",
        },
      ],
    },
  ];

  function onOpenChange() {
    // change the data fields to the value of the form fields
    forms.forEach((form) => {
      form.fields.forEach((field) => {
        data[field.id] = field.value;
      });
    });
    dispatch("close");
  }

  function createData() {
    // update the data fields with the value of the form fields
    forms.forEach((form) => {
      form.fields.forEach((field) => {
        data[field.id] = field.value;
      });
    });

    // send the data to the server
    createState = "LOADING";

    createEntity(data)
      .then((response) => {
        console.log(response);
        createState = "SUCCESS";
        dispatch("close");
      })
      .catch((error) => {
        createState = "ERROR";
      });
  }

  function handleUpload(id) {
    return async (event) => {
      const file = event.target.files[0];
      await uploadLogo(id + ".png", file);
    };
  }
</script>

<div class="dialog-container max-h-full">
  <Dialog.Root {open} {onOpenChange}>
    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title>ایجاد گروه جدید</Dialog.Title>
        <Dialog.Description>
          اطلاعات خود را وارد کنید و در نهایت برای ذخیره کردن دکمه‌ی ذخیره را
          بزنید.
        </Dialog.Description>
      </Dialog.Header>

      <Tabs.Root value="overall">
        <Tabs.List class="flex flex-row justify-center items-center w-full">
          {#each forms as form}
            <Tabs.Trigger value={form.value}>
              {form.name}
            </Tabs.Trigger>
          {/each}
        </Tabs.List>
        <div class="dialog-root">
          {#each forms as form}
            <Tabs.Content value={form.value}>
              <div class="grid gap-4 py-4">
                {#each form.fields as field}
                  <div class="grid grid-cols-4 items-center gap-4">
                    {#if field.type === "textarea"}
                      <Label for={field.id} class="text-right">
                        {field.displayName}
                      </Label>
                      <Textarea
                        class="col-span-3"
                        bind:value={field.value}
                        placeholder=""
                      />
                    {:else if field.type === "countrySelect"}
                      <Label for={field.id} class="text-right">
                        {field.displayName}
                      </Label>
                      <div class="col-span-3">
                        <CountrySelect bind:value={field.value} />
                      </div>
                    {:else if field.type === "image_upload"}
                      <Label for="picture">
                        {field.displayName}
                      </Label>
                      <Input
                        on:change={handleUpload(field.id)}
                        class="col-span-3"
                        type="file"
                      />
                    {:else if field.type === "id"}
                      <Label for={field.id} class="text-right">
                        {field.displayName}
                      </Label>
                      <div
                        class="col-span-3 flex flex-row items-center justify-start"
                      >
                        <span class="text-left w-full">
                          #{field.value}
                        </span>
                      </div>
                    {:else}
                      <Label for={field.id} class="text-right">
                        {field.displayName}
                      </Label>
                      <Input
                        id={field.id}
                        bind:value={field.value}
                        type={field.type}
                        class="col-span-3"
                        disabled={field.disabled}
                      />
                    {/if}
                  </div>
                {/each}
              </div>
            </Tabs.Content>
          {/each}
        </div>
      </Tabs.Root>

      <Dialog.Footer>
        {#if !suggestable}
          <Button
            type="submit"
            on:click={createData}
            disabled={createState === "LOADING"}
          >
            {#if createState === "LOADING"}
              در حال بارگذاری...
            {:else if createState === "SUCCESS"}
              ذخیره شد
            {:else if createState === "ERROR"}
              خطا
            {:else}
              ذخیره
            {/if}
          </Button>
        {/if}

        {#if suggestable}
          <Button type="submit">مرحله بعد</Button>
        {/if}
      </Dialog.Footer>
    </Dialog.Content>
  </Dialog.Root>
</div>

<style>
  .dialog-container {
    direction: rtl;
  }
  .dialog-root {
    @apply w-full;
    max-height: calc(100vh - 200px);
    overflow-y: auto;
    padding: 0 6px;
    max-width: 600px;
  }
</style>
