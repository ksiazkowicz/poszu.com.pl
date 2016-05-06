from crawler.app import GenericCrawler


class Oglaszamy24Crawler(GenericCrawler):
    name = "oglaszamy24"
    crawling_urls = [
        "https://extraction.import.io/query/runtime/b95b5a1a-ef4f-4663-92d9-b59825eccd87?_apikey=1d7510385b8a44e0aae52fcb69cd92596aab14039d36aca6e26593d0719c357aecfc66c2fd72b082368a1d8a81e60a1750d29277d4b9de345ac6d6a95dff63f49c528c9985929814ea31dd0f875a4b4d&url=http%3A%2F%2Fwww.oglaszamy24.pl%2Fogloszenia%2Fpozostale%2Fzgubione%2F%3Fstd%3D{{ page }}%26amp%3Bresults%3D{{ page }}",
        "https://extraction.import.io/query/runtime/b95b5a1a-ef4f-4663-92d9-b59825eccd87?_apikey=1d7510385b8a44e0aae52fcb69cd92596aab14039d36aca6e26593d0719c357aecfc66c2fd72b082368a1d8a81e60a1750d29277d4b9de345ac6d6a95dff63f49c528c9985929814ea31dd0f875a4b4d&url=http%3A%2F%2Fwww.oglaszamy24.pl%2Fogloszenia%2Fpozostale%2Fznalezione%2F%3Fstd%3D{{ page }}%26amp%3Bresults%3D{{ page }}"
    ]
    lost_urls_ids = [0, ]
    manual_detection = False
    schema = {
        "desc": ('DESCRIPTION', "text"),
        "name": ('TITLE LINK', "text"),
        "url": ('TITLE LINK', "href"),
        "photo": ('IMAGE', 'src'),
        "location": ('CAT LINK', 'text'),
    }
