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
	import { RelayService, ActionService, $ActionModule as ActionModule, UserService, type Relay, type Action, type User, TargetService, type Target } from "$lib/openapi";
	import type { SelectOptionType } from "flowbite-svelte";
	import { showNotification } from "$lib/notification";
	import { createEventDispatcher } from "svelte";
    import Confirm from "$lib/components/Confirm.svelte";

    
    const dispatch=createEventDispatcher<{updated:{action:Action}}>();
    export let action:Action={
        id:"",
        name:"",
        action_module:"collect_ip",
        action_info:{},
        interval:3600
    };
    let action_info=JSON.stringify(action.action_info);
    const actionType:SelectOptionType<string>[]=ActionModule.enum
        .map((v)=>{return {name: v, value:v}})
    const onSubmit=async (e:SubmitEvent) => {
        e.preventDefault()
        action.action_info=JSON.parse(action_info);
        if(action.id===""){
            action=await ActionService.actionCreate({requestBody:action})
            showNotification({title:`Action "${action.name}" was created!`, kind:"info"})
        } else {
            action=await ActionService.actionUpdate({requestBody:action, actionId:action.id})
            showNotification({title:`Action "${action.name}" was updated!`, kind:"info"})
        }
        dispatch("updated", {action})
    }
    let targets:Relay[]=[];
    let target_ids:string[]=[];
    const getTargets=async () => {
        targets=await TargetService.targetGets();
        target_ids=(await ActionService.actionGetTarget({actionId:action.id})).map((v)=>v.id)
    }
    const setTargets=async () => {
        const currentTargets=await ActionService.actionGetTarget({actionId:action.id});
        let selectedTargets=structuredClone(target_ids);
        for (const target of currentTargets){
            const findIndex=selectedTargets.findIndex((tid)=>tid===target.id);
            if(findIndex===-1){
                await ActionService.actionDelTarget({actionId:action.id, targetId:target.id});
            } else {
                delete selectedTargets[findIndex];
            }
        }
        for (const tid of selectedTargets){
            if(!tid) continue;
            await ActionService.actionAddTarget({actionId:action.id, targetId:tid});
        }
    }
    let ownerDeleteModal:User|undefined=undefined;
    const ownerDelete=async () => {
        if(!ownerDeleteModal) return;
        owners=await ActionService.actionDelOwner({actionId:action.id, userId:ownerDeleteModal.id})
        showNotification({title:`Owner of "${action.name}", "${ownerDeleteModal.name}" has been deleted!`, kind:"info"})
        ownerDeleteModal=undefined;
    }
    let ownerAddUser:string|undefined=undefined;
    const ownerAdd=async () => {
        if(!ownerAddUser) return;
        owners=await ActionService.actionAddOwner({actionId:action.id, userId:ownerAddUser})
        showNotification({title:"New owner has been added!", kind:"info"})
        ownerAddUser=undefined;
    }
    let owners:User[]=[];
    const getOwners=async () => {
        owners=await ActionService.actionGetOwner({actionId:action.id})
    }
</script>

<form class="space-y-1" on:submit={onSubmit}>
    <Label for="name">Name</Label>
    <Input id="name" type="text" bind:value={action.name} required />
    <Label for="type">Type</Label>
    <Select id="type" items={actionType} bind:value={action.action_module} required />
    <Label for="addr">Interval</Label>
    <Input id="addr" type="number" bind:value={action.interval} required />
    <Label for="conn_info">Connection Info</Label>
    <Textarea id="conn_info" bind:value={action_info}/>
    {#if action.id===""}
        <Button type="submit">作成</Button>
    {:else}
        <Button type="submit">変更</Button>
    {/if}
</form>

<Heading tag="h3">Target</Heading>
{#if action.id===""}
    まず、Actionの作成を完了してください。
{:else}
    {#await getTargets() then}
        <MultiSelect items={targets.map((v)=>{return {name:v.name, value:v.id}})} 
        bind:value={target_ids} on:input={setTargets}/>
    {/await}
{/if}

<Heading tag="h3">Owner</Heading>
<Confirm open={!!ownerDeleteModal} on:close={ownerDelete}>
    本当に"{ownerDeleteModal?.name}"を消去してもよろしいですか?
</Confirm>
{#if action.id===""}
    まず、Actionの作成を完了してください。
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