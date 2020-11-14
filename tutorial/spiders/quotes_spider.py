# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.selector import Selector
import re
from datetime import datetime


class BaomoiSpider(scrapy.Spider):
    name = 'baomoi'
    allowed_domains = ['baomoi.com']
    #   start_urls = ['http://baomoi.com/']
    start_urls = [
        "https://baomoi.com"
        "https://baomoi.com/thoi-su.epi",
        "https://baomoi.com/giao-thong.epi",
        "https://baomoi.com/moi-truong-khi-hau.epi",
        "https://baomoi.com/the-gioi.epi",
        "https://baomoi.com/van-hoa.epi",
        "https://baomoi.com/nghe-thuat.epi",
        "https://baomoi.com/am-thuc.epi",
        "https://baomoi.com/du-lich.epi",

        "https://baomoi.com/kinh-te.epi",
        "https://baomoi.com/lao-dong-viec-lam.epi",
        "https://baomoi.com/tai-chinh.epi",
        "https://baomoi.com/chung-khoan.epi",
        "https://baomoi.com/kinh-doanh.epi",

        "https://baomoi.com/giao-duc.epi",
        "https://baomoi.com/hoc-bong-du-hoc.epi",
        "https://baomoi.com/dao-tao-thi-cu.epi",

        "https://baomoi.com/the-thao.epi",
        "https://baomoi.com/bong-da-quoc-te.epi",
        "https://baomoi.com/bong-da-viet-nam.epi",
        "https://baomoi.com/quan-vot.epi",

        "https://baomoi.com/giai-tri.epi",
        "https://baomoi.com/am-nhac.epi",
        "https://baomoi.com/thoi-trang.epi",
        "https://baomoi.com/dien-anh-truyen-hinh.epi",

        "https://baomoi.com/phap-luat.epi",
        "https://baomoi.com/an-ninh-trat-tu.epi",
        "https://baomoi.com/hinh-su-dan-su.epi",

        "https://baomoi.com/khoa-hoc-cong-nghe.epi",
        "https://baomoi.com/cntt-vien-thong.epi",
        "https://baomoi.com/thiet-bi-phan-cung.epi",

        "https://baomoi.com/khoa-hoc.epi",

        "https://baomoi.com/doi-song.epi",
        "https://baomoi.com/dinh-duong-lam-dep.epi",
        "https://baomoi.com/tinh-yeu-hon-nhan.epi",
        "https://baomoi.com/suc-khoe-y-te.epi",

        "https://baomoi.com/xe-co.epi",
        "https://baomoi.com/nha-dat.epi",
        "https://baomoi.com/quan-ly-quy-hoach.epi",
        "https://baomoi.com/khong-gian-kien-truc.epi"
    ]

    def parse(self, response):
        posts = Selector(response).xpath('//div[@class="story"]')
        for post in posts:
            title = post.xpath('h4[@class="story__heading"]/a/text()').extract()[0].replace("\n", "").strip()
            url = post.xpath('h4[@class="story__heading"]/a/@href').extract()[0].replace("\n", "").strip()
            newspaper = post.xpath('div[@class="story__meta"]/a/text()').extract()[0].replace("\n", "").strip()
            sponsor = ''
            try:
                sponsor = post.xpath('div[@class="hidden-False"]/text()').extract()[0].replace("\n", "").strip()
            except:
                sponsor = ''
            #   Get Baomoi's id from url
            baomoi_id = url.split('/r/')[1].split('.epi')[0]
            yield scrapy.Request(
                str("https://baomoi.com" + url),
                callback=self.parse_baomoi_url,
                meta={'title': title, 'url': url, 'newspaper': newspaper, 'baomoi_id': baomoi_id, 'sponsor': sponsor})

    def parse_baomoi_url(self, response):
        abstract = Selector(response).xpath('//meta[@name="description"]/@content').extract()[0]
        keywords = Selector(response).xpath('//meta[@name="keywords"]/@content').extract()[0]
        original_url = response.xpath('//script[@type="text/javascript"]/text()').re(r"window\.location\.replace\(\"(.*?)\"\)")[0]

        meta = response.meta
        meta['abstract'] = abstract
        meta['keywords'] = keywords
        meta['original_url'] = original_url
        yield {
            'source': 'baomoi',
            'baomoi_id': response.meta['baomoi_id'],
            'title': response.meta['title'],
            'baomoi_url': response.meta['url'],
            'newspaper': response.meta['newspaper'],
            'original_url': original_url,
            'sponsor': response.meta['sponsor'],
            'abstract': abstract,
            'keywords': keywords,
            "crawled_at": datetime.now().isoformat()
        }
