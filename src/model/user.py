
import model
from model import Base

class User(model.StateObject):
    version = 1
    collection = 'user'
    tenant_aware = False
    default_state = 'disabled'
    states = {
        'inactive':{    'active':[
                    ]},
        'active':{    'inactive':[
                    ], 'deleted':[
                    ],  'locked':[
                    ]},
        'locked':{    'inactive':[
                    ], 'deleted':[
                    ],  'active':[
                    ]
                  },
        'deleted':{     'active':[
                    ], 'removed':[
                    ]}
    }
    def __init__(self):
        super(User, self).__init__()
        
    def validate(self):
        super(User, self).validate(self)
        
    def enable(self):
        self.change_state('active')
        self.save()
        