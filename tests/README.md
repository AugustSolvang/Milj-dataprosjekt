Explains the test structure and how to run tests

Unit_test.py:
Her har vi alle unittestene våre. Vi har både negative og positive tester for funksjonene i Data_Process.py, og tester av plottefunksjonene i Data_Plot.py. De diverse testene sjekker blant annet om gyldig filtype, rensing av data, SQL-analyse, lineær regresjon og at de ulike plottypene kan tegnes. Kommentarer over hver enkel kode er inkludert i selve filen for mer informasjon over hva de diverse funksjonene tester.

Testene kjøres med `pytest` fra rotmappen. Plottene tegnes uten å åpne vinduer (se `conftest.py`).