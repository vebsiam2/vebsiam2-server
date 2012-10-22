from server.settings import MONGO_DB
import bson
import threading

def delete_by_id(id, tenant, basecollection):
    ''' Helper function to delete any object simply by ID. Note that this is 
    hard delete, and perhaps we may want to preserve all objects, since we will need history'''
    _id = bson.objectid.ObjectId(id)
    if(tenant): col = tenant + "." + basecollection
    else: col = basecollection 
    MONGO_DB[col].delete({'_id':_id})

class Base(object):
    def __init__(self):
        self._id = None
        self._version = None
    
    @classmethod
    def find_by_id(cls, objid, type_coerce=False):
        bsonid = bson.objectid.ObjectId(objid)
        data = MONGO_DB[cls.collectionName()].find_one({'_id':bsonid})
        return cls.construct_from_data(data, type_coerce)
    
    @classmethod
    def construct_from_data(cls,data,type_coerce=False):
        if(not data): return None
        
        if(data["_type"]!=cls.__name__):
            # FUTURE NOTE: Potentially look for hierarchy and accept
            raise ModelError("Invalid type being loaded")
        
        o = cls() # This might change if we accept hierarchy to reflect the class from data
        o._id = data.pop('_id')
        
        # Check the data version and call upgrade
        if(data["_version"]!=cls.version):
            cls.upgrade(data)
        o._version = data.pop("_version")
        o.__dict__.update(data["object"])
        
        return o
    
    @classmethod
    def find_by_unique_field(cls, field, value, type_coerce=False):
        data = MONGO_DB[cls.collectionName()].find_one({'object.'+str(field):value})
        return cls.construct_from_data(data,type_coerce)
        
    
    def delete(self):
        ''' Hard deletes the object from repository.  We might not really want this'''
        if(not self._id):
            raise ModelError("Can't delete transient object")
        MONGO_DB[Base.collectionName(self.__class__)].delete({'_id':self._id})
        

    def save(self, tenant=None):
        self.validate()
        if(not self._id): self._version = self.version
        if(self._version != self.version):
            raise ModelError("Version must be upgraded before saving")
        if(self.tenant_aware and not tenant):
            raise ModelError("Class is tenant aware, but it is not supplied")
            
        # Get the data and remove ID
        data = {}
        data["object"] = self.__dict__.copy()
        data["object"].pop('_id', None)
        data["_type"] = self.__class__.__name__
        data["_version"] = data["object"].pop("_version", self.version)
        if(self._id): 
            data["_id"] = self._id
        
        # Save the data into a collection
        self._id = MONGO_DB[self.collectionName()].save(data)
    
    def validate(self):
        pass
    
    @classmethod
    def collectionName(cls):
        # Get the tenant from threading definition
        # All workers must set the tenant name
        # vebsiam middleware sets the tenant name 
        tenant = threading.local().__dict__.get('tenant',None)
        if(cls.tenant_aware and not tenant):
            raise ModelError("Tenant is mandatory when model class is tenant aware: " + cls.__name__)
        if(cls.tenant_aware): 
            return tenant + "." + cls.collection
        return cls.collection

class StateObject(Base):
    def __init__(self):
        super(StateObject, self).__init__()
        self._state = self.default_state

    def change_state(self, newstate):
        try:
            self._state = self.states[self._state][newstate]
        except KeyError:
            raise ModelError(str.format("Transition to {1} not allowed from {0}", newstate, self._state))

class ModelError(Exception):
    def __init__(self, error):
        self.error = error
