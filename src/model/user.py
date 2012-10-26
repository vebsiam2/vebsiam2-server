import model

class User(model.StateObject):
    version = 1
    collection = 'user'
    tenant_aware = False
    default_state = 'inactive'
    states = {
        'transitions': {
            'inactive':{ 'active' },
            'active'  :{ 'inactive', 'deleted','locked' },
            'locked'  :{ 'inactive', 'deleted','active' },
            'deleted' :{ 'active', 'removed' }
        },
        'operations': {
            'enable' : {'from':{'inactive'}, 'to':'active'},
            'disable': {'from':{'locked','active'}, 'to':'inactive'},
            'delete' : {'from':{'locked','active','inactive'}, 'to':'deleted'},
            'undelete': {'from':{'deleted'}, 'to':'active'},
            'lock': {'from':{'active'}, 'to':'locked'},
            'unlock': {'from':{'locked'}, 'to':'active'},
        }
    }
    def __init__(self):
        super(User, self).__init__()
        
    def validate(self):
        super(User, self).validate()
