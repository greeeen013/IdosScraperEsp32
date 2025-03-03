import network
import time
# Konfigurace Wi-Fi připojení
SSID = "YOUR WIFI NAME"
PASSWORD = "YOUR WIFI PASSWORD"

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Připojování k síti...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print("Připojeno:", wlan.ifconfig())

# Připojení k Wi-Fi
connect_wifi(SSID, PASSWORD)

import urequests
import ure



# URL stránky s odjezdy
url = 'https://idos.cz/hradeckralove/odjezdy/vysledky/?f=Muzeum&fc=329003'
debug = 0
debug_sleep = 5

    
def pamet():
    import gc
    # Získání informací o použité paměti
    gc.collect()  # Vynutí garbage collect (uvolnění nepoužívané paměti)
    used_memory = gc.mem_free()  # Získání volné paměti (v bytech)
    total_memory = gc.mem_alloc()  # Získání celkové alokované paměti (v bytech)
    time.sleep(debug_sleep)

    print("Volná paměť:", gc.mem_free()," bytes")  # Vytiskne volnou paměť
    print("Využívaná paměť:", gc.mem_alloc()," bytes")  # Vytiskne celkově alokovanou paměť
    # Pro ESP32 je celková paměť pro data SRAM obvykle kolem 520 KB
    


def fetch_and_process_url(url, skip_bytes=23340, read_bytes=20000, buffer_size=1024):
    """
    Načte data z URL, přeskočí zadaný počet bajtů a načte určený počet znaků.

    Args:
        url (str): URL pro načtení dat.
        skip_bytes (int): Počet bajtů, které se mají přeskočit na začátku.
        read_bytes (int): Počet bajtů, které se mají přečíst po přeskočení.
        buffer_size (int): Velikost bufferu pro postupné čtení.

    Returns:
        str: Načtená a dekódovaná data z URL.
    """
    try:
        # Načtení odpovědi z URL
        response = urequests.get(url)

        # Přeskočení zadaného počtu bajtů
        skipped = 0
        while skipped < skip_bytes:
            to_read = min(buffer_size, skip_bytes - skipped)
            response.raw.read(to_read)
            skipped += to_read

        # Načtení požadovaného počtu bajtů po přeskočení
        data = response.raw.read(read_bytes).decode('utf-8')

        # Zavření spojení
        response.close()

        return data
    except Exception as e:
        # Zpracování případné chyby
        return f"Error while fetching and processing URL: {str(e)}"
    
    
html = fetch_and_process_url(url)



# Práce s daty
if debug == 1:
    print(data)
        

if debug == 1:
    pamet()
    
if debug == 1:
    pamet()
    print("delka html: " + str(len(html)))
    time.sleep(debug_sleep)
    print(type(html))
    time.sleep(debug_sleep/5)
    print("html zdroj:")
    time.sleep(debug_sleep/5)
    print(html)
    time.sleep(debug_sleep)

def remove_diacritics(s):
    """Převede znaky s diakritikou na znaky bez diakritiky."""
    replacements = {
        "á": "a", "č": "c", "ď": "d", "é": "e", "ě": "e", "í": "i", "ň": "n",
        "ó": "o", "ř": "r", "š": "s", "ť": "t", "ú": "u", "ů": "u", "ý": "y", "ž": "z",
        "Á": "A", "Č": "C", "Ď": "D", "É": "E", "Ě": "E", "Í": "I", "Ň": "N",
        "Ó": "O", "Ř": "R", "Š": "S", "Ť": "T", "Ú": "U", "Ů": "U", "Ý": "Y", "Ž": "Z",
        "&#201;": "E","&#193;": "A", "&#205;": "I", "&#225;": "a", "&#233;": "e", "&#237;": "i"
    }
    for original, replacement in replacements.items():
        s = s.replace(original, replacement)
    return s

def html_unescape(s):
    # Nahrazení známých entit ručně
    s = s.replace("&#201;", "É")
    s = s.replace("&#193;", "Á")
    s = s.replace("&#205;", "Í")
    s = s.replace("&#225;", "á")
    s = s.replace("&#233;", "é")
    s = s.replace("&#237;", "í")
    s = s.replace("&amp;", "&")
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", "\"")
    s = s.replace("&apos;", "'")
    # Přidejte další entity podle potřeby
    return s

