from telethon import TelegramClient, events, sync
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from telethon.sessions import StringSession

from urllib.parse import urlparse, parse_qs
import re

# Use your own values from my.telegram.org
api_id = 27417836
api_hash = '0a8f28bc5d9ba95fb81687b4e59e458b'

session_string = '1BVtsOHoBuyasj-5vyg11HGDpjRUNChOXSTPbkpPGTQ-NzK9r0T-NF48h3fFaEgQiNqjmflilUm-FJ4Ij0YV7ki85zY9MVUBQH797MhesKgMCdCNGXtaBVjG7qvanPCE9RX6rylH3GLwCiULCl_zkDCfwg9BjjwzUjvdnbrUVDH2h96wc1X6JZ61Cmv6tRxu7N7hgR0dvC433vP0yJ55iW5VdtjcxKSiZOhdusJZifq8ZE9nUfRsYoMphPGruUC8H538dVjhL0ew7tRC2WdV_pxRUWpJF-ExFJm5NE6BfhzokPlvDqFausmAFRV7v4XZuoiYgkxmXak5_b_QR4WWTT-o4CEgb33M='

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Replace the channel IDs below with the IDs of the channels you want to monitor
channel_ids = ['homepaa', 'lallantopdealss', 'Flipkart_Shopping_Loots_Deals', 'INDLootDeals', 'indian_shopping_deals_loots']
@client.on(events.NewMessage(chats=channel_ids))
async def handle_new_message(event):
    msg_text = event.message.message
    links= re.findall("(?P<url>https?://[^\s]+)", msg_text)
    for link in links:
        try:
            # follow redirects to get the final URL
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            driver.get(link)
            final_url = driver.current_url

            driver.close()
            # parse the URL to get the domain and query parameters
            parsed_url = urlparse(final_url)
            domain = parsed_url.netloc
            query_params = parse_qs(parsed_url.query)
            # add the affid tag if the domain is flipkart or amazon
            if domain == "www.flipkart.com":
 #               query_params["affid"] = "saurabhpp1"
                 modified_url =f"{parsed_url.scheme}://{domain}{parsed_url.path}"+'?pid='+query_params["pid"][0]+'&affid=saurabhpp1' #               resp= requests.get(modified_u)
#                modified_url= resp.json()['response']['shortened_url']
            elif domain == "www.amazon.in":
#                query_params["tag"] = 'lootdealsfree-21'
                modified_url = f"{parsed_url.scheme}://{domain}{parsed_url.path}"+'?tag=lootdealsfree-21'
            # replace the original link with the modified link in the message text
            msg_text = msg_text.replace(link, modified_url)
        except:
            # if there's an error with the link, just move on to the next one
            pass
    await client.send_message('lootdeals_free', msg_text)
client.start()
client.run_until_disconnected()
