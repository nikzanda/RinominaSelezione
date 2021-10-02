# Rinomina Selezione
Rinomina gli episodi delle serie TV nel formato: **Serie TV**. **stagione**x**episodio** **titolo italiano** - **titolo originale** mantenendo l'estensione originale del file, ad esempio:
```
Person of Interest. 1x01 La macchina della conoscenza - Pilot
```
I titoli vengono letti dalla pagina Wikipedia corrispondente alla serie TV e alla stagione inserite.

Lo script chiede in input:
1. Percorso assoluto della directory contenente i file da rinominare;
2. Nome della serie TV;
3. Stagione della serie TV.

Se la directory e la pagina Wikipedia vengono trovate correttamente, prima di proseguire lo script mostrerà un'anteprima _vecchio file_ > _nuovo file_ e chiederà all'utente se vuole procedere con l'esecuzione. Alla conferma i file verranno rinominati.