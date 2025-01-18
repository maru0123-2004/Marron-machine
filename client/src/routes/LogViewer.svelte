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
	import { onMount } from "svelte";
	import { ActionService, type Action } from "$lib/openapi";
    let actions:Action[]=[];
    onMount(async () => {
        actions=await ActionService.actionGets();
    })
</script>

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
                <TableBodyCell>
                    {#await ActionService.actionGetHistorys({actionId:action.id})}
                        Retrieving history...
                    {:then historys} 
                        <Badge rounded large>
                            o
                        </Badge>
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