import streamlit as st
import json


st.set_page_config(page_title="Kelam Rehberi", page_icon="🔍", layout="wide")

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

data = load_data("kelam_rehberi.json")

if data:
    st.sidebar.title("🔍 Kelam Rehberi")
    search_query = st.sidebar.text_input("Spesifik konu veya kavram ara...", placeholder="Örn: Mîzan, İstıtâat, Rüya...").lower()
    
    bolum_adlari = [f"{b['bolum_no']}. {b['bolum_basligi']}" for b in data['bolumler']]
    
    if not search_query:
        secilen_bolum_adi = st.sidebar.radio("Bölümler", bolum_adlari)
        secilen_index = bolum_adlari.index(secilen_bolum_adi)
        gosterilecek_icerik = [data['bolumler'][secilen_index]]
        is_searching = False
    else:
        is_searching = True
        gosterilecek_icerik = data['bolumler']

    for bolum in gosterilecek_icerik:
        header_printed = False
        detaylar = bolum['detaylar']

        for anahtar, deger in detaylar.items():
            deger_str = str(deger).lower()
            anahtar_str = anahtar.lower()
            
            if not is_searching or (search_query in deger_str or search_query in anahtar_str):
              
                if not header_printed:
                    st.title(bolum['bolum_basligi'])
                    header_printed = True
                
                clean_title = anahtar.replace("_", " ").title()
                st.subheader(f"🔹 {clean_title}")

                if isinstance(deger, list):
                    for item in deger:
                        if isinstance(item, dict):
                            
                            with st.expander(f"📍 {item['ad']}", expanded=True):
                                st.write(item['aciklama'])
                                if "alt_dallar" in item:
                                    for alt in item['alt_dallar']: st.markdown(f"- {alt}")
                        else:
                            st.markdown(f"• {item}")
                elif isinstance(deger, dict):
                    if "liste" in deger:
                        if "tanim" in deger: st.info(deger["tanim"])
                        cols = st.columns(2)
                        for idx, sifat in enumerate(deger["liste"]):
                            s_parca = sifat.split(":")
                            
                            with cols[idx % 2].expander(s_parca[0], expanded=is_searching):
                                st.write(s_parca[1] if len(s_parca) > 1 else "")
                        if "ozel_vurgu" in deger: st.warning(deger["ozel_vurgu"])
                    else:
                        for k, v in deger.items(): st.write(f"**{k.title()}:** {v}")
                else:
                    st.write(deger)
                
                st.divider()

    if is_searching and not header_printed:
        st.warning("Eşleşen bir sonuç bulunamadı.")

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Kaynak: {data['muellif']}")
