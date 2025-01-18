<script lang="ts">
	import { ActionService, type Action } from "$lib/openapi";
	import type { PageData } from "./$types";
	import ActionForms from "../ActionForms.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
	import { onMount } from "svelte";
    export let data:PageData;

    let action:Action={
        id:"",
        name:"",
        action_module:"collect_ip",
        action_info:{},
        interval:3600
    };
    onMount(async () => {
        action=await ActionService.actionUpdate({actionId:data.action_id, requestBody:{}});
    })
</script>

<Heading>Action の編集</Heading>
<ActionForms bind:action={action} />