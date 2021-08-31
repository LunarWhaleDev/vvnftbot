#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging
from uuid import uuid4
import requests
import json
import pickledb
from telegram import InlineQueryResultArticle, InlineQueryResultGif, InlineQueryResultPhoto, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from blacklist import get_blacklist

TOKEN "token from BotFather"

db = pickledb.load("bot.db", True)
if not db.get("tokens"):
    db.set("tokens", [])
dblist = db.get("tokens")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("This is an inline bot. Use anywhere, in any group. Start your search by entering '@vvnftbot' followed by your search parameter. This bot supports NFT ID numbers as well as metadata text. Please note, the search is case sensitive.\n\n\nTry the following:\n@vvnftbot 15734\n@vvnftbot Asterion\n@vvnftbot Gods\n@vvnftbot Apollo\n@vvnftbot Titan\n@vvnftbot Olympian\n@vvnftbot Boreas\n@vvnftbot Notus\n@vvnftbot Hades\n@vvnftbot Arcadia\n@vvnftbot Berserk\n@vvnftbot Coddle Pets\n\nDeveloped by @floydvulcan")

def startjob(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Starting JobQueue!')
    context.job_queue.run_repeating(getdb, 43200)
    update.effective_chat.send_message("Job Started!")

def updatedb(update: Update, context: CallbackContext):
    getdb(context)
    update.message.reply_text("DB Updated!")

def getdb(context):
    api = "http://api.vulcanforged.com/getAllArts"
    r = requests.get(api)
    data = json.loads(r.text)
    list = data['data']
    print("Tokens: ", len(list))
    blacklist = get_blacklist()
    print("Blacklist: ", len(blacklist))
    for a in blacklist:
        for token in list:
            if a == token['id']:
                list.remove(token)
    print("Updated Tokens: ", len(list))
    global dblist
    dblist = list
    db.set("tokens", dblist)

def build_default(update, context):
    list = {'Vulcanites': ['Tomyios', 'Aelio', 'Thunder', 'Kopis', 'Asterion', 'Phearei', 'Alpha', 'Soter', 'Velosina', 'Chiron', 'Venomtail', 'Syna', 'Chthonius', 'Nemean', 'Numatox', 'Wolfshadow', 'Trapjaw', 'Medusa', 'Lost Shade', 'Blubberjaw', 'Charon'],
            'Boreas': ['Tomyios', 'Aelio', 'Thunder', 'Kopis', 'Asterion'],
            'Arcadia': ['Phearei', 'Alpha', 'Soter', 'Velosina', 'Chiron'],
            'Notus': ['Venomtail', 'Syna', 'Chthonius', 'Nemean', 'Numatox'],
            'Hades': ['Wolfshadow', 'Trapjaw', 'Medusa', 'Lost Shade', 'Blubberjaw', 'Charon'],
            'Gods': ['Zeus', 'Poseidon', 'Ares', 'Hermes', 'Apollo', 'Aphrodite', 'Hera', 'Demeter', 'Cronus', 'Hyperion', 'Coeus', 'Crius', 'Iapetus', 'Oceanus', 'Rhea', 'Tethys'],
            'Olympian': ['Zeus', 'Poseidon', 'Ares', 'Hermes', 'Apollo', 'Aphrodite', 'Hera', 'Demeter'],
            'Titan': ['Cronus', 'Hyperion', 'Coeus', 'Crius', 'Iapetus', 'Oceanus', 'Rhea', 'Tethys'],
            'Death Dealer': ['The Death Dealer', 'Helm of the Death Dealer', 'Sword of the Death Dealer', 'Shield of the Death Dealer'],
            'Berserk': ['Sunfire Strike', 'Velosina of the Sacred Stables', 'Gift of the Great Green Ones', 'Snares of the Fae', 'Stranglevines', 'Summer Palace', 'Pipes of Pan', 'Centaur Warband', 'Summer Storms', 'Bushwhack Wolf', 'The Fortress of Winds', 'The Breath of Boreas', "Hippolyta's Bow", 'Panoply of Minos', 'Hilltop Fort of the Amazons', 'Claws of the Harpy', 'Cantankerous Mammoth', 'Sudden Snowdrifts', 'Rip and Rend', 'Cyclops Rock Rain', 'Edge of Night', 'Cerberus, Hound of Hades', 'Funeral Barge of Acheron', 'A Storm of Strix', 'The Hymn of Thanatos', 'A Mustering of Souls', 'Sepurchral Armour', 'Javelins of Thanatos', 'Trapjaw Berserk', 'Shade Warrior', 'Blood of the Cockatrice', 'Myrmidon Warrior', 'Shield of Achilles', 'The Spear of Achilles', 'Sandstorm', 'Scorpion Stance', 'Venomtail Berserk', 'Desert Winds', 'Storm Surge', 'The Ones Who Drink'],
            'Coddlepets': ['Oversizedhat', 'Kaida', 'Iseran', 'Wyvernie', 'Mergess', 'Lavender', 'Spudfire', 'Skandy', 'Bleu', 'Khione', 'Zeekeez', 'Ash', 'Jade', 'Aquadra', 'Ember', 'Comet', 'Eira', 'Podgy', 'Lotus', 'Chase', 'Farasha', 'Aye-aye', 'Salana', 'Fleta', 'Yukio', 'Augino OG', 'Pink Juni Leaf', 'Blue Juni Leaf'],
            'GeoCats': ['Machine Cat', '0xoplasma Felidae', 'NONACO, 2020 Long-Cat', 'King Lasagne', 'Maneki Model #9', 'NONACO Fancy Edition', 'Ta Miu, Crown Prince Thutmose', 'GeoKitten', 'Viking GeoCat', 'Catstronaut', 'Shinobi', 'NeoCat', 'Hypercat', 'Ancient Sphinx', 'AvoCato', 'Solar Cat', 'Lunar Cat', 'Cowboy Cat', 'Mushroom Cat', 'Yule Cat - 2020 ', 'Yule Cat - 2020 Luxury Edition', 'GeoKey', 'OG Catnip', 'Chimera', "Felidsalia Felidsalis, the Cat O' War", 'Garbatage', 'AffoGato']}
    for group in list:
        results = []
        groupitems = list[group]
        for token in groupitems:
            text, ipfs = nft(token)
            results.append([token, ipfs, text])
        print(f"{group} items: {len(results)}")
        list[group] = results
    for key, value in list.items():
        print(f"{key}: {len(value)} successfully added.")
    db.set("list", list)

def nft(id):
    text = ""
    count = 0
    image = "none"
    if id.isdigit():
        for a in dblist:
            count = count + 1
            if int(id) == a['id']:
                data = json.loads(a['ipfs_data_json'])
                text = f"NFT {id}\n"
                for key, value in data.items():
                    text = f"{text}{key} : {value}\n"
                try:
                    image = data['image']
                except:
                    pass
    else:
        count1 = 0
        text1 = ""
        for a in dblist:
            count = count + 1
            data = json.loads(a['ipfs_data_json'])
            for key, value in data.items():
                if id == 'Hippolytas Bow':
                    id = 'Hippolyta’s Bow'
                id = id.lower()
                if isinstance(value, str) == True:
                    value = value.lower()
                if (value == id and id != 'hermes' and id != 'trapjaw' and id != 'lost shade' and id != 'venomtail' and id != 'zeus') or (value == id and id == 'lost shade' and data['dappid'] == 3) or (value == 'venomtail' and id == 'venomtail berserk' and data['dappid'] == 11) or (value == id and id == 'venomtail' and data['dappid'] == 3) or (value == id and id == "trapjaw" and data['dappid'] == 3) or (value == 'trapjaw' and id == 'trapjaw berserk' and data['dappid'] == 11) or (value == id and id == 'hermes' and data['dappid'] == 8) or (value == id and id == 'zeus' and data['dappid'] != 0):
                    count1 = count1 + 1
                    if (count1 == 1 and id != 'fleta' and id != 'eira' and id != 'javelins of thanatos') or (count1 == 4 and id == 'javelins of thanatos') or (count1 == 4 and id == 'eira') or (count1 == 5 and id == 'fleta'):
#                        print(a['id'])
                        try:
                            image = data['image']
                        except:
                            pass
                        for key, value in data.items():
                            text1 = f"{text1}{key} : {value}\n"
                    text = f"{text1}\nEstimated NFT Matches: {count1}"
    if text != "":
        text = f"{text}\nTotal number of VF NFTs: {count}"
    if text == "":
        text = "none"
    if image != "none":
        ipfs = f"https://cloudflare-ipfs.com/ipfs/{image}"
    if image == "none":
        ipfs = "https://vulcannfts.com/w/images/c/c8/OG_jimi-x_appreciation.jpg"

    return text, ipfs

def inlinequery(update: Update, context: CallbackContext):
    query = update.inline_query.query

    results = []
    list = db.get("list")
    if query == "":
        query = "Vulcanites"
    if query.lower == "coddle pets":
        query = "coddlepets"
    for group in list:
        if query.lower() == group.lower():
            groupitems = list[group]
            for token in groupitems:
                results.append(
                    InlineQueryResultPhoto(
                        id=str(uuid4()),
                        title=token[0],
                        photo_url=token[1],
                        thumb_url=token[1],
                        caption=token[2],
                    )
                )
        if query.lower() == "geocats":
            results = []
            groupitems = list['GeoCats']
            for token in groupitems:
                results.append(
                    InlineQueryResultGif(
                        id=str(uuid4()),
                        title=token[0],
                        gif_url=token[1],
                        thumb_url=token[1],
                        caption=token[2],
                        thumb_mime_type='image/gif',
                    )
                )

    if results == []:
        text, ipfs = nft(query)
        if text == "none":
            return
        else:
            results = [
                InlineQueryResultPhoto(
                    id=str(uuid4()),
                    title=query,
                    photo_url=ipfs,
                    thumb_url=ipfs,
                    caption=text,
                ),
            ]

    update.inline_query.answer(results, timeout=3000)

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("startjob", startjob))
    dispatcher.add_handler(CommandHandler("updatedb", updatedb))
    dispatcher.add_handler(CommandHandler("build", build_default))
#    dispatcher.add_handler(CommandHandler("test", test))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

