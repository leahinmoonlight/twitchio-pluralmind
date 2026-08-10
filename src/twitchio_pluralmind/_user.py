from typing import TYPE_CHECKING, Self

from pluralmind import Member, System
from twitchio.user import Chatter, PartialUser
from twitchio.utils import Colour

from ._types import PluralmindData
from ._util import copy_state

if TYPE_CHECKING:
    _MixinBase = PartialUser
else:
    _MixinBase = object


_pluralmind_slots = (
    'system',
    'member',
    'original_display_name',
)


class PluralmindPartialUserMixin(_MixinBase):
    system: System | None
    """
    The Pluralmind system associated with this user, if one exists.
    Note: This will always be set if a system exists, even if the event wasn't
    associated with a proxied message.
    """

    member: Member | None
    """
    The Pluralmind member that sent the event, if Pluralmind was used to proxy
    the event.
    """

    original_display_name: str | None
    """
    The user's original display name from Twitch, prior to Pluralmind applying
    any proxy information.
    """

    display_name: str | None
    """
    The name of the member that sent the event, or the regular Twitch display
    name if the event wasn't proxied.
    """

    __slots__ = ()

    @classmethod
    def from_twitchio(cls, source: PartialUser, data: PluralmindData) -> Self:
        # Clone from the existing PartialUser or Chatter
        target = object.__new__(cls)
        copy_state(source, target)

        # Prep general state regardless of whether the message was proxied
        target.system = data.system
        target.member = data.proxied_message['member'] if data.proxied_message else None
        target.original_display_name = target.display_name

        # Apply the proxied message (if there is one)
        if data.proxied_message:
            target.display_name = data.proxied_message['member']['name']

        return target


class PluralmindChatter(PluralmindPartialUserMixin, Chatter):
    __slots__ = _pluralmind_slots

    @property
    def colour(self) -> Colour | None:
        return self._pluralmind_color or self._colour

    @property
    def color(self) -> Colour | None:
        return self._pluralmind_color or self._colour

    @property
    def _pluralmind_color(self) -> Colour | None:
        # We only apply color on proxied messages (when a member is set)
        if self.member:
            if color := self.member.get('color'):
                return Colour.from_hex(color)

            # System will always exist, but just to appease pyright
            if self.system and (color := self.system.get('color')):
                return Colour.from_hex(color)

        return None


class PluralmindPartialUser(PluralmindPartialUserMixin, PartialUser):
    __slots__ = _pluralmind_slots
