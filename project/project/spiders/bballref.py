import scrapy
from scrapy_redis.spiders import RedisSpider

import csv
import os
import json
from pprint import pprint
import time
from scrapy_selenium import SeleniumRequest
import pandas as pd

data = []


class BballrefSpider(RedisSpider):
    name = "bballref"
    allowed_domains = ["basketball-reference.com"]
    lines = []
    # my_file = open("playerurls.json", "r")
    # reader = csv.reader(my_file)
    # for row in reader:
    #     l.append(row)
    # print(lines)
    redis_key = "myspider:start_urls"

    # def start_requests(self):
    #     with open("playerurls.json") as file:
    #         lines = file.readlines()
    #         lines = ['https://www.basketball-reference.com' + line.rstrip().strip('\"') for line in lines]
    #     for player in lines:
    #         yield scrapy.Request(url=player, callback=self.parse)

    def parse(self, response):
        season_rows = response.xpath('*//th[@data-stat="season"]')
        for season in season_rows:
            next_page = season.xpath("a/@href").get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield SeleniumRequest(url=next_page, callback=self.parse_second)

    def parse_second(self, response):
        name = response.css("#meta").xpath("div[2]/p[1]/strong/strong/text()").get()
        if not name:
            name = response.css("#meta").xpath("div/p[1]/strong/strong/text()").get()
        if not name:
            name = response.css("#meta").xpath("div[2]/p[2]/strong/strong/text()").get()

        nameList = name.split(" ")
        name = "_".join(nameList)
        # time.sleep(2)

        rows = response.css("#pgl_basic").xpath("//tbody")
        rows = rows.xpath("//tr")

        # Parse regular season table
        for table_row in rows:
            date = table_row.xpath('td[@data-stat="date_game"]/a/text()').get()
            age = table_row.xpath('td[@data-stat="age"]/text()').get()
            tm = table_row.xpath('td[@data-stat="team_id"]/a/text()').get()
            game_location = table_row.xpath(
                'td[@data-stat="game_location"]/text()'
            ).get()
            opp_id = table_row.xpath('td[@data-stat="opp_id"]/a/text()').get()
            game_result = table_row.xpath('td[@data-stat="game_result"]/text()').get()
            gs = table_row.xpath('td[@data-stat="gs"]/text()').get()
            mp = table_row.xpath('td[@data-stat="mp"]/text()').get()
            fg = table_row.xpath('td[@data-stat="fg"]/text()').get()
            fga = table_row.xpath('td[@data-stat="fga"]/text()').get()
            fg_pct = table_row.xpath('td[@data-stat="fg_pct"]/text()').get()
            fg3 = table_row.xpath('td[@data-stat="fg3"]/text()').get()
            fg3a = table_row.xpath('td[@data-stat="fg3a"]/text()').get()
            fg3_pct = table_row.xpath('td[@data-stat="fg3_pct"]/text()').get()
            ft = table_row.xpath('td[@data-stat="ft"]/text()').get()
            fta = table_row.xpath('td[@data-stat="fta"]/text()').get()
            ft_pct = table_row.xpath('td[@data-stat="ft_pct"]/text()').get()
            orb = table_row.xpath('td[@data-stat="orb"]/text()').get()
            drb = table_row.xpath('td[@data-stat="drb"]/text()').get()
            trb = table_row.xpath('td[@data-stat="trb"]/text()').get()
            ast = table_row.xpath('td[@data-stat="ast"]/text()').get()
            stl = table_row.xpath('td[@data-stat="stl"]/text()').get()
            blk = table_row.xpath('td[@data-stat="blk"]/text()').get()
            tov = table_row.xpath('td[@data-stat="tov"]/text()').get()
            pf = table_row.xpath('td[@data-stat="pf"]/text()').get()
            pts = table_row.xpath('td[@data-stat="pts"]/text()').get()
            game_score = table_row.xpath('td[@data-stat="game_score"]/text()').get()
            row_stats = dict(
                name=name,
                date=date,
                age=age,
                tm=tm,
                game_location=game_location,
                opp_id=opp_id,
                game_result=game_result,
                gs=gs,
                mp=mp,
                fg=fg,
                fga=fga,
                fg_pct=fg_pct,
                fg3=fg3,
                fg3a=fg3a,
                fg3_pct=fg3_pct,
                ft=ft,
                fta=fta,
                ft_pct=ft_pct,
                orb=orb,
                drb=drb,
                trb=trb,
                ast=ast,
                stl=stl,
                blk=blk,
                tov=tov,
                pf=pf,
                pts=pts,
                game_score=game_score,
            )
            print(row_stats)
            if row_stats["date"] is not None:
                yield row_stats
        # Parse Playoff Table
        rows = response.css("#pgl_basic_playoffs").xpath("//tbody")
        rows = rows.xpath("//tr")
        for table_row in rows:
            date = table_row.xpath('td[@data-stat="date_game"]/a/text()').get()
            age = table_row.xpath('td[@data-stat="age"]/text()').get()
            tm = table_row.xpath('td[@data-stat="team_id"]/a/text()').get()
            game_location = table_row.xpath(
                'td[@data-stat="game_location"]/text()'
            ).get()
            opp_id = table_row.xpath('td[@data-stat="opp_id"]/a/text()').get()
            game_result = table_row.xpath('td[@data-stat="game_result"]/text()').get()
            gs = table_row.xpath('td[@data-stat="gs"]/text()').get()
            mp = table_row.xpath('td[@data-stat="mp"]/text()').get()
            fg = table_row.xpath('td[@data-stat="fg"]/text()').get()
            fga = table_row.xpath('td[@data-stat="fga"]/text()').get()
            fg_pct = table_row.xpath('td[@data-stat="fg_pct"]/text()').get()
            fg3 = table_row.xpath('td[@data-stat="fg3"]/text()').get()
            fg3a = table_row.xpath('td[@data-stat="fg3a"]/text()').get()
            fg3_pct = table_row.xpath('td[@data-stat="fg3_pct"]/text()').get()
            ft = table_row.xpath('td[@data-stat="ft"]/text()').get()
            fta = table_row.xpath('td[@data-stat="fta"]/text()').get()
            ft_pct = table_row.xpath('td[@data-stat="ft_pct"]/text()').get()
            orb = table_row.xpath('td[@data-stat="orb"]/text()').get()
            drb = table_row.xpath('td[@data-stat="drb"]/text()').get()
            trb = table_row.xpath('td[@data-stat="trb"]/text()').get()
            ast = table_row.xpath('td[@data-stat="ast"]/text()').get()
            stl = table_row.xpath('td[@data-stat="stl"]/text()').get()
            blk = table_row.xpath('td[@data-stat="blk"]/text()').get()
            tov = table_row.xpath('td[@data-stat="tov"]/text()').get()
            pf = table_row.xpath('td[@data-stat="pf"]/text()').get()
            pts = table_row.xpath('td[@data-stat="pts"]/text()').get()
            game_score = table_row.xpath('td[@data-stat="game_score"]/text()').get()
            row_stats = dict(
                name=name,
                date=date,
                age=age,
                tm=tm,
                game_location=game_location,
                opp_id=opp_id,
                game_result=game_result,
                gs=gs,
                mp=mp,
                fg=fg,
                fga=fga,
                fg_pct=fg_pct,
                fg3=fg3,
                fg3a=fg3a,
                fg3_pct=fg3_pct,
                ft=ft,
                fta=fta,
                ft_pct=ft_pct,
                orb=orb,
                drb=drb,
                trb=trb,
                ast=ast,
                stl=stl,
                blk=blk,
                tov=tov,
                pf=pf,
                pts=pts,
                game_score=game_score,
            )
            print(row_stats)

            if row_stats["date"] is not None:
                yield row_stats
            # table_elements = table_row.xpath('//td')
            # rows_list = {}
            # for row in table_elements:
            #     # rows_list = {'name':name}
            #     values = row.xpath('text()').get()
            #     if not values:
            #         values = row.xpath('*/text()').get()
            #     labels = row.xpath('@data-stat').get()
            #     row_element = {labels: values}
            #     if labels:
            #         rows_list.update(row_element)
            # elements.append(rows_list.copy())
        # df = pd.DataFrame(elements)
        # print(df.to_string())
        # with open('test.json', 'a') as f:
        #     f.write(json.dumps(elements)+'\n')
