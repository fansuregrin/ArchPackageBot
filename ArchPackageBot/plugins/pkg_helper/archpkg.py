import time
from httpx import AsyncClient
import asyncio


async def get_pkg_info(pkg_name: str='') -> str:
    if not pkg_name:
        return '不加参数是个坏文明！'
    url = f'https://archlinux.org/packages/search/json/?name={pkg_name}'
    async with AsyncClient() as client:
        rep = await client.get(url=url)
    rep = rep.json()
    # print(rep)
    info_dict = rep['results']
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
        info = f"包名: {pkgname}\n版本号: {pkgver}\n平台: {arch}\n仓库: {repo}\n描述: {pkgdesc}\nurl: {url}\n维护者: {maintainers}\n打包者: {packager}\n压缩包体积: {zip_size}\n发布日期: {build_date}\n最近更新日期: {last_update}\n依赖: {depends}\n协议: {licenses}"
        # print(info)
    else:
        info = f'未找到『{pkg_name}』;('

    return info


async def get_pkg_info_aur(pkg_name: str='') -> str:
    if not pkg_name:
        return '不加参数是个坏文明！'
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
        info = f'包名：{name}\n版本号：{version}\n描述：{desc}\nurl：{url}\n过期时间：{outdate}\n维护者：{maintainer}\n依赖：{depends}\n编译所需依赖：{mk_depends}\n可选依赖：{opt_depends}\n冲突：{conflicts}\n协议：{licenses}'
    else:
        info = f'未找到『{pkg_name}』~'
    # print(info)
    return info


async def search_aur_pkg(keyword: str='') -> str:
    url = f'https://aur.archlinux.org/rpc/?v=5&type=search&arg={keyword}'
    async with AsyncClient() as client:
        rep = await client.get(url=url)
    info_dict = rep.json()
    pkg_count = info_dict['resultcount']
    info_type = info_dict['type']
    pkg_list = []
    if info_type == 'search':
        if pkg_count:
            pkg_objs = info_dict['results']
            count = 0
            for pkg_obj in pkg_objs:
                if(count==10):
                    break
                count += 1
                pkg_list.append(pkg_obj['Name'])
            pkgs = '\n'.join(pkg_list)
            pkgs = f'在aur上与"{keyword}"有关的包有以下{pkg_count}个：\n{pkgs}......'
        else:
            pkgs = '啥也没有丫～'
    elif info_type == 'error':
        pkgs = f'❌出错啦！<{info_dict["error"]}>'
    # print(pkgs)
    return pkgs


async def search_aur_maintainer(name: str='') -> str:
    url = f'https://aur.archlinux.org/rpc/?v=5&type=search&by=maintainer&arg={name}'
    async with AsyncClient() as client:
        rep = await client.get(url)
    info_dict = rep.json()
    pkg_count = info_dict['resultcount']
    pkg_list = info_dict['results']
    pkg_names = []
    for pkg in pkg_list[0:10]:
        pkg_names.append(pkg['Name'])
    pkg_string = '\n'.join(pkg_names)
    # print(f'在aur上，{name} 维护了 {pkg_count} 个包!\n{pkg_string}...')
    return f'在aur上，{name} 维护了 {pkg_count} 个包!\n{pkg_string}...'


if __name__ == '__main__':
    asyncio.run(search_aur_maintainer('fansuregrin'))