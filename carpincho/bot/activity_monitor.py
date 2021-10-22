import json
import re
import string
from collections import Counter

import discord
from carpincho.logger import get_logger

log = get_logger(__name__)


class ActivityMonitor(discord.Client):

    async def on_message(self, message):
        if message.channel.type == discord.ChannelType.private:
            return
        words = self.tokenize_message(message.content)
        counter = Counter(words.split(' '))
        log.info("Message", extra={'channel': message.channel.id,
                                   'author': f"\"{message.author.name}\"",
                                   'words': json.dumps(counter)})

    async def on_raw_reaction_add(self, payload):
        if payload.event_type == 'REACTION_ADD':
            log.info("Reaction",
                     extra={'channel': payload.channel_id,
                            'dmessage': payload.message_id,
                            'user': f"\"{payload.member.name}\"",
                            'emoji': payload.emoji})

    @staticmethod
    def tokenize_message(message):
        # Remove punctuation and other stuff that we don't want to include
        excluded_chars = str.maketrans('', '', string.punctuation + "·¡¿1234567890\\\"")
        words = message.translate(excluded_chars).strip().lower().replace('\n', ' ')
        # Remove duplicated spaces
        words = re.sub(' +', ' ', words)
        # exclude words of two characters or less
        words = ' '.join([w for w in words.split(' ') if len(w) > 2])
        return words
