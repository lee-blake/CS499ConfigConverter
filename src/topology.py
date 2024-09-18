

class RouterInterface:
    def __init__(self, router_name, interface_name):
        self._router_name = router_name
        self._interface_name = interface_name

    @property
    def router_name(self):
        return self._router_name

    @property
    def interface_name(self):
        return self._interface_name

    def __eq__(self, other):
        return self._router_name == other._router_name \
                and self._interface_name == other._interface_name

    def __hash__(self):
        return hash(self._router_name)

    def __str__(self):
        return f"{self._router_name}:{self._interface_name}"


class TopologyBuilder:
    def __init__(self, log_duplicates=True):
        self._connection_map = {}
        self._log_duplicates = log_duplicates

    def register_connection(self, router_interface, subnet_prefix):
        subnet_connections = self._connection_map.get(subnet_prefix)
        if not subnet_connections:
            subnet_connections = set()
            self._connection_map[subnet_prefix] = subnet_connections
        if self._log_duplicates and router_interface in subnet_connections:
            print(f"Duplicate router interface {router_interface} for subnet {subnet_prefix}")
        subnet_connections.add(router_interface)

    def write_topology(self, writeable_object):
        for subnet_prefix in self._connection_map.keys():
            subnet_neighbors_str = "\t".join(f"{router_interface.router_name} {router_interface.interface_name}" for router_interface in self._connection_map[subnet_prefix])
            subnet_summary_str = f"{subnet_neighbors_str}\t{subnet_prefix}\n"
            writeable_object.write(subnet_summary_str)

            

