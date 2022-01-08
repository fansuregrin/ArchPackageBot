from nonebot import get_driver
from .config import Config
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from .archpkg import *


global_config = get_driver().config
config = Config(**global_config.dict())

# archlinux官方仓库的包
arch_repo_pkg = on_command('pkg')
# aur上的包
aur_pkg = on_command('aur')
# 搜索aur上的相关包
aur_keyword_pkg = on_command('saur')
# 查询维护者
query_maintainer = on_command('mater')

@arch_repo_pkg.handle()
async def _(bot: Bot, event: MessageEvent):
    pkg_info = await get_pkg_info(event.get_plaintext())
    await arch_repo_pkg.finish(MessageSegment.text(pkg_info))

@aur_pkg.handle()
async def _(bot: Bot, event: MessageEvent):
    pkg_info = await get_pkg_info_aur(event.get_plaintext())
    await aur_pkg.finish(MessageSegment.text(pkg_info))

@aur_keyword_pkg.handle()
async def _(bot: Bot, event: MessageEvent):
    pkg_info = await search_aur_pkg(event.get_plaintext())
    await aur_keyword_pkg.finish(MessageSegment.text(pkg_info))

@query_maintainer.handle()
async def _(bot: Bot, event: MessageEvent):
    mater_info = await search_aur_maintainer(event.get_plaintext())
    await query_maintainer.finish(MessageSegment.text(mater_info))