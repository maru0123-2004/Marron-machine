import { showNotification } from "$lib/notification";
import { ApiError, AuthService, OpenAPI, UserService, type Token } from "$lib/openapi";
import { get, writable } from "svelte/store";

export const prerender = true
export const ssr = false

const user = writable<Token|undefined>(undefined);

export const load = async ()=>{
    try {
        const token = (await AuthService.authSession())[0];
        OpenAPI.TOKEN=token.access_token;
        user.set(token);
        showNotification({title: 'Login Successfull!', kind:'info'})
    } catch(e){
        console.debug("auth error")
        const token=undefined;
    }
    OpenAPI.interceptors.response.use(async (response) => {
        if (!response.ok) {
            const body=await response.json()
            showNotification({title:'Error', kind:'warn', subtitle: body.detail})
        }
        return response
    })
    return {user}
}