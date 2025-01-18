<script lang="ts">
	import A from "flowbite-svelte/A.svelte";
    import type { PageData } from "./$types";
	import LogViewer from "./LogViewer.svelte";
    export let data:PageData;
    const user=data.user;
</script>

{#if !$user}
    このページを使用するには、<A href="/signin"> サインイン</A>が必要です。<br />
    アカウントをお持ちでない場合は、<A href="/signup">サインアップ</A>してください。
{:else}
    <LogViewer />
{/if}

