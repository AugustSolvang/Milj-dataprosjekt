Describes the data directory and datasets

Vi har testet ut to forskjellige metoder å hente ut data, som begge tar i bruk API-kall. Først lagde vi en fil med navn "Weather_Data_MET.py" denne filen henter ut data og printer det som en pandas dataframe. Så prøvde vi å lage en kode som dumpet all dataen i en json fil. begge metodene brukte sinnsyk lang tid for å kjøre. På det værste kunne det ta fem minutter å hente ut all dataen. Dette skyldes nok apien vi brukte. Vi tok i bruk en api som hentet ut flere verdier for hver dag. Det gikk helt greit fra 1960-1990, men noe nyere tid enn det fikk vi med oss flere og flere målinger for hver dag. Det gikk rett og slett ikke ann å helte ut all dataen ved bruk at noen få api kall. 
Vi brukte denne apien i utgangspunktet fordi vi ville regne oss frem til den daten vi ville ut ifra temperaturen, men måtte bytte til en api som kunn hentet ut dataen som var nødvendig for oss, sånn at programmet kunne kjøre raskere. Dermed Lagde vi "Best_Estimate_Mean.py", som lager json fil for temperaturavik fra hver måned fra tidsintervallet 1961 til 1990.
APIen henter værdata fra [Frost API](https://frost.met.no/api.html#/) levert av Meteorologisk institutt.
Link til APIen:
https://frost.met.no/observations/v0.jsonld?sources=SN18700&elements=best_estimate_mean(air_temperature_anomaly P1M 1961_1990)&referencetime=1940-01-01/2025-01-01

For å hente ut data for nedbørsmengde i forhold til normen fra 1961-1990 brukte vi samme koden i "Json_Dump_MET.py" for å dumpe data fra frost inn i en egen json fil.
Link til APIen:
https://frost.met.no/observations/v0.jsonld?sources=SN18700&elements=best_estimate_sum(precipitation_amount_anomaly P1M 1961_1990)&referencetime=1940-01-01/2025-01-01

For å hente ut data for luftkvalitet var vi nødt til å laste ned en csv fil fra nettet, da vi ikke fant noen API som ga oss tilgang til denne typen data. Dataen er hentet fra [NILU](https://luftkvalitet.nilu.no/historikk)
