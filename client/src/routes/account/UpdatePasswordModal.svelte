<script lang="ts">
	import Modal from "flowbite-svelte/Modal.svelte";
    import Label from "flowbite-svelte/Label.svelte";
    import Input from "flowbite-svelte/Input.svelte";
    import Button from "flowbite-svelte/Button.svelte";
	import { UserService } from "$lib/openapi";
	import { showNotification } from "$lib/notification";

    export let open=false;
    let oldPassword="";
    let newPassword="";
    let newPasswordConfirm="";
    const changePassword=async (e:SubmitEvent) => {
        e.preventDefault();
        if (newPassword!==newPasswordConfirm){
            showNotification({title:"New passwords are not match.", kind:"warn"})
            return
        }
        await UserService.userUpdateMe({requestBody:{oldPassword, newPassword}})
        oldPassword="";
        newPassword="";
        newPasswordConfirm="";
        showNotification({title:"Password was changed!", kind:"info"});
        open=false
    }
</script>

<Modal bind:open title="パスワードの変更">
    <form on:submit={changePassword} class="space-y-1">
        <Label for="oldPassword">古いパスワード</Label>
        <Input id="oldPassword" type="password" bind:value={oldPassword} required />
        <Label for="newPassword">新しいパスワード</Label>
        <Input id="newPassword" type="password" bind:value={newPassword} required />
        <Label for="newPasswordConfirm">新しいパスワード(確認)</Label>
        <Input id="newPasswordConfirm" type="password" bind:value={newPasswordConfirm} required />
        <Button type="submit">変更</Button>
        <Button type="button" on:click={()=>{open=false}}>キャンセル</Button> 
    </form>
</Modal>