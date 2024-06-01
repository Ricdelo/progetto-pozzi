import telebot
import requests
import messaggi

BOT_TOKEN = "7340572849:AAFERqqSCr5shXnejBgIcpdExFTni8tAPaI"
API_TOKEN="5e4ce336b55348c4bb710f846eb4e5af"

# Crea un'istanza dell'oggetto Bot
bot = telebot.TeleBot(BOT_TOKEN)

def scelta_competionze():
    # Crea la tastiera con i bottoni
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = telebot.types.KeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿Premier League")
    button2 = telebot.types.KeyboardButton("🇮🇹Seria A")
    button3 = telebot.types.KeyboardButton("🇩🇪Bundesliga")
    button4 = telebot.types.KeyboardButton("🇪🇸La Liga")
    button5 = telebot.types.KeyboardButton("🇫🇷Ligue 1")
    markup.add(button1, button2)
    markup.add(button3,button4,button5)
    return markup

#funzione per resituore le squadre di una competizione
def competizione(comp):
    base_url = 'https://api.football-data.org/v4/competitions'
    
    url = f'{base_url}/{comp}/teams'
    headers = {'X-Auth-Token': API_TOKEN}
    params = {'season': "2022"}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        # Se la richiesta è stata fatta con successo, processare i dati
        data = response.json()
        team_names = [team['name'] for team in data['teams']]
        return team_names
    else:
        # In caso di errore, stampare il codice di stato e il testo della risposta
        print(f"Errore {response.status_code}: {response.text}")
        return None

#funzione per creare i bottoni con i nomi delle squadre params: id della competione    
def crea_bottoni(comp):
    markup = telebot.types.InlineKeyboardMarkup()
    for team in competizione(comp):
        btn = telebot.types.InlineKeyboardButton(team, callback_data="btn")
        markup.add(btn)
    return markup

#funzione per gestire le callback dei bottoni
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "btn1":
        bot.answer_callback_query(call.id, "Hai premuto Bottone 1")
    elif call.data == "btn2":
        bot.answer_callback_query(call.id, "Hai premuto Bottone 2")
    elif call.data == "btn3":
        bot.answer_callback_query(call.id, "Hai premuto Bottone 3")   




#"/start"
@bot.message_handler(commands=['start'])
def start_command(message):
    
    bot.send_message(message.chat.id, messaggi.mss_introduzione_bot())    
    bot.send_message(message.chat.id, messaggi.mss_competizione(), reply_markup=scelta_competionze())
    
#scelta competione
@bot.message_handler(func=lambda message: message.text in ["🏴󠁧󠁢󠁥󠁮󠁧󠁿Premier League", "🇮🇹Seria A","🇩🇪Bundesliga","🇪🇸La Liga","🇫🇷Ligue 1"])
def option_selected(message):

    selected_option = message.text
     
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
