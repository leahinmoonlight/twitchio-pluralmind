from typing import TYPE_CHECKING, Any

from pluralmind import AsyncPluralmindClient, get_proxied_message
from twitchio.ext import commands
from twitchio.models import ChatMessage

from ._context import PluralmindContext
from ._types import PluralmindData, TwitchIOPayload
from ._user import PluralmindChatter, PluralmindPartialUser
from ._util import convert_twitchio_fragments, get_pluralmind_data, patch_twitchio_fragment, store_pluralmind_data

if TYPE_CHECKING:
    _Base = commands.Bot
else:
    _Base = object


class PluralmindBotMixin(_Base):
    """
    Takes care of adding in Pluralmind data as part of the process_commands
    step, and updates the default context to PluralmindContext.
    """

    _pluralmind: AsyncPluralmindClient | None = None

    @property
    def pluralmind(self) -> AsyncPluralmindClient:
        if not self._pluralmind:
            self._pluralmind = AsyncPluralmindClient()

        return self._pluralmind

    def get_context(self, payload: TwitchIOPayload, *, cls: Any = None):
        cls = cls or PluralmindContext
        return super().get_context(payload, cls=cls)

    async def process_commands(self, payload: TwitchIOPayload) -> None:
        await self._prepare_pluralmind_payload(payload)
        await super().process_commands(payload)

    async def _prepare_pluralmind_payload(self, payload: TwitchIOPayload) -> None:
        """
        Checks the payload against Pluralmind and adds information about the
        detected system and proxied message (if applicable).

        This is normally called automatically as part of `process_commands`,
        but be sure to call this manually if you're overriding it (without
        calling its super method).
        """
        # Check if this payload has already been processed
        if get_pluralmind_data(payload) is not None:
            return

        # Start by storing empty PluralmindData, since it indicates we've at
        # least looked at this payload
        data = PluralmindData()
        store_pluralmind_data(payload, data)

        if isinstance(payload, ChatMessage):
            data.system = await self.pluralmind.get_system(payload.chatter.id)
            data.proxied_message = get_proxied_message(data.system, convert_twitchio_fragments(payload.fragments))

            # Apply any changes to the payload's fragments
            if data.proxied_message:
                data.original_fragments = payload.fragments
                data.original_text = payload.text

                deltas = data.proxied_message['changed_fragments']
                payload.fragments = [
                    patch_twitchio_fragment(f, delta) if (delta := deltas.get(idx)) else f
                    for idx, f in enumerate(payload.fragments)
                    if idx not in deltas or deltas[idx] is not None
                ]
                payload.text = data.proxied_message['body']
        else:
            data.system = await self.pluralmind.get_system(payload.user.id)
            data.proxied_message = get_proxied_message(data.system, payload.user_input)
            if data.proxied_message:
                data.original_user_input = payload.user_input
                payload.user_input = data.proxied_message['body']

        # Update the chatter or user (even if this wasn't a proxied message)
        if isinstance(payload, ChatMessage):
            payload.chatter = PluralmindChatter.from_twitchio(payload.chatter, data)
        else:
            payload.user = PluralmindPartialUser.from_twitchio(payload.user, data)

    async def close(self, **options: Any) -> None:
        if self._pluralmind:
            await self._pluralmind.aclose()

        await super().close(**options)


class PluralmindBot(PluralmindBotMixin, commands.Bot):
    pass


class PluralmindAutoBot(PluralmindBotMixin, commands.AutoBot):
    pass
