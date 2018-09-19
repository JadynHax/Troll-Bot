import traceback
import inspect
import textwrap
import io
import asyncio
from contextlib import redirect_stdout
from importlib import reload as importlib_reload
import copy
from async_timeout import timeout
import discord
from discord.ext import commands
from utils.helpers import *

@commands.command(hidden=True, name='eval')
async def _eval(self, ctx, *, body: str):
    """Evaluates Python code"""

    env = {
        'bot': self.bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': self._last_result
    }

    env.update(globals())

    body = self.cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('blackcheck:441826948919066625')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            self._last_result = ret
            await ctx.send(f'```py\n{value}{ret}\n```')

@commands.command(aliases=dead)
async def ded():
