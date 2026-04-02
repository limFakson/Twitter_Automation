import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import (
    Updater,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CommandHandler,
    ChatMemberHandler,
)
from config.environment import load_environment
from utils.types import Tweet, TweetType
from services.twitter_service import TwitterService
from services.content_service import ContentService
from services.news_service import NewsService
from services.telegram_channel_service import TelegramChannelService

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self):
        self.config = load_environment()
        self.updater = Updater(token=self.config["TELEGRAM_BOT_TOKEN"])
        self.chat_id = self.config["TELEGRAM_CHAT_ID"]
        self.twitter = TwitterService()
        self.content_service = ContentService()
        self.news_service = NewsService()
        self.channel_service = TelegramChannelService()
        self.pending_tweets = {}

        # setup handlers once
        self._setup_handlers()

    def _setup_handlers(self):
        logger.info("Starting Telegram bot service...")
        dp = self.updater.dispatcher
        dp.add_handler(CallbackQueryHandler(self._handle_button_click))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self._handle_text_input))
        dp.add_handler(ChatMemberHandler(self._handle_chat_member, ChatMemberHandler.CHAT_MEMBER))
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("tweet", self.tweeter))
        dp.add_handler(CommandHandler("news", self.news))
        dp.add_handler(CommandHandler("channel", self.channel_post_command))
        dp.add_handler(CommandHandler("analytics", self.analytics_command))
        dp.add_handler(CommandHandler("hashtags", self.hashtag_search_command))
        dp.add_handler(CommandHandler("help", self.help_command))

    def start_bot(self):
        """Starts polling for Telegram updates"""
        self.updater.start_polling(allowed_updates=["message", "callback_query", "chat_member", "my_chat_member"])
        self.updater.idle()
    
    def start(self, update: Update, context: CallbackContext):
        keyboard = [
            [
                InlineKeyboardButton("📝 New Tweet", callback_data="/tweet"),
                InlineKeyboardButton("📢 New Channel Post", callback_data="/channel")
            ],
            [
                InlineKeyboardButton("🔍 Hashtag Search", callback_data="/hashtags"),
                InlineKeyboardButton("📊 Channel Analytics", callback_data="/analytics")
            ],
            [
                InlineKeyboardButton("📰 News", callback_data="/news"),
                InlineKeyboardButton("❓ Help", callback_data="/help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "🤖 **Bot Control Panel**\nChoose an action:", 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    def tweeter(self, update, context):
        """Start the telegram bot service"""
        try:
            tweet = self.content_service.generate_tweet()
            self.send_preview(tweet)

        except Exception as e:
            logger.error(f"Failed to start tweet service: {e}")
            raise

    # --- News Command Handler Version (expects update + context) ---
    def news(self, update: Update, context: CallbackContext):
        """Triggered when user types /news"""
        news_feed = self.news_service.games_news()  # however you get it
        self._send_news(news_feed)

    def channel_post_command(self, update: Update, context: CallbackContext):
        """Trigger generation of a channel post"""
        try:
            tweet = self.content_service.generate_channel_post()
            # Ensure we mark it as a channel post so acceptance sends it to the channel
            tweet.tweet_type = TweetType.CHANNEL_POST 
            self.send_preview(tweet)
        except Exception as e:
            logger.error(f"Failed to generate channel post: {e}")
            context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to generate post.")

    def analytics_command(self, update: Update, context: CallbackContext):
        """Show channel analytics"""
        analytics_text = self.channel_service.get_analytics()
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=analytics_text,
            parse_mode=ParseMode.MARKDOWN
        )

    def hashtag_search_command(self, update: Update, context: CallbackContext):
        """Initiate hashtag search"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🔍 **Hashtag Search**\n\nSend me a keyword to search for trending hashtags (e.g., 'Gaming', 'IndieDev')."
        )
        context.user_data["mode"] = "hashtag_search"

    def _handle_chat_member(self, update: Update, context: CallbackContext):
        """Handle new member joining a channel"""
        # Ensure the update is from the configured channel
        if str(update.effective_chat.id) != str(self.channel_service.channel_id):
            return

        old_status = update.chat_member.old_chat_member.status
        new_status = update.chat_member.new_chat_member.status

        was_member = old_status in ["member", "administrator", "creator", "restricted"]
        is_member = new_status in ["member", "administrator", "creator", "restricted"]

        if not was_member and is_member:
            # User joined
            member = update.chat_member.new_chat_member.user
            self.channel_service.send_welcome_message(member)
        
    # --- Shared sender ---
    def _send_news(self, news_feed):
        try:
            if not news_feed:
                self.updater.bot.send_message(
                    chat_id=self.chat_id,
                    text="No recent news available for now",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return

            for news in news_feed:
                tweet = self.content_service.generate_tweet_news(news)
                self.send_preview(tweet)

        except Exception as e:
            logger.error(f"Error while sending news: {e}")
        
    # Help command
    def help_command(self, update: Update, context: CallbackContext):
        commands = """
        **Available commands:**
        /start - Open Control Panel
        /tweet - Generate Tweet
        /channel - Generate Channel Post
        /hashtags - Search Hashtags
        /analytics - View Channel Stats
        /news - Get latest Game News
        /help - Show this message
        """
        update.message.reply_text(commands, parse_mode=ParseMode.MARKDOWN)

    def stop(self):
        """Stop the telegram bot service"""
        self.updater.stop()
        logger.info("Telegram bot service stopped")

    def send_preview(self, tweet: Tweet):
        """Send tweet preview to Telegram"""
        try:
            keyboard = self._create_keyboard(tweet)
            keyboard = self._create_keyboard(tweet)
            preview = tweet.format_preview()
            
            # Add header to distinguish content
            header = "📢 **Channel Post Preview**" if tweet.tweet_type == TweetType.CHANNEL_POST else "🐦 **Tweet Preview**"
            caption = f"{header}\n\n{preview}"

            if tweet.image_path:
                message = self.updater.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=open(tweet.image_path, "rb"),
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard,
                )
            elif tweet.image_url:
                message = self.updater.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=tweet.image_url,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard,
                )
            else:
                message = self.updater.bot.send_message(
                    chat_id=self.chat_id,
                    text=caption,
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
        # Determine Post button label
        post_label = "✅ Post to Channel" if tweet.tweet_type == TweetType.CHANNEL_POST else "✅ Post to X"

        buttons = [
            [
                InlineKeyboardButton(post_label, callback_data="accept"),
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

        if query.data == "/tweet":
            return self.tweeter(update, context)
        elif query.data == "/channel":
            return self.channel_post_command(update, context)
        elif query.data == "/analytics":
            return self.analytics_command(update, context)
        elif query.data == "/hashtags":
            return self.hashtag_search_command(update, context)
        elif query.data == "/help":
            return self.help_command(update, context)
        elif query.data == "/news":
            return self.news(update, context)
    
        message_id = query.message.message_id
        if message_id not in self.pending_tweets:
            if query.message.photo or query.message.video or query.message.document:
                query.message.reply_text("❌ Error: Data not found (expired/restarted)!")
            else:
                query.edit_message_text(text="❌ Error: Data not found (expired/restarted)!")
            return

        tweet = self.pending_tweets[message_id]

        if query.data == "accept":
            success = False
            # Route to correct service
            if tweet.tweet_type == TweetType.CHANNEL_POST:
                success = self.channel_service.send_post(tweet.content, tweet.image_path, tweet.image_url)
                dest_name = "Channel"
            else:
                success = self.twitter.post_tweet(tweet)
                dest_name = "Twitter"

            if success:
                try:
                    msg_text = f"✅ Successfully posted to {dest_name}!"
                    if query.message.photo or query.message.video or query.message.document:
                        query.message.reply_text(msg_text)
                    else:
                        query.edit_message_text(text=msg_text)
                    
                    del self.pending_tweets[message_id]
                except Exception as e:
                    print(f"Error displaying message \n error-{e}")
            else:
                if query.message.photo or query.message.video or query.message.document:
                     query.message.reply_text(f"❌ Failed to post to {dest_name}. Check logs.")
                else:
                    query.edit_message_text(text=f"❌ Failed to post to {dest_name}. Check logs.")

        elif query.data == "decline":
            if query.message.photo or query.message.video or query.message.document:
                query.message.reply_text("❌ Declined!")
            else:
                query.edit_message_text(text="❌ Declined!")
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

    def _handle_text_input(self, update: Update, context: CallbackContext):
        """Handle text input for Edits and Hashtag Search"""
        mode = context.user_data.get("mode")
        
        if not mode:
            return # Ignore random text if not in a mode

        # Hashtag Search Mode
        if mode == "hashtag_search":
            keyword = update.message.text
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔍 Searching hashtags for '{keyword}'...")
            
            tags = []
            source = "Twitter"
            try:
                tags = self.twitter.search_hashtags(keyword)
            except Exception as e:
                logger.warning(f"Twitter search failed: {e}. Falling back to AI generation.")
            
            if not tags:
                source = "AI Generation (Twitter Search unavailable)"
                tags = self.content_service.suggest_hashtags(keyword)

            if tags:
                response = f"**Top Hashtags for '{keyword}' ({source}):**\n\n" + " ".join(tags)
            else:
                response = f"No hashtags found for '{keyword}'."
            
            context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.MARKDOWN)
            context.user_data.clear() # Exit mode
            return

        # Editing Mode
        if mode in ["edit", "edit_thread", "edit_poll"]:
            message_id = context.user_data.get("editing_message_id")
            if message_id and message_id in self.pending_tweets:
                original_tweet = self.pending_tweets[message_id]
                new_tweet = self.content_service.update_tweet(
                    original_tweet, update.message.text, mode
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
