<script lang="ts">
	import { Alert, Button } from 'flowbite-svelte';
	import Google from '$lib/components/Google.svelte';
	import type { PageData } from '../$types';
    export let data:PageData;
    const user=data.user
</script>


{#if !$user}
    <Alert>
        Please login to use this page.
    </Alert>
    <Button tag="a" href="/api/v1/auth/login" color="alternative"><Google/>Continue with Google</Button>
{/if}
