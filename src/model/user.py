
import model

class User(model.Base):
    version = 1
    collection = 'user'
    tenant_aware = False
    def __init__(self):
        super(User, self).__init__()