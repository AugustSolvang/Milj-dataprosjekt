Explains the source code structure

Data_Process.py:
I denne koden har vi lagd en class ved navn "Data_Process", som inneholder 4 ulike funksjoner. Disse 4 funksjonene har i oppgave å rense data, produsere et velfungerende dataframe, analysere dataene ved hjelp av pandasSQL og prediktere dataene ved hjelp av linear regresjon, respektivt.
Classen blir videre brukt i main med de resterende kodene.

Data_Plot.py:
I denne koden har vi lagd en class ved navn "Data_Plot, der vi har 3 ulike funksjoner som plotter ulike type grafer. Her har vi benyttet oss av Matplotlib og Seaborn for å produsere funksjoner som lager lineplots, scatterplots og barplots.
Classen blir videre brukt i main med de resterende kodene.

Interactive_Plot.py:
Denne koden produserer det interaktive plottet som en nettside i webbrowser. Innholdet i programmet baserer seg på Bokeh, et svært nyttig bibliotek hva det gjelder av fleksibilitet og interaktivitet av grafer.
Denne koden inneholder ikke en class, men brukes ved å kjøre en kode i terminalen:
--> bokeh serve src/Interactive_Plot.py --show --port 5006