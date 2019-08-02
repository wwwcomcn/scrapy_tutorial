from lxml import etree
import aiohttp
import asyncio
import aiofiles
import time


async def request_web(session, web_site):
    async with session.get(web_site) as resp:
        content = await resp.read()
        paths = web_site.split("/")
        filename = paths[-1]
        book = paths[-2]
        await write_chapter(book, filename, content)


async def parse_html(session, url, html):
    parse = etree.HTML(html)
    a_list = parse.xpath("//div[@class='listmain']//a")
    gather_list = []
    for a in a_list:
        href = a.get('href')
        chapter_href = "{}{}".format(url, href)
        gather_list.append(request_web(session, chapter_href))
    await asyncio.gather(*gather_list)

    # 异步写入文件
    # write_tasks = [write_chapter(index, content) for index, content in enumerate(chapter_list)]
    # await asyncio.gather(*write_tasks)

    # 常规写入文件
    # for index, content in enumerate(chapter_list):
    #     write_chapter(index, content)


async def write_chapter(book, name, content):
    async with aiofiles.open(r'E:\path\2\{}\{}'.format(book, name), mode='wb') as fw:
        await fw.write(content)


async def main():
    urls = [
        "http://www.shuquge.com/txt/343/",
        "http://www.shuquge.com/txt/9249/",
        "http://www.shuquge.com/txt/1894/",
        "http://www.shuquge.com/txt/350/",
        "http://www.shuquge.com/txt/74671/"
    ]

    session = aiohttp.ClientSession()
    for url in urls:
        async with session.get(url) as resp:
            html = await resp.text()
        await parse_html(session, url, html)

    await session.close()


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print('total: {:.2f}s'.format(end - start))
