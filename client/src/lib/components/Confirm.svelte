<script>
    import Button from "flowbite-svelte/Button.svelte";
    import Modal from 'flowbite-svelte/Modal.svelte';
    import Exclamation from 'flowbite-svelte-icons/ExclamationCircleOutline.svelte';
	import { createEventDispatcher } from 'svelte';
    export let open = false;
    const dispatch=createEventDispatcher();

</script>
  
<Modal bind:open={open} size="xs" autoclose outsideclose>
    <div class="text-center">
        <Exclamation class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" />
        <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400"><slot>Are you sure to do this?</slot></h3>
        <Button color="red" class="me-2" on:click={()=>dispatch('close')}>Yes, I'm sure</Button>
        <Button color="alternative">No, cancel</Button>
    </div>
</Modal>

  