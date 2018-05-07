# -*- coding: utf-8 -*-
import scrapy, urllib
# from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest


# from douBanSpider.items import DoubanspiderItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    # start_urls = ['https://www.douban.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

    def __init__(self, *args, **kwargs):
        super(DoubanSpider, self).__init__(self, *args, **kwargs)
        self.captcha = ''

    def start_requests(self):
        return [Request("https://accounts.douban.com/login",
                        method='POST',
                        headers=self.header,
                        meta={'cookiejar': 1},
                        callback=self.start_login,
                        encoding='utf-8'
                        )]

    def start_login(self, response):
        self.captcha = response.xpath('//*[@id="captcha_image"]/@src').extract()  # 获取验证码图片的链接
        if len(self.captcha) > 0:
            urllib.urlretrieve(self.captcha[0], filename="E:\zyb\githubs\douBanSpider\douBanSpider\spiders\captcha.png")
            captcha_value = raw_input('查看captcha.png,有验证码请输入:')
            data = {
                "form_email": "*******",
                "form_password": "****",
                "captcha-solution": captcha_value
            }
            print '验证码为：', captcha_value
        else:
            data = {
                "form_email": "*******",
                "form_password": "*****",
            }

        return [
            FormRequest.from_response(
                response,
                meta={"cookiejar": response.meta["cookiejar"]},
                headers=self.header,
                formdata=data,
                callback=self.after_login,
            )
        ]

    def after_login(self, response):
        title = response.xpath('//title/text()').extract()[0]
        if u'登录豆瓣' in title:
            print '登录失败，请重试！'
        else:
            print '登录成功'
