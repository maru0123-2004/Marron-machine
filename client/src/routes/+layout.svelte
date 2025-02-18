<script lang="ts">
	import { DarkMode, NavBrand, NavHamburger, NavLi, NavUl, Navbar } from 'flowbite-svelte';
	import '../app.pcss';
	import { AuthService, OpenAPI } from '$lib/openapi';
	import { goto } from '$app/navigation';
	import type { LayoutData } from './$types';
	import {destroyNotification, notifications} from '$lib/notification'
	import Notification from '$lib/components/Notification.svelte';
	import { fade } from 'svelte/transition';

	export let data:LayoutData
	const user=data.user;

	const logout=async (e: Event) => {
		e.preventDefault();
		await AuthService.authSignout();
		user.set(undefined)
		OpenAPI.TOKEN=undefined
		await goto('/')
	}
</script>
<Navbar>
	<NavBrand href="/">
	<!-- <NavBrand href="/" class="dark:bg-gray-500 rounded"> -->
		Top
		<!-- <img src="/logo.png" alt="Logo" class="m-1 h-6 sm:h-9" />
		<img src="/title.png" alt="Title" class="m-1 h-6 sm:h-9" /> -->
	</NavBrand>
	<NavHamburger />
	<NavUl>
		{#if $user}
			<NavLi href="/action">Action</NavLi>
			<NavLi href="/target">Target</NavLi>
			<NavLi href="/relay">Relay</NavLi>
			<NavLi href="/inventory">Inventory</NavLi>
			<NavLi href="/account">Account</NavLi>
			<NavLi on:click={logout}>Log out</NavLi>
		{:else}
			<NavLi href="/signin">Sign in</NavLi>
			<NavLi href="/signup">Sign up</NavLi>
		{/if}
		<DarkMode btnClass="m-0" />
	</NavUl>
</Navbar>
<div class="p-4 space-y-2">
	{#if $notifications}
		<div class="absolute top-20 right-5 w-full max-w-xs z-[100] isolation space-y-1">
		{#each $notifications as nortification (nortification.id)}
			<div transition:fade>
				<Notification  title={nortification.title} subtitle={nortification.subtitle} kind={nortification.kind}
				on:close={() => destroyNotification(nortification.id??0)} />
			</div>
		{/each}
		</div>
    {/if}
	<slot />
</div>

