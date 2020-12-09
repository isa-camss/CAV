import math
import pandas as pd
import hashlib
import uuid
from rdflib import URIRef, Literal
from rdflib import Namespace, Graph
from rdflib.namespace import RDF as rdf, RDFS as rdfs, SKOS as skos, XSD as xsd, OWL as owl, DCTERMS as dct, \
    FOAF as foaf
import criteria as c

cap = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/extension/cap#")
cav = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c#")
epo = Namespace("http://data.europa.eu/a4g/ontology#")
cccev = Namespace("https://data.europe.eu/semanticassets/ns/cv/cccev_v2.0.0#")
roles = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/resource/role-type#")
cv = Namespace("http://data.europa.eu/m8g#")
ct = Namespace("http://data.europa.eu/w21/2c930c7b-5e2f-4954-8522-bd3411339d6c/resource/criterion-type#")

EXCEL_FILE = 'evaluation-tool.xlsm'
DATA_TAB = 'REPORTS PER EVALUATOR'
CRITERIA_TAB = 'MAIN REPORT'


def graph() -> Graph:
    g = Graph()
    g.namespace_manager.bind('base', URIRef(cap))
    g.bind('skos', skos)
    g.bind('cap', cap)
    g.bind('cav', cav)
    g.bind('epo', epo)
    g.bind('cccev', cccev)
    g.bind('owl', owl)
    g.bind('foaf', foaf)
    g.bind('roles', roles)
    g.bind('cv', cv)
    g.bind('ct', ct)
    return g


def concept(g: Graph, _id: str, label: Literal, parent: URIRef, concept_scheme: URIRef) -> URIRef:
    uri = URIRef(roles + _id)
    g.add((uri, rdf.type, skos.Concept))
    g.add((uri, skos.broader, parent))
    g.add((uri, skos.prefLabel, label))
    return uri


def person(g, given_name, family_name) -> URIRef:
    p = given_name.lower().strip() + "-" + family_name.lower().strip()
    p = str(hashlib.md5(str(p).encode('utf-8')).hexdigest())
    p = URIRef(cap + 'agent-' + p)
    g.add((p, rdf.type, foaf.Person))
    g.add((p, rdf.type, owl.NamedIndividual))
    g.add((p, foaf.givenName, Literal(given_name, lang='en')))
    g.add((p, foaf.familyName, Literal(family_name, lang='en')))
    return p


def evaluators(g) -> []:
    """
    Instantiates three agent-persons
    :param g: the graph
    :return: a vector with the three URI of the persons
    """
    pa = [person(g, 'Bob', 'Mc Alister'), person(g, 'Alice', 'Mauricius'), person(g, 'Martha', 'Casanova')]
    return pa


def value(v) -> (str, int):

    if type(v) == float and math.isnan(v):
        return 'aSa', 0            # No comparison (A=A .. L=L)

    if type(v) == str and len(v) == 1:
        if v.strip() == '':
            return '', 0

    elif type(v) == str and len(v) == 2:           # S+ or S-
        return v[0], v[1]

    elif type(v) == int:
        return 'even', str(v)   # S= even match


def reify(g, agent, winner, weight, source, target, role, criterion) -> Graph:
    """
    Description: creates an instance of the reification with...
    :param g: the graph containing the reification individual
    :param agent: the person-agent evaluating
    :param winner: the letter identifying the winner tender-lot
    :param weight: the numeric value provided by the evaluator
    :param source: the source action (a)
    :param target: the target action (a')
    :param role: the role of the agent (evaluator)
    :param criterion: the criterion evaluated
    :return: the graph
    """
    iv = URIRef(cap + "input-value-" + str(uuid.uuid4()))

    g.add((iv, rdf.type, owl.NamedIndividual))
    g.add((iv, rdf.type, cap.InputValue))
    g.add((iv, cv.role, role))
    g.add((iv, cap.comparesSourceThing, Literal(source)))
    g.add((iv, cap.comparesWithTargetThing, Literal(target)))
    g.add((iv, cap.hasBetterCandidate, Literal(winner)))
    g.add((iv, cap.isProvidedBy, agent))
    g.add((iv, cap.refersToCriterion, criterion))
    g.add((iv, cap.hasNumericValue, Literal(weight, datatype=xsd.integer)))

    return g


def not_e_column(t) -> bool:
    """
    Used to skip Columns E1, E2, E3
    :param t: the text in that column, 'A', 'B', ... 'L'
    :return: whether the column is an Evaluator Column or not
    """
    if (type(t) == float and math.isnan(t)) or type(t) == int:
        return True

    if t.isalpha() and len(t) == 1:
        n = ord(t.upper())
        if 65 <= n <= 90:
            return False

    return True


