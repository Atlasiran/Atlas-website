<script>
export let headerBg = "";
    export let id = "";
    export let title = "";
    export let created_at = "";
    export let deleted_at = "";
    export let updated_at = "";
    export let delete_reason = "";
    export let logo = "";
    export let name_fa = "";
    export let name_en = "";
    export let name_short = "";
    export let estimationOfMembers = "";
    export let location = "";
    export let about;
    export let pageLink;
    export let manifest;
    export let internetAddress;
    export let constitution;
    export let social_x;
    export let social_instagram;
    export let social_telegram;
    export let social_youtube;
    export let editable = true;
    export let markForEdit = false;
    export let org_type = "";
    export let post_location = "";
    export let contact = "";
    export let phone = "";
    export let expertise = "";
    export let activities = "";
    export let history = "";
    export let codeOfConduct = "";
    export let projects = "";
    export let others1 = "";
    export let others2 = "";
    export let political_orientation = "";
    export let social_facebook = null;
    export let plan = "";
    export let shortDescription = "";
    export let mark_for_delete = "";
</script>

<div class="w-full bg-white h-64 p-8 shadow-sm" style={headerBg}></div>

<div class="w-full mx-auto max-w-[800px] relative">
  <div
    class="w-16 h-16 bg-white rounded-md border top-[-40px] absolute p-2 text-gray-700 md:right-0 right-8"
  >
    <slot name="page-logo" />
  </div>
  <h1 class="pt-8 pb-8 text-5xl md:pr-0 px-8">
    {title}
  </h1>
  <div class="flex flex-col gap-2 text-sm mt-2 md:pr-0 px-8">
    <div>
      <b>نوشته شده در:</b>
      <span>{created_at}</span>
    </div>
    <div>
      <b>بروزرسانی شده در:</b>
      <span>{updated_at}</span>
    </div>
    <div>
      <b>نام فارسی:</b>
      <span>{name_fa}</span>
    </div>
    <div>
      <b>نوع نهاد:</b>
      <span>{org_type}</span>
    </div>
    <div>
      <b>نشانی روی اطلس:</b>
      <a
        href={`https://atlasiran.org${pageLink}`}
        class="text-blue-500"
        dir="ltr">{`https://atlasiran.org${pageLink}`}</a
      >
    </div>
    <div>
      <b>نام لاتین:</b>
      <span>{name_en}</span>
    </div>
    <div>
      <b>نام کوتاه:</b>
      <span>{name_short}</span>
    </div>
    <div>
      <b>مکان:</b>
      <span>{location}</span>
    </div>
    <div>
      <b>نشانی پستی:</b>
      <span>{post_location}</span>
    </div>
    <div>
      <b>نشانی وب‌سایت:</b>
      <a href={internetAddress} class="text-blue-500" dir="ltr"
        >{internetAddress}</a
      >
    </div>
    <div>
      <b>ایمیل:</b>
      <span>{contact}</span>
    </div>
    <div>
      <b>تلفن:</b>
      <span>{phone}</span>
      <div>
        <b>تخصص‌ها:</b>
        <span>{expertise}</span>
      </div>
      <div>
        <b>تاریخ‌چه:</b>
        <span>{history}</span>
      </div>
      <div>
        <b>منیفست:</b>
        <span>{manifest}</span>
      </div>
      <div>
        <b>مرام‌نامه:</b>
        <span>{codeOfConduct}</span>
      </div>
      <div>
        <b>تعداد تخمینی اعضا:</b>
        <span>{estimationOfMembers}</span>
      </div>
      <div>
        <b>گرایش سیاسی:</b>
        <span>{political_orientation}</span>
      </div>
      <div>
        <b>نشانی تلگرام:</b>
        <span>{social_telegram}</span>
      </div>
      <div>
        <b>نشانی فیس‌بوک:</b>
        <span>{social_facebook}</span>
      </div>
      <div>
        <b>نشانی یوتیوب:</b>
        <span>{social_youtube}</span>
      </div>
      <div>
        <b>نشانی توییتر:</b>
        <span>{social_x}</span>
      </div>
      <div>
        <b>نشانی اینستاگرم:</b>
        <span>{social_instagram}</span>
      </div>
      <div>
        <b>درباره:</b>
        <span>{about}</span>
      </div>
    </div>
  </div>
</div>

<style>
</style>
