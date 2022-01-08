from nonebot import get_driver
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.plugin import on_command
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

help = on_command('help')

@help.handle()
async def _(bot: Bot, event: MessageEvent):
    help_menu = f"""咱支持的命令有:
- pkg: 查询archlinux官方仓库的包
- aur: 查询aur上的包
- saur: 模糊搜索aur上的包
- mater: 查询aur上的包维护者
⚠️以上命令都要以<{'或者'.join(list(global_config.command_start))}>开头！
""" 
    await help.finish(MessageSegment.text(help_menu))