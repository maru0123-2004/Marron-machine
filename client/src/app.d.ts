// See https://kit.svelte.dev/docs/types#app

import type { Action, Relay, Target } from "$lib/openapi";

// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		interface PageState {
			modalOpen?: boolean=false;
			modalModel?: Action|Target|Relay
			modalTitle?: string="";
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
