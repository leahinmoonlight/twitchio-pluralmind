from dataclasses import dataclass

from pluralmind import ProxiedMessage, System
from twitchio.models import ChannelPointsRedemptionAdd, ChannelPointsRedemptionUpdate, ChatMessage
from twitchio.models import ChatMessageFragment as TwitchIOFragment

TwitchIOPayload = ChatMessage | ChannelPointsRedemptionAdd | ChannelPointsRedemptionUpdate


@dataclass(slots=True)
class PluralmindData:
    proxied_message: ProxiedMessage | None = None
    """
    The proxied message information from Pluralmind, if a proxied message was
    detected.
    """

    system: System | None = None
    """
    The system associated with the sender, even if they didn't proxy their
    message.
    """

    original_fragments: list[TwitchIOFragment] | None = None
    """The message fragments prior to Pluralmind removing the proxy."""

    original_text: str | None = None
    """The message text prior to Pluralmind removing the proxy."""

    original_user_input: str | None = None
    """The user input prior to Pluralmind removing the proxy."""
