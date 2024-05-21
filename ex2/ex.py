import csv

symptoms = open('Disease_Syntoms.csv', 'r')
description = open('Disease_Description.csv', 'r')
treatment = open('Disease_Treatment.csv', 'r')

diseases = {}
symptoms = {"Fever", "Cough", "SoreThroat", "IncreasedThirst", "FrequentUrination", "Fatigue"}
treatments = {"Rest", "Hydration", "AntiviralDrugs", "InsulinTherapy", "DietModification", "Exercise"}

print("symptoms")

for row in csv.reader(symptoms):
    #Fungal infection,itching, skin_rash, nodal_skin_eruptions, dischromic _patches,,,,,,,,,,,,,
    disease = row[0].strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
    symptoms = row[1:]
    if disease not in diseases:
        diseases[disease] = {"sintomas": set(), "tratamento": set(),"description":""}
    for symptom in symptoms:
        if symptom!="":
            symptom = symptom.strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
            symptoms.add(symptom)
            diseases[disease]["sintomas"].add(symptom)

print("description")
for row in csv.reader(description):
    disease, desc = row
    disease = disease.strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
    desc = desc.strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
    if disease not in diseases:
        diseases[disease] = {"sintomas": set(), "tratamento": set(),"description": description} 
    diseases[disease]["description"] = desc

print("treatment")
for row in csv.reader(treatment):
    disease = row[0].strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
    treatments = row[1:]
    if disease not in diseases:
        diseases[disease] = {"sintomas": set(), "tratamento": set(),"description":""} 
    for treatment in treatments:
        if treatment!="":
            treatment = treatment.strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
            diseases[disease]["tratamento"].add(treatment)
            treatments.append(treatment)


#print(diseases)
    



ttl =""""""

#EX1
print("EX1")
for syntom in symptoms:
    ttl += f"""
    :{syntom} a :Symptom  .
    """

#EX2
print("EX2")
for disease in diseases:
    ttl += f"""
    :{disease} a :Disease.
    """


#EX3
print("EX3")

for syntom in symptoms:
    syntom = syntom.strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
    ttl += f"""
    :{disease} :hasSymptom :{syntom}.
    """
#EX4
print("EX4")
"""A partir de 
Disease_Description.csv
 vais associar uma descrição a cada doença
 (cria esta nova propriedade)"""
ttl += f"""
    :description a owl:DatatypeProperty .
    """
for disease in diseases:
    ttl += f"""
    :{disease} :description "{diseases[disease]["description"]}" .
    """
print("EX6")
#EX6
for treatment in treatments:
    treatment = treatment.strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
    ttl += f"""
    :{treatment} a :Treatment  .
    """

#EX7
print("EX7")
for disease in diseases:
    for treatment in diseases[disease]["tratamento"]:
        ttl += f"""
        :{disease} :hasTreatment :{treatment} .
        """


#EX9
print("EX9")
import json
"""

# Patient instances
:Patient1 a :Patient ;
    :name "Paul Harrods" ;
    :exhibitsSymptom :Fever ;
    :exhibitsSymptom :Cough ;
    :exhibitsSymptom :SoreThroat .

:Patient2 a :Patient ;
    :name "Ana Montana";
    :exhibitsSymptom :IncreasedThirst ;
    :exhibitsSymptom :FrequentUrination ;
    :exhibitsSymptom :Fatigue .
"""
f = open("pg54162.json")
bd = json.load(f)
i = 1
for pessoa in bd:
    id = pessoa["nome"].strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","").replace(",","").replace(".","").replace("'","").replace("'","").replace("`´","")
    ttl += f"""
    :{id} a :Patient ;
    :name "{id}" .
    """
    for sintoma in pessoa["sintomas"]:
        sintoma = sintoma.strip().replace(" ","_").replace("(","").replace(")","").replace('"',"").replace("()","")
        ttl += f"""
        :{id} :exhibitsSymptom :{sintoma}.
        """
    #remove last ;

    if (i%100 == 0):
        print(i)



with open("medical.ttl","a") as f:
    f.write(ttl)
    f.close()