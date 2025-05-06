from flask import Flask, render_template, request
import requests, datetime, logging, os

aplikacja = Flask(__name__, template_folder="szablony", static_folder="style")


logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # tylko wiadomość, bez poziomu logowania, czasu, modułu itd.
)
logger = logging.getLogger(__name__)

AUTOR = "Joanna Jurkowska"
PORT = int(os.environ.get("PORT", 8080))  
KLUCZ_API = "2abc04c28f6034d8fd49c8819f1bd440"

LOKALIZACJE = {
    "Polska": ["Lublin", "Warszawa", "Wroclaw"],
    "Wlochy": ["Mediolan", "Wenecja", "Bolonia"],
    "Hiszpania": ["Madryt", "Barcelona"]
}

@aplikacja.route('/', methods=['GET', 'POST'])
def strona_glowna():
    pogoda = None
    if request.method == 'POST':
        kraj = request.form.get('kraj')
        miasto = request.form.get('miasto')
        if kraj and miasto:
            pogoda = pobierz_pogode(miasto)
    return render_template('strona.html', miasta=LOKALIZACJE, pogoda=pogoda)

def pobierz_pogode(miasto):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={KLUCZ_API}&units=metric&lang=pl"
    odpowiedz = requests.get(url)
    dane = odpowiedz.json()
    if dane.get("main"):
        return {
            "miasto": miasto,
            "temperatura": dane["main"]["temp"],
            "wilgotnosc": dane["main"]["humidity"],
            "cisnienie": dane["main"]["pressure"],
            "opis": dane["weather"][0]["description"]
        }
    return None

if __name__ == '__main__':
    logger.info(f"Aplikacja uruchomiona: {datetime.datetime.now()}")
    logger.info(f"Autor: {AUTOR}")
    logger.info(f"Nasłuchiwanie na porcie: {PORT}")
    aplikacja.run(host='0.0.0.0', port=PORT)
