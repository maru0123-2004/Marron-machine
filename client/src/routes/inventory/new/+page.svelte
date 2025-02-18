<script lang="ts">
    import { InventoryService, TargetService, type InventoryDict, type Target } from "$lib/openapi";
	import type { SelectOptionType } from "flowbite-svelte";
import Select from "flowbite-svelte/Select.svelte";
import Button from "flowbite-svelte/Button.svelte"
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
    let suggestions: Record<string, InventoryDict[]>={};
    let targets:Target[]=[];
    let target_id: string|undefined=undefined;
    let device_id: string|undefined=undefined;
    onMount(async ()=>{
        targets=await TargetService.targetGets();
        suggestions=await InventoryService.inventorySuggest();
    })

    const suggestions2Items=(suggestions:Record<string, InventoryDict[]>)=>{
        const items:SelectOptionType<string>[]=[];
        for(const suggest of Object.keys(suggestions)){
            items.push({name:targets.find((t)=>t.id===suggest)?.name??"", value:suggest})
        }
        return items
    }
    const createInventory=async () => {
        if (!target_id || !device_id) return;
        const device=suggestions[target_id].find((i)=>i.id===device_id)
        if (!device) return;
        const inventory=await InventoryService.inventoryCreate({requestBody:{name:device.name, inventory_id:device.id, ipam_id:target_id}})
        goto(`/inventory/${inventory.id}`);
    }
</script>

<Select placeholder="Select Target..." items={suggestions2Items(suggestions)} bind:value={target_id}/>

{#if target_id}
    <Select bind:value={device_id} placeholder="Select Device..." items={suggestions[target_id].map((i)=>{return {name:i.name, value:i.id}})} />
{:else}
    <Select placeholder="" disabled />
{/if}

<Button on:click={createInventory} disabled={!device_id}>Create</Button>