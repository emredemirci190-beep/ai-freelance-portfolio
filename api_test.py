from google import genai
from google.genai import types
import time

client = genai.Client(api_key="Write your API key here")

# Dosyayı oku ve PARÇALARA BÖLE
with open("techstore_kilavuz.txt", "r", encoding="utf-8") as f:
    icerik = f.read()

# Dökümanı bölümlere ayır (boş satırlardan böl)
parcalar = [p.strip() for p in icerik.split("\n\n") if p.strip()]

print(f"Döküman {len(parcalar)} parçaya bölündü.\n")

def ilgili_parcalari_bul(soru, parcalar):
    """
    Sorudaki kelimeleri parçalarda ara.
    Eşleşen parçaları döndür.
    Bu basit RAG — gerçekte embedding kullanılır.
    """
    soru_kelimeleri = soru.lower().split()
    eslesme_skoru = []
    
    for i, parca in enumerate(parcalar):
        parca_kucuk = parca.lower()
        skor = sum(1 for kelime in soru_kelimeleri if kelime in parca_kucuk)
        eslesme_skoru.append((skor, i, parca))
    
    # En yüksek skorlu 2 parçayı al
    eslesme_skoru.sort(reverse=True)
    en_iyi = [p for skor, i, p in eslesme_skoru[:2] if skor > 0]
    
    return en_iyi

print("Manuel RAG sistemi hazır. Sorularınızı yazın.\n")

while True:
    soru = input("Soru: ")
    if soru.lower() == "quit":
        break
    
    # Adım 1: İlgili parçaları bul
    bulunan_parcalar = ilgili_parcalari_bul(soru, parcalar)
    
    if not bulunan_parcalar:
        print("Cevap: Bu bilgi dokümanda yer almıyor.\n")
        continue
    
    # Adım 2: Sadece o parçaları Gemini'ye gönder
    baglam = "\n\n".join(bulunan_parcalar)
    
    print(f"[RAG: {len(bulunan_parcalar)} parça seçildi — {len(baglam)} karakter gönderiliyor]")
    
    sistem = f"""Sadece aşağıdaki metni kullanarak soruyu cevapla.
Metinde yoksa "Bu bilgi dokümanda yer almıyor" de.

METİN:
{baglam}"""
    
    time.sleep(5)
    
    cevap = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=soru,
        config=types.GenerateContentConfig(
            system_instruction=sistem,
            temperature=0.1
        )
    )
    
    print(f"Cevap: {cevap.text}\n")