<script lang="ts">
	import { TargetService, type Target } from "$lib/openapi";
	import type { PageData } from "./$types";
	import TargetForms from "../TargetForms.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
	import { onMount } from "svelte";
    export let data:PageData;

    let target:Target={
        id:"",
        name:"",
        type:"netbox",
        addr:"",
        conn_info:{},
    };
    onMount(async () => {
        target=await TargetService.targetUpdate({targetId:data.target_id, requestBody:{}});
    })
</script>

<Heading>Target の編集</Heading>
<TargetForms bind:target={target} />