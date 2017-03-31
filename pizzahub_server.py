
import sys
from modules.threaded_jsonserver import ThreadedServer
from modules.sales import SalesDB


class PizzaHubServer(ThreadedServer):
    """
    A threaded server connected to the order inventory database, 
    response to requests from clients.
    """

    def __init__(self, hostname='127.0.0.1', port=1617):
        super(PizzaHubServer, self).__init__(hostname, port)
        self.inventory = SalesDB()  ## initialize an order inventory database if not exist
    
    def processPackage(self, package):
        if package.get('customer_id') == -1:
            id = self.inventory.AllocateCustomerID()
            package['customer_id'] = id
            self.sendPackage(package)
        
        else:
            self.inventory.InsertOrder(package['customer_id'], package['order_price'])
            package['order_received'] = True
            self.sendPackage(package)


if __name__ == '__main__':

    app_server = PizzaHubServer()
    app_server.start()
    
    sys.exit(0)

