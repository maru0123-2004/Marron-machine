<script lang="ts">
	import { InventoryService, type Inventory } from "$lib/openapi";
    import Card from "flowbite-svelte/Card.svelte"
    import Button from "flowbite-svelte/Button.svelte";
    import Select from "flowbite-svelte/Select.svelte";
    import QRCode from '@castlenine/svelte-qrcode';
    import Heading from "flowbite-svelte/Heading.svelte";
	import { onMount } from "svelte";
	import type { PageData } from "./$types";
    export let data:PageData;
    let inventory:Inventory|undefined=undefined;
    onMount(async () => {
        inventory=(await InventoryService.inventoryGets()).find((v)=>v.id===data.inventory_id)
    })
    const gotoIPAM=async (inventory:Inventory) => {
        location.href=await InventoryService.inventoryGetUrl({inventoryId:inventory.id})
    }
</script>

{#if inventory}
    <Heading>{inventory.name}</Heading>
    <Card class="space-y-1">
        <QRCode data={`${location.origin}/inventory/${inventory.id}`} />
        <Button on:click={async (e)=>{e.preventDefault();gotoIPAM(inventory)}}>IPAMで見る</Button>
        <Button>使用者を自分にする</Button>
        <Select placeholder="使用場所を選択" />
        <Button>使用場所を変更する</Button>
    </Card>
{/if}