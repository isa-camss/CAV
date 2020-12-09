import pandas as pd
import hashlib
from rdflib import URIRef, Literal
from rdflib import Namespace, Graph
from rdflib.namespace import RDF as rdf, RDFS as rdfs, SKOS as skos, XSD as xsd, OWL as owl, DCTERMS as dct, \
    FOAF as foaf
import uuid

cap = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/extension/cap#")
cav = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c#")
epo = Namespace("http://data.europa.eu/a4g/ontology#")
cccev = Namespace("https://data.europe.eu/semanticassets/ns/cv/cccev_v2.0.0#")
roles = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/resource/role-type#")
cv = Namespace("http://data.europa.eu/m8g#")

C1 = 'Unnamed: 0'
C2 = 'Unnamed: 1'


def extract(x: str, t: str):
    """
    Creates a pandas data frame with the indicated tab of the indicated excel file
    :param x: the Excel file
    :param t: the tab
    :return: the pandas data frame
    """
    e = pd.ExcelFile(x).parse(t)
    e.drop(e.index[26:], axis='rows', inplace=True)
    e.drop(e.index[0:3], axis='rows', inplace=True)
    return e


def dimension(g, t) -> (Graph, URIRef):
    uri = URIRef(cap + 'criterion-dimension-' + str(hashlib.md5(str(t[C1]).encode('utf-8')).hexdigest()))
    g.add((uri, rdf.type, owl.NamedIndividual))
    g.add((uri, rdf.type, epo.AwardCriterion))
    g.add((uri, cap.hasMaximumScore, Literal(str(t[C2]))))
    g.add((uri, cap.hasMinimumScore, Literal(1)))
    g.add((uri, cccev.hasName, Literal(str(t[C1]).strip(), lang='en')))
    return g, uri


def criterion(g, t, d) -> (Graph, URIRef, str):
    """
    Instantiates a Criterion
    :param g: the graph where the criterion is added
    :param t: the pandas data
    :param d: the parent dimension
    :return: the graph and the criterion URI
    """
    # hcn -> the hashed name of the criterion. It's later on used, too, to lookup for a criterion
    hcn = str(hashlib.md5(str(t[C1]).encode('utf-8')).hexdigest())
    uri = URIRef(cap + 'criterion-' + hcn)
    g.add((uri, rdf.type, owl.NamedIndividual))
    g.add((uri, rdf.type, epo.AwardCriterion))
    g.add((uri, cap.hasMaximumScore, Literal(str(t[C2]))))
    g.add((uri, cap.hasMinimumScore, Literal(1)))
    g.add((uri, cccev.hasName, Literal(str(t[C1]).strip(), lang='en')))
    g.add((d, cap.hasChild, uri))
    g.add((uri, cap.hasParent, d))
    return g, uri, hcn


def transform(g, e) -> (Graph, []):
    """
    Populates the graph with instances of criterion dimensions and criteria
    :param g: the graph to populate
    :param e: the dataset inside a pandas data frame
    :return: the graph and the criteria in a vector
    """
    cl = {}   # criteria list
    d = None  # URIRef of a parent dimension

    for n, v in e.iterrows():
        t = v.T
        if str(t[C1]).lower().find("dimension") != -1:
            g, d = dimension(g, t)
        else:
            g, c, hcn = criterion(g, t, d)
            # Add the criterion to a dictionary where the key is the hashed name of the criterion,
            # as taken from the Excel file.
            cl[hcn] = c

    return g, cl



