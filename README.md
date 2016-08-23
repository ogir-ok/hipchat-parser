# hipchat-parser
hipchat-like parser for text

also go version (not final yet) https://github.com/ogir-ok/hipchat-parser-go

# installation
git clone https://github.com/ogir-ok/hipchat-parser.git

cd hipchat-parser

pip install -r requirements.txt

# usage
python3 -m "parser" "your message with @mentions http://urls.com  (emotion)"

output example:

<pre>
{
    "emoticons": [
        "emotion"
    ],
    "mentions": [
        "mentions"
    ],
    "links": [
        {
            "title": null,
            "url": "http://urls.com"
        }
    ]
}
</pre>

# tests
run python3 test.py
