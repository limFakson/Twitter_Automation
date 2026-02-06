import logging
import telegram
from config.environment import load_environment

logger = logging.getLogger(__name__)

class TelegramChannelService:
    def __init__(self):
        self.config = load_environment()
        self.bot = telegram.Bot(token=self.config["TELEGRAM_BOT_TOKEN"])
        self.channel_id = self.config.get("TELEGRAM_CHANNEL_ID")

    def send_post(self, content, media_path=None, media_url=None):
        """Send a post to the Telegram Channel"""
        if not self.channel_id:
            logger.error("TELEGRAM_CHANNEL_ID not set in environment.")
            return False

        try:
            if media_path:
                with open(media_path, "rb") as photo:
                    self.bot.send_photo(
                        chat_id=self.channel_id,
                        photo=photo,
                        caption=content,
                        parse_mode=telegram.ParseMode.MARKDOWN
                    )
            elif media_url:
                 self.bot.send_photo(
                    chat_id=self.channel_id,
                    photo=media_url,
                    caption=content,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
            else:
                self.bot.send_message(
                    chat_id=self.channel_id,
                    text=content,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
            return True
        except Exception as e:
            logger.error(f"Failed to post to channel: {e}")
            return False

    def get_analytics(self):
        """Get basic channel analytics (member count)"""
        if not self.channel_id:
            return "Channel ID not configured."

        try:
            count = self.bot.get_chat_member_count(chat_id=self.channel_id)
            chat = self.bot.get_chat(chat_id=self.channel_id)
            title = chat.title
            return f"📊 **Channel Analytics**\n\n**Name:** {title}\n**Subscribers:** {count}"
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            if "Chat not found" in str(e):
                 return "❌ **Error: Channel not found.**\n\n1. Check `TELEGRAM_CHANNEL_ID` in `.env`.\n2. Ensure the Bot is an **Administrator** in the channel."
            return f"Error fetching analytics: {e}"
