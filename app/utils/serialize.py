from bson import ObjectId

def serialize_mongo(doc: dict) -> dict:
    if not doc:
        return doc
    
    doc = doc.copy()
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['id'] = str(doc['_id'])
    
    return doc