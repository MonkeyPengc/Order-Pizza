
import sys
from modules.threaded_jsonserver import ThreadedServer
from modules.database import Customers, OrderInventory


class PizzaHubServer(ThreadedServer):
    """
    A threaded server connected to databases, and response
    to requests from clients via Json packages.
    """

    def __init__(self, hostname='127.0.0.1', port=1617):
        super(PizzaHubServer, self).__init__(hostname, port)
        self.customers_table = Customers()
        self.orders_table = OrderInventory()
    
    def processPackage(self, package):
        if package.get('customer_id') == -1:
            name, addr = package.get('customer_name'), package.get('customer_address')
            cid = self.customers_table.AllocateCustomerID(name, addr)
            package['customer_id'] = cid
            self.sendPackage(package)
        
        else:
            cid, price = package['customer_id'], package['order_price']
            self.orders_table.InsertOrder(cid, price)
            package['order_received'] = True
            self.sendPackage(package)


if __name__ == '__main__':

    app_server = PizzaHubServer()
    app_server.start()
    
    sys.exit(0)

