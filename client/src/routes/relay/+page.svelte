<script lang="ts">
	import { goto, pushState } from "$app/navigation";
	import { RelayService, type Relay } from "$lib/openapi";
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
	import RelayForms from "./RelayForms.svelte";
    import Modal from "flowbite-svelte/Modal.svelte"
    import Create from "flowbite-svelte-icons/PlusOutline.svelte";
    import Edit from "flowbite-svelte-icons/EditOutline.svelte";
    import Delete from "flowbite-svelte-icons/TrashBinOutline.svelte";
    import Check from "flowbite-svelte-icons/CheckOutline.svelte";
	import { destroyNotification, showNotification } from "$lib/notification";
    export let data:PageData;
    const token=data.user
    let relays:Relay[]=[];

    onMount(async () => {
        if(!$token){
            goto("/");
            return
        }
        relays=await RelayService.relayGets();
    })
    const relayDelete=async (relay_id:string) => {
        const relay=await RelayService.relayDelete({relayId:relay_id});
        relays=relays.filter((v)=>v.id!==relay_id);
        showNotification({title:`Relay "${relay.name}"を削除しました`, kind:"info"})
    }
    let relayDeleteModal:Relay|undefined=undefined;
    const relayPing=async (relay_id:string) => {
        const nid=showNotification({title:"Pingを送信しています...", kind:"info"});
        try{
            if (await RelayService.relayPing({relayId:relay_id})){
                showNotification({title:"Pingに成功しました!", kind:"info"});
            } else {
                throw Error();
            }
        } catch(e){
            showNotification({title:"Pingに失敗しました。", kind:"warn"});
        }
        destroyNotification(nid??-1);
    }
    const shallowRouting=async (e:MouseEvent, relay:Relay|undefined=undefined) => {
        if (innerWidth < 640 || e.shiftKey || e.metaKey || e.ctrlKey || !e.currentTarget) return;
        e.preventDefault();
        /* @ts-ignore */
        const {href} = e.currentTarget;
        if(relay){
            pushState(href, {modalOpen:true, modalModel:relay, modalTitle:"Relayの編集"})
        } else {
            relay={id:"",name:"",addr:"",conn_info:{}}
            pushState(href, {modalOpen:true, modalTitle:"Relayの作成"})
        }
    }
    const shallowRoutingHandler=async (e:CustomEvent<{relay:Relay}>) => {
        const i=relays.findIndex((t)=>t.id===e.detail.relay.id)
        if(i === -1){
            relays=[...relays, e.detail.relay]
        } else {
            relays[i]=e.detail.relay
        }
    }
</script>

<Modal open={$page.state.modalOpen} title={$page.state.modalTitle} on:close={()=>goto("/relay")}>
    <RelayForms relay={$page.state.modalModel} on:updated={shallowRoutingHandler}/>
</Modal>

<Confirm open={!!relayDeleteModal} on:close={async ()=>{await relayDelete(relayDeleteModal?.id??"")}}>
    本当に"{relayDeleteModal?.name}"を消去してもよろしいですか?
</Confirm>

<Heading>Relay</Heading>
<Button href="/relay/new" on:click={async (e)=>shallowRouting(e)}><Create /> Add Relay</Button>
<Table>
    <TableHead>
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell>Address</TableHeadCell>
        <TableHeadCell></TableHeadCell>
    </TableHead>
    <TableBody>
        {#each relays as relay(relay.id)}
            <TableBodyRow>
                <TableBodyCell>
                    <A href={`/relay/${relay.id}/`} on:click={async (e)=>shallowRouting(e, relay)}>{relay.name}</A>
                </TableBodyCell>
                <TableBodyCell>{relay.addr}</TableBodyCell>
                <TableBodyCell>
                    <Button size="sm" href={`/relay/${relay.id}/`} on:click={async (e)=>shallowRouting(e, relay)}><Edit />編集</Button>
                    <Button size="sm" on:click={()=>{relayDeleteModal=relay}}><Delete /> 削除</Button>
                    <Button size="sm" on:click={async()=>await relayPing(relay.id)}><Check /> Ping</Button>
                </TableBodyCell>
            </TableBodyRow>
        {:else}
            <TableBodyRow>
                <TableBodyCell>まだRelayが定義されていないようです。</TableBodyCell>
                <TableBodyCell></TableBodyCell>
                <TableBodyCell></TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>

