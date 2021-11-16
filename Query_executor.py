import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import string

class QueryExecutor:
    def __init__(self):
        self.ontologyBaseURI = 'http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/project-ontology/'
        self.endPoint = 'http://LAPTOP-45QEIGK2:7200/repositories/KDE-project'

    def loading_default_data(self):

        selectAllCountiesQuery = '''PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A
        PREFIX%20ours%3A%20%3Chttp%3A%2F%2Fwww.semanticweb.org%2Fashutoshbansal%2Fontologies%2F2021%2F10%2Fproject-ontology%3E%0A
        select DISTINCT ?name ?county where {
         	?county rdf:type ours:county .
            ?county ours:name ?name .
        }&Accept=application/sparql-results%2Bjson'''
        urlForSelectAllCounties = f'{self.endPoint}?query={selectAllCountiesQuery}'
        countyResponse = requests.request('GET', urlForSelectAllCounties)
        counties = countyResponse.json()
        countyNames = [e['name']['value'] for e in counties['results']['bindings']]
        countyIRIs = [e['county']['value'] for e in counties['results']['bindings']]

        selectAllTownsQuery = '''PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A
        PREFIX%20ours%3A%20%3Chttp%3A%2F%2Fwww.semanticweb.org%2Fashutoshbansal%2Fontologies%2F2021%2F10%2Fproject-ontology%3E%0A
        select DISTINCT ?name ?town where {
         	?town rdf:type ours:town .
            ?town ours:name ?name .
        }&Accept=application/sparql-results%2Bjson'''
        urlForSelectAllTowns = f'{self.endPoint}?query={selectAllTownsQuery}'
        townResponse = requests.request('GET', urlForSelectAllTowns)
        towns = townResponse.json()
        townNames = [e['name']['value'] for e in towns['results']['bindings']]
        townIRIs = [e['town']['value'] for e in towns['results']['bindings']]

        townsForDropdown = []
        for i in range(len(townNames)):
            townsForDropdown.append({'label': townNames[i], 'value': townIRIs[i]})

        countiesForDropdown = []
        for i in range(len(countyNames)):
            countiesForDropdown.append({'label': countyNames[i], 'value': countyIRIs[i]})

        return countiesForDropdown, townsForDropdown

    def getPointsOfInterestInPlace(self, entityType, location):
        listOfTypes = 'FILTER (?place IN ('
        numTypes = 0

        for t in entityType:
            if numTypes > 0:
                listOfTypes = listOfTypes + ','
            if t == 'Pilgrim Path':
                listOfTypes = listOfTypes + 'ours:pilgrimPath'
            elif t == 'Walled Towns':
                listOfTypes = listOfTypes + ' ours:walledTown'
            elif t == 'Museum':
                listOfTypes = listOfTypes + 'dbo:Museum'
            elif t == 'Landmarks':
                listOfTypes = listOfTypes + ' ours:landmark'
            numTypes = numTypes + 1

        listOfTypes = listOfTypes + '))'

        sparql = SPARQLWrapper("http://LAPTOP-45QEIGK2:7200/repositories/KDE-project")
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/project-ontology>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            select ?name WHERE {
                ?s rdf:type ?place .
                ?s ours:name ?name .
                ?s ours:locatedIn <$LOCATION> .
                $FILTER
            }
            ORDER BY ASC(UCASE(str(?name)))
        """
        query = string.Template(query).substitute(LOCATION=location, FILTER=listOfTypes)
        # sparql.setQuery("""
        #        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        # PREFIX ours: <http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/project-ontology>
        # SELECT ?name WHERE {
        #     ?s rdf:type ?o .
        #     ?s ours:name ?name .
        #     ?s ours:locatedIn <http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/project-ontology#countyKerry> .
        #     FILTER(?o IN (ours:pilgrimPath, ours:walledTown, ours:landmark))
        # }
        # ORDER BY ASC(UCASE(str(?name)))
        #     """)
        sparql.setQuery(
        """
        
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/project-ontology>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            select ?name WHERE {
                ?s rdf:type ?place .
                ?s ours:name ?name .
                ?s ours:locatedIn <http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/project-ontology/#countyKerry> .
                FILTER (?place IN (ours:pilgrimPath, ours:walledTown, ours:landmark))
            }
            ORDER BY ASC(UCASE(str(?name)))
        """)
        # sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        print(results)





        selectPointsOfInterestQuery = '''PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A
        PREFIX%20ours%3A%20%3Chttp%3A%2F%2Fwww.semanticweb.org%2Fashutoshbansal%2Fontologies%2F2021%2F10%2Fproject-ontology%3E%0A
        select DISTINCT ?name ?place where {
            ?place ours:name ?name .
            ?place ours:locatedIn <$LOCATION> .
            $FILTER
        }&Accept=application/sparql-results%2Bjson'''
        query = string.Template(selectPointsOfInterestQuery).substitute(LOCATION=location, FILTER=listOfTypes)
        urlForSelectPOI = f'{self.endPoint}?query={query}'
        POIresponse = requests.request('GET', urlForSelectPOI)
        POIs = POIresponse.json()
        poiNames = [e['name']['value'] for e in POIs['results']['bindings']]
        poiIRIs = [e['town']['value'] for e in POIs['results']['bindings']]

        # townsForDropdown = []
        # for i in range(len(townNames)):
        #    townsForDropdown.append({'label': townNames[i], 'value' : townIRIs[i]});
        return np.column_stack((poiNames, poiIRIs))




