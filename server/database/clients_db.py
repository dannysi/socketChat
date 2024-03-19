
class ClientsDB(object):
    clients = {}

    def add(self, socket, user):
        self.clients[socket] = user

    def get_all_clients(self):
        return self.clients

    def remove(self, socket):
        del self.clients[socket]

    def get(self, socket):
        return self.clients[socket]

    def __len__(self):
        return len(self.clients)