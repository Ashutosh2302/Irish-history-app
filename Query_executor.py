import requests
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import string
import json


class QueryExecutor:
    def __init__(self):
        self.ontologyBaseURI = 'http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/irishhistory/'
        self.endPoint = 'http://LAPTOP-45QEIGK2:7200/repositories/KDE-project'




    def loading_default_data(self):

        sparql = SPARQLWrapper("http://LAPTOP-45QEIGK2:7200/repositories/KDE-project")

        #
        query = '''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
        select DISTINCT ?county ?name where {
	        ?county rdf:type ours:county .
                ?county ours:name ?name .
            }
        ORDER BY ASC(UCASE(str(?name)))
        '''

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        counties = sparql.query().convert()

        # urlForSelectAllCounties = f'{self.endPoint}?query={selectAllCountiesQuery}'
        # countyResponse = requests.request('GET', urlForSelectAllCounties)
        # counties = countyResponse.json()
        countyNames = [e['name']['value'] for e in counties['results']['bindings']]
        countyIRIs = [e['county']['value'] for e in counties['results']['bindings']]
        # countyIRIs = [e[0: e.rfind('/'):] + e[e.rfind('/') + 1::] for e in countyIRIs]

        # selectAllTownsQuery = '''PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A
        # PREFIX%20ours%3A%20%3Chttp%3A%2F%2Fwww.semanticweb.org%2Fashutoshbansal%2Fontologies%2F2021%2F10%2Firishhistory%3E%0A
        # select DISTINCT ?name ?town where {
        #  	?town rdf:type ours:town .
        #     ?town ours:name ?name .
        # }&Accept=application/sparql-results%2Bjson'''
        # urlForSelectAllTowns = f'{self.endPoint}?query={selectAllTownsQuery}'
        # townResponse = requests.request('GET', urlForSelectAllTowns)
        # towns = townResponse.json()

        sparql = SPARQLWrapper("http://LAPTOP-45QEIGK2:7200/repositories/KDE-project")
        query = '''
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                select DISTINCT ?name ?town where { 
	                ?town rdf:type dbo:Town .
                    ?town ours:name ?name .
                }
                ORDER BY ASC(UCASE(str(?name)))

                '''

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        towns = sparql.query().convert()
        townNames = [e['name']['value'] for e in towns['results']['bindings']]
        townIRIs = [e['town']['value'] for e in towns['results']['bindings']]
        # townIRIs = [e[0: e.rfind('/'):] + e[e.rfind('/') + 1::] for e in townIRIs]

        townsForDropdown = []
        for i in range(len(townNames)):
            townsForDropdown.append({'label': townNames[i], 'value': townIRIs[i]})

        countiesForDropdown = []
        for i in range(len(countyNames)):
            countiesForDropdown.append({'label': countyNames[i], 'value': countyIRIs[i]})

        return countiesForDropdown, townsForDropdown

    @staticmethod
    def create_filter(entityType, varibale):
        listOfTypes = f'FILTER (?{varibale} IN ('
        numTypes = 0

        for t in entityType:
            if numTypes > 0:
                listOfTypes = listOfTypes + ','
            if t == 'Pilgrim Path':
                listOfTypes = listOfTypes + 'ours:pilgrimPath'
            elif t == 'Walled Towns':
                listOfTypes = listOfTypes + 'ours:walledTown'
            elif t == 'Museum':
                listOfTypes = listOfTypes + 'dbo:Museum'
            elif t == 'Landmarks':
                listOfTypes = listOfTypes + 'ours:landmark'
            numTypes = numTypes + 1

        listOfTypes = listOfTypes + '))'
        return listOfTypes

    def query_1(self, entityType, location):
        FILTER = QueryExecutor().create_filter(entityType, 'thing')

        sparql = SPARQLWrapper("http://LAPTOP-45QEIGK2:7200/repositories/KDE-project")

        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX gn: <http://www.geonames.org/ontology#>

            SELECT *  WHERE {
                ?place a ?thing .
                ?place ours:name ?name .
                ?place ours:locatedIn <$LOCATION>

                $FILTER
            }
            ORDER BY ASC(UCASE(str(?name)))
        """
        query = string.Template(query).substitute(
            LOCATION=location,
            FILTER=FILTER)

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
        print("results:", results)
