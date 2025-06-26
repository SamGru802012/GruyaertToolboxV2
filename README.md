# Pack Optimizer App

Deze Streamlit-app helpt bij het optimaliseren van productverpakkingen en het stapelen van dozen op een pallet.  
Gecombineerde kennis van logistiek en Python maakt het mogelijk om:

- Producten met 6 rotaties in omdozen te simuleren
- Omdozen te beheren via SQLite
- Visualisatie in Plotly
- Export van resultaten

## Installatie

```bash
pip install streamlit pandas
streamlit run main.py
```

## Bestanden

- `main.py` — Opstartpunt voor de Streamlit app
- `ui.py` — Bevat de gebruikersinterface met tabs
- `data_manager.py` — Laadt en beheert de SQLite database
- `omverpakkingen.db` — De dozenvoorraad (geïmporteerd vanuit CSV)