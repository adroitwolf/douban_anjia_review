from anjia.items import ReviewItem
from scrapy.http import Request
import scrapy
import requests
import re
from bs4 import BeautifulSoup


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['movie.douban.com']
    
    start_url= 'https://movie.douban.com/subject/30482003/reviews'

    page = 0
    item_num = 0
    # 爬虫开始入口
    def start_requests(self):
        yield Request(url=self.start_url,callback= self.parse,dont_filter=True)
        
    # 解析网页    
    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')

        # 获取当前页所有评论
        reviews = soup.find_all('div', {'class': 'main review-item'})
        # 说明后面的评论被折叠了 需要进行模拟登录，直接退出
        
        if len(reviews)==0:
            print("爬取完成,共爬取{}条数据".format(self.item_num))
            return 
        for rev  in reviews:
            # 获取item值
            author = rev.find('a', {'class': 'name'}).text
            author = self.str_format(author)
            # 发布时间
            pub_time = rev.find('span', {'class': 'main-meta'}).text
            # 评分
            rating = rev.find('span', {'class': 'main-title-rating'})
            if rating:
                rating = rating.get('title')
            else:
                rating = ""
             # 标题
            title = rev.find('div', {'class': 'main-bd'}).find('a').text

            # 是否有展开按钮
            is_unfold = rev.find('a', {'class': 'unfold'})
            if is_unfold:
                # 获取评论id
                review_id = rev.find('div', {'class': 'review-short'}).get('data-rid')
                # 根据评论id，获取被折叠的评论内容
                content = self.get_fold_content(review_id)
            else:
                content = rev.find('div', {'class': 'short-content'}).text
            item = ReviewItem(author= author,pub_time=pub_time,rating=rating,title=title,content=content)
            self.item_num = self.item_num + 1
            yield item
        
        # 判断是否有下一页
        next_url = soup.find('span', {'class': 'next'}).find('a')

        if next_url:
            # 请求下一页的数据
            url = next_url.get('href')
            next_page_url = self.start_url + url
            self.page = self.page+1
            print("爬取完成第{}页数据".format(self.page))
            yield Request(url=next_page_url, callback=self.parse, dont_filter=True)
        else:
            pass
    

    # 获取详细评论内容
    def get_fold_content(self,review_id):
        '''
        根据评论id，获取被折叠的评论内容
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        url = "https://movie.douban.com/j/review/{}/full".format(review_id)

        resp = requests.get(url,headers=headers)
        data = resp.json()

        content = data['html']
        content = re.sub(r"(<.+?>)","",content)

        #去除content中双引号和单引号
        content = self.str_format(content)
        return content
    def str_format(self,line):
        '''
        去除content中特殊字符，单引号、双引号、反斜杠
        '''
        error_list = ['\'','\"','\\',',']
        for c in line:
            if  c in error_list:
                line=line.replace(c,'')
        return line