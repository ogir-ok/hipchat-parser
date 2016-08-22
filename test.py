import unittest
from parser import parse_message


class TestParser(unittest.TestCase):
    CASES = [
        ("@chris you around?",
            {"mentions": ["chris"]}),
        ("Good morning! (megusta) (coffee)",
            {"emoticons": ["megusta", "coffee"]}),
        ("Olympics are starting soon; http://www.google.com",
            {'links': [{'title': 'Google', 'url': 'http://www.google.com'}]}),
        ("""@bob @john (success) such a cool feature;
            https://twitter.com/jdorfman/status/430511497475670016""",
                 {'mentions': ['bob', 'john'],
                  'emoticons': ['success'],
                  'links': [{'url': 'https://twitter.com/jdorfman/status/430511497475670016',
                             'title': 'Justin Dorfman on Twitter: "nice @littlebigdetail from @HipChat (shows hex colors when pasted in chat). http://t.co/7cI6Gjy5pq"'}
                            ]
                  })
    ]
    def test_parse(self):
        for case, waited_res in self.CASES:
            res = parse_message(case, as_json=False)
            print(res, waited_res)
            assert res == waited_res

def test_main():
    unittest.main()

if __name__ == '__main__':
    test_main()

