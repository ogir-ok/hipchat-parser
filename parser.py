#!/bin/python3

import re
import json
from urllib import request

import lxml.html

HTTP_REGEX = re.compile(r"https?://.*")

# Links parsing regexp got from http://Qryancompton.net/2015/02/16/url-extraction-in-python/
LINK_REGEX = re.compile(r"""(?P<value>(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@))))""")
MENTION_REGEX = re.compile(r"\B@(?P<value>\w+)")
EMOTICON_REGEX = re.compile(r"\((?P<value>\w{1,15})\)")

# timeout to fetch urls to get title
FETCH_TIMEOUT = 2


class Parser(object):
    regex = None

    def __init__(self):
        self.occurences = []

    def parse(self, message):
        for match in self.regex.finditer(message):
            dict_data = match.groupdict()
            parsed = self.parse_value(dict_data['value'])
            self.occurences.append(parsed)

    def parse_value(self, value):
        return value


class LinksParser(Parser):
    regex = LINK_REGEX

    def parse_value(self, value):
        res = {
            'url': value,
            'title': None
        }
        try:
            page_url = value
            if not HTTP_REGEX.match(page_url):
                page_url = "http://" + value
            with request.urlopen(page_url, timeout=FETCH_TIMEOUT) as page:
                html = lxml.html.parse(page.read())
                res['title'] = html.find("./head/title").text
        except Exception as e:
            # in case of exception during fetch or parse, no title
            # print(e)
            pass

        return res






class MentionsParser(Parser):
    regex = MENTION_REGEX


class EmoticonsParser(Parser):
    regex = EMOTICON_REGEX


def parse_message(message, as_json=True, indent=4):
    # Tried to merge all regexps in one big, but lot of small is easier to
    # understand and work faster according testing
    res = {}
    parsers = {
        'mentions': MentionsParser(),
        'emoticons': EmoticonsParser(),
        'links': LinksParser()
    }


    for key, parser in parsers.items():
        parser.parse(message)
        if parser.occurences:
            res[key] = parser.occurences

    if as_json:
        res = json.dumps(res, indent=indent)
    return res





def main():
    res = parse_message("""
                        @bob, @john! (success) such a cool feature@;
                        https://twitter.com/jdorfman/status/430511497475670016 @maria (good) (start) (toolongtobeemotionreally)
                         @! https:// is cool staff www. www.google.com
                        http://google.com
                        email is assa@google.com
                        password is !@iam!!
                         """)
    print(res)

if __name__ == "__main__":
    main()
