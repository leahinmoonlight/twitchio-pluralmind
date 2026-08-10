# twitchio-pluralmind

Pluralmind allows plural folks to share which of their system members is sending a message on Twitch. You can learn more about Pluralmind over at [pluralmind.chat](https://pluralmind.chat).

This integration lets you quickly make your TwitchIO bot plural-aware.

If you want to add Pluralmind to something other than TwitchIO, check out our [Python library](https://github.com/leahinmoonlight/pluralmind-py) or [JavaScript library](https://github.com/leahinmoonlight/pluralmind).

[![pypi version](https://img.shields.io/pypi/v/twitchio-pluralmind?color=ff69b4)](https://pypi.org/project/twitchio-pluralmind/) [![license](https://img.shields.io/pypi/l/twitchio-pluralmind?color=ff69b4)](https://github.com/leahinmoonlight/twitchio-pluralmind/blob/main/LICENSE)
[![Pyright Strict](https://img.shields.io/badge/Pyright-Strict-ff69b4)](https://github.com/leahinmoonlight/twitchio-pluralmind/blob/main/pyproject.toml)

## Installation

With pip (or your favorite package manager):

```bash
pip install twitchio-pluralmind
```

(Note: Python 3.12+ is required. Everything is fully typed~!)

## Integrating Pluralmind

### Bot Setup

Simply swap your Bot or AutoBot's class over to the Pluralmind version! For example, if you're using `AutoBot`, you can use the `PluralmindAutoBot` class instead:

```python
from twitchio_pluralmind import PluralmindAutoBot


class Bot(PluralmindAutoBot):
    #  all your usual stuff here~
    ...
```

Alternatively, if you're already using a specialized Bot class, you can add Pluralmind via mixin:

```python
from twitchio_pluralmind import PluralmindBotMixin


class Bot(PluralmindBotMixin, SomeOtherBot):
    #  all your usual stuff here~
    ...
```

That's it! Pluralmind will automatically load system and member information for you.

### Usage

Once you add Pluralmind to your bot, your bot's Context classes will be extended with plural info!

For example, if a message is sent from a system member, `display_name` will automatically be set to the member's name:

```python
from twitchio.ext import commands
from twitchio_pluralmind import PluralmindContext


class ChatComponent(commands.Component):
    @commands.command()
    async def lurk(self, ctx: PluralmindContext):
        await ctx.send(f'have a cozy lurk, {ctx.chatter.display_name}! we appreciate you~')
```

> [!TIP]
> In this example, you can still access Twitch's version of the display name with `ctx.chatter.original_display_name`.

You can also reference `ctx.chatter.system` and `ctx.chatter.member` to get more details about that system/member. `ctx.proxied_message` will give you the full Pluralmind message info, when it exists.

### We're happy to help~!

Our TwitchIO integration docs are still WIP, but feel free to reach out if you have any questions! There's contact options near the bottom of the [pluralmind website](https://pluralmind.chat/).
