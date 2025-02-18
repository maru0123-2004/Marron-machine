export type APIError = {
	status_code?: number;
	detail?: string;
};

export type Action = {
	id: string;
	name: string;
	action_module: ActionModule;
	action_info: Record<string, unknown>;
	interval: number;
};

export type ActionCreate = {
	name: string;
	action_module: ActionModule;
	action_info: Record<string, unknown>;
	interval: number;
};

export type ActionModule = 'dhcp_dnsmasq' | 'dns_dnsmasq' | 'collect_ip';

export type ActionUpdate = {
	name?: string | null;
	action_module?: ActionModule | null;
	action_info?: Record<string, unknown> | null;
	interval?: number | null;
};

export type Body_Auth_signin = {
	grant_type?: string | null;
	username: string;
	password: string;
	scope?: string;
	client_id?: string | null;
	client_secret?: string | null;
};

export type Forbidden = {
	status_code?: number;
	detail?: string;
};

export type HTTPValidationError = {
	detail?: Array<ValidationError>;
};

export type History = {
	id: string;
	status: HistoryStatus;
	time: string;
	logs: string;
};

export type HistoryStatus = 0 | 1 | 2;

export type Inventory = {
	id: string;
	name: string;
	inventory_id: string;
	ipam_id: string;
};

export type InventoryCreate = {
	name: string;
	inventory_id: string;
	ipam_id: string;
};

export type InventoryCreateForIPMI = {
	name: string;
	inventory_id?: string | null;
	ipam_id: string;
	ipaddr: string;
	username: string;
	password: string;
	ipmi_interface_type?: string | null;
	ipmi_hostname?: string | null;
};

export type InventoryDict = {
	id: string;
	name: string;
};

export type NotFound = {
	status_code?: number;
	detail?: string;
};

export type Relay = {
	id: string;
	name: string;
	addr: string;
	conn_info: Record<string, unknown>;
};

export type RelayCreate = {
	name: string;
	addr: string;
	conn_info: Record<string, unknown>;
};

export type RelayUpdate = {
	name?: string | null;
	addr?: string | null;
	conn_info?: Record<string, unknown> | null;
};

export type Target = {
	id: string;
	name: string;
	addr: string;
	conn_info: Record<string, unknown>;
	type: TargetType;
};

export type TargetCreate = {
	name: string;
	addr: string;
	conn_info: Record<string, unknown>;
	type: TargetType;
};

export type TargetType = 'netbox' | 'server' | 'network';

export type TargetUpdate = {
	name?: string | null;
	addr?: string | null;
	conn_info?: Record<string, unknown> | null;
	type?: TargetType | null;
};

export type Token = {
	access_token: string;
	token_type?: string;
	user_id: string;
	expired_in: string;
};

export type User = {
	id: string;
	name: string;
	mail: string;
};

export type UserCreate = {
	name: string;
	mail: string;
	password: string;
};

export type UserNoMail = {
	id: string;
	name: string;
};

export type UserUpdate = {
	name?: string;
	mail?: string;
	oldPassword?: string;
	newPassword?: string;
};

export type ValidationError = {
	loc: Array<string | number>;
	msg: string;
	type: string;
};
