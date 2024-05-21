import csv
import json

symptomsFile = open('Disease_Syntoms.csv', 'r')
descriptionFile = open('Disease_Description.csv', 'r')
treatmentFile = open('Disease_Treatment.csv', 'r')

diseases = {}
symptoms = {"Fever", "Cough", "SoreThroat", "IncreasedThirst", "FrequentUrination", "Fatigue"}
treatments = {"Rest", "Hydration", "AntiviralDrugs", "InsulinTherapy", "DietModification", "Exercise"}

symptomTTL = ""
treatmentTTL = ""
diseaseTTL = ""

inicio="""
@prefix : <http://www.example.org/disease-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix swrl: <http://www.w3.org/2003/11/swrl#> .
@prefix swrlb: <http://www.w3.org/2003/11/swrlb#> .

:Ontology a owl:Ontology .

# Classes
:Disease a owl:Class .
:Symptom a owl:Class .
:Treatment a owl:Class .
:Patient a owl:Class .

# Properties
:hasSymptom a owl:ObjectProperty ;
    rdfs:domain :Disease ;
    rdfs:range :Symptom .

:hasTreatment a owl:ObjectProperty ;
    rdfs:domain :Disease ;
    rdfs:range :Treatment .

:exhibitsSymptom a owl:ObjectProperty ;
    rdfs:domain :Patient ;
    rdfs:range :Symptom .

:hasDisease a owl:ObjectProperty ;
    rdfs:domain :Patient ;
    rdfs:range :Disease .

:receivesTreatment a owl:ObjectProperty ;
    rdfs:domain :Patient ;
    rdfs:range :Treatment .

# Disease instances
:Flu a :Disease ;
    :hasSymptom :Fever, :Cough, :SoreThroat ;
    :hasTreatment :Rest, :Hydration, :AntiviralDrugs .


# Symptom instances
:Fever a :Symptom .
:Cough a :Symptom .
:SoreThroat a :Symptom .
:IncreasedThirst a :Symptom .
:FrequentUrination a :Symptom .
:Fatigue a :Symptom .

# Treatment instances
:Rest a :Treatment .
:Hydration a :Treatment .
:AntiviralDrugs a :Treatment .
:InsulinTherapy a :Treatment .
:DietModification a :Treatment .
:Exercise a :Treatment .


:description rdf:type owl:DatatypeProperty ;
        rdfs:domain :Disease .

"""

first=True
for row in csv.reader(symptomsFile, delimiter=','):
    if first:
        first=False
        continue
    disease = row[0].strip()
    disease = disease.replace(" ", "_")
    disease = disease.replace("(", "\(")
    disease = disease.replace(")", "\)")
    ss = row[1:]
    if disease not in diseases:
        diseases[disease] = {"sintomas": set(), "tratamento": set(),"description":""}
    for symptom in ss:
        if symptom!="":
            symptom = symptom.strip()
            symptom = symptom.replace("(", "\(")
            symptom = symptom.replace(")", "\)")
            symptom = symptom.replace(" ", "_")
            if symptom not in symptoms:
                symptoms.add(symptom)
                inicio += f":{symptom} a :Symptom .\n"
            diseases[disease]["sintomas"].add(symptom)

first=True
for row in csv.reader(descriptionFile):
    if first:
        first=False
        continue
    disease, desc = row
    disease = disease.strip()
    disease = disease.replace(" ", "_")
    disease = disease.replace("(", "\(")
    disease = disease.replace(")", "\)")
    desc = desc.strip()
    desc = desc.replace('"', '\\"')
    if disease not in diseases:
        diseases[disease] = {"sintomas": set(), "tratamento": set(),"description":""} 
    diseases[disease]["description"] = desc


for disease in diseases:
    sintomas = ", ".join([f":{s}" for s in diseases[disease]["sintomas"]])
    description = diseases[disease]["description"]
    diseaseTTL += f":{disease} a :Disease ;\n"
    if sintomas:
        diseaseTTL += f"\t:hasSymptom {sintomas} ;\n"
    if description:
        diseaseTTL += f"\t:description \"{description}\" .\n"
    else:
        diseaseTTL = diseaseTTL[:-2] + " .\n"

with open("med_doencas.ttl", "w") as f:
    f.write(inicio)
    f.write(diseaseTTL)

############################################################################################### 

first=True
for row in csv.reader(treatmentFile):
    if first:
        first=False
        continue
    disease = row[0].strip()
    disease = disease.replace(" ", "_")
    disease = disease.replace("(", "\(")
    disease = disease.replace(")", "\)")
    ts = row[1:]
    if disease not in diseases:
        diseases[disease] = {"sintomas": [], "tratamento": [],"description":""} 
    for treatment in ts:
        if treatment!="":
            treatment = treatment.strip()
            treatment = treatment.replace(" ", "_")
            if treatment not in treatments:
                treatments.add(treatment)
                inicio += f":{treatment} a :Treatment .\n"
            diseases[disease]["tratamento"].add(treatment)
            

for disease in diseases:
    sintomas = ", ".join([f":{s}" for s in diseases[disease]["sintomas"]])
    tratamentos = ", ".join([f":{t}" for t in diseases[disease]["tratamento"]])
    description = diseases[disease]["description"]
    inicio += f":{disease} a :Disease ;\n"
    if sintomas:
        inicio += f"\t:hasSymptom {sintomas} ;\n"
    if tratamentos:
        inicio += f"\t:hasTreatment {tratamentos} ;\n"
    if description:
        inicio += f"\t:description \"{description}\" .\n"
    else:
        inicio = inicio[:-2] + " .\n"
    
with open("med_tratamentos.ttl", "w") as f:
    f.write(inicio)




############################################################################

with open("doentes/pg53816.json","r") as doentes:
    doentes = json.load(doentes)

id_doente = 1
for doente in doentes:
    sintomas = ""
    for sintoma in doente["sintomas"]:
        sintoma = sintoma.strip()
        sintoma = sintoma.replace("(", "\(")
        sintoma = sintoma.replace(")", "\)")
        sintoma = sintoma.replace(" ", "_")
        sintomas+=f":exhibitsSymptom :{sintoma} ;\n"
    sintomas = sintomas[:-2]
    inicio += f"""
    :Patient{id_doente} a :Patient ;
    :name "{doente['nome']}" ;
    {sintomas}.
    """
    id_doente += 1

with open("med_doentes.ttl", "w") as f:
    f.write(inicio)



