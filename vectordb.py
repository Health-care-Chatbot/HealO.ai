from langchain_community.vectorstores import Chroma


def empty_vectordb(vector_db: Chroma) -> None:
    """
    Empties the vector database by deleting all the vectors stored in it.

    Args:
        vector_db (Chroma): The vector database object.

    Returns:
        None
    """
    ids = vector_db.get()["ids"]
    if len(ids) > 0:
        vector_db._collection.delete(ids=ids)

def is_vectordb_empty(vector_db: Chroma) -> bool:
    """
    Check if the VectorDB is empty.

    Parameters:
    vector_db: The vector database instance to check.

    Returns:
    bool: True if the vector database is empty, False otherwise.
    """
    documents = vector_db.get()["documents"]
    return len(documents) == 0

