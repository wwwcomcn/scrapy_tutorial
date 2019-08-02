import scrapy


class FictionSpider(scrapy.Spider):
    name = "fiction"
    start_urls = ["http://www.shuquge.com/txt/8659/index.html"]

    def parse(self, response):
        for chapter in response.xpath("//div[@class='listmain']//a"):
            href = chapter.xpath(".//@href").get()
            chapter_href = "http://www.shuquge.com/txt/8659/{}".format(href)
            yield scrapy.Request(chapter_href, callback=self.write_chapter)

    def write_chapter(self, response):
        filename = response.url.split("/")[-1]
        chapter_content = response.xpath("//div[@id='content']//text()").get()
        with open(r'E:\path\2\{}'.format(filename), 'wb') as fw:
            fw.write(response.body)
