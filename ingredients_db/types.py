import ipaddress

from sqlalchemy import types


class IPv4Network(types.TypeDecorator):
    impl = types.TEXT

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return ipaddress.IPv4Network(value) if value else None
