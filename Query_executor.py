from SPARQLWrapper import SPARQLWrapper, JSON
import string


class QueryExecutor:
    def __init__(self):
        self.ontologyBaseURI = 'http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/irishhistory/'
        self.endPoint = 'http://localhost:7200/repositories/KDE-project'

    def loading_default_data(self):

        sparql = SPARQLWrapper(self.endPoint)

        query = '''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
        select DISTINCT ?county ?name where {
	        ?county rdf:type ours:county .
                ?county ours:name ?name .
            }
        ORDER BY ASC(UCASE(str(?name)))
        '''

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        counties = sparql.query().convert()

        countyNames = [e['name']['value'] for e in counties['results']['bindings']]
        countyIRIs = [e['county']['value'] for e in counties['results']['bindings']]

        sparql = SPARQLWrapper(self.endPoint)
        query = '''
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
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

        query = '''      
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX gn: <http://www.geonames.org/ontology#>
            
            SELECT ?period ?name WHERE {
                ?period a ?timePeriod .
                ?period ours:name ?name
                FILTER(?timePeriod IN (ours:HistoricalPeriod, dbo:HistoricalPeriod))
            }
            ORDER BY ASC(UCASE(str(?name)))
            '''

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        historic_periods = sparql.query().convert()
        historic_period_names = [e['name']['value'] for e in towns['results']['bindings']]
        historic_period_IRIs = [e['town']['value'] for e in towns['results']['bindings']]

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

        sparql = SPARQLWrapper(self.endPoint)

        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
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
        print("results:", results)

        return results

    def query_2(self, entityType, location):
        FILTER = QueryExecutor().create_filter(entityType, 'POI')
        sparql = SPARQLWrapper(self.endPoint)
        output = {'max': '', 'min': ''}
        for pattern in ['DESC', 'ASC']:
            query = """           
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX gn: <http://www.geonames.org/ontology#>
                    
                    SELECT ?name (COUNT(?o) as ?count) WHERE {
                        ?t ours:containsLocation ?o .
                        ?t ours:name ?name .	
                        ?t a $LOCATION .
                        ?o a ?POI .
                        $FILTER
                    }
                    GROUP BY ?name
                    ORDER BY $PATTERN(?count)
                    LIMIT 1
    
                 """
            if location.lower() == 'county':
                LOCATION = 'ours:county'
            else:
                LOCATION = 'dbo:Town'
            query = string.Template(query).substitute(FILTER=FILTER, PATTERN=pattern, LOCATION=LOCATION)

            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print("results:", results)
            if pattern == 'DESC':
                output['max'] = results['results']['bindings'][0]['name']['value'], \
                                results['results']['bindings'][0]['count']['value']
            else:
                output['min'] = results['results']['bindings'][0]['name']['value'], \
                                results['results']['bindings'][0]['count']['value']
        print(output)
        return output
