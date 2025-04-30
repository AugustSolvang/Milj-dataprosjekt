Vi benytter oss av åpne miljødata fra API-er som openweathermap, API.met og frost.met. 


RELEVANTE KILDER:
For å vurdere troverdigheten til disse nettsidene, sjekker vi på datakildene, metode for innsamling og hvordan de kvalitetssikrer informasjonen. Informasjonen knyttet til både API.met og Frost.met er av god kvalitet, da disse henter sine data fra offisielle værstasjoner i Norge og andre internasjonale kilder, samtidig som hyppig oppdateringer og kvalitetsikrede data, med deres samarbeid med internasjonale meteorologiske institutter.
OpenWeatherMap kombinerer data fra værstasjoner og meteorologiske modeller. Informasjonen deres derimot kan variere avhengig av området som observeres, da noen områder har tettere nettverk av værstasjoner som gir bedre data.

HVILKE BEHANDLINGSTEKNIKKER:
For det meste bruker vi API-er sammen med JSON-data for lesing av dataene, da dette gir et strukturert og lettlest resultat. Samtidig støtter JSON ulike datatyper som lister, objekter, strenger, tall og boolske verdier. Likevel, kan det oppstå uønskede/ugyldig data som må tas hensyn til videre i prosessen. Her kommer rensing og databehandling inn i bilde. ALternativt, kan CSV-filer benyttes, men det må da ta hensyn til to forskjellige filer, som da krever ekstra håndtering og filbehandling.

VIKTIGSTE DATAENE:
De nevnte API-nettsidene over inneholder god og åpen historisk data. Noen av disse kan strekke seg så langt som 1940-tallet. Hvis vi leker oss litt rundt med nettsidene kan vi finne svært varierende data, f.eks min/maks/gjennomsnittlig temperatur, nedbør, vindhastighet, luftkvalitet og mer. Dette gir et godt spekter av data som kan benyttes til analyse og visualisering. 

TILGJENGELIGHET:
API-met og Frost.met har gratis tilgang på deres API-er. OpenWeatherMap har en god mengde gratis API-er, men tilbyr også noen som krever betaling/abonemment. Det er nødvendig å opprette en bruker på alle nettsidene for å få tilgang til deres API-er, samtidig trengs API-key til både OpenWeatherMap og Frost for tilgang til API-ene.

*Vurderingskriterier:*

1. Hvilke åpne datakilder er identifisert som relevante for miljødata, og hva er kriteriene (f.eks. kildeautoritet, datakvalitet, tilgjengelighet, brukervennlighet osv.) for å vurdere deres pålitelighet og kvalitet?
2. Hvilke teknikker (f.eks. håndtering av CSV-filer, JSON-data) er valgt å bruke for å lese inn dataene, og hvordan påvirker disse valgene datakvaliteten og prosessen videre?
3. Dersom det er brukt API-er, hvilke spesifikke API-er er valgt å bruke, og hva er de viktigste dataene som kan hentes fra disse kildene?


Her skal dere fokusere på databehandling ved å utvikle funksjoner som renser og formaterer de innsamlede dataene, med særlig vekt på håndtering av manglende verdier og uregelmessigheter ved hjelp av Pandas. I tillegg skal dere benytte teknikker som list comprehensions, iteratorer, pandas og pandas sql (sqldf) for å manipulere dataene effektivt, noe som vil bidra til å forberede dataene for videre analyse.

METODER FOR HÅNDTERING AV MANGLENDE VERDIER:
Mulige metoder innebærer:
isnull().sum() - Identifiserer manglende verdier
fillna() - Erstatter manglende verdier
dropna() - Fjerner rader med manglende verdier

LIST COMPREHENSIONS FOR MANIPULASJON AV DATA::
Brukes som oftest i stedet for " for løkker" for å gjøre koden lettere og mer effektiv.

f.eks ["hot" if temperature > 20 else "cold" for temperature in .....]

Dette gjør koden mer oversiktlig og lesbar.

HVORDAN PANDAS SQL FORBEDRER DATAMANIPULERING:

Pandasql.sqldf lar oss bruke SQL-spørringer dirkete på Pandas-dataframes, noe som igjen gjør koden lettere og mer fleksibelt.

f.eks
from pandasql import sqldf

query = "SELECT * FROM ... WHERE temperature > 20"

dette henter data kun da temperaturen var over 20.

HVILKE UREGELMESSIGHETER:


1. Hvilke metoder vil du bruke for å identifisere og håndtere manglende verdier i datasettet?
2. Kan du gi et eksempel på hvordan du vil bruke list comprehensions for å manipulere dataene?
3. Hvordan kan Pandas SQL (sqldf) forbedre datamanipuleringen sammenlignet med tradisjonelle Pandas-operasjoner?
4. Hvilke spesifikke uregelmessigheter i dataene forventer du å møte, og hvordan planlegger du å håndtere dem?