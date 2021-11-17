from SPARQLWrapper import SPARQLWrapper, JSON
import string


class QueryExecutor:
    
    def __init__(self):
        self.ontologyBaseURI = 'http://www.semanticweb.org/ontology/irishhistory'
        self.endPoint = 'http://localhost:7200/repositories/KDE-project'

    def loading_default_data(self):

        sparql = SPARQLWrapper(self.endPoint)

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

        countyNames = [e['name']['value'] for e in counties['results']['bindings']]
        countyIRIs = [e['county']['value'] for e in counties['results']['bindings']]

        sparql = SPARQLWrapper(self.endPoint)
        query = '''
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                select DISTINCT ?name ?town where { 
	                ?town rdf:type ours:locality .
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
        
        sparql = SPARQLWrapper("http://localhost:7200/repositories/KDE-project")
        query = '''
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX gn: <http://www.geonames.org/ontology#>

                SELECT ?museum ?name WHERE {
                    ?museum a dbo:Museum .
                    ?museum dbo:name ?name .
                    }
                ORDER BY ASC(UCASE(str(?name)))
                '''
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        museums = sparql.query().convert()
        museumNames = [e['name']['value'] for e in museums['results']['bindings']]
        museumIRIs = [e['museum']['value'] for e in museums['results']['bindings']]
        
        sparql = SPARQLWrapper("http://localhost:7200/repositories/KDE-project")
        query = '''
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX gn: <http://www.geonames.org/ontology#>

                SELECT ?landmark ?name WHERE {
                    ?landmark a ours:landmark .
                    ?landmark ours:name ?name .
                    }
                ORDER BY ASC(UCASE(str(?name)))
                '''
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        landmarks = sparql.query().convert()
        landmarkNames = [e['name']['value'] for e in landmarks['results']['bindings']]
        landmarkIRIs = [e['landmark']['value'] for e in landmarks['results']['bindings']]

        sparql = SPARQLWrapper("http://localhost:7200/repositories/KDE-project")
        query = '''
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX gn: <http://www.geonames.org/ontology#>

                SELECT ?walledTown ?name WHERE {
                    ?walledTown a ours:walledTown .
                    ?walledTown ours:name ?name .
                    }
                ORDER BY ASC(UCASE(str(?name)))
                '''
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        walledTowns = sparql.query().convert()
        walledTownNames = [e['name']['value'] for e in walledTowns['results']['bindings']]
        walledTownIRIs = [e['walledTown']['value'] for e in walledTowns['results']['bindings']]
        
        sparql = SPARQLWrapper("http://localhost:7200/repositories/KDE-project")
        query = '''
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX gn: <http://www.geonames.org/ontology#>

               SELECT ?pilgrimPath ?name WHERE {
                   ?pilgrimPath a ours:pilgrimPath .
                   ?pilgrimPath ours:name ?name .
                   }
                ORDER BY ASC(UCASE(str(?name)))
                '''
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        pilgrimPaths = sparql.query().convert()
        pilgrimPathNames = [e['name']['value'] for e in pilgrimPaths['results']['bindings']]
        pilgrimPathIRIs = [e['pilgrimPath']['value'] for e in pilgrimPaths['results']['bindings']]

        query = '''      
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX gn: <http://www.geonames.org/ontology#>
            
            SELECT DISTINCT ?period ?name WHERE {
            ?period a ?timePeriod .
            ?period dbo:name ?name
            FILTER(?timePeriod IN (ours:HistoricalPeriod, dbo:HistoricalPeriod))
            }
            ORDER BY ASC(UCASE(str(?name)))
            '''

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        historic_periods = sparql.query().convert()
        historic_period_names = [e['name']['value'] for e in historic_periods['results']['bindings']]
        historic_period_IRIs = [e['period']['value'] for e in historic_periods['results']['bindings']]

        query = '''      
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX gn: <http://www.geonames.org/ontology#>
            
            SELECT DISTINCT ?century ?name WHERE {
            ?century a ?centuryType .
            ?century dbo:name ?name
            FILTER(?centuryType IN (ours:historicCentury))
            }
            ORDER BY ASC(UCASE(str(?name)))
            '''

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        historicCenturies = sparql.query().convert()
        historicCenturyNames = [e['name']['value'] for e in historicCenturies['results']['bindings']]
        historicCenturyIRIs = [e['century']['value'] for e in historicCenturies['results']['bindings']]

        query = '''      
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX gn: <http://www.geonames.org/ontology#>
            
           SELECT DISTINCT ?year ?name WHERE {
            ?year a dbo:Year .
 	        #?year dbo:name ?name   
            }
            ORDER BY ASC(UCASE(str(?name)))
            '''

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        years = sparql.query().convert()
        yearNames = [e['year']['value'] for e in years['results']['bindings']]     #No name for years yet
        yearIRIs = [e['year']['value'] for e in years['results']['bindings']]

        townsForDropdown = []
        for i in range(len(townNames)):
            townsForDropdown.append({'label': townNames[i], 'value': townIRIs[i]})

        countiesForDropdown = []
        for i in range(len(countyNames)):
            countiesForDropdown.append({'label': countyNames[i], 'value': countyIRIs[i]})
            
        museumsForDropdown = []
        for i in range(len(museumNames)):
            museumsForDropdown.append({'label': museumNames[i], 'value': museumIRIs[i]})

        landmarksForDropdown = []
        for i in range(len(landmarkNames)):
            landmarksForDropdown.append({'label': landmarkNames[i], 'value': landmarkIRIs[i]})     
            
        walledTownsForDropdown = []
        for i in range(len(walledTownNames)):
            walledTownsForDropdown.append({'label': walledTownNames[i], 'value': walledTownIRIs[i]})      
            
        pilgrimPathsForDropdown = []
        for i in range(len(pilgrimPathNames)):
            pilgrimPathsForDropdown.append({'label': pilgrimPathNames[i], 'value': pilgrimPathIRIs[i]})     

        historicPeriodsForDropdown = []
        for i in range(len(historic_period_names)):
            historicPeriodsForDropdown.append({'label': historic_period_names[i], 'value': historic_period_IRIs[i]}) 

        historicCenturiesForDropdown = []
        for i  in range(len(historicCenturyNames)):
            historicCenturiesForDropdown.append({'label': historicCenturyNames[i], 'value': historicCenturyIRIs[i]})

        yearsForDropdown = []
        for i in range(len(yearNames)):
            yearsForDropdown.append({'label': yearNames[i].split('#')[-1], 'value': yearIRIs[i]})
            
            
        return countiesForDropdown, townsForDropdown, museumsForDropdown, landmarksForDropdown, walledTownsForDropdown, pilgrimPathsForDropdown, historicPeriodsForDropdown, historicCenturiesForDropdown, yearsForDropdown

    @staticmethod
    def create_filter(entityType, varibale):
        print(entityType)
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
                ?place dbo:name ?name .
                ?place gn:locatedIn <$LOCATION>

                $FILTER
            }
            ORDER BY ASC(UCASE(str(?name)))
        """
        query = string.Template(query).substitute(
            LOCATION=location,
            FILTER=FILTER)
        print(query)
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
                LOCATION = 'ours:locality'

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

    def query_4(self, entityType, locationType, otherPoiInLocation):
        FILTER = QueryExecutor().create_filter(entityType, 'POI')

        sparql = SPARQLWrapper("http://localhost:7200/repositories/KDE-project")
        output = { 'placesOfInterest' : ''}
        
        query = """           
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ours: <http://www.semanticweb.org/ontology/irishhistory>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX gn: <http://www.geonames.org/ontology#>
                SELECT ?place ?name WHERE {
                    ?place a ?POI .
                    ?place gn:locatedIn ?town .
                    ?town a $LOCATION .
                    ?place ours:name ?name .
                    <$otherPoiInLocation2> gn:locatedIn ?town .
                    $FILTER
                    }
                ORDER BY ASC(UCASE(str(?name)))
                """
        if locationType.lower() == 'county':
            subLOCATION = 'ours:county'
        else:
            subLOCATION = 'ours:locality'
        query = string.Template(query).substitute(FILTER=FILTER, LOCATION = subLOCATION, otherPoiInLocation2=otherPoiInLocation)
        print(query);
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
        #print("results:", results)
        #output['otherPOIs'] = [];
        #if (len(results['results']['bindings']) > 0): output['otherPOIs'] = [e['place']['value'] for e in results['results']['bindings']]
        #return output
    

    #def query_4(self, p):
#poiType = ['Pilgrim Path', 'Walled Towns']
#debug = QueryExecutor()
#debug.query_4(poiType, 'County', 'http://www.semanticweb.org/ontology/irishhistory#pointOfinterestAbbey%20Theatre%20Archive')
#QueryExecutor().query_4( poiType, 'County', 'Landmarks', 'http://www.semanticweb.org/ontology/irishhistory#pointOfinterestAbbey%20Theatre%20Archive');

