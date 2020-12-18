from rdflib import Graph, URIRef, Literal, Namespace
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST


cap = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/extension/cap#")


def connect():
    sparql = SPARQLWrapper("http://localhost:7200/repositories/cav-pilot")
    sparql.setHTTPAuth(DIGEST)
    sparql.setCredentials("anonymous", "public")
    sparql.setMethod(POST)
    return sparql


def drop(sparql):
    query = """DROP GRAPH <http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/extension/cap#>"""
    results = sparql.setQuery(query)
    print("DROP done" if not results else results.response.read())
    return


def insert(g, sparql, skip: bool = True):
    if skip:
        print("INSERT done")
        return

    triples = ""
    for subject, predicate, obj in g:
        triples = triples + subject.n3() + " " + predicate.n3() + " " + obj.n3() + " . \n"

    query = """
            WITH <http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/extension/cap#>
            INSERT {""" + triples + """}
            """

    results = sparql.setQuery(query)

    print("INSERT done" if not results else results.response.read())
    return


def run(g: Graph):
    sparql = connect()
    drop(sparql)
    insert(g, sparql, True)


if __name__ == "__main__":
    run()
