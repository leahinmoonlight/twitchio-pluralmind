from typing import TYPE_CHECKING

from pluralmind import ProxiedMessage
from twitchio.ext import commands

from ._types import PluralmindData
from ._user import PluralmindChatter, PluralmindPartialUser
from ._util import get_pluralmind_data

if TYPE_CHECKING:
    from ._bot import PluralmindBotMixin


class PluralmindContext[BotT: PluralmindBotMixin](commands.Context[BotT]):
    @property
    def pluralmind_data(self) -> PluralmindData:
        if (data := get_pluralmind_data(self._payload)) is None:
            raise RuntimeError(
                'PluralmindContext did not find pluralmind data on the payload. Please ensure you are calling await '
                'super().process_commands(payload) if you are overriding process_commands in your bot class.'
            )

        return data

    @property
    def proxied_message(self) -> ProxiedMessage | None:
        return self.pluralmind_data.proxied_message

    @property
    def chatter(self) -> PluralmindChatter | PluralmindPartialUser:
        chatter = super().chatter

        if not isinstance(chatter, (PluralmindChatter, PluralmindPartialUser)):
            raise RuntimeError(
                'Found a non-Pluralmind Chatter/PartialUser on the payload. Please ensure you are calling '
                'await super().process_commands(payload) if you are overriding process_commands in your bot class.'
            )

        return chatter

    @property
    def author(self) -> PluralmindChatter | PluralmindPartialUser:
        return self.chatter
