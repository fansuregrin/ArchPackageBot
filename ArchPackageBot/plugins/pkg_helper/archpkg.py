import re
import time
from httpx import AsyncClient
import asyncio


async def get_pkg_info(pkg_name: str='') -> str:
    if not pkg_name:
        return '不加参数超级坏！'
    url = f'https://archlinux.org/packages/search/json/?name={pkg_name}'
    async with AsyncClient() as client:
        rep = await client.get(url=url)
    info_dict = rep.json()['results']
    if info_dict:
        full_info = info_dict[0]
        pkgname = full_info['pkgname']
        pkgver = full_info['pkgver']
        arch = full_info['arch']
        repo = full_info['repo']
        pkgdesc = full_info['pkgdesc']
        url = full_info['url']
        maintainers = ' '.join(full_info['maintainers'])
        packager = full_info['packager']
        zip_size = full_info['compressed_size']
        build_date = full_info['build_date']
        last_update = full_info['last_update']
        licenses = ' '.join(full_info['licenses'])
        depends = ' '.join(full_info['depends'])
        pkg_string = f"包名: {pkgname}\n版本号: {pkgver}\n平台: {arch}\n仓库: {repo}\n描述: {pkgdesc}\nurl: {url}\n维护者: {maintainers}\n打包者: {packager}\n压缩包体积: {zip_size}\n发布日期: {build_date}\n最近更新日期: {last_update}\n依赖: {depends}\n协议: {licenses}"
        # print(pkg_string)
    else:
        pkg_string = f'未找到『{pkg_name}』;('

    return pkg_string

async def search_repo_pkg(description: str='', limit: int=100):
    if not description:
        return '不加参数超级坏！'
    url = f'https://archlinux.org/packages/search/json/?q={description}&limit={limit}'
    async with AsyncClient() as client:
        rep = await client.get(url)
    rep = rep.json()
    pkg_list = rep['results']
    pkg_num = len(pkg_list)
    pkg_names = []
    if pkg_num:
        count = 0
        for pkg in pkg_list:
            if count == 15:
                break
            pkg_name = pkg['pkgname']
            pkg_names.append(f'{pkg_name}')
            count += 1
        pkg_info = '\n'.join(pkg_names)
        pkg_string = f"与『{description}』相关的包有 {pkg_num}+ 个:\n{pkg_info}......"
        # print(pkg_string)
    else:
        pkg_string = f'未找到与『{description}』相关的包;('

    return pkg_string


async def search_repo_maintainer(name: str='', limit: int=100):
    if not name:
        return '不加参数超级坏！'
    url = f'https://archlinux.org/packages/search/json/?maintainer={name}&limit={limit}'
    async with AsyncClient() as client:
        rep = await client.get(url)
    info_dict = rep.json()
    pkg_list = info_dict['results']
    pkg_count = len(pkg_list)
    pkg_names = []
    for pkg in pkg_list[0:10]:
        pkg_names.append(pkg['pkgname'])
    pkgs = '\n'.join(pkg_names)
    if pkg_count == limit:
        pkg_string = f'在arch官方仓库中上，{name} 维护了 {pkg_count}+ 个包!\n{pkgs}......'
    else:
        pkg_string = f'在arch官方仓库中上，{name} 维护了 {pkg_count} 个包!\n{pkgs}......'

    return pkg_string


async def get_pkg_info_aur(pkg_name: str='') -> str:
    if not pkg_name:
        return '不加参数超级坏！'
    url = f'https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={pkg_name}'
    async with AsyncClient() as cliet:
        rep = await cliet.get(url)
    info_dict = rep.json()['results']
    if info_dict:
        full_info = info_dict[0]
        info_keys = list(full_info.keys())
        # print(info_keys)
        name = full_info['Name']
        version = full_info['Version']
        desc = full_info['Description']
        url = full_info['URL']
        outdate = full_info['OutOfDate']
        maintainer = full_info['Maintainer']
        licenses = ' '.join(full_info['License'])
        if 'Depends' in info_keys:
            depends = ' '.join(full_info['Depends'])
        else:
            depends = '无'
        if 'MakeDepends' in info_keys:
            mk_depends = ' '.join(full_info['MakeDepends'])
        else:
            mk_depends = '无'
        if 'OpeDepends' in info_keys:
            opt_depends = ' '.join(full_info['OptDepends'])
        else:
            opt_depends = '无'
        if 'Conflicts' in info_keys:
            conflicts = ' '.join(full_info['Conflicts'])
        else:
            conflicts = '无'
        if outdate:
            outdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(outdate))
        else:
            outdate = '未过期'
        pkg_string = f'包名：{name}\n版本号：{version}\n描述：{desc}\nurl：{url}\n过期时间：{outdate}\n维护者：{maintainer}\n依赖：{depends}\n编译所需依赖：{mk_depends}\n可选依赖：{opt_depends}\n冲突：{conflicts}\n协议：{licenses}'
    else:
        pkg_string = f'未找到『{pkg_name}』~'

    return pkg_string


async def search_aur_pkg(keyword: str='') -> str:
    url = f'https://aur.archlinux.org/rpc/?v=5&type=search&arg={keyword}'
    async with AsyncClient() as client:
        rep = await client.get(url=url)
    info_dict = rep.json()
    pkg_count = info_dict['resultcount']
    info_type = info_dict['type']
    pkg_names = []
    if info_type == 'search':
        if pkg_count:
            pkg_list = info_dict['results']
            count = 0
            for pkg in pkg_list:
                if(count==10):
                    break
                count += 1
                pkg_names.append(pkg['Name'])
            pkgs = '\n'.join(pkg_names)
            pkg_string = f'在aur上与"{keyword}"有关的包有以下{pkg_count}个：\n{pkgs}......'
        else:
            pkg_string = '啥也没有丫～'
    elif info_type == 'error':
        pkg_string = f'❌出错啦！<{info_dict["error"]}>'

    return pkg_string


async def search_aur_maintainer(name: str='') -> str:
    if not name:
        return '不加参数超级坏！'
    url = f'https://aur.archlinux.org/rpc/?v=5&type=search&by=maintainer&arg={name}'
    async with AsyncClient() as client:
        rep = await client.get(url)
    info_dict = rep.json()
    pkg_count = info_dict['resultcount']
    pkg_list = info_dict['results']
    pkg_names = []
    for pkg in pkg_list[0:10]:
        pkg_names.append(pkg['Name'])
    pkgs = '\n'.join(pkg_names)
    pkg_string = f'在aur上，{name} 维护了 {pkg_count} 个包!\n{pkgs}......'

    return pkg_string


if __name__ == '__main__':
    asyncio.run(search_repo_pkg('firefox'))