<script lang="ts">
	import { goto, pushState } from "$app/navigation";
	import { ActionService, type Action } from "$lib/openapi";
	import { onMount } from "svelte";
    import Table from "flowbite-svelte/Table.svelte";
	import TableHead from "flowbite-svelte/TableHead.svelte";
	import TableHeadCell from "flowbite-svelte/TableHeadCell.svelte";
	import TableBody from "flowbite-svelte/TableBody.svelte";
	import TableBodyRow from "flowbite-svelte/TableBodyRow.svelte";
	import TableBodyCell from "flowbite-svelte/TableBodyCell.svelte";
    import A from "flowbite-svelte/A.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Button from "flowbite-svelte/Button.svelte";
	import type { PageData } from "./$types";
	import Confirm from "$lib/components/Confirm.svelte";
	import { page } from "$app/stores";
	import ActionForms from "./ActionForms.svelte";
    import Modal from "flowbite-svelte/Modal.svelte"
    import Create from "flowbite-svelte-icons/PlusOutline.svelte";
    import Edit from "flowbite-svelte-icons/EditOutline.svelte";
    import Delete from "flowbite-svelte-icons/TrashBinOutline.svelte";
    import Check from "flowbite-svelte-icons/CheckOutline.svelte";
	import { destroyNotification, showNotification } from "$lib/notification";
    export let data:PageData;
    const token=data.user
    let actions:Action[]=[];

    onMount(async () => {
        if(!$token){
            goto("/");
            return
        }
        actions=await ActionService.actionGets();
    })
    const actionDelete=async (action_id:string) => {
        const action=await ActionService.actionDelete({actionId:action_id});
        actions=actions.filter((v)=>v.id!==action_id);
        showNotification({title:`Action "${action.name}"を削除しました`, kind:"info"})
    }
    let actionDeleteModal:Action|undefined=undefined;
    const actionRunOnce=async (action_id:string) => {
        const nid=showNotification({title:"Pingを送信しています...", kind:"info"});
        try{
            if (await ActionService.actionRunOnce({actionId:action_id})){
                showNotification({title:"Pingに成功しました!", kind:"info"});
            } else {
                throw Error();
            }
        } catch(e){
            showNotification({title:"Pingに失敗しました。", kind:"warn"});
        }
        destroyNotification(nid??-1);
    }
    const shallowRouting=async (e:MouseEvent, action:Action|undefined=undefined) => {
        if (innerWidth < 640 || e.shiftKey || e.metaKey || e.ctrlKey || !e.currentTarget) return;
        e.preventDefault();
        /* @ts-ignore */
        const {href} = e.currentTarget;
        if(action){
            pushState(href, {modalOpen:true, modalModel:action, modalTitle:"Actionの編集"})
        } else {
            action={id:"",name:"",action_module:"collect_ip",action_info:{},interval:3600}
            pushState(href, {modalOpen:true, modalTitle:"Actionの作成"})
        }
    }
    const shallowRoutingHandler=async (e:CustomEvent<{action:Action}>) => {
        const i=actions.findIndex((t)=>t.id===e.detail.action.id)
        if(i === -1){
            actions=[...actions, e.detail.action]
        } else {
            actions[i]=e.detail.action
        }
    }
</script>

<Modal open={$page.state.modalOpen} title={$page.state.modalTitle} on:close={()=>goto("/action")}>
    <ActionForms action={$page.state.modalModel} on:updated={shallowRoutingHandler}/>
</Modal>

<Confirm open={!!actionDeleteModal} on:close={async ()=>{await actionDelete(actionDeleteModal?.id??"")}}>
    本当に"{actionDeleteModal?.name}"を消去してもよろしいですか?
</Confirm>

<Heading>Action</Heading>
<Button href="/action/new" on:click={async (e)=>shallowRouting(e)}><Create /> Add Action</Button>
<Table>
    <TableHead>
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell>Type</TableHeadCell>
        <TableHeadCell>Interval</TableHeadCell>
        <TableHeadCell></TableHeadCell>
    </TableHead>
    <TableBody>
        {#each actions as action(action.id)}
            <TableBodyRow>
                <TableBodyCell>
                    <A href={`/action/${action.id}/`} on:click={async (e)=>shallowRouting(e, action)}>{action.name}</A>
                </TableBodyCell>
                <TableHeadCell>{action.action_module}</TableHeadCell>
                <TableBodyCell>{action.interval}</TableBodyCell>
                <TableBodyCell>
                    <Button size="sm" href={`/action/${action.id}/`} on:click={async (e)=>shallowRouting(e, action)}><Edit />編集</Button>
                    <Button size="sm" on:click={()=>{actionDeleteModal=action}}><Delete /> 削除</Button>
                    <Button size="sm" on:click={async()=>await actionRunOnce(action.id)}><Check /> Run</Button>
                </TableBodyCell>
            </TableBodyRow>
        {:else}
            <TableBodyRow>
                <TableBodyCell>まだActionが定義されていないようです。</TableBodyCell>
                <TableBodyCell></TableBodyCell>
                <TableBodyCell></TableBodyCell>
                <TableBodyCell></TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>

