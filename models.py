import copy


class FieldType():

    def __init__(self,type) -> None:
        self.type = type

    def setValue(self, value):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def validation(self):
        pass


class LongField(FieldType):

    def __init__(self) -> None:
        super().__init__("long")

class IntegerField(FieldType):

    def __init__(self) -> None:
        super().__init__("integer")


class ShortField(FieldType):
    def __init__(self) -> None:
        super().__init__("short")


class TextField(FieldType):
    def __init__(self) -> None:
        super().__init__("text")



class Model():
    
    def __init__(self,_index,_type = None, _type_field = None) -> None:
        self._index = _index

        if _type != None: 
            self._type = _type 
        else:
            self._type = self.__name__

        self._type_field = _type_field

        self._exeptions = ["_type", "_index", "_type_field", "_exeptions"]


    def getAll(self, clienteDB,_size = 10000, **kwargs):

        body = {
            "size" : _size,
            "query" : {
                "bool" : {
                    "must" : [
                        
                    ]
                }
            }
        }

        if self._type_field != "_default":
            body["query"]["bool"]["must"].append({"term" : { self._type_field : self._type  } })

        else:
            body["query"]["bool"]["must"].append({"term" : { "_type" : self._type  } })


        
        for filter in kwargs.keys():
            body["query"]["bool"]["must"].append({"term" : {  filter : kwargs[filter] } })

    

        data = clienteDB.search(
            index = self._index,
            body = body
        )

        list_objects = []
        for hit in data["hits"]["hits"]:

            _object = copy.deepcopy(self)

            for field in _object.__dict__:

                if not field in _object._exeptions:
                    _object.__dict__[field].setValue(hit["_source"].get(field,None))
                
            _object.metadata = { "_id" : hit["_id"], "_index" : hit["_index"] }

            list_objects.append(_object)
            
        return list_objects
        




