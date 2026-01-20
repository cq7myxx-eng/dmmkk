import streamlit as st
from supabase import create_client, Client

# --- KONFIGURACJA SUPABASE ---
# Te dane znajdziesz w Project Settings -> API w Supabase
URL = "TWOJ_SUPABASE_URL"
KEY = "TWOJ_SUPABASE_ANON_KEY"
supabase: Client = create_client(URL, KEY)

st.set_page_config(page_title="Magazyn Streamlit", layout="wide")

## --- FUNKCJE ---
def pobierz_produkty():
    response = supabase.table("produkty").select("*").execute()
    return response.data

def dodaj_produkt(nazwa, ilosc, cena):
    supabase.table("produkty").insert({"nazwa": nazwa, "ilosc": ilosc, "cena": cena}).execute()

def usun_produkt(id_produktu):
    supabase.table("produkty").delete().eq("id", id_produktu).execute()

## --- INTERFEJS UŻYTKOWNIKA ---
st.title("📦 System Zarządzania Magazynem")

# Sidebar - Dodawanie produktów
with st.sidebar:
    st.header("Dodaj nowy produkt")
    nazwa = st.text_input("Nazwa produktu")
    ilosc = st.number_input("Ilość", min_value=0, step=1)
    cena = st.number_input("Cena (PLN)", min_value=0.0, step=0.01)
    
    if st.button("Dodaj do bazy"):
        if nazwa:
            dodaj_produkt(nazwa, ilosc, cena)
            st.success(f"Dodano: {nazwa}")
            st.rerun()
        else:
            st.error("Podaj nazwę produktu!")

# Widok główny - Tabela produktów
produkty = pobierz_produkty()

if produkty:
    # Wyświetlamy dane w ładnej tabeli
    st.subheader("Aktualny stan magazynowy")
    
    # Przekształcenie do tabeli z przyciskiem usuwania
    for p in produkty:
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
        col1.write(f"ID: {p['id']}")
        col2.write(f"**{p['nazwa']}**")
        col3.write(f"Ilość: {p['ilosc']}")
        col4.write(f"Cena: {p['cena']} zł")
        
        if col5.button("Usuń", key=f"del_{p['id']}"):
            usun_produkt(p['id'])
            st.rerun()
        st.divider()
else:
    st.info("Magazyn jest pusty. Dodaj pierwszy produkt w panelu bocznym.")
