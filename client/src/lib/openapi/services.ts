import type { CancelablePromise } from './core/CancelablePromise';
import { OpenAPI } from './core/OpenAPI';
import { request as __request } from './core/request';

import type {
	Body_Auth_signin,
	Token,
	User,
	UserCreate,
	UserNoMail,
	UserUpdate,
	Relay,
	Target,
	TargetCreate,
	TargetUpdate,
	RelayCreate,
	RelayUpdate,
	Action,
	ActionCreate,
	ActionUpdate,
	History,
	Inventory,
	InventoryCreate,
	InventoryCreateForIPMI,
	InventoryDict
} from './models';

export type AuthData = {
	AuthSignin: {
		formData: Body_Auth_signin;
	};
	AuthSignup: {
		requestBody: UserCreate;
	};
};

export type UserData = {
	UserDeleteMe: {
		password?: string;
	};
	UserUpdateMe: {
		requestBody: UserUpdate;
	};
	UserGet: {
		id: string;
	};
};

export type TargetData = {
	TargetCreate: {
		requestBody: TargetCreate;
	};
	TargetUpdate: {
		requestBody: TargetUpdate;
		targetId: string;
	};
	TargetDelete: {
		targetId: string;
	};
	TargetGetOwner: {
		targetId: string;
	};
	TargetAddOwner: {
		targetId: string;
		userId: string;
	};
	TargetDelOwner: {
		targetId: string;
		userId: string;
	};
	TargetGetRelays: {
		targetId: string;
	};
	TargetSetRelays: {
		requestBody: Array<string>;
		targetId: string;
	};
	TargetPing: {
		targetId: string;
	};
};

export type RelayData = {
	RelayCreate: {
		requestBody: RelayCreate;
	};
	RelayUpdate: {
		relayId: string;
		requestBody: RelayUpdate;
	};
	RelayDelete: {
		relayId: string;
	};
	RelayGetOwner: {
		relayId: string;
	};
	RelayAddOwner: {
		relayId: string;
		userId: string;
	};
	RelayDelOwner: {
		relayId: string;
		userId: string;
	};
	RelayPing: {
		relayId: string;
	};
};

export type ActionData = {
	ActionCreate: {
		requestBody: ActionCreate;
	};
	ActionUpdate: {
		actionId: string;
		requestBody: ActionUpdate;
	};
	ActionDelete: {
		actionId: string;
	};
	ActionGetOwner: {
		actionId: string;
	};
	ActionAddOwner: {
		actionId: string;
		userId: string;
	};
	ActionDelOwner: {
		actionId: string;
		userId: string;
	};
	ActionGetTarget: {
		actionId: string;
	};
	ActionAddTarget: {
		actionId: string;
		targetId: string;
	};
	ActionDelTarget: {
		actionId: string;
		targetId: string;
	};
	ActionGetHistorys: {
		actionId: string;
	};
	ActionDelHistory: {
		actionId: string;
		historyId: string;
	};
	ActionRunOnce: {
		actionId: string;
	};
};

export type InventoryData = {
	InventoryCreate: {
		requestBody: InventoryCreate;
	};
	InventoryCreateFromIpmi: {
		requestBody: InventoryCreateForIPMI;
	};
	InventoryGetUrl: {
		inventoryId: string;
	};
	InventoryDelete: {
		inventoryId: string;
	};
	InventoryGetOwner: {
		inventoryId: string;
	};
	InventoryAddOwner: {
		inventoryId: string;
		userId: string;
	};
	InventoryDelOwner: {
		inventoryId: string;
		userId: string;
	};
};

