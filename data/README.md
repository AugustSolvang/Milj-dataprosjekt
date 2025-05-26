Denne mappen inneholder data, som blir bearbeidet og visualiert i andre filer.
Dataen er henholdsvis luftkvalitet (Air_Quality.csv), lufttemperatur i forhold til normen fra 1961-1990(Ait_Temp_Anomaly_1961-1990.json) og nedbørsmengde i forhold til normen til normen fra 1961-1990 (Precipitation_Sum_Anomaly_1961-1990.json)

For å hente ut data for lufttemperatur i forhold til normen fra 1961-1990 brukte vi samme koden i "Json_Dump_MET.py" for å dumpe data fra frost inn i en egen json fil.
APIen henter værdata fra [Frost API](https://frost.met.no/api.html#/) levert av Meteorologisk institutt.
Link til APIen:
https://frost.met.no/observations/v0.jsonld?sources=SN18700&elements=best_estimate_mean(air_temperature_anomaly P1M 1961_1990)&referencetime=1940-01-01/2025-01-01

For å hente ut data for nedbørsmengde i forhold til normen fra 1961-1990 brukte vi samme koden i "Json_Dump_MET.py" for å dumpe data fra frost inn i en egen json fil.
Link til APIen:
https://frost.met.no/observations/v0.jsonld?sources=SN18700&elements=best_estimate_sum(precipitation_amount_anomaly P1M 1961_1990)&referencetime=1940-01-01/2025-01-01

For å hente ut data for luftkvalitet var vi nødt til å laste ned en csv fil fra nettet, da vi ikke fant noen API som ga oss tilgang til denne typen data. Dataen er hentet fra [NILU](https://luftkvalitet.nilu.no/historikk)

Denne delen ble fjernet fra starten av csv filen vår (Air_Quality.csv), sånn at CSVLint fikk status "OK":
Det gjennomfoeres kvalitetskontroll av luftkvalitetsdata.QC-flagg viser hvilket nivaa av kvalitetskontroll dataene har vaert gjennom.QC=1 (Raadata) QC = 2(Automatisk kontrollerte data) QC= 3(Skalerte data) QC= 4(Kvalitetssikrede data / Godkjente data)
Ved kvalitetskontroll flagges verdier som gyldige eller ugyldige(f.eks ved instrumentfeil).QA = 0(Gyldig verdi) QA = 1(Ugyldig verdi)
Data er hentet fra loesningen https://luftkvalitet.nilu.no 
Tid;Bekkestua NO µg/m³ Month;Dekning
