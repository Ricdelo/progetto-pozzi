import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import messaggi
import config

BOT_TOKEN = config.TOKEN_BOT
API_TOKEN=config.TOKEN_API

# Crea un'istanza dell'oggetto Bot
bot = telebot.TeleBot(BOT_TOKEN)

def scelta_competionze():
    # Crea la tastiera con i bottoni con le top 5 cinque competizioni
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = telebot.types.KeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿Premier League")
    button2 = telebot.types.KeyboardButton("🇮🇹Seria A")
    button3 = telebot.types.KeyboardButton("🇩🇪Bundesliga")
    button4 = telebot.types.KeyboardButton("🇪🇸La Liga")
    button5 = telebot.types.KeyboardButton("🇫🇷Ligue 1")
    markup.add(button1, button2)
    markup.add(button3,button4,button5)
    return markup

#funzione per prendere i trofei vinto nazionali
def get_frotei_nazionali(id_squadra,id_area):
    url="http://api.football-data.org/v4/competitions"
    headers = {'X-Auth-Token': API_TOKEN}
    params = {'areas': id_area}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        #se richiesta va a buon fine salva tutti i team in una lista
        data = response.json()
    

#funzione per resituore le squadre di una competizione
def competizione(comp):
    base_url = 'https://api.football-data.org/v4/competitions'
    
    url = f'{base_url}/{comp}/teams'
    headers = {'X-Auth-Token': API_TOKEN}
    params = {'season': "2022"} #stagione 2022
    
    response = requests.get(url, headers=headers, params=params)    
    if response.status_code == 200:
        #se richiesta va a buon fine salva tutti i team in una lista
        data = response.json()
        #id dell'area, id della squadra e il nome della squadra
        teams = []
        for team in data['teams']:
            area_id = team['area']['id']
            id_squadra = team['id']
            nome_squadra = team['name']
            teams.append((area_id, id_squadra, nome_squadra))
        return teams
    else:
        # In caso di errore, stampare il codice di stato e il testo della risposta
        print(f"Errore {response.status_code}: {response.text}")
        return None

#funzione per creare i bottoni con i nomi delle squadre params: id della competione    
def crea_bottoni(comp):
    markup = telebot.types.InlineKeyboardMarkup()
    for team in competizione(comp):
        area_id=team[0] #l id dell'area serve per calcolare i trofei della nazione di una squadra
        id_squadra = team[1]
        nome_squadra = team[2]
        btn = telebot.types.InlineKeyboardButton(nome_squadra, callback_data=id_squadra+","+area_id)
        markup.add(btn)
    return markup

#funzione per gestire le callback dei bottoni
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    #come call data viene passata un astringa con competizione e id della squadra
    parts = call.data.split(',')
    if len(parts) == 2:
        id_squadra = parts[0]
        id_area = parts[1]
    get_frotei_nazionali(id_squadra,id_area)   




#"/start"
@bot.message_handler(commands=['start'])
def start_command(message):
    
    bot.send_message(message.chat.id, messaggi.mss_introduzione_bot())    
    bot.send_message(message.chat.id, messaggi.mss_competizione(), reply_markup=scelta_competionze())
    
#scelta competione
@bot.message_handler(func=lambda message: message.text in ["🏴󠁧󠁢󠁥󠁮󠁧󠁿Premier League", "🇮🇹Seria A","🇩🇪Bundesliga","🇪🇸La Liga","🇫🇷Ligue 1"])
def option_selected(message):

    selected_option = message.text
    #quando viene scelta una competizione viene passato l ID a crea_bottoni()
    if selected_option == "🏴󠁧󠁢󠁥󠁮󠁧󠁿Premier League":
        bot.send_message(message.chat.id, messaggi.mss_competizione(), reply_markup=crea_bottoni("PL"))            
    elif selected_option == "🇮🇹Seria A":
        bot.send_message(message.chat.id, messaggi.mss_competizione(), reply_markup=crea_bottoni("SA"))
    elif selected_option == "🇩🇪Bundesliga":
        bot.send_message(message.chat.id, messaggi.mss_competizione(), reply_markup=crea_bottoni("BL1"))
    elif selected_option == "🇪🇸La Liga":
        bot.send_message(message.chat.id, messaggi.mss_competizione(), reply_markup=crea_bottoni("PD"))
    elif selected_option == "🇫🇷Ligue 1":
        bot.send_message(message.chat.id, messaggi.mss_competizione(), reply_markup=crea_bottoni("FL1"))
    
        
        
        
# Avvia il bot
bot.polling()
