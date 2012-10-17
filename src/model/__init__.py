from server.settings import MONGO_DB

class Base(object):
    def __init__(self):
        self._id = None
        self._version = None
        pass
    
    def delete(self):
        pass

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
            
        # Different tenants will have different collections
        # This will enable us to have separate schema, index etc
        if(tenant): 
            collectionName = tenant+"."+self.collection
        else: collectionName = self.collection
        
        # Save the data into a collection
        self._id = MONGO_DB[collectionName].save(data)
    
    def validate(self):
        pass

class ModelError:
    def __init__(self,error):
        self.error = error
