import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import messaggi
import config

API_TOKEN=config.TOKEN_API
BOT_TOKEN=config.TOKEN_BOT


chat_id=0  #id chat telegram per far inviare i messaggi al bot

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

#funzione per calolare una squadre quante volte ha vinto una competizione
#params: json con tutte le squadre che hanno vinto la competizione, id della squadra di cui vengono ritornate le volte che ha vinto
def count_winner(data, id_squadra):
    count = 0
    for season in data['seasons']:
        if season['winner'] and season['winner']['id'] == id_squadra:
            count += 1
    return count

#funzione per calcolare i trofei di una squadra
#params: id della squadra e lista contenente code e nome della competizione
def get_trofei(id_squadra, comps):
    
    s="" #stringa per i trofei 
    codes = [tup[0] for tup in comps]
    codes.append('CL')  #aggiungo champions league (trofeo europeo)
    codes.append('EC')  #aggiungo europa league (trofeo europeo)
    for code in codes:
        url=f"http://api.football-data.org/v4/competitions/{code}"
        headers = {'X-Auth-Token': API_TOKEN}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            #se richiesta va a buon fine 
            data = response.json()
            if(code =='CL' or code=='EC'):
                s+="🏆🇪🇺"+data['name']+": "+str(count_winner(data,id_squadra))+"\n"
            else:
                s+="🏆"+data['name']+": "+str(count_winner(data,id_squadra))+"\n"
    return s
    
            
        
    
    

#funzione per prendere i trofei vinto nazionali
def get_competizioniNaz(id_area):
    #print(id_squadra+"  "+id_area)
    url="http://api.football-data.org/v4/competitions"
    headers = {'X-Auth-Token': API_TOKEN}
    params = {'areas': id_area}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        #se richiesta va a buon fine 
        data = response.json()
        competitions = data.get('competitions', [])
        competition_info = [(comp['code'], comp['name']) for comp in competitions]
        #print(competition_info)
        return competition_info

    else:
        print(f"Errore {response.status_code}: {response.text}")
        return None
    

#funzione per resituore le squadre di una competizione
def get_squadre_competizione(comp):
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
        print(f"Errore {response.status_code}: {response.text}")
        return None

#funzione per creare i bottoni con i nomi delle squadre params: id della competione    
def crea_bottoni(comp):
    markup = telebot.types.InlineKeyboardMarkup()
    for team in get_squadre_competizione(comp):
        area_id=team[0] #l id dell'area serve per calcolare i trofei della nazione di una squadra
        id_squadra = team[1]
        nome_squadra = team[2]
        btn = telebot.types.InlineKeyboardButton(nome_squadra, callback_data=str(id_squadra)+","+str(area_id))
        markup.add(btn)
    return markup

#funzione per gestire le callback dei bottoni
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    #come call data viene passata una stringa con competizione e id della squadra
    parts = call.data.split(',')
    if len(parts) == 2:
        id_squadra = parts[0]
        id_area = parts[1]
    competizioni=get_competizioniNaz(id_area)
    invia_messaggio(chat_id,get_trofei(id_squadra,competizioni))
       


#"/start"
@bot.message_handler(commands=['start'])
def start_command(message):
    
    bot.send_message(message.chat.id, messaggi.mss_introduzione_bot())    
    global chat_id
    chat_id =message.chat.id
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
    
def invia_messaggio(chat_id,messaggio):
    bot.send_message(chat_id, messaggio)
        
        
# Avvia il bot
bot.polling()