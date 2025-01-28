import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import (
    Updater,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CommandHandler,
)
from config.environment import load_environment
from utils.types import Tweet, TweetType
from services.twitter_service import TwitterService
from services.content_service import ContentService
from services.news_service import NewsService

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self):
        self.config = load_environment()
        self.updater = Updater(token=self.config["TELEGRAM_BOT_TOKEN"])
        self.chat_id = self.config["TELEGRAM_CHAT_ID"]
        self.twitter = TwitterService()
        self.content_service = ContentService()
        self.news_service = NewsService()
        self.pending_tweets = {}
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up telegram message handlers"""
        dp = self.updater.dispatcher
        dp.add_handler(CallbackQueryHandler(self._handle_button_click))
        dp.add_handler(
            MessageHandler(Filters.text & ~Filters.command, self._handle_edited_tweet)
        )
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("news", self.news))
        dp.add_handler(CommandHandler("tweet", self.tweeter))
        dp.add_handler(CommandHandler("help", self.help_command))

        self.updater.start_polling()
        self.updater.idle()
    
    

    def start(self, update, context):
        keyboard = [
            [InlineKeyboardButton("News", callback_data="get_news")],
            [InlineKeyboardButton("Tweeter", callback_data="tweet")],
            [InlineKeyboardButton("Help", callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Welcome! Choose an option:", reply_markup=reply_markup
        )

    def tweeter(self, update, context):
        """Start the telegram bot service"""
        try:
            logger.info("Starting Telegram bot service...")
            tweet = self.content_service.generate_tweet()
            self.send_preview(tweet)

        except Exception as e:
            logger.error(f"Failed to start Telegram service: {e}")
            raise

    # News command
    def news(self, update, context):
        try:
            logger.info("Starting Telegram bot service...")
            news_feed = self.news_service.games_news()
            
            # If news_feed is none or not exist
            if not news_feed:
                message = self.updater.bot.send_message(
                    chat_id=self.chat_id,
                    text="No recent news available for now",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return
            
            for news in news_feed:
                tweet = self.content_service.generate_tweet_news(news)
                self.send_preview(tweet)

            # self.updater.start_polling()
            # self.updater.idle()

        except Exception as e:
            logger.error(f"Failed to start Telegram service: {e}")
            raise
        
    # Help command
    def help_command(self, update: Update, context: CallbackContext):
        commands = """
        Available commands:
        /start - Start the bot
        /help - Show this help message
        /news - Get the latest news
        /tweet - Generate random tweets from gemini
        """
        update.message.reply_text(commands)

    def stop(self):
        """Stop the telegram bot service"""
        self.updater.stop()
        logger.info("Telegram bot service stopped")

    def send_preview(self, tweet: Tweet):
        """Send tweet preview to Telegram"""
        try:
            keyboard = self._create_keyboard(tweet)
            preview = tweet.format_preview()

            if tweet.image_path:
                message = self.updater.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=open(tweet.image_path, "rb"),
                    caption=preview,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard,
                )
            elif tweet.image_url:
                message = self.updater.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=tweet.image_url,
                    caption=preview,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard,
                )
            else:
                message = self.updater.bot.send_message(
                    chat_id=self.chat_id,
                    text=preview,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard,
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
                InlineKeyboardButton("✅ Post", callback_data="accept"),
                InlineKeyboardButton("❌ Decline", callback_data="decline"),
            ]
        ]

        edit_buttons = []
        if tweet.tweet_type == TweetType.THREAD:
            edit_buttons.append(
                InlineKeyboardButton("📝 Edit Thread", callback_data="edit_thread")
            )
        elif tweet.tweet_type == TweetType.POLL:
            edit_buttons.append(
                InlineKeyboardButton("📊 Edit Poll", callback_data="edit_poll")
            )
        edit_buttons.append(InlineKeyboardButton("✒️ Edit Text", callback_data="edit"))

        buttons.append(edit_buttons)
        return InlineKeyboardMarkup(buttons)

    def _handle_button_click(self, update: Update, context: CallbackContext):
        """Handle button clicks in telegram messages"""
        query = update.callback_query
        query.answer()

        message_id = query.message.message_id
        if message_id not in self.pending_tweets:
            query.edit_message_text(text="Error: Tweet data not found!")
            return

        tweet = self.pending_tweets[message_id]

        if query.data == "accept":
            success = self.twitter.post_tweet(tweet)
            if success:
                try:
                    if query.message.photo or query.message.video or query.message.document:
                        query.message.reply_text("Tweet successfully posted!")
                    else:
                        query.edit_message_text(text="Tweet successfully posted!")
                    
                    del self.pending_tweets[message_id]
                except Exception as e:
                    print(f"Error displaying message \n error-{e}")
            else:
                query.edit_message_text(text="Failed to post tweet. Check logs.")

        elif query.data == "decline":
            if query.message.photo or query.message.video or query.message.document:
                query.message.reply_text("Tweet Declined!")
            else:
                query.edit_message_text(text="Tweet Declined!")
            del self.pending_tweets[message_id]

        elif query.data in ["edit", "edit_thread", "edit_poll"]:
            self._handle_edit_mode(query, context, message_id, query.data)

    def _handle_edit_mode(self, query, context, message_id, edit_type):
        """Handle entering edit mode for tweets"""
        context.user_data["edit_mode"] = edit_type
        context.user_data["editing_message_id"] = message_id

        if edit_type == "edit_thread":
            query.edit_message_text(
                text="Thread Edit Mode:\nSend each tweet of the thread as a separate message.\n"
                "Send /done when finished."
            )
        elif edit_type == "edit_poll":
            query.edit_message_text(
                text="Poll Edit Mode:\nFirst message: Poll question\n"
                "Following messages: Poll options\n"
                "Send /done when finished."
            )
        else:
            query.edit_message_text(text="Edit Mode: Send your new tweet text")

    def _handle_edited_tweet(self, update: Update, context: CallbackContext):
        """Handle edited tweet messages"""
        if "edit_mode" in context.user_data and context.user_data["edit_mode"]:
            edit_type = context.user_data["edit_mode"]
            message_id = context.user_data.get("editing_message_id")

            if message_id and message_id in self.pending_tweets:
                original_tweet = self.pending_tweets[message_id]
                new_tweet = self.content_service.update_tweet(
                    original_tweet, update.message.text, edit_type
                )

                try:
                    context.bot.delete_message(
                        chat_id=update.effective_chat.id, message_id=message_id
                    )
                except Exception as e:
                    logger.warning(f"Failed to delete previous message: {e}")

                # Send new preview
                self.send_preview(new_tweet)

                # Clear edit mode
                context.user_data.clear()
