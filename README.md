# Miljødataprosjekt – klima og luftkvalitet i Oslo-området

Gruppeprosjekt (sammen med Mani) i TDT4114 Anvendt programmering, NTNU, vår 2025.

Prosjektet henter, renser og analyserer miljødata for Oslo-området. Det beregner årlig statistikk (gjennomsnitt, median, min og maks), estimerer langsiktige trender med lineær regresjon og viser resultatene i statiske plott og i et interaktivt dashboard.

> Videreutviklet etter innlevering: rettet filtrering av negative temperaturavvik og fjernet API-nøkler fra repoet. Innlevert versjon: tag v1.0-innlevert.

## Datakilder

- **Frost-API-et fra Meteorologisk institutt**, stasjon SN18700 Oslo–Blindern:
  - månedlig temperaturavvik fra normalen 1961–1990, 1940–2024 ([data/Air_Temp_Anomaly_1961-1990.json](data/Air_Temp_Anomaly_1961-1990.json))
  - månedlig nedbørsavvik fra normalen 1961–1990, 2006–2024 ([data/Precipitation_Sum_Anomaly_1961-1990.json](data/Precipitation_Sum_Anomaly_1961-1990.json))
- **Luftkvalitet fra NILU**, målestasjon Bekkestua ([data/Air_Quality.csv](data/Air_Quality.csv))

## Metoder

- **pandas** for innlesing, rensing og transformasjon av JSON- og CSV-data
- **SQL via pandasql** for årlig aggregering
- **Lineær regresjon med scikit-learn** for trendanalyse og fremskrivning
- **Interaktivt dashboard i Bokeh** med valg av statistikk, plottype, farger og regresjon
- **Enhetstester** med unittest/pytest i [tests/Unit_test.py](tests/Unit_test.py)

![Interaktivt Bokeh-dashboard](docs/Interactive%20plot.png)

## Kjøre prosjektet

Krever Python 3.10 eller nyere.

```bash
git clone https://github.com/AugustSolvang/Milj-dataprosjekt.git
cd Milj-dataprosjekt
python -m venv venv
venv\Scripts\activate          # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

Ferdig nedlastede data ligger i `data/`, så du trenger ikke API-nøkkel for å kjøre analysen.

- **Statiske plott:** `python src/main.py` (svar «No» på spørsmålet om interaktivt plott)
- **Interaktivt dashboard:** `bokeh serve src/Interactive_Plot.py --show --port 5006`. Velg datasett med `FILENAME` øverst i [src/Interactive_Plot.py](src/Interactive_Plot.py).
- **Hente data på nytt fra Frost:** kopier `.env.example` til `.env`, fyll inn din egen klient-ID fra [frost.met.no](https://frost.met.no) og kjør `python src/Json_Dump_MET.py`.
- **Enhetstester:** kjøres fra `data/`-mappen med `src/` på `PYTHONPATH`, for eksempel `cd data` og så `PYTHONPATH=../src pytest ../tests/Unit_test.py`.

---

## Opprinnelig oppgavetekst

# Project

The course has portfolio assessment which forms the basis for the grade in the subject. Portfolio assessment is based on the work you do in your project. The project should be solved in groups, and it is sufficient for one person in the group to submit the answer in Blackboard. When you have solved all the tasks, upload the entire answer as one zip file in BB. The zip file should contain the entire project directory, including all source code, .git directory, etc. It is important that you include the .git directory (an "invisible" directory in the root directory of your project) because it contains your version history. You will receive written feedback on what you have submitted in BB, and you can make improvements to the code right up until the final portfolio submission.


The project is divided into the following parts:

1. General Part: Background information about the project and tasks that are common to all parts.
2. Portfolio Part 1: Focuses on data collection and preparation.
3. Portfolio Part 2: Focuses on data analysis and visualization.

Final project has to be delivered in Inspera for assessment. The grading scale is A-F.

```{Note}
We do not recommend starting work on the project before week 6, as we might make changes to it. Until then, you can prepare yourself and focus on learning topics relevant to increasing your competency to deliver the project successfully.
```

```{Note}
Your final project solution should be submitted for assessment in Inspera. Please ensure that the virtual environment folder is NOT included in the zip file you upload. Only the requirements.txt file should be included. Additionally, make your central repository publicly accessible and share the link in Inspera.
```


```{important}
To access the project template, click <a href="https://jupyterhub.apps.stack.it.ntnu.no/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgit.ntnu.no%2FTDT4114%2Fproj_environment.git&#38;urlpath=lab%2Ftree%2Fproj_environment.git%2FREADME.md&#38;branch=main">here</a> to copy source files to Jupyter Hub (NTNU). And/Or clone/download from the GitHub repository: <a href="https://git.ntnu.no/TDT4114/proj_environment">https://git.ntnu.no/TDT4114/proj_environment</a>.
```