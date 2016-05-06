# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

from app import GumtreeCrawler


def pull(request, template="gumtree_result.html"):
    crawler = GumtreeCrawler()
    imported_data, crawled_pages = crawler.pull()

    return render_to_response(template, locals(), context_instance=RequestContext(request))

