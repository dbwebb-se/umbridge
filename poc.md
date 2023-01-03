# hur kan vi skilja på submissions som är grupp eller inte?

1. Hämta submissions
2. Hämta assignment och kolla om den är grupp
3. Sortera ut den andra studenten
4. Rätta ena
5. rapportera
6. Hur hantera den andra studenten i databasen?
    - bygg ut databas med ny kolumn som refererar till den andra studenten?
    - Skippa det


Frågor:
 - kan båda komma åt filen i kommentaren?

Bygga om utan databasen:
 - skippa uppdelningen mellan getch, test och grade. Gör allt för en submission direkt. for each sub test and grade.
 - lägg till loggfilen som en filkommentar och gör samma lösning som med kod visaren.


changes:
eve
    - routes
        - move fetch code to wall-e
    - courses
        - move to wall-e
    - models
        - move
    - delete

results
    - change log code to work as browse

templates
    - ones again check if can add line numbers to browse files

wall-e
    - models
      - rewrite to use canvasapi module

models
    - remove submissions model