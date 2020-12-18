from SPARQLWrapper import SPARQLWrapper, POST, DIGEST
import matplotlib.pyplot as plt
import numpy as np


# %matplotlib inline

def _connect():
    sparql = SPARQLWrapper("http://192.168.1.46:7200/repositories/cav-pilot")
    sparql.setHTTPAuth(DIGEST)
    sparql.setCredentials("anonymous", "public")
    sparql.setMethod(POST)
    return sparql


def _query(sparql):
    sparql.setQuery("""
                        # User Story: I, as the algorithm calculating and ranking which is the winner of Lot1 of the procurement procedure X, want to get all input values introduced by all evaluators for this procedure's lot and concerning exclusively 'Qualitative Subjective Criteria', so I can assess the deviations between the evaluators' decisions. 
                        # Competency Question: Retrieve all the input values assigned by all evaluators to 'Qualitative Subjective Criteria', as well as the information related to the input value.
                        PREFIX cap: <http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/extension/cap#>
                        PREFIX owl: <http://www.w3.org/2002/07/owl#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX cccev: <https://data.europe.eu/semanticassets/ns/cv/cccev_v2.0.0#>
                        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        PREFIX ct: <http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/resource/criterion-type#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        SELECT 	?input (concat(?givenName, " ", ?familyName) as ?agent) ?source ?target ?winner ?value (str(?crit) as ?criterion) (str(?cObj) as ?cid) 
                                ?maxscore ?note
                        FROM cap:
                        WHERE {
                            ?input rdf:type cap:InputValue ;
                               cap:comparesSourceThing ?source ;
                               cap:comparesWithTargetThing ?target ;
                               cap:hasBetterCandidate ?winner ;
                               cap:hasNumericValue ?value ;
                               cap:isProvidedBy ?agentObj;
                               cap:refersToCriterion ?cObj .
                            ?cObj cccev:hasName ?crit ; 
                                       cap:hasMaximumScore ?maxscore ;
                                       skos:scopeNote ?note .
                            ?agentObj foaf:givenName ?givenName ;
                                      foaf:familyName ?familyName .
                                
                            FILTER EXISTS {?cObj cccev:hasType ct:qs}
                            FILTER (?source != ?target && ?value != 0)
                            
                        } ORDER BY ?agent


        """)
    sparql.setReturnFormat(format="json")
    results = sparql.query().convert()
    return results


def run():
    sparql = _connect()
    return _query(sparql)


if __name__ == "__main__":
    run()