def extract_tags_with_span(string):
    results = []
    start_index = 0  # Počáteční index pro hledání

    while True:
        # Najdi začátek a konec dalšího tagu <span>
        start_index = string.find('<span title="proj&#237;žd&#237; přes" class="color-lightgrey">', start_index)
        if start_index == -1:
            if debug == 1:
                print("Nenalezen žádný další <span> tag.")  # Debug
                time.sleep(debug_sleep)
            break  # Pokud už nejsou žádné další tagy, ukonči smyčku

        end_index = string.find("</span>", start_index)
        if end_index == -1:
            if debug == 1:
                print("Chybí ukončovací </span> tag.")  # Debug
                time.sleep(debug_sleep)
            break

        # Debug: Výpis pozic nalezeného tagu
        if debug == 1:
            print(f"Start index: {start_index}, End index: {end_index}") # debug
            time.sleep(debug_sleep/10)

        # Extrahuj obsah tagu mezi značkami
        content = string[start_index + string[start_index:].find(">") + 1:end_index]
        content = html_unescape(content)  # Dekódování HTML entit
        results.append(content)
        
        # Posuň index za aktuální nalezený tag
        start_index = end_index + 7

    return results

def extract_tags_with_style(string):
    results = []
    start_index = 0  # Počáteční index pro hledání

    while True:
        # Najdi začátek a konec dalšího tagu <h3 style=...>
        start_index = string.find('<h3 style="', start_index)
        end_index = string.find("</h3>", start_index)
        
        if start_index == -1 or end_index == -1:
            break  # Pokud už nejsou žádné další tagy, ukonči smyčku
        
        # Extrahuj obsah tagu mezi značkami
        content = string[start_index + string[start_index:].find(">") + 1:end_index]
        content = html_unescape(content)  # Dekódování HTML entit
        results.append(content)
        
        # Posuň index za aktuální nalezený tag
        start_index = end_index + 5
    
    return results

# Funkce pro extrakci obsahu běžných <h3> tagů
def extract_all_h3_contents(string):
    results = []
    start_index = 0  # Počáteční index pro hledání

    while True: # pokud chceme menší pocet zmenime cislo
        # Najdi začátek a konec dalšího tagu
        start_index = string.find("<h3>", start_index)
        end_index = string.find("</h3>", start_index)
        
        if start_index == -1 or end_index == -1:
            break  # Pokud už nejsou žádné tagy, ukonči smyčku
        
        # Posuň začátek o délku tagu "<h3>" a extrahuj obsah
        content = string[start_index + 4:end_index]
        content = html_unescape(content)
        results.append(content)
        
        # Posuň index za aktuální tag
        start_index = end_index + 5
    
    return results

# Použití funkce
styled_contents = extract_tags_with_style(html)
extracted_contents = extract_all_h3_contents(html)
span_contents = extract_tags_with_span(html)


# definovani oled
from machine import Pin, SoftI2C
import ssd1306
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

if extracted_contents:
    print("Extrahované texty:")
    for i in range(0, len(extracted_contents), 2):
        # Získání aktuální styled_content a span_content
        styled_content = styled_contents[i // 2] if i // 2 < len(styled_contents) else ""
        span_content = span_contents[i // 2] if i // 2 < len(span_contents) else ""
        first = extracted_contents[i]
        second = extracted_contents[i + 1] if i + 1 < len(extracted_contents) else ""
        # Odstranění nových řádků a mezer z span_content
        span_content = span_content.replace("\n", " ").replace("\r", " ").strip() if span_content else ""
        # Výpis ve formátu styled | h3_1 | h3_2 | span
        oled.text('autobusy', 0, 0)
        oled.text('--------------', 0, 10)
        clean_text=remove_diacritics(styled_content.strip())
        oled.text(clean_text, 0, 20)
        clean_text=remove_diacritics(first.strip())
        oled.text(clean_text, 0, 30)
        oled.text(clean_text[16:], 0, 40)
        clean_text=remove_diacritics(second.strip())
        oled.text(clean_text, 0, 50)
        oled.show()
        time.sleep(2)
        oled.fill(0)
        oled.show()
        print(f"{styled_content.strip()} | {first.strip()} | {second.strip()} | přes {span_content[18:]}")
else:
    print("Nebyly nalezeny žádné značky <h3>.")

