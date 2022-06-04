from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client


def get_index(index_name= 'tur_Article'):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query, **kwargs):
    params = {}
    if 'tags' in kwargs:
        tags = kwargs.pop('tags') or []
        if len(tags) != 0:
            params['tagFilters'] = tags

    index = get_index()
    result = index.search(query, params)
    return result