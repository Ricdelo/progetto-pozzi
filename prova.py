from telegram.ext import Updater, CommandHandler

# Funzione per gestire il comando /start
def start(update, context):
    update.message.reply_text('ciao')

def main():
    # Inserisci qui il tuo token
    token = '7340572849:AAFERqqSCr5shXnejBgIcpdExFTni8tAPaI'

    # Crea l'Updater e il Dispatcher
    updater = Updater(token)

    # Ottieni il dispatcher per registrare i gestori di comando
    dispatcher = updater.dispatcher

    # Registra il gestore per il comando /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Avvia il Bot
    updater.start_polling()

    # Mantieni il bot in esecuzione fino a quando non viene interrotto
    updater.idle()

if __name__ == '__main__':
    main()
