import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
from config.environment import load_environment
from content.types import Tweet, TweetType
from services.twitter_service import TwitterService

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.config = load_environment()
        self.updater = Updater(token=self.config["TELEGRAM_BOT_TOKEN"])
        self.chat_id = self.config["TELEGRAM_CHAT_ID"]
        self.twitter = TwitterService()
        self.pending_tweets = {}
    
    def send_preview(self, tweet: Tweet):
        """Send tweet preview to Telegram"""
        try:
            keyboard = self._create_keyboard(tweet)
            preview = tweet.format_preview()
            
            if tweet.image_path:
                message = self.updater.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=open(tweet.image_path, 'rb'),
                    caption=preview,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard
                )
            else:
                message = self.updater.bot.send_message(
                    chat_id=self.chat_id,
                    text=preview,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard
                )
            
            if message:
                self.pending_tweets[message.message_id] = tweet
                logger.info(f"Preview sent for tweet type: {tweet.tweet_type}")
        
        except Exception as e:
            logger.error(f"Failed to send preview: {e}")
    
    def _create_keyboard(self, tweet: Tweet) -> InlineKeyboardMarkup:
        """Create appropriate keyboard based on tweet type"""
        buttons = [
            [
                InlineKeyboardButton("✅ Post", callback_data='accept'),
                InlineKeyboardButton("❌ Decline", callback_data='decline')
            ]
        ]
        
        edit_buttons = []
        if tweet.tweet_type == TweetType.THREAD:
            edit_buttons.append(InlineKeyboardButton("📝 Edit Thread", callback_data='edit_thread'))
        elif tweet.tweet_type == TweetType.POLL:
            edit_buttons.append(InlineKeyboardButton("📊 Edit Poll", callback_data='edit_poll'))
        edit_buttons.append(InlineKeyboardButton("✒️ Edit Text", callback_data='edit'))
        
        buttons.append(edit_buttons)
        return InlineKeyboardMarkup(buttons)