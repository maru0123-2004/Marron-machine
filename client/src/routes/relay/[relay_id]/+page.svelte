<script lang="ts">
	import { RelayService, type Relay } from "$lib/openapi";
	import type { PageData } from "./$types";
	import RelayForms from "../RelayForms.svelte";
    import Heading from "flowbite-svelte/Heading.svelte";
	import { onMount } from "svelte";
    export let data:PageData;

    let relay:Relay={
        id:"",
        name:"",
        addr:"",
        conn_info:{},
    };
    onMount(async () => {
        relay=await RelayService.relayUpdate({relayId:data.relay_id, requestBody:{}});
    })
</script>

<Heading>Relay の編集</Heading>
<RelayForms bind:relay={relay} />