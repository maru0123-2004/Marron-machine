from typing import Any, Optional, Type, Union
from ipaddress import IPv4Address, IPv6Address, ip_address, IPv4Network, IPv6Network, ip_network
from tortoise.fields import Field
from tortoise import Model

class IPAddressField(Field[Union[IPv4Address, IPv6Address]]):
    class _db_postgres:
        SQL_TYPE="INET"
    def to_db_value(self, value: Any, instance: "Union[Type[Model], Model]") -> Optional[str]:
        return value and str(value)

    def to_python_value(self, value: Any) -> Optional[Union[IPv4Address, IPv6Address]]:
        if value is None or isinstance(value, IPv4Address) or isinstance(value, IPv6Address):
            return value
        return ip_address(value)

class IPNetworkField(Field[Union[IPv4Network, IPv6Network]]):
    class _db_postgres:
        SQL_TYPE="INET"
    def to_db_value(self, value: Any, instance: "Union[Type[Model], Model]") -> Optional[str]:
        return value and str(value)

    def to_python_value(self, value: Any) -> Optional[Union[IPv4Network, IPv6Network]]:
        if value is None or isinstance(value, IPv4Network) or isinstance(value, IPv6Network):
            return value
        return ip_network(value)