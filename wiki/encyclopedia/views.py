from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

from markdown2 import Markdown


def index(request):
    entries = util.list_entries()
    q = request.GET.get('q', '')

    if q:
        if q in entries:
            return HttpResponseRedirect(reverse("entry", args=[q]))
        else:
            entries = [title for title in entries if q in title]

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    if entry:
        entry = markdowner.convert(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title, "entry": entry
    })