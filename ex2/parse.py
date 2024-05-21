from rdflib import Graph,URIRef,Literal,Namespace
from rdflib.namespace import RDF,OWL
import json

g = Graph()

#nome da ontologia - criada no protege, normalmente, isto serve para acrescentar coisas
g.parse("medical.ttl")


#mesmo do protege
namespace = Namespace("http://www.example.org/disease-ontology#Ontology")

#open Disease_Treatment.csv
with open("Disease_Syntoms.csv") as f:
    #ler o ficheiro
    data = f.readlines()
    #para cada linha
    for line in data:
        #the first element is the disease and the rest in syntoms

        #separar por virgula
        line = line.split(",")
        #separar o primeiro elemento
        disease = line[0]
        disease = disease.replace(" ","_")  
        #separar o segundo elemento
        treatments = line[1:]
        #adicionar a ontologia
        #for treatment in treatments:
            
        g.add((URIRef(f"{namespace}{disease}"),RDF.type,OWL.NamedIndividual))
        g.add((URIRef(f"{namespace}{disease}"),RDF.type,namespace.Disease)) 
        
    """

with open("filmes2.json","w"):
    filmes = json.load()
for filme in filmes:
    #para criar algo do tipo filme neste caso, por sempre o tipo(filme) e o OWL.NamedIndividual
    g.add((URIRef(f"{namespace}{filme["filme"]}"),RDF.type,OWL.NamedIndividual))
    g.add((URIRef(f"{namespace}{filme["filme"]}"),RDF.type,namespace.Film)) 
    for actor in filme["actors"]:
        # adicionar um ator
        g.add((URIRef(f"{namespace}{actor}"),RDF.type,OWL.NamedIndividual))
        g.add((URIRef(f"{namespace}{actor}"),RDF.type,namespace.actor)) 
        
        #adicionar relacao entre filme e ator que se chama hasActor
        g.add((URIRef(f"{namespace}{filme["filme"]}"),namespace.hasActor,namespace.Film)) 
        
        #adicionar atributo nome a ator
        g.add((URIRef(f"{namespace}{actor}"),namespace.hasName,Literal(actor["name"])))

    """

#print(len(g))
print(g.serialize())


# print("=====================================")
# import pprint
# for stmt in g:
#     pprint.pprint(stmt)