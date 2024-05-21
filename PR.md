EX1:

. Quantas classes estão definidas na Ontologia?
```
SELECT (COUNT(?class) AS ?classCount) WHERE {
  ?class a owl:Class .
}
```
 . Quantas Object Properties estão definidas na Ontologia?
 ```
SELECT (COUNT(?o) as ?nObj) WHERE{
    ?s a owl:ObjectProperty .
}
```

 . Quantos indivíduos existem na tua ontologia?
 ```
SELECT (COUNT(?i) as ?ni)
WHERE {

    ?c a owl:Class.
    ?i a ?c.

}
```


 . Quem planta tomates?
 ```
 SELECT * WHERE{
    ?pessoa :cultiva :tomate.
}
```

 . Quem contrata trabalhadores temporários?
```
SELECT * WHERE {
    ?s :contrataTemporario "sim".
}
```
EX2:
```
Quantas doenças estão presentes na ontologia?
SELECT * WHERE {
   ?d a :Disease.
}
```
 Que doenças estão associadas ao sintoma "yellowish_skin"?
 ```
 SELECT ?d WHERE {
   ?d a :Disease.
   ?d :hasSymptom :yellowish_skin.
}
```

 Que doenças estão associadas ao tratamento "exercise" ?
 ```
 SELECT ?doenca WHERE{
    ?doenca a :Disease.
    ?doenca :hasTreatment :exercise. 
}
```

 Produz uma lista ordenada alfabeticamente com o nome dos doentes.
 ```
 SELECT ?p WHERE{
    ?p a :Patient.
	?p :name ?name
}ORDER BY (?name)

```

Cria uma query CONSTRUCT que diagnostique a doença de cada pessoa, ou seja,
produza uma lista de triplos com a forma :patientX :hasDisease :diseaseY. No fim, acrescenta estes triplos à ontologia;
```
CONSTRUCT {
  ?patient :hasDisease ?disease .
}
WHERE {
  ?patient rdf:type :Patient ;
           :exhibitsSymptom ?symptom .
  ?disease :hasSymptom ?symptom .
}
```

Distribuição dos doentes pelas doenças, ou seja, dá como resultado uma lista de pares (doença, nº de doentes);
```
SELECT ?doenca (COUNT(?doente) as ?ndoentes)
WHERE {
    ?doente a :Patient.
    ?doenca a :Disease.
    ?doente :hasDisease  ?doenca.
}
group by ?doenca
```



Distribuição das doenças pelos sintomas, ou seja, dá como resultado uma lista de pares (sintoma, nº de doenças com o sintoma);
```
SELECT ?sintoma (COUNT(?doenca) as ?nd)
WHERE {
    ?doenca a :Disease.
    ?doenca :hasSymptom  ?sintoma.
}
group by ?sintoma
```


Distribuição das doenças pelos tratamentos, ou seja, dá como resultado uma lista de pares (tratamento, nº de doenças com o tratamento).
```
SELECT ?tratamento (COUNT(?doenca) as ?nd)
WHERE {
    ?doenca a :Disease.
    ?doenca :hasTreatment  ?tratamento.
}
group by ?tratamento
```


Para o exercicio 2 basta correr o ex2.py

Ignore as pastas extra que fiz asneira.