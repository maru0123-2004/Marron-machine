<script lang="ts">
    import Label from "flowbite-svelte/Label.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Button from "flowbite-svelte/Button.svelte";
    import Select from "flowbite-svelte/Select.svelte";
    import Textarea from "flowbite-svelte/Textarea.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Table from "flowbite-svelte/Table.svelte";
	import TableHead from "flowbite-svelte/TableHead.svelte";
	import TableHeadCell from "flowbite-svelte/TableHeadCell.svelte";
	import TableBody from "flowbite-svelte/TableBody.svelte";
	import TableBodyRow from "flowbite-svelte/TableBodyRow.svelte";
	import TableBodyCell from "flowbite-svelte/TableBodyCell.svelte";
	import { RelayService, UserService, type Relay, type User } from "$lib/openapi";
	import { showNotification } from "$lib/notification";
	import { createEventDispatcher } from "svelte";
    import Confirm from "$lib/components/Confirm.svelte";

    
    const dispatch=createEventDispatcher<{updated:{relay:Relay}}>();
    export let relay:Relay={
        id:"",
        name:"",
        addr:"",
        conn_info:{},
    };
    let conn_info=JSON.stringify(relay.conn_info);
    const onSubmit=async (e:SubmitEvent) => {
        e.preventDefault()
        relay.conn_info=JSON.parse(conn_info);
        if(relay.id===""){
            relay=await RelayService.relayCreate({requestBody:relay})
            showNotification({title:`Relay "${relay.name}" was created!`, kind:"info"})
        } else {
            relay=await RelayService.relayUpdate({requestBody:relay, relayId:relay.id})
            showNotification({title:`Relay "${relay.name}" was updated!`, kind:"info"})
        }
        dispatch("updated", {relay})
    }
    let ownerDeleteModal:User|undefined=undefined;
    const ownerDelete=async () => {
        if(!ownerDeleteModal) return;
        owners=await RelayService.relayDelOwner({relayId:relay.id, userId:ownerDeleteModal.id})
        showNotification({title:`Owner of "${relay.name}", "${ownerDeleteModal.name}" has been deleted!`, kind:"info"})
        ownerDeleteModal=undefined;
    }
    let ownerAddUser:string|undefined=undefined;
    const ownerAdd=async () => {
        if(!ownerAddUser) return;
        owners=await RelayService.relayAddOwner({relayId:relay.id, userId:ownerAddUser})
        showNotification({title:"New owner has been added!", kind:"info"})
        ownerAddUser=undefined;
    }
    let owners:User[]=[];
    const getOwners=async () => {
        owners=await RelayService.relayGetOwner({relayId:relay.id})
    }
</script>

<form class="space-y-1" on:submit={onSubmit}>
    <Label for="name">Name</Label>
    <Input id="name" type="text" bind:value={relay.name} required />
    <Label for="addr">Address</Label>
    <Input id="addr" type="text" bind:value={relay.addr} required />
    <Label for="conn_info">Connection Info</Label>
    <Textarea id="conn_info" bind:value={conn_info}/>
    {#if relay.id===""}
        <Button type="submit">作成</Button>
    {:else}
        <Button type="submit">変更</Button>
    {/if}
</form>

<Heading tag="h3">Owner</Heading>
<Confirm open={!!ownerDeleteModal} on:close={ownerDelete}>
    本当に"{ownerDeleteModal?.name}"を消去してもよろしいですか?
</Confirm>
{#if relay.id===""}
    まず、Relayの作成を完了してください。
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