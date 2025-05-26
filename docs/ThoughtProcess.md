RELEVANTE KILDER:
For å vurdere troverdigheten til disse nettsidene, sjekker vi på datakildene, metode for innsamling og hvordan de kvalitetssikrer informasjonen. Informasjonen knyttet til både API.met og Frost.met er av god kvalitet, da disse henter sine data fra offisielle værstasjoner i Norge og andre internasjonale kilder, samtidig som hyppig oppdateringer og kvalitetsikrede data, med deres samarbeid med internasjonale meteorologiske institutter.
OpenWeatherMap kombinerer data fra værstasjoner og meteorologiske modeller. Informasjonen deres derimot kan variere avhengig av området som observeres, da noen områder har tettere nettverk av værstasjoner som gir bedre data.

HVILKE BEHANDLINGSTEKNIKKER:
For det meste bruker vi API-er sammen med JSON-data for lesing av dataene, da dette gir et strukturert og lettlest resultat. Samtidig støtter JSON ulike datatyper som lister, objekter, strenger, tall og boolske verdier. Likevel, kan det oppstå uønskede/ugyldig data som må tas hensyn til videre i prosessen. Her kommer rensing og databehandling inn i bilde. ALternativt, kan CSV-filer benyttes, men det må da ta hensyn til to forskjellige filer, som da krever ekstra håndtering og filbehandling.

VIKTIGSTE DATAENE:
De nevnte API-nettsidene over inneholder god og åpen historisk data. Noen av disse kan strekke seg så langt som 1940-tallet. Hvis vi leker oss litt rundt med nettsidene kan vi finne svært varierende data, f.eks min/maks/gjennomsnittlig temperatur, nedbør, vindhastighet, luftkvalitet og mer. Dette gir et godt spekter av data som kan benyttes til analyse og visualisering. 

TILGJENGELIGHET:
API-met og Frost.met har gratis tilgang på deres API-er. OpenWeatherMap har en god mengde gratis API-er, men tilbyr også noen som krever betaling/abonemment. Det er nødvendig å opprette en bruker på alle nettsidene for å få tilgang til deres API-er, samtidig trengs API-key til både OpenWeatherMap og Frost for tilgang til API-ene.

METODER FOR HÅNDTERING AV MANGLENDE VERDIER:
Mulige metoder innebærer:
isnull().sum() - Identifiserer manglende verdier
fillna() - Erstatter manglende verdier
dropna() - Fjerner rader med manglende verdier

LIST COMPREHENSIONS FOR MANIPULASJON AV DATA::
Brukes som oftest i stedet for "for løkker" for å gjøre koden lettere og mer effektiv.

f.eks ["hot" if temperature > 20 else "cold" for temperature in .....]

Dette gjør koden mer oversiktlig og lesbar.

HVORDAN PANDAS SQL FORBEDRER DATAMANIPULERING:

Pandasql.sqldf lar oss bruke SQL-spørringer dirkete på Pandas-dataframes, noe som igjen gjør koden lettere og mer fleksibelt.

f.eks
from pandasql import sqldf

query = "SELECT * FROM ... WHERE temperature > 20"

dette henter data kun da temperaturen var over 20.