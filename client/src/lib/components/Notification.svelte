<script lang="ts">
    export let title:string
    export let subtitle:string|undefined
    export let kind="info"
    import Toast from 'flowbite-svelte/Toast.svelte';
	import Exclamation from "flowbite-svelte-icons/ExclamationCircleOutline.svelte";
    import Info  from 'flowbite-svelte-icons/InfoCircleOutline.svelte';

    const kinds:{[key: string]: {color:'blue'|'yellow', icon: any}}={
        'info':{ color:"blue", icon:Info},
        'warn':{ color:"yellow", icon:Exclamation },
    }
</script>

<Toast on:close color={kinds[kind].color}>
    <svelte:component slot="icon" this={kinds[kind].icon} />
    {#if subtitle}
        <span class="font-semibold text-gray-900 dark:text-white">{title}</span>
    {:else}
        {title}
    {/if}
    <div class="mt-3">  
        <div class="mb-2 text-sm font-normal">{subtitle}</div>
        <slot name="actions"></slot>
    </div>
</Toast>
