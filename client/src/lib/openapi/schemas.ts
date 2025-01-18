export const $APIError = {
	properties: {
		status_code: {
			type: 'number',
			default: 400
		},
		detail: {
			type: 'string',
			default: 'Something Wrong'
		}
	}
} as const;

export const $Action = {
	properties: {
		id: {
			type: 'string',
			isRequired: true,
			format: 'uuid'
		},
		name: {
			type: 'string',
			isRequired: true
		},
		action_module: {
			type: 'ActionModule',
			isRequired: true
		},
		action_info: {
			type: 'dictionary',
			contains: {
				properties: {}
			},
			isRequired: true
		},
		interval: {
			type: 'number',
			isRequired: true
		}
	}
} as const;

export const $ActionCreate = {
	properties: {
		name: {
			type: 'string',
			isRequired: true
		},
		action_module: {
			type: 'ActionModule',
			isRequired: true
		},
		action_info: {
			type: 'dictionary',
			contains: {
				properties: {}
			},
			isRequired: true
		},
		interval: {
			type: 'number',
			isRequired: true
		}
	}
} as const;

export const $ActionModule = {
	type: 'Enum',
	enum: ['dhcp_dnsmasq', 'dns_dnsmasq', 'collect_ip']
} as const;

export const $ActionUpdate = {
	properties: {
		name: {
			type: 'any-of',
			contains: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			]
		},
		action_module: {
			type: 'any-of',
			contains: [
				{
					type: 'ActionModule'
				},
				{
					type: 'null'
				}
			]
		},
		action_info: {
			type: 'any-of',
			contains: [
				{
					type: 'dictionary',
					contains: {
						properties: {}
					}
				},
				{
					type: 'null'
				}
			]
		},
		interval: {
			type: 'any-of',
			contains: [
				{
					type: 'number'
				},
				{
					type: 'null'
				}
			]
		}
	}
} as const;

export const $Body_Auth_signin = {
	properties: {
		grant_type: {
			type: 'any-of',
			contains: [
				{
					type: 'string',
					pattern: 'password'
				},
				{
					type: 'null'
				}
			]
		},
		username: {
			type: 'string',
			isRequired: true
		},
		password: {
			type: 'string',
			isRequired: true
		},
		scope: {
			type: 'string',
			default: ''
		},
		client_id: {
			type: 'any-of',
			contains: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			]
		},
		client_secret: {
			type: 'any-of',
			contains: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			]
		}
	}
} as const;

export const $Forbidden = {
	properties: {
		status_code: {
			type: 'number',
			default: 401
		},
		detail: {
			type: 'string',
			default: 'Not authenticated'
		}
	}
} as const;

export const $HTTPValidationError = {
	properties: {
		detail: {
			type: 'array',
			contains: {
				type: 'ValidationError'
			}
		}
	}
} as const;

export const $History = {
	properties: {
		id: {
			type: 'string',
			isRequired: true,
			format: 'uuid'
		},
		status: {
			type: 'HistoryStatus',
			isRequired: true
		},
		time: {
			type: 'string',
			isRequired: true,
			format: 'date-time'
		},
		logs: {
			type: 'string',
			isRequired: true
		}
	}
} as const;

export const $HistoryStatus = {
	type: 'Enum',
	enum: [0, 1, 2]
} as const;

export const $NotFound = {
	properties: {
		status_code: {
			type: 'number',
			default: 404
		},
		detail: {
			type: 'string',
			default: 'Not found'
		}
	}
} as const;

export const $Relay = {
	properties: {
		id: {
			type: 'string',
			isRequired: true,
			format: 'uuid'
		},
		name: {
			type: 'string',
			isRequired: true
		},
		addr: {
			type: 'string',
			isRequired: true,
			format: 'ipvanyaddress'
		},
		conn_info: {
			type: 'dictionary',
			contains: {
				properties: {}
			},
			isRequired: true
		}
	}
} as const;

export const $RelayCreate = {
	properties: {
		name: {
			type: 'string',
			isRequired: true
		},
		addr: {
			type: 'string',
			isRequired: true,
			format: 'ipvanyaddress'
		},
		conn_info: {
			type: 'dictionary',
			contains: {
				properties: {}
			},
			isRequired: true
		}
	}
} as const;

