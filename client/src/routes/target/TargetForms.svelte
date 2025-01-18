<script lang="ts">
    import Label from "flowbite-svelte/Label.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Button from "flowbite-svelte/Button.svelte";
    import Select from "flowbite-svelte/Select.svelte";
    import Textarea from "flowbite-svelte/Textarea.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import MultiSelect from "flowbite-svelte/MultiSelect.svelte";
    import Table from "flowbite-svelte/Table.svelte";
	import TableHead from "flowbite-svelte/TableHead.svelte";
	import TableHeadCell from "flowbite-svelte/TableHeadCell.svelte";
	import TableBody from "flowbite-svelte/TableBody.svelte";
	import TableBodyRow from "flowbite-svelte/TableBodyRow.svelte";
	import TableBodyCell from "flowbite-svelte/TableBodyCell.svelte";
	import { RelayService, TargetService, $TargetType as TargetType, UserService, type Relay, type Target, type User } from "$lib/openapi";
	import type { SelectOptionType } from "flowbite-svelte";
	import { showNotification } from "$lib/notification";
	import { createEventDispatcher } from "svelte";
    import Confirm from "$lib/components/Confirm.svelte";

    
    const dispatch=createEventDispatcher<{updated:{target:Target}}>();
    export let target:Target={
        id:"",
        name:"",
        type:"netbox",
        addr:"",
        conn_info:{},
    };
    let conn_info=JSON.stringify(target.conn_info);
    const targetType:SelectOptionType<string>[]=TargetType.enum
        .map((v)=>{return {name: v, value:v}})
    const onSubmit=async (e:SubmitEvent) => {
        e.preventDefault()
        target.conn_info=JSON.parse(conn_info);
        if(target.id===""){
            target=await TargetService.targetCreate({requestBody:target})
            showNotification({title:`Target "${target.name}" was created!`, kind:"info"})
        } else {
            target=await TargetService.targetUpdate({requestBody:target, targetId:target.id})
            showNotification({title:`Target "${target.name}" was updated!`, kind:"info"})
        }
        dispatch("updated", {target})
    }
    let relays:Relay[]=[];
    let relay_ids:string[]=[];
    const getRelays=async () => {
        relays=await RelayService.relayGets();
        relay_ids=(await TargetService.targetGetRelays({targetId:target.id})).map((v)=>v.id)
    }
    const setRelays=async () => {
        await TargetService.targetSetRelays({targetId:target.id, requestBody:relay_ids});
    }
    let ownerDeleteModal:User|undefined=undefined;
    const ownerDelete=async () => {
        if(!ownerDeleteModal) return;
        owners=await TargetService.targetDelOwner({targetId:target.id, userId:ownerDeleteModal.id})
        showNotification({title:`Owner of "${target.name}", "${ownerDeleteModal.name}" has been deleted!`, kind:"info"})
        ownerDeleteModal=undefined;
    }
    let ownerAddUser:string|undefined=undefined;
    const ownerAdd=async () => {
        if(!ownerAddUser) return;
        owners=await TargetService.targetAddOwner({targetId:target.id, userId:ownerAddUser})
        showNotification({title:"New owner has been added!", kind:"info"})
        ownerAddUser=undefined;
    }
    let owners:User[]=[];
    const getOwners=async () => {
        owners=await TargetService.targetGetOwner({targetId:target.id})
    }
</script>

<form class="space-y-1" on:submit={onSubmit}>
    <Label for="name">Name</Label>
    <Input id="name" type="text" bind:value={target.name} required />
    <Label for="type">Type</Label>
    <Select id="type" items={targetType} bind:value={target.type} required />
    <Label for="addr">Nerwork Address (CIDR)</Label>
    <Input id="addr" type="text" bind:value={target.addr} required />
    <Label for="conn_info">Connection Info</Label>
    <Textarea id="conn_info" bind:value={conn_info}/>
    {#if target.id===""}
        <Button type="submit">作成</Button>
    {:else}
        <Button type="submit">変更</Button>
    {/if}
</form>

<Heading tag="h3">Relay</Heading>
{#if target.id===""}
    まず、Targetの作成を完了してください。
{:else}
    {#await getRelays() then}
        <MultiSelect items={relays.map((v)=>{return {name:v.name, value:v.id}})} 
        bind:value={relay_ids} on:change={setRelays} />
    {/await}
{/if}

<Heading tag="h3">Owner</Heading>
<Confirm open={!!ownerDeleteModal} on:close={ownerDelete}>
    本当に"{ownerDeleteModal?.name}"を消去してもよろしいですか?
</Confirm>
{#if target.id===""}
    まず、Targetの作成を完了してください。
{:else}
    {#await getOwners() then}
    <Table>
        <TableHead>
            <TableHeadCell>Name</TableHeadCell>
            <TableHeadCell></TableHeadCell>
        </TableHead>
        <TableBody>
            {#each owners as owner(owner.id)}
                <TableBodyRow>
                    <TableHeadCell>{owner.name}</TableHeadCell>
                    <TableBodyCell>
                        <Button on:click={()=>{ownerDeleteModal=owner}}>削除</Button>
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
            {#await UserService.userGets() then users}
                <TableBodyRow>
                    <TableBodyCell>
                        <Select items={users.filter((v)=>!owners.some((o)=>o.id==v.id)).map((v)=>{return {name: v.name, value:v.id}})} bind:value={ownerAddUser} />
                    </TableBodyCell>
                    <TableBodyCell>
                        <Button on:click={ownerAdd}>Add</Button>
                    </TableBodyCell>
                </TableBodyRow>
            {/await}
        </TableBody>
    </Table>
    {/await}
{/if}