export class AuthService {
	/**
	 * Signin
	 * @returns Token Successful Response
	 * @throws ApiError
	 */
	public static authSignin(data: AuthData['AuthSignin']): CancelablePromise<Token> {
		const { formData } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/auth/signin',
			formData: formData,
			mediaType: 'application/x-www-form-urlencoded',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Signup
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static authSignup(data: AuthData['AuthSignup']): CancelablePromise<User> {
		const { requestBody } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/auth/signup',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Signout
	 * @returns unknown Successful Response
	 * @throws ApiError
	 */
	public static authSignout(): CancelablePromise<unknown> {
		return __request(OpenAPI, {
			method: 'POST',
			url: '/auth/signout',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Session
	 * @returns Token Successful Response
	 * @throws ApiError
	 */
	public static authSession(): CancelablePromise<Array<Token>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/auth/session',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}
}

export class UserService {
	/**
	 * Gets
	 * @returns UserNoMail Successful Response
	 * @throws ApiError
	 */
	public static userGets(): CancelablePromise<Array<UserNoMail>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/user/',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Me
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static userMe(): CancelablePromise<User> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/user/me',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Delete Me
	 * @returns unknown Successful Response
	 * @throws ApiError
	 */
	public static userDeleteMe(data: UserData['UserDeleteMe'] = {}): CancelablePromise<unknown> {
		const { password } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/user/me',
			query: {
				password
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update Me
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static userUpdateMe(data: UserData['UserUpdateMe']): CancelablePromise<User> {
		const { requestBody } = data;
		return __request(OpenAPI, {
			method: 'PATCH',
			url: '/user/me',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get
	 * @returns UserNoMail Successful Response
	 * @throws ApiError
	 */
	public static userGet(data: UserData['UserGet']): CancelablePromise<UserNoMail> {
		const { id } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/user/{id}',
			path: {
				id
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}
}

export class TargetService {
	/**
	 * Gets
	 * @returns Target Successful Response
	 * @throws ApiError
	 */
	public static targetGets(): CancelablePromise<Array<Target>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/target/',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Create
	 * @returns Target Successful Response
	 * @throws ApiError
	 */
	public static targetCreate(data: TargetData['TargetCreate']): CancelablePromise<Target> {
		const { requestBody } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/target/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update
	 * @returns Target Successful Response
	 * @throws ApiError
	 */
	public static targetUpdate(data: TargetData['TargetUpdate']): CancelablePromise<Target> {
		const { targetId, requestBody } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/target/{target_id}',
			path: {
				target_id: targetId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete
	 * @returns Target Successful Response
	 * @throws ApiError
	 */
	public static targetDelete(data: TargetData['TargetDelete']): CancelablePromise<Target> {
		const { targetId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/target/{target_id}',
			path: {
				target_id: targetId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static targetGetOwner(data: TargetData['TargetGetOwner']): CancelablePromise<Array<User>> {
		const { targetId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/target/{target_id}/owner',
			path: {
				target_id: targetId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static targetAddOwner(data: TargetData['TargetAddOwner']): CancelablePromise<Array<User>> {
		const { targetId, userId } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/target/{target_id}/owner',
			path: {
				target_id: targetId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Del Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static targetDelOwner(data: TargetData['TargetDelOwner']): CancelablePromise<Array<User>> {
		const { targetId, userId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/target/{target_id}/owner',
			path: {
				target_id: targetId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Relays
	 * @returns Relay Successful Response
	 * @throws ApiError
	 */
	public static targetGetRelays(
		data: TargetData['TargetGetRelays']
	): CancelablePromise<Array<Relay>> {
		const { targetId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/target/{target_id}/relay',
			path: {
				target_id: targetId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Set Relays
	 * @returns Relay Successful Response
	 * @throws ApiError
	 */
	public static targetSetRelays(
		data: TargetData['TargetSetRelays']
	): CancelablePromise<Array<Relay>> {
		const { targetId, requestBody } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/target/{target_id}/relay',
			path: {
				target_id: targetId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Ping
	 * @returns boolean Successful Response
	 * @throws ApiError
	 */
	public static targetPing(data: TargetData['TargetPing']): CancelablePromise<boolean> {
		const { targetId } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/target/{target_id}/ping',
			path: {
				target_id: targetId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}
}

export class RelayService {
	/**
	 * Gets
	 * @returns Relay Successful Response
	 * @throws ApiError
	 */
	public static relayGets(): CancelablePromise<Array<Relay>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/relay/',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Create
	 * @returns Relay Successful Response
	 * @throws ApiError
	 */
	public static relayCreate(data: RelayData['RelayCreate']): CancelablePromise<Relay> {
		const { requestBody } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/relay/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update
	 * @returns Relay Successful Response
	 * @throws ApiError
	 */
	public static relayUpdate(data: RelayData['RelayUpdate']): CancelablePromise<Relay> {
		const { relayId, requestBody } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/relay/{relay_id}',
			path: {
				relay_id: relayId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete
	 * @returns Relay Successful Response
	 * @throws ApiError
	 */
	public static relayDelete(data: RelayData['RelayDelete']): CancelablePromise<Relay> {
		const { relayId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/relay/{relay_id}',
			path: {
				relay_id: relayId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static relayGetOwner(data: RelayData['RelayGetOwner']): CancelablePromise<Array<User>> {
		const { relayId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/relay/{relay_id}/owner',
			path: {
				relay_id: relayId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static relayAddOwner(data: RelayData['RelayAddOwner']): CancelablePromise<Array<User>> {
		const { relayId, userId } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/relay/{relay_id}/owner',
			path: {
				relay_id: relayId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Del Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static relayDelOwner(data: RelayData['RelayDelOwner']): CancelablePromise<Array<User>> {
		const { relayId, userId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/relay/{relay_id}/owner',
			path: {
				relay_id: relayId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Ping
	 * @returns boolean Successful Response
	 * @throws ApiError
	 */
	public static relayPing(data: RelayData['RelayPing']): CancelablePromise<boolean> {
		const { relayId } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/relay/{relay_id}/ping',
			path: {
				relay_id: relayId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}
}

export class ActionService {
	/**
	 * Gets
	 * @returns Action Successful Response
	 * @throws ApiError
	 */
	public static actionGets(): CancelablePromise<Array<Action>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/action/',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Create
	 * @returns Action Successful Response
	 * @throws ApiError
	 */
	public static actionCreate(data: ActionData['ActionCreate']): CancelablePromise<Action> {
		const { requestBody } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/action/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Update
	 * @returns Action Successful Response
	 * @throws ApiError
	 */
	public static actionUpdate(data: ActionData['ActionUpdate']): CancelablePromise<Action> {
		const { actionId, requestBody } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/action/{action_id}',
			path: {
				action_id: actionId
			},
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete
	 * @returns Action Successful Response
	 * @throws ApiError
	 */
	public static actionDelete(data: ActionData['ActionDelete']): CancelablePromise<Action> {
		const { actionId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/action/{action_id}',
			path: {
				action_id: actionId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static actionGetOwner(data: ActionData['ActionGetOwner']): CancelablePromise<Array<User>> {
		const { actionId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/action/{action_id}/owner',
			path: {
				action_id: actionId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static actionAddOwner(data: ActionData['ActionAddOwner']): CancelablePromise<Array<User>> {
		const { actionId, userId } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/action/{action_id}/owner',
			path: {
				action_id: actionId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Del Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static actionDelOwner(data: ActionData['ActionDelOwner']): CancelablePromise<Array<User>> {
		const { actionId, userId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/action/{action_id}/owner',
			path: {
				action_id: actionId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Target
	 * @returns Target Successful Response
	 * @throws ApiError
	 */
	public static actionGetTarget(
		data: ActionData['ActionGetTarget']
	): CancelablePromise<Array<Target>> {
		const { actionId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/action/{action_id}/target',
			path: {
				action_id: actionId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Target
	 * @returns Target Successful Response
	 * @throws ApiError
	 */
	public static actionAddTarget(
		data: ActionData['ActionAddTarget']
	): CancelablePromise<Array<Target>> {
		const { actionId, targetId } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/action/{action_id}/target',
			path: {
				action_id: actionId
			},
			query: {
				target_id: targetId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Del Target
	 * @returns Target Successful Response
	 * @throws ApiError
	 */
	public static actionDelTarget(
		data: ActionData['ActionDelTarget']
	): CancelablePromise<Array<Target>> {
		const { actionId, targetId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/action/{action_id}/target',
			path: {
				action_id: actionId
			},
			query: {
				target_id: targetId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Historys
	 * @returns History Successful Response
	 * @throws ApiError
	 */
	public static actionGetHistorys(
		data: ActionData['ActionGetHistorys']
	): CancelablePromise<Array<History>> {
		const { actionId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/action/{action_id}/history',
			path: {
				action_id: actionId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Del History
	 * @returns History Successful Response
	 * @throws ApiError
	 */
	public static actionDelHistory(
		data: ActionData['ActionDelHistory']
	): CancelablePromise<Array<History>> {
		const { actionId, historyId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/action/{action_id}/history/{history_id}',
			path: {
				action_id: actionId,
				history_id: historyId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Run Once
	 * @returns unknown Successful Response
	 * @throws ApiError
	 */
	public static actionRunOnce(data: ActionData['ActionRunOnce']): CancelablePromise<unknown> {
		const { actionId } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/action/{action_id}/run',
			path: {
				action_id: actionId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}
}

export class InventoryService {
	/**
	 * Gets
	 * @returns Inventory Successful Response
	 * @throws ApiError
	 */
	public static inventoryGets(): CancelablePromise<Array<Inventory>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/inventory/',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Create
	 * @returns Inventory Successful Response
	 * @throws ApiError
	 */
	public static inventoryCreate(
		data: InventoryData['InventoryCreate']
	): CancelablePromise<Inventory> {
		const { requestBody } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/inventory/',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Suggest
	 * @returns InventoryDict Successful Response
	 * @throws ApiError
	 */
	public static inventorySuggest(): CancelablePromise<Record<string, Array<InventoryDict>>> {
		return __request(OpenAPI, {
			method: 'GET',
			url: '/inventory/suggest',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`
			}
		});
	}

	/**
	 * Create From Ipmi
	 * @returns Inventory Successful Response
	 * @throws ApiError
	 */
	public static inventoryCreateFromIpmi(
		data: InventoryData['InventoryCreateFromIpmi']
	): CancelablePromise<Inventory> {
		const { requestBody } = data;
		return __request(OpenAPI, {
			method: 'POST',
			url: '/inventory/create_from_ipmi',
			body: requestBody,
			mediaType: 'application/json',
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Url
	 * @returns string Successful Response
	 * @throws ApiError
	 */
	public static inventoryGetUrl(data: InventoryData['InventoryGetUrl']): CancelablePromise<string> {
		const { inventoryId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/inventory/{invntory_id}',
			query: {
				inventory_id: inventoryId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Delete
	 * @returns Inventory Successful Response
	 * @throws ApiError
	 */
	public static inventoryDelete(
		data: InventoryData['InventoryDelete']
	): CancelablePromise<Inventory> {
		const { inventoryId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/inventory/{inventory_id}',
			path: {
				inventory_id: inventoryId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Get Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static inventoryGetOwner(
		data: InventoryData['InventoryGetOwner']
	): CancelablePromise<Array<User>> {
		const { inventoryId } = data;
		return __request(OpenAPI, {
			method: 'GET',
			url: '/inventory/{inventory_id}/owner',
			path: {
				inventory_id: inventoryId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Add Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static inventoryAddOwner(
		data: InventoryData['InventoryAddOwner']
	): CancelablePromise<Array<User>> {
		const { inventoryId, userId } = data;
		return __request(OpenAPI, {
			method: 'PUT',
			url: '/inventory/{inventory_id}/owner',
			path: {
				inventory_id: inventoryId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}

	/**
	 * Del Owner
	 * @returns User Successful Response
	 * @throws ApiError
	 */
	public static inventoryDelOwner(
		data: InventoryData['InventoryDelOwner']
	): CancelablePromise<Array<User>> {
		const { inventoryId, userId } = data;
		return __request(OpenAPI, {
			method: 'DELETE',
			url: '/inventory/{inventory_id}/owner',
			path: {
				inventory_id: inventoryId
			},
			query: {
				user_id: userId
			},
			errors: {
				400: `Bad Request`,
				401: `Unauthorized`,
				404: `Not Found`,
				422: `Validation Error`
			}
		});
	}
}