export const $RelayUpdate = {
	properties: {
		name: {
			type: 'any-of',
			contains: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			]
		},
		addr: {
			type: 'any-of',
			contains: [
				{
					type: 'string',
					format: 'ipvanyaddress'
				},
				{
					type: 'null'
				}
			]
		},
		conn_info: {
			type: 'any-of',
			contains: [
				{
					type: 'dictionary',
					contains: {
						properties: {}
					}
				},
				{
					type: 'null'
				}
			]
		}
	}
} as const;

export const $Target = {
	properties: {
		id: {
			type: 'string',
			isRequired: true,
			format: 'uuid'
		},
		name: {
			type: 'string',
			isRequired: true
		},
		addr: {
			type: 'string',
			isRequired: true,
			format: 'ipvanynetwork'
		},
		conn_info: {
			type: 'dictionary',
			contains: {
				properties: {}
			},
			isRequired: true
		},
		type: {
			type: 'TargetType',
			isRequired: true
		}
	}
} as const;

export const $TargetCreate = {
	properties: {
		name: {
			type: 'string',
			isRequired: true
		},
		addr: {
			type: 'string',
			isRequired: true,
			format: 'ipvanynetwork'
		},
		conn_info: {
			type: 'dictionary',
			contains: {
				properties: {}
			},
			isRequired: true
		},
		type: {
			type: 'TargetType',
			isRequired: true
		}
	}
} as const;

export const $TargetType = {
	type: 'Enum',
	enum: ['netbox', 'server', 'network']
} as const;

export const $TargetUpdate = {
	properties: {
		name: {
			type: 'any-of',
			contains: [
				{
					type: 'string'
				},
				{
					type: 'null'
				}
			]
		},
		addr: {
			type: 'any-of',
			contains: [
				{
					type: 'string',
					format: 'ipvanynetwork'
				},
				{
					type: 'null'
				}
			]
		},
		conn_info: {
			type: 'any-of',
			contains: [
				{
					type: 'dictionary',
					contains: {
						properties: {}
					}
				},
				{
					type: 'null'
				}
			]
		},
		type: {
			type: 'any-of',
			contains: [
				{
					type: 'TargetType'
				},
				{
					type: 'null'
				}
			]
		}
	}
} as const;

export const $Token = {
	properties: {
		access_token: {
			type: 'string',
			isRequired: true
		},
		token_type: {
			type: 'string',
			default: 'bearer'
		},
		user_id: {
			type: 'string',
			isRequired: true,
			format: 'uuid'
		},
		expired_in: {
			type: 'string',
			isRequired: true,
			format: 'date-time'
		}
	}
} as const;

export const $User = {
	properties: {
		id: {
			type: 'string',
			isRequired: true,
			format: 'uuid'
		},
		name: {
			type: 'string',
			isRequired: true
		},
		mail: {
			type: 'string',
			isRequired: true,
			format: 'email'
		}
	}
} as const;

export const $UserCreate = {
	properties: {
		name: {
			type: 'string',
			isRequired: true,
			maxLength: 1024
		},
		mail: {
			type: 'string',
			isRequired: true,
			format: 'email'
		},
		password: {
			type: 'string',
			isRequired: true,
			format: 'password'
		}
	}
} as const;

export const $UserNoMail = {
	properties: {
		id: {
			type: 'string',
			isRequired: true,
			format: 'uuid'
		},
		name: {
			type: 'string',
			isRequired: true
		}
	}
} as const;

export const $UserUpdate = {
	properties: {
		name: {
			type: 'string'
		},
		mail: {
			type: 'string',
			format: 'email'
		},
		oldPassword: {
			type: 'string'
		},
		newPassword: {
			type: 'string'
		}
	}
} as const;

export const $ValidationError = {
	properties: {
		loc: {
			type: 'array',
			contains: {
				type: 'any-of',
				contains: [
					{
						type: 'string'
					},
					{
						type: 'number'
					}
				]
			},
			isRequired: true
		},
		msg: {
			type: 'string',
			isRequired: true
		},
		type: {
			type: 'string',
			isRequired: true
		}
	}
} as const;
