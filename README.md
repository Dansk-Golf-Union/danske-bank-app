# Danske Bank Samlet Data Webapp

Denne Streamlit-app gør det nemt at samle data fra tre kilder: CallMe, BBTilmeld og Playable.

## Sådan bruges den

1. Åbn Terminal og gå til mappen:
   ```bash
   cd stien/til/mappen
   ```

2. Start appen:
   ```bash
   streamlit run app.py
   ```

3. Upload dine tre filer i browseren og klik 'Generér samlet fil'.

## Krav

- Python 3.8+
- Installer afhængigheder:
   ```bash
   pip install streamlit openpyxl
   ```

Appen virker med både `.csv` og `.xlsx` filer.