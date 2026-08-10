import copy
from typing import Any, cast

from pluralmind import MessageFragment as PluralmindFragment
from twitchio.models import ChatMessageFragment as TwitchIOFragment

from ._types import PluralmindData, TwitchIOPayload

_PLURALMIND_ATTR = '_pluralmind'


def convert_twitchio_fragments(fragments: list[TwitchIOFragment]) -> list[PluralmindFragment]:
    return [{'type': f.type, 'text': f.text} for f in fragments]


def patch_twitchio_fragment(source: TwitchIOFragment, updated: PluralmindFragment) -> TwitchIOFragment:
    if text := updated.get('text'):
        source = copy.copy(source)
        source.text = text

    return source


def get_pluralmind_data(payload: TwitchIOPayload) -> PluralmindData | None:
    return getattr(payload, _PLURALMIND_ATTR, None)


def store_pluralmind_data(payload: TwitchIOPayload, data: PluralmindData) -> None:
    setattr(payload, _PLURALMIND_ATTR, data)


def copy_state(source: object, target: object) -> None:
    """
    Copies the state from one object to another, regardless of whether the
    object is using __dict__, __slots__, or both. This assumes both objects are
    using 3.11's default __getstate__ implementation:
    https://docs.python.org/3/library/pickle.html#object.__getstate__
    """
    source_dict: dict[str, Any] | None
    source_slots: dict[str, Any] | None

    state: Any = source.__getstate__()
    source_dict, source_slots = cast(
        'tuple[dict[str, Any] | None, dict[str, Any] | None]',
        state if isinstance(state, tuple) else (state, None),
    )

    if source_dict:
        target.__dict__.update(source_dict)

    if source_slots:
        for name, value in source_slots.items():
            object.__setattr__(target, name, value)
