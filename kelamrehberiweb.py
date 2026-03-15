import streamlit as st
import json


st.set_page_config(
    page_title="Kelam Rehberi - Mâtürîdiyye Akaidi",
    page_icon="🔍",
    layout="wide"
)


def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Hata: '{file_path}' dosyası bulunamadı.")
        return None

data = load_data("kelam_rehberi.json")

if data:
    
    st.sidebar.title("🔍 Kelam Rehberi")
    
    
    search_query = st.sidebar.text_input("Rehberde Ara...", placeholder="Örn: Tekvin, Akıl, Rızık...")
    
    st.sidebar.markdown("---")
    
    
    bolum_adlari = [f"{b['bolum_no']}. {b['bolum_basligi']}" for b in data['bolumler']]
    
    if not search_query:
        secilen_bolum_adi = st.sidebar.radio("Bölümler", bolum_adlari)
        secilen_index = bolum_adlari.index(secilen_bolum_adi)
        gosterilecek_bolumler = [data['bolumler'][secilen_index]]
    else:
     
        gosterilecek_bolumler = []
        for b in data['bolumler']:
           
            bolum_metni = str(b).lower()
            if search_query.lower() in bolum_metni:
                gosterilecek_bolumler.append(b)
        
        if not gosterilecek_bolumler:
            st.sidebar.warning("Sonuç bulunamadı.")

    
    if search_query:
        st.info(f"'{search_query}' için {len(gosterilecek_bolumler)} sonuç listeleniyor...")

    for bolum in gosterilecek_bolumler:
        with st.container():
            st.title(bolum['bolum_basligi'])
            detaylar = bolum['detaylar']

            for anahtar, deger in detaylar.items():
                clean_title = anahtar.replace("_", " ").title()
                
               
                st.subheader(f"🔹 {clean_title}")

                if isinstance(deger, list):
                    for item in deger:
                        if isinstance(item, dict): 
                            with st.expander(f"📍 {item['ad']}", expanded=True):
                                st.write(item['aciklama'])
                                if "alt_dallar" in item:
                                    for alt in item['alt_dallar']:
                                        st.markdown(f"- {alt}")
                        else:
                            st.markdown(f"• {deger if isinstance(deger, str) else item}")

                elif isinstance(deger, dict):
                    if "liste" in deger:
                        if "tanim" in deger: st.info(deger["tanim"])
                        sifatlar = deger["liste"]
                        cols = st.columns(2)
                        for idx, sifat in enumerate(sifatlar):
                            col = cols[idx % 2]
                            s_parca = sifat.split(":")
                            with col.expander(s_parca[0]):
                                st.write(s_parca[1] if len(s_parca) > 1 else "")
                        if "ozel_vurgu" in deger: st.warning(deger["ozel_vurgu"])
                    else:
                        for k, v in deger.items():
                            st.write(f"**{k.title()}:** {v}")
                else:
                    st.write(deger)
                
                st.divider()

    
    st.sidebar.markdown(f"---")
    st.sidebar.caption(f"Kaynak: {data['muellif']} - {data['kitap_adi']}")

else:
    st.error("Veri yüklenemedi.")