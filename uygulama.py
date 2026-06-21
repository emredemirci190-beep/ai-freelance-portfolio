import streamlit as st
from google import genai
from google.genai import types
import time

# ── SAYFA AYARI ──────────────────────────────
st.set_page_config(page_title="Döküman Asistanı", page_icon="📄")
st.title("📄 Döküman Analiz Asistanı")
st.caption("Bir metin dosyası yükle, sorularını sor.")

# ── API BAĞLANTISI ────────────────────────────
client = genai.Client(api_key="Write your API key here")

# ── DOSYA YÜKLEYİCİ ──────────────────────────
yuklenen = st.file_uploader("Metin dosyası seç (.txt)", type="txt")

if yuklenen is not None:
    icerik = yuklenen.read().decode("utf-8")
    icerik = icerik.replace("\r\n", "\n")
    parcalar = [p.strip() for p in icerik.split("\n\n") if len(p.strip()) > 50]
    st.success(f"✓ Dosya yüklendi — {len(parcalar)} bölüm bulundu.")

    # ── SORU KUTUSU ──────────────────────────
    soru = st.text_input("Sorunuzu yazın:")

    if st.button("Sor") and soru:
        # RAG: ilgili parçaları bul
        soru_kelimeleri = soru.lower().split()
        skorlar = []
        for parca in parcalar:
            skor = sum(1 for k in soru_kelimeleri if k in parca.lower())
            skorlar.append((skor, parca))
        skorlar.sort(reverse=True)
        secilen = [p for s, p in skorlar[:2] if s > 0]

        if not secilen:
            st.warning("Bu bilgi dokümanda yer almıyor.")
        else:
            baglam = "\n\n".join(secilen)
            sistem = f"""Sadece aşağıdaki metni kullanarak soruyu cevapla.
Metinde yoksa 'Bu bilgi dokümanda yer almıyor' de.

METİN:
{baglam}"""

            with st.spinner("Yanıt üretiliyor..."):
                time.sleep(5)
                cevap = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=soru,
                    config=types.GenerateContentConfig(
                        system_instruction=sistem,
                        temperature=0.1
                    )
                )

            st.markdown("### Cevap")
            st.write(cevap.text)

            with st.expander("Hangi bölümler kullanıldı?"):
                for i, p in enumerate(secilen, 1):
                    st.text(f"Bölüm {i}:\n{p[:200]}...")