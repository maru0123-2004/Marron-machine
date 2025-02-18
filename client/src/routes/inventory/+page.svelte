<script lang="ts">
	import { goto } from '$app/navigation';
    import { InventoryService, type Inventory } from '$lib/openapi';
    import QRCode from '@castlenine/svelte-qrcode';
	import { onMount } from 'svelte';
    import type { PageData } from "./$types";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Button from "flowbite-svelte/Button.svelte";
    import Create from "flowbite-svelte-icons/PlusOutline.svelte";
    import Card from "flowbite-svelte/Card.svelte"
	import Confirm from '$lib/components/Confirm.svelte';
    import Delete from "flowbite-svelte-icons/TrashBinOutline.svelte";
	import { showNotification } from '$lib/notification';

    let inventories:Inventory[]=[]
    export let data:PageData;
    const token=data.user
    onMount(async ()=>{
        if(!$token){
            goto("/");
            return
        }
        inventories=await InventoryService.inventoryGets()
    })
    const inventoryDelete=async (inventory_id:string) => {
        const inventory=await InventoryService.inventoryDelete({inventoryId:inventory_id});
        inventories=inventories.filter((v)=>v.id!==inventory_id);
        showNotification({title:`Inventory "${inventory.name}"を削除しました`, kind:"info"})
    }
    let inventoryDeleteModal:Inventory|undefined=undefined;
    const gotoIPAM=async (inventory:Inventory) => {
        location.href=await InventoryService.inventoryGetUrl({inventoryId:inventory.id})
    }
</script>

<Confirm open={!!inventoryDeleteModal} on:close={async ()=>{await inventoryDelete(inventoryDeleteModal?.id??"")}}>
    本当に"{inventoryDeleteModal?.name}"を消去してもよろしいですか?
</Confirm>

<Heading>Inventory</Heading>
<Button href="/inventory/new"><Create /> Add Inventory</Button>
<Button href="/inventory/device"><Create /> Add Inventory(with IPMI to IPAM)</Button>
{#each inventories as inventory(inventory.id)}
    <Card href={`/inventory/${inventory.id}`} class="space-y-1">
        {inventory.name}
        <QRCode data={`${location.origin}/inventory/${inventory.id}`} />
    <Button on:click={async (e)=>{e.preventDefault();gotoIPAM(inventory)}}>IPAMで見る</Button>
    <Button on:click={(e)=>{e.preventDefault();inventoryDeleteModal=inventory}}><Delete /> Delete</Button>
    </Card>
{/each}
