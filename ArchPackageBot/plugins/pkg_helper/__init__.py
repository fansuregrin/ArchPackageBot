from nonebot import get_driver
from .config import Config
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment, event
from .archpkg import *


global_config = get_driver().config
config = Config(**global_config.dict())

# 查询archlinux官方仓库的包
archrepo_pkg = on_command('pkg')
# 搜索archlinux官方仓库的相关包
query_archrepo_pkg = on_command('spkg')
# 查询archlinux官方仓库里的包维护者
query_archrepo_maintainer = on_command('mter')
# 查询aur上的包
aur_pkg = on_command('aur')
# 搜索aur上的相关包
query_aur_pkg = on_command('saur')
# 查询aur上的包维护者
query_aur_maintainer = on_command('mater')

@archrepo_pkg.handle()
async def _(bot: Bot, event: MessageEvent):
    pkg_info = await get_pkg_info(event.get_plaintext())
    await archrepo_pkg.finish(MessageSegment.text(pkg_info))

@query_archrepo_pkg.handle()
async def _(bot: Bot, event: MessageEvent):
    pkg_info = await search_repo_pkg(event.get_plaintext())
    await query_archrepo_pkg.finish(MessageSegment.text(pkg_info))

@query_archrepo_maintainer.handle()
async def _(bot: Bot, event: MessageEvent):
    mater_info = await search_repo_maintainer(event.get_plaintext())
    await query_archrepo_maintainer.finish(MessageSegment.text(mater_info))

@aur_pkg.handle()
async def _(bot: Bot, event: MessageEvent):
    pkg_info = await get_pkg_info_aur(event.get_plaintext())
    await aur_pkg.finish(MessageSegment.text(pkg_info))

@query_aur_pkg.handle()
async def _(bot: Bot, event: MessageEvent):
    pkg_info = await search_aur_pkg(event.get_plaintext())
    await query_aur_pkg.finish(MessageSegment.text(pkg_info))

@query_aur_maintainer.handle()
async def _(bot: Bot, event: MessageEvent):
    mater_info = await search_aur_maintainer(event.get_plaintext())
    await query_aur_maintainer.finish(MessageSegment.text(mater_info))