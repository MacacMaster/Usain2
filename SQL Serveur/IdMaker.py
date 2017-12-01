
class IdMaker():
    id=0
    def prochainid():
        IdMaker.id+=1
        str_id="id_"+str(IdMaker.id)
        return str_id 