def data(g, t, p, tl, source, role, criterion) -> Graph:
    """
    For this simulation we do not waste time calculating automatically how many tenderers participate nor how many
    criteria or evaluators intervene. These parameters are set to constants: 3 evaluators, 10 TenderLots, 11 Quality
    Critera and 2 Economic Criteria.
    :param g: the graph
    :param t: the vector in the pandas data frame containing the values associated to the letter identifying the tender-lot
    :param p: the evaluators, person-agents (the role is always the same: 'evaluator')
    :param tl: the list of tender-lots associated to its action letter
    :param source: the source action (a)
    :param role: the role of the agent (evaluator)
    :param criterion: the criterion evaluated
    :return: the graph once effected
    """
    lt = len(t)
    for i in range(lt):
        evaluator_modulo = i % 3      # States who, out of three evaluators, is the current evaluator
        action_modulo = i % 10        # States the letter of the target tender-lot. Zero == columns E1, E2 and E3
        if action_modulo != 0 and not_e_column(t[i]):  # Skip En evaluator columns
            winner, weight = value(t[i])  # Letter and number
            # If weight equals zero -> the source the value is NaN, therefore target and source are the same
            # The columns C8 and E1 introduce an offset of 2 in the modulo calculation thus the subtraction
            target = source if weight == 0 else tl[action_modulo-2][0]
            # Evaluator 1 is in position 0 of the array, of course, thus the subtraction due to columns C8 and E1
            reify(g, p[evaluator_modulo-2], winner, weight, source, target, role, criterion)
    return g


def get_criterion(g, i, m) -> (Graph, URIRef):
    # Static count, in this example we have 11 criteria quality criteria and 2 price criteria
    # Each criterion amounts to 10 comparisons (of ten tender-lots, represented by a letter [A, L]
    # return g, uri
    return g


def nan(v) -> bool:
    c8 = v.T['C8']
    if type(c8) == float and math.isnan(c8):
        return True
    return False


def transform(e, g, tl, role, criteria) -> Graph:
    """
    Generates the reification sub-graph
    :param e: the pandas data frame
    :param g: the graph being constructed
    :param tl: the tender-lot individuals associated to a letter range ['A', 'L']
    :param role: the role of the agent (evaluator)
    :param criteria: the dictionary with the name of the criteria as a key and the criteria as URIRefs
    :return: the reification added to the graph
    """
    # Each 12 rows you get the Criterion
    p = evaluators(g)
    for n, v in e.iterrows():
        # Skip rows that do not contain criteria and values (e.g. separators between criteria)
        if not nan(v):
            # Source is the letter representing the tender-lot that is being compared with the rest of tender-lots:
            # its the a of the a S a' in the ELECTRE method.
            # Given the horizontal ordering of the evaluators in the IT-excel-method file, E1, E2 and E3 columns
            # indicate always the same letter.
            source = v.T['E1']
            hcn = str(hashlib.md5(str(v.T['C8']).strip().encode('utf-8')).hexdigest())
            criterion = criteria[hcn]
            data(g, v.T, p, tl, source, role, criterion)

    return g


def extract(x: str, t: str):
    e = pd.ExcelFile(x).parse(t)
    # e.drop(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'], axis='columns', inplace=True)
    e.drop(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C9', 'C10'], axis='columns', inplace=True)
    e.drop(e.index[0:4], axis='rows', inplace=True)
    return e


def show_save(t, save: bool = False):
    content = t.serialize(format="turtle").decode("utf-8")
    print(content)
    if save:
        t.serialize(format="turtle", destination='./a-box.ttl')
    return None


def build_roles(g: Graph) -> (Graph, URIRef):
    r = concept(g, 'evaluator', Literal('Evaluator', lang='en'), roles.Role, roles)  # Punning!
    return g, r


def lot(g: Graph) -> Graph:
    """
    Creates one instance of one Lot, Lot1. This exercise simulates a procedue with only one lot
    :param g:
    :return:
    """
    g.add((URIRef(cap + 'Lot1'), rdf.type, owl.NamedIndividual))
    g.add((URIRef(cap + 'Lot1'), rdf.type, epo.Lot1))
    return g


def lots_tendered(g: Graph) -> (Graph, []):
    """
    Instantiates 10 'Tender Lots'. Each Lot is submitted by a different tenderer (participant)
    :param g: the graph to which the instances are added to
    :return: the graph effected and a vector of pairs, tender-lot id and tender-lot individual
    """
    tls = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L']
    tlp = []
    for i in range(len(tls)):
        s = URIRef(cap + tls[i] + '-tender-lot-' + str(uuid.uuid4()))
        g.add((s, rdf.type, owl.NamedIndividual))
        g.add((s, rdf.type, epo.TenderLot))
        g.add((s, epo.relatesTo, epo.Lot1))
        tlp.append((tls[i], s))
    return g, tlp


def instantiate_criteria(g, x, t) -> (Graph, []):
    criteria = []
    e = c.extract(x, t)
    g, criteria = c.transform(g, e)
    return g, criteria


def run() -> Graph:
    g = graph()  # Creates the graph of the ABox
    g, criteria = instantiate_criteria(g, EXCEL_FILE, CRITERIA_TAB)
    e = extract(EXCEL_FILE, DATA_TAB)           # Creates a pandas data frame from the Excel dataset
    g, r = build_roles(g)                       # Instantiates the role 'evaluator'
    g, tl = lots_tendered(g)                    # Instantiates TenderLots 'A' to 'L'
    g = transform(e, g, tl, r, criteria)        # Populates the graph
    return g
