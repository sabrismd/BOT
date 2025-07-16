# main.py
from telethon import TelegramClient, events
import re
from s1 import convert_link
import logging

# Setup logging
logging.basicConfig(filename="log.txt", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

api_id = 27933611
api_hash = '6e0188223ada54e320be697698e4291e'
source_channel = 'https://t.me/roobai24x7'   # without @
target_channel = 'https://t.me/stealkarodev'   # without @

client = TelegramClient('session_name', api_id, api_hash)

def replace_links_in_message(text):
    try:
        links = re.findall(r'https?://\S+', text)
        updated = text

        for link in links:
            if link.startswith("https://amzn.to"):
                logging.info(f"Ignored Amazon link: {link}")
                continue

            new_link = convert_link(link)
            if new_link:
                updated = updated.replace(link, new_link)
            else:
                logging.warning(f"Link could not be converted: {link}")

        return updated
    except Exception as e:
        logging.exception("Failed to replace links in message")
        return text  # fallback: send original

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        message = event.message
        text = message.message or ""
        updated_text = replace_links_in_message(text)

        # If media (photo, document, etc.)
        if message.media:
            await client.send_file(
                target_channel,
                file=message.media,
                caption=updated_text
            )
            logging.info("✅ Media with updated caption sent.")
        else:
            # Text-only message
            await client.send_message(target_channel, updated_text)
            logging.info("✅ Text message sent.")

    except Exception as e:
        logging.exception("❌ Failed to handle or forward message.")

def main():
    try:
        print("🚀 Starting bot...")
        logging.info("Bot started.")
        client.start()
        client.run_until_disconnected()
    except Exception as e:
        logging.exception("Bot crashed.")
        raise

if __name__ == '__main__':
    main()
