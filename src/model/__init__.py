from server.settings import MONGO_DB
import bson

def delete_by_id(id,tenant,basecollection):
    ''' Helper function to delete any object simply by ID. Note that this is 
    hard delete, and perhaps we may want to preserve all objects, since we will need history'''
    _id = bson.objectid.ObjectId(id)
    if(tenant): col = tenant+"."+basecollection
    else: col = basecollection 
    MONGO_DB[col].delete({'_id':_id})

class Base(object):
    def __init__(self,param):
        self._id = None
        self._version = None
        pass
    
    def delete(self,tenant=None):
        if(not self._id):
            raise ModelError("Can't delete transient object")
        MONGO_DB[self.collectionName(tenant)].delete({'_id':self._id})

    def save(self,tenant=None):
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
        data["_version"] = self.version
        if(self._id): 
            data["_id"] = self._id
        
        # Save the data into a collection
        self._id = MONGO_DB[self.collectionName(tenant)].save(data)
    
    def validate(self):
        pass
    
    def collectionName(self,tenant):
        # Different tenants will have different collections
        # This will enable us to have separate schema, index etc
        if(tenant): return tenant+"."+self.collection
        return self.collection        

class ModelError(Exception):
    def __init__(self,error):
        self.error = error
