from telegram.ext import Updater, CommandHandler

# Funzione per gestire il comando /start
def start(update, context):
    update.message.reply_text('Ciao!')

def main():
    # Inserisci qui il token del tuo bot
    token = '7340572849:AAFERqqSCr5shXnejBgIcpdExFTni8tAPaI'

    # Crea l'Updater con il token del bot
    updater = Updater(token)

    # Ottieni il dispatcher per registrare i gestori di comando
    dispatcher = updater.dispatcher

    # Registra il gestore per il comando /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Avvia il bot
    updater.start_polling()

    # Mantieni il bot in esecuzione fino a quando non viene interrotto
    updater.idle()

if __name__ == '__main__':
    main()
