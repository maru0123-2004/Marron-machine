<script lang="ts">
	import { goto, pushState } from "$app/navigation";
	import { TargetService, type Target } from "$lib/openapi";
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
	import TargetForms from "./TargetForms.svelte";
    import Modal from "flowbite-svelte/Modal.svelte"
    import Create from "flowbite-svelte-icons/PlusOutline.svelte";
    import Edit from "flowbite-svelte-icons/EditOutline.svelte";
    import Delete from "flowbite-svelte-icons/TrashBinOutline.svelte";
    import Check from "flowbite-svelte-icons/CheckOutline.svelte";
	import { destroyNotification, showNotification } from "$lib/notification";
    export let data:PageData;
    const token=data.user
    let targets:Target[]=[];
    onMount(async () => {
        if(!$token){
            goto("/");
            return
        }
        targets=await TargetService.targetGets();
    })
    const targetDelete=async (target_id:string) => {
        const target=await TargetService.targetDelete({targetId:target_id});
        targets=targets.filter((v)=>v.id!==target_id);
        showNotification({title:`Target "${target.name}"を削除しました`, kind:"info"})
    }
    let targetDeleteModal:Target|undefined=undefined;
    const targetPing=async (target_id:string) => {
        const nid=showNotification({title:"Pingを送信しています...", kind:"info"});
        try{
            if (await TargetService.targetPing({targetId:target_id})){
                showNotification({title:"Pingに成功しました!", kind:"info"});
            } else {
                throw Error();
            }
        } catch(e){
            showNotification({title:"Pingに失敗しました。", kind:"warn"});
        }
        destroyNotification(nid??-1);
    }
    const shallowRouting=async (e:MouseEvent, target:Target|undefined=undefined) => {
        if (innerWidth < 640 || e.shiftKey || e.metaKey || e.ctrlKey || !e.currentTarget) return;
        e.preventDefault();
        /* @ts-ignore */
        const {href} = e.currentTarget;
        if(target){
            pushState(href, {modalOpen:true, modalModel:target, modalTitle:"Targetの編集"})
        } else {
            target={id:"",name:"",type:"netbox",addr:"",conn_info:{}}
            pushState(href, {modalOpen:true, modalTitle:"Targetの作成"})
        }
    }
    const shallowRoutingHandler=async (e:CustomEvent<{target:Target}>) => {
        const i=targets.findIndex((t)=>t.id===e.detail.target.id)
        if(i === -1){
            targets=[...targets, e.detail.target]
        } else {
            targets[i]=e.detail.target
        }
    }
</script>

<Modal open={$page.state.modalOpen} title={$page.state.modalTitle} on:close={()=>goto("/target")}>
    <TargetForms target={$page.state.modalModel} on:updated={shallowRoutingHandler}/>
</Modal>

<Confirm open={!!targetDeleteModal} on:close={async ()=>{await targetDelete(targetDeleteModal?.id??"")}}>
    本当に"{targetDeleteModal?.name}"を消去してもよろしいですか?
</Confirm>

<Heading>Target</Heading>
<Button href="/target/new" on:click={async (e)=>shallowRouting(e)}><Create /> Add Target</Button>
<Table>
    <TableHead>
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell>Type</TableHeadCell>
        <TableHeadCell>Address</TableHeadCell>
        <TableHeadCell></TableHeadCell>
    </TableHead>
    <TableBody>
        {#each targets as target(target.id)}
            <TableBodyRow>
                <TableBodyCell>
                    <A href={`/target/${target.id}/`} on:click={async (e)=>shallowRouting(e, target)}>{target.name}</A>
                </TableBodyCell>
                <TableHeadCell>{target.type}</TableHeadCell>
                <TableBodyCell>{target.addr}</TableBodyCell>
                <TableBodyCell>
                    <Button size="sm" href={`/target/${target.id}/`} on:click={async (e)=>shallowRouting(e, target)}><Edit />編集</Button>
                    <Button size="sm" on:click={()=>{targetDeleteModal=target}}><Delete /> 削除</Button>
                    <Button size="sm" on:click={async()=>await targetPing(target.id)}><Check /> Ping</Button>
                </TableBodyCell>
            </TableBodyRow>
        {:else}
            <TableBodyRow>
                <TableBodyCell>まだTargetが定義されていないようです。</TableBodyCell>
                <TableBodyCell></TableBodyCell>
                <TableBodyCell></TableBodyCell>
                <TableBodyCell></TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>

