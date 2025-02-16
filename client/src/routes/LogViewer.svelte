<script lang="ts">
	import Table from "flowbite-svelte/Table.svelte";
	import TableHead from "flowbite-svelte/TableHead.svelte";
	import TableHeadCell from "flowbite-svelte/TableHeadCell.svelte";
	import TableBody from "flowbite-svelte/TableBody.svelte";
	import TableBodyRow from "flowbite-svelte/TableBodyRow.svelte";
	import TableBodyCell from "flowbite-svelte/TableBodyCell.svelte";
    import A from "flowbite-svelte/A.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Badge from "flowbite-svelte/Badge.svelte";
    import Check from "flowbite-svelte-icons/CheckOutline.svelte";
	import { onMount } from "svelte";
	import { ActionService, type Action, type HistoryStatus, $HistoryStatus as HistoryStatusEnum,type History } from "$lib/openapi";
	import Modal from "flowbite-svelte/Modal.svelte";
    let actions:Action[]=[];
    let selectedHistory:History|undefined=undefined;
    $: historyModal=!!selectedHistory;
    onMount(async () => {
        actions=await ActionService.actionGets();
    })
    const status2color=(status:HistoryStatus):"red"|"yellow"|"green"=>{
        if(status===0){
            return "yellow";
        } else if (status===1){
            return "green";
        } else {
            return "red";
        }
    }
</script>

<Modal open={historyModal} on:close={()=>{selectedHistory=undefined}} title={selectedHistory?.time}>
<pre>{selectedHistory?.logs}</pre>
</Modal>

<Heading>Action History</Heading>
<Table>
    <TableHead>
        <TableHeadCell>Action</TableHeadCell>
        <TableHeadCell>Attempts</TableHeadCell>
    </TableHead>
    <TableBody>
        {#each actions as action(action.id)}
            <TableBodyRow>
                <TableBodyCell><A href={`/action/${action.id}/`}>{action.name}</A></TableBodyCell>
                <TableBodyCell class="space-x-1">
                    {#await ActionService.actionGetHistorys({actionId:action.id})}
                        Retrieving history...
                    {:then historys}
                        {historys.length}
                        {#each historys as history(history.id)}
                            <button on:click={()=>{console.log("aaaa");selectedHistory=history}}>
                            <Badge rounded large color={status2color(history.status)}>
                                {#if history.status===1}
                                    <Check />
                                {/if}
                            </Badge>
                            </button>
                        {/each}
                    {/await}
                </TableBodyCell>
            </TableBodyRow>
        {:else}
            <TableBodyRow>
                <TableBodyCell>まだActionが定義されていないようです。</TableBodyCell>
                <TableBodyCell></TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>