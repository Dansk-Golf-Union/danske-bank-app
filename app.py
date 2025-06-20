import streamlit as st
import pandas as pd
import io

def read_file(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file, sep=None, engine='python')
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file, engine="openpyxl")
    else:
        st.error("Kun CSV eller Excel (.xlsx) filer understøttes.")
        return None

def standardize_dataframe(df, source_name):
    df = df.copy()
    df["Source"] = source_name

    if source_name == "CallMe":
        return pd.DataFrame({
            "Source": df["Source"],
            "Serial number": df.get("Serial number"),
            "Id": None,
            "Created": df.get("Created"),
            "Completed": df.get("Completed"),
            "Fornavn": df.get("Fornavn"),
            "Efternavn": df.get("Efternavn"),
            "E-mail": df.get("Email"),
            "Adresse (gade og nr.)": df.get("Adresse (gade og nr.)"),
            "Etage m.v.": df.get("Etage m.v."),
            "Postnummer": df.get("Postnummer"),
            "By": df.get("By"),
            "Telefonnummer": df.get("Telefonnummer"),
            "Angiv dit DGU-nr. / union-id": df.get("Angiv dit DGU-nr."),
            "Er du kunde hos Danske Bank i dag?": df.get("Er du kunde hos Danske Bank i dag?"),
            "Ja, Danske Bank må kontakte mig": df.get("Ja, Danske Bank må kontakte mig"),
            "newsletter": None,
        })

    elif source_name == "BBTilmeld":
        return pd.DataFrame({
            "Source": df["Source"],
            "Serial number": None,
            "Id": df.get("id"),
            "Created": None,
            "Completed": None,
            "Fornavn": df.get("first_name"),
            "Efternavn": df.get("last_name"),
            "E-mail": df.get("email"),
            "Adresse (gade og nr.)": df.get("address_street"),
            "Etage m.v.": df.get("address_additional"),
            "Postnummer": df.get("address_post_code"),
            "By": df.get("address_city"),
            "Telefonnummer": df.get("phone"),
            "Angiv dit DGU-nr. / union-id": df.get("union_id"),
            "Er du kunde hos Danske Bank i dag?": df.get("danske_bank_customer"),
            "Ja, Danske Bank må kontakte mig": df.get("danske_bank_can_call"),
            "newsletter": df.get("newsletter"),
        })

    elif source_name == "Playable":
        return pd.DataFrame({
            "Source": df["Source"],
            "Serial number": None,
            "Id": df.get("Registration ID"),
            "Created": df.get("Created on"),
            "Completed": None,
            "Fornavn": df.get("Fornavn"),
            "Efternavn": df.get("Efternavn"),
            "E-mail": df.get("Email"),
            "Adresse (gade og nr.)": df.get("Adresse (Gade og nr.)"),
            "Etage m.v.": df.get("Etage m.v."),
            "Postnummer": df.get("Postnummer"),
            "By": df.get("By"),
            "Telefonnummer": df.get("Telefon"),
            "Angiv dit DGU-nr. / union-id": df.get("Angiv dit DGU-nr."),
            "Er du kunde hos Danske Bank i dag?": df.get("Er du kunde hos Danske Bank i dag?"),
            "Ja, Danske Bank må kontakte mig": df.get("Ja, Danske Bank må kontakte mig"),
            "newsletter": None,
        })

    return df

st.set_page_config(page_title="Danske Bank - Samlet Data Generator")
st.title("Danske Bank - Samlet Data Generator")
st.write("Upload de tre filer nedenfor (CallMe, BBTilmeld, Playable)")

callme_file = st.file_uploader("Upload CallMe fil", type=["csv", "xlsx"])
bbtilmeld_file = st.file_uploader("Upload BBTilmeld fil", type=["csv", "xlsx"])
playable_file = st.file_uploader("Upload Playable fil", type=["csv", "xlsx"])

if st.button("Generér samlet fil"):
    if not any([callme_file, bbtilmeld_file, playable_file]):
        st.warning("Upload mindst én fil for at fortsætte.")
    else:
        dfs = []

        if callme_file:
            df = read_file(callme_file)
            if df is not None:
                dfs.append(standardize_dataframe(df, "CallMe"))

        if bbtilmeld_file:
            df = read_file(bbtilmeld_file)
            if df is not None:
                dfs.append(standardize_dataframe(df, "BBTilmeld"))

        if playable_file:
            df = read_file(playable_file)
            if df is not None:
                dfs.append(standardize_dataframe(df, "Playable"))

        if dfs:
            final_df = pd.concat(dfs, ignore_index=True)
            csv = final_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download samlet CSV", csv, "danske_bank_samlet.csv", "text/csv")
        else:
            st.error("Ingen gyldige data at samle.")
