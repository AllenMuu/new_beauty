# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class NewBeautyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for imgUrl in item['imgUrls']:
            yield Request(imgUrl, meta={"name": item['imgName']})

    def file_path(self, request, response=None, info=None):
        # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
        image_guid = request.url.split('/')[-1]  # 提取url前面名称作为图片名。
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(name, image_guid)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item
