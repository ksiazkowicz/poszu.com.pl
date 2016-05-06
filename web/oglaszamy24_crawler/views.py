# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

from app import Oglaszamy24Crawler


def pull(request, template="gumtree_result.html"):
    crawler = Oglaszamy24Crawler()
    imported_data, crawled_pages = crawler.pull()

    return render_to_response(template, locals(), context_instance=RequestContext(request))

