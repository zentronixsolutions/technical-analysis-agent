import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
TELEGRAM_BOT_TOKEN = "7726352331:AAHnjJ8hBiTZTNA1G0T-8Je6aOJ30AMcoQM"

API_URL = "http://localhost:5000/analyze"    # Change this to your API endpoint

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    logger.info(f"User {update.effective_user.id} started the bot")
    await update.message.reply_text(
        "👋 Welcome! Send me a message and I'll process it through the API."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /help command"""
    await update.message.reply_text(
        "Send any message to me, and I'll forward it to the API and return the response."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for all text messages"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    logger.info(f"Received message from User {user_id}: {message_text}")
    
    # Send a "typing" action to show the bot is processing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Let user know we're processing
    status_message = await update.message.reply_text("Processing your request... please wait.")
    
    try:
        # Send request to API
        logger.info(f"Sending request to API: {message_text}")
        response = requests.post(
            API_URL,
            json={"query": message_text},
            timeout=30  # Timeout after 30 seconds
        )
        
        # Handle API response
        if response.status_code == 200:
            api_response = response.json()
            logger.info(f"API response received: {api_response}")
            
            # Get the main response text (adjust based on your API's response structure)
            result_text = api_response.get("response", 
                       api_response.get("result", 
                       api_response.get("data", 
                       api_response.get("analysis", "No specific response field found."))))
            
            # Delete the "processing" message
            await status_message.delete()
            
            # Send the API response back to the user
            await update.message.reply_text(result_text)
            
            # If there are other fields in the response you want to handle (like images, files, etc.)
            # you can add specific handling for them here
            
        else:
            error_msg = f"API returned error code {response.status_code}"
            logger.error(error_msg)
            await status_message.edit_text(f"⚠️ {error_msg}")
            
    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        await status_message.edit_text("⚠️ The API request timed out. Please try again later.")
    
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to API")
        await status_message.edit_text("⚠️ Could not connect to the API. Is it running?")
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await status_message.edit_text(f"⚠️ An error occurred: {str(e)}")

def main():
    """Start the bot"""
    logger.info("Starting bot...")
    
    # Create the Application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    logger.info("Bot started, polling for messages...")
    application.run_polling()

if __name__ == "__main__":
    main()