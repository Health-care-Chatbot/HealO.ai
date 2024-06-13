def empty_vectordb(vectordb):
    ids = vectordb.get()["ids"]
    vectordb._collection.delete(ids=ids)

def is_vectordb_empty(vectordb):
    documents = vectordb.get()["documents"]
    return len(documents) == 0

