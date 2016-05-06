from crawler.app import GenericCrawler


class GumtreeCrawler(GenericCrawler):
    name = "gumtree"
    crawling_urls = [
        "https://extraction.import.io/query/runtime/eeb84685-a55f-4dd2-929c-acf349c8025f?_apikey=1d7510385b8a44e0aae52fcb69cd92596aab14039d36aca6e26593d0719c357aecfc66c2fd72b082368a1d8a81e60a1750d29277d4b9de345ac6d6a95dff63f49c528c9985929814ea31dd0f875a4b4d&url=http%3A%2F%2Fwww.gumtree.pl%2Fs-rzeczy-zagubione%2Fpage-{{ page }}%2Fv1c9036p{{ page }}"
    ]
    manual_detection = True
    schema = {
        "desc": ('HIDDEN DESCRIPTION', "text"),
        "name": ('HREF LINK', "text"),
        "url": ('HREF LINK', "href"),
        "photo": ('THUMBM IMAGE', 'src'),
        "location": None,
    }

    def process_request(self, data):
        """
        Gets data from request and parses it. Built with import.io in mind.
        :param data: item from import.io
        :return: processed dictionary
        """
        results = super(GumtreeCrawler, self).process_request(data)

        # get location from data
        try:
            location_verbose = data['CATEGORY VALUE'][0]['text'].replace("zgubiono lub znaleziono , ", "")
        except:
            location_verbose = ""

        # attempt to process it
        try:
            location = self.geolocator.geocode(location_verbose)
        except:
            print "Detecting location failed."
            location = None

        results["location"] = location

        # our work is done
        return results

