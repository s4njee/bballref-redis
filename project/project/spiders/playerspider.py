import scrapy
import csv
import json
from pprint import pprint

data = []


class PlayerSpider(scrapy.Spider):
    name = "playerspider"
    allowed_domains = ["basketball-reference.com"]
    l = []

    def start_requests(self):
        start_urls = [
            "https://www.basketball-reference.com/players/a/",
            "https://www.basketball-reference.com/players/b/",
            "https://www.basketball-reference.com/players/c/",
            "https://www.basketball-reference.com/players/d/",
            "https://www.basketball-reference.com/players/e/",
            "https://www.basketball-reference.com/players/f/",
            "https://www.basketball-reference.com/players/g/",
            "https://www.basketball-reference.com/players/h/",
            "https://www.basketball-reference.com/players/i/",
            "https://www.basketball-reference.com/players/j/",
            "https://www.basketball-reference.com/players/k/",
            "https://www.basketball-reference.com/players/l/",
            "https://www.basketball-reference.com/players/m/",
            "https://www.basketball-reference.com/players/n/",
            "https://www.basketball-reference.com/players/o/",
            "https://www.basketball-reference.com/players/p/",
            "https://www.basketball-reference.com/players/q/",
            "https://www.basketball-reference.com/players/r/",
            "https://www.basketball-reference.com/players/s/",
            "https://www.basketball-reference.com/players/t/",
            "https://www.basketball-reference.com/players/u/",
            "https://www.basketball-reference.com/players/v/",
            "https://www.basketball-reference.com/players/w/",
            "https://www.basketball-reference.com/players/x/",
            "https://www.basketball-reference.com/players/y/",
            "https://www.basketball-reference.com/players/z/",
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_letter)

    def parse(self, response):
        letters_list_ul = response.css("#content").xpath('//ul[@class="page_index"]')
        letters_list = letters_list_ul.xpath("//li")
        for letter in letters_list:
            next_page = letter.xpath("a/@href").get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_letter)

    def parse_letter(self, response):
        print(response.xpath('//*[@id="players"]/tbody').get())
        players = response.xpath('//*[@id="players"]/tbody/tr')
        for player in players:
            player_url = player.xpath("th/a/@href").get()
            if player_url is None:
                player_url = player.xpath("th/strong/a/@href").get()
            yield dict(url=player_url)
