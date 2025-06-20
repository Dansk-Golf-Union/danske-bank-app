import streamlit as st
import pandas as pd
import io

def read_file(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file, sep=None, engine='python')
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
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
            "newsletter": None
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
            "newsletter": df.get("newsletter")
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
            "Ja, Danske Bank må kontakte mig": df.iloc[:, 11] if df.shape[1] > 11 else None,
            "newsletter": None
        })
    else:
        return None

st.title("Danske Bank - Samlet Data Generator")

st.markdown("Upload de tre filer nedenfor (CallMe, BBTilmeld, Playable)")

callme_file = st.file_uploader("Upload CallMe fil", type=["csv", "xlsx"])
bb_file = st.file_uploader("Upload BBTilmeld fil", type=["csv", "xlsx"])
playable_file = st.file_uploader("Upload Playable fil", type=["csv", "xlsx"])

if st.button("Generér samlet fil"):
    if not all([callme_file, bb_file, playable_file]):
        st.warning("Alle tre filer skal uploades.")
    else:
        callme_df = read_file(callme_file)
        bb_df = read_file(bb_file)
        playable_df = read_file(playable_file)

        callme_std = standardize_dataframe(callme_df, "CallMe")
        bb_std = standardize_dataframe(bb_df, "BBTilmeld")
        playable_std = standardize_dataframe(playable_df, "Playable")

        combined = pd.concat([callme_std, bb_std, playable_std], ignore_index=True)

        output = io.BytesIO()
        combined.to_excel(output, index=False, engine='openpyxl')
        st.success("Filen er genereret!")
        st.download_button(
            label="Download samlet fil (.xlsx)",
            data=output.getvalue(),
            file_name="Danske_Bank_samlet.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )