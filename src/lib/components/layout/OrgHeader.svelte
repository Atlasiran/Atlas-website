<script>
    export let title;
    export let created_at;
    export let updated_at;
    export let name_fa;
    export let org_type;
    export let pageLink;
    export let name_en;
    export let name_short;
    export let location;
    export let post_location;
    export let internetAddress;
    export let email;
    export let phone;
    export let about;
    export let expertise;
    export let history;
    export let manifest;
    export let coc;
    export let estimation_of_members;
    export let political_orientation;
    export let social_telegram;
    export let social_facebook;
    export let social_youtube;
    export let social_x;
    export let social_instagram;
    export let headerBg =
        "background-image: linear-gradient(-225deg, #fffeff 0%, #d7fffe 100%)";
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
                href={`https://atlasiran.github.io/Atlas-website/${pageLink}`}
                class="text-blue-500"
                dir="ltr"
                >{`https://atlasiran.github.io/Atlas-website/${pageLink}`}</a
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
            <span>{email}</span>
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
                <span>{coc}</span>
            </div>
            <div>
                <b>تعداد تخمینی اعضا:</b>
                <span>{estimation_of_members}</span>
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
