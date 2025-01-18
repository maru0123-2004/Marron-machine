<script lang="ts">
	import { OpenAPI, UserService, type User } from "$lib/openapi";
	import { onMount } from "svelte";
	import type { PageData } from "./$types";
	import { goto } from "$app/navigation";
    import Heading from "flowbite-svelte/Heading.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Label from "flowbite-svelte/Label.svelte";
    import Button from "flowbite-svelte/Button.svelte";
	import { showNotification } from "$lib/notification";
	import Confirm from "$lib/components/Confirm.svelte";
	import UpdatePasswordModal from "./UpdatePasswordModal.svelte";
    export let data:PageData;
    const token=data.user;
    let user:User={
        id: "",
        name:"取得しています...",
        mail:""
    };
    onMount(async ()=>{
        if(!$token){
            goto("/");
            return
        }
        user=await UserService.userMe();
    })
    const updateUser=async (e:SubmitEvent) => {
        e.preventDefault()
        await UserService.userUpdateMe({requestBody:user})
        showNotification({title:"Account info has been updated!", kind:"info"})
    }
    const deleteUser=async () => {
        await UserService.userDeleteMe({password:deleteUserModalPassword})
        showNotification({title:"Account has been deleted. See you!", kind:"info"})
        token.set(undefined);
        OpenAPI.TOKEN=undefined;
        deleteUserModalPassword="";
        goto("/");
    }
    let deleteUserModal=false;
    let deleteUserModalPassword="";
    let updatePasswordModal=false;
</script>

<Confirm bind:open={deleteUserModal} on:close={deleteUser}>
    本当にアカウントを削除してもよろしいですか?<br />
    問題なければ以下にパスワードを入力して"Yes"を押してください。
    <Input type="password" bind:value={deleteUserModalPassword} placeholder="Password..." />
</Confirm>
<UpdatePasswordModal bind:open={updatePasswordModal} />

<Heading>アカウント</Heading>
<form class="space-y-1" on:submit={updateUser}>
    <Label for="name">ユーザ名</Label>
    <Input id="name" type="text" bind:value={user.name} required />
    <Label for="mail">メールアドレス</Label>
    <Input id="mail" type="email" bind:value={user.mail} required />
    <Button type="submit">変更の適用</Button><br />
    <Button type="button" on:click={()=>{updatePasswordModal=true}}>パスワードの変更</Button>
    <Button type="button" on:click={()=>{deleteUserModal=true}}>アカウントの削除</Button>
</form>