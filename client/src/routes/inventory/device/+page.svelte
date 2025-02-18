<script lang="ts">
    import { InventoryService, TargetService, type InventoryDict, type Target } from "$lib/openapi";
	import type { SelectOptionType } from "flowbite-svelte";
    import Select from "flowbite-svelte/Select.svelte";
    import Button from "flowbite-svelte/Button.svelte";
    import Input from "flowbite-svelte/Input.svelte";
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
    let suggestions: Record<string, InventoryDict[]>={};
    let targets:Target[]=[];
    let target_id: string|undefined=undefined;
    onMount(async ()=>{
        targets=await TargetService.targetGets();
        suggestions=await InventoryService.inventorySuggest();
    })
    let name="";
    let ipaddr="";
    let username="";
    let password="";
    const suggestions2Items=(suggestions:Record<string, InventoryDict[]>)=>{
        const items:SelectOptionType<string>[]=[];
        for(const suggest of Object.keys(suggestions)){
            items.push({name:targets.find((t)=>t.id===suggest)?.name??"", value:suggest})
        }
        return items
    }
    const createInventory=async (e:Event) => {
        e.preventDefault()
        if (!target_id) return;
        const inventory=await InventoryService.inventoryCreateFromIpmi({requestBody:{name:name, ipam_id:target_id, username, ipaddr, password}})
        goto(`/inventory/${inventory.id}`);
    }
</script>

<form on:submit={createInventory} class="space-y-1">
<Select placeholder="Select Target..." items={suggestions2Items(suggestions)} bind:value={target_id} required/>
<Input bind:value={name} placeholder="Name" required />
<Input bind:value={ipaddr} placeholder="IP Address" required />
<Input bind:value={username} placeholder="User name" required />
<Input bind:value={password} type="password" placeholder="Password" required />
<Button type="submit">Create</Button>
</form>