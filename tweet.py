import sys
import os
import re
import datetime
from bs4 import BeautifulSoup
import requests
import tweepy


class TimeTable:

    def __init__(self, time, broadcaster_list, CONSUMER_KEY="_", CONSUMER_SECRET="_", ACCESS_TOKEN="_", ACCESS_TOKEN_SECRET="_"):
        if not isinstance(time, datetime.datetime):
            sys.stderr.write('Error: usage: class initialized error: argment type is not datetime.datetime\n')
            sys.exit(1)
        self.time = time
        self.url = "http://cal.syoboi.jp/"
        self.broadcaster = broadcaster_list
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def show_all(self):
        soup = self._return_soup()
        programs = soup.find("td", {"class": "v3dayCell v3cellR "}).find_all("div", {"class": "pid-item v3div"})
        for program in programs:
            sys.stdout.write(program["title"] + "\n")

    def now_program(self):
        soup = self._return_soup()
        programs = soup.find("td", {"class": "v3dayCell v3cellR "}).find_all("div", {"class": "pid-item v3div"})
        for program in programs:
            if self._time_check(program, 0, 0):
                if self._broadcaster_check(program) != "_":
                    message = "放送中です。"
                    self._tweet_with_picture(program, self._broadcaster_check(program), message)

    def _time_check(self, program, *time_ago):  # *time_age = [時,分]
        regex = "^([0-9]{2}):([0-9]{2})-([0-9]{2}):([0-9]{2}).*$"
        start_hour = int(re.sub(r"{}".format(regex), r"\1", program["title"]))
        start_minute = int(re.sub(r"{}".format(regex), r"\2", program["title"]))
        end_hour = int(re.sub(r"{}".format(regex), r"\3", program["title"]))
        end_minute = int(re.sub(r"{}".format(regex), r"\4", program["title"]))
        if start_hour >= 6:
            start_time = datetime.datetime(self.time.year, self.time.month, self.time.day, start_hour, start_minute, 0)
            if end_hour >= 6:
                end_time = datetime.datetime(self.time.year, self.time.month, self.time.day, end_hour, end_minute, 0)
            else:
                end_time = datetime.datetime(self.time.year, self.time.month, self.time.day + 1, end_hour, end_minute, 0)
        else:
            start_time = datetime.datetime(self.time.year, self.time.month, self.time.day + 1, start_hour, start_minute, 0)
            end_time = datetime.datetime(self.time.year, self.time.month, self.time.day + 1, end_hour, end_minute, 0)
        check_time = self.time + datetime.timedelta(hours=time_ago[0]) + datetime.timedelta(minutes=time_ago[1])
        if start_time < check_time and check_time < end_time:
            return True
        else:
            return False

    def _broadcaster_check(self, program):
        for i in self.broadcaster:
            if program.find("a", {"class": "v3ch"}).text == i:
                return i
        return "_"

    def _return_soup(self):
        response = requests.get(self.url + "?date=" + self.time.strftime("%Y/%m/%d"))
        if response.status_code == 404:
            sys.stderr.write('Error: usage: URL page notfound.\n')
            sys.exit(1)
        html = response.text.encode('utf-8', 'ignore')
        return BeautifulSoup(html, "lxml")

    def _tweet_with_picture(self, program, broadcaster, message):
        title = program.find("a", {"class": "v3title"}).text
        atime = program["title"]
        weekday = self._check_weekday()
        tweet = title + "\n" + broadcaster + ": " + weekday + " " + atime + "\n" + "\n" + message
        self.api.update_with_media(filename="{0}/.images/{1}-{2}/{3}.jpg".format(os.path.expanduser('~'), str(self.time.year), self._check_season(), self._escaping(title)), status=tweet)

    def _check_weekday(self):
        if self.time.weekday() == 0:
            return "月曜"
        elif self.time.weekday() == 1:
            return "火曜"
        elif self.time.weekday() == 2:
            return "水曜"
        elif self.time.weekday() == 3:
            return "木曜"
        elif self.time.weekday() == 4:
            return "金曜"
        elif self.time.weekday() == 5:
            return "土曜"
        elif self.time.weekday() == 6:
            return "日曜"
        else:
            return "_"

    def _check_season(self):
        if 1 <= self.time.month and self.time.month <= 3:
            return "winter"
        elif 4 <= self.time.month and self.time.month <= 6:
            return "spring"
        elif 7 <= self.time.month and self.time.month <= 9:
            return "summer"
        elif 10 <= self.time.month and self.time.month <= 12:
            return "autumn"

    def _escaping(self, title):
        escape_list = ['\\', '/', ':', '*', '?', '"', '>', '<', '|']
        for i in escape_list:
            title = title.replace(i, " ")
        return title


def main():
    broadcaster_list = [
        "NHK Eテレ",
        "日本テレビ",
        "テレビ朝日",
        "TBS",
        "テレビ東京",
        "フジテレビ",
        "TOKYO MX",
        "AT-X",
    ]
    C= "8K6BcNqg1OHPh2t2CZLOlxuDb"
    CO= "S4W13zYtG6GjH7xzaSQlVbUgx4h0sNVAkWPBUIZBdnsICQ7h02"
    A= "830059724624125952-faRkknQmBtleYPfV8XjeOS3aiLLFmI8"
    AC= "COv4C7HiUda1JltjvYus4ePhDXzKrpWKhQ8o6XYVrZK4k"
    now = datetime.datetime.now()
    Today_timetable = TimeTable(now, broadcaster_list,C,CO,A,AC)
    # Today_timetable.show_all()
    Today_timetable.now_program()
    # Today_timetable._return_soup()


if __name__ == "__main__":
    main()
