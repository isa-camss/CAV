import sparql as s
import electre as e


def run():
    r = s.run()           # Returns the results of the SPARQL query as a JSON
    return e.run(r)       # Applies the ELECTRE-II algorithm and produces the scores for each criterion

