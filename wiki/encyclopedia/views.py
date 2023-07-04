import random

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages

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


class EntryForm(forms.Form):
    title = forms.CharField(max_length=255, label="Title")
    text = forms.CharField(label="content", widget=forms.Textarea(attrs=
                {'placeholder': 'Type your text as Markdown'}))

def create_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if util.get_entry(title):
                message_text = "The entry with this title already exist! " \
                                "please choose another title"
                messages.error(request, message_text)
                return render(request, "encyclopedia/entry_form.html", {
                    "form":form
                })

            else:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("entry", args=[title]))
    
    return render(request, "encyclopedia/entry_form.html", {
        "form":EntryForm()
    })


def edit_entry(request, title):
    content = util.get_entry(title)
    form = EntryForm(initial={"title":title, "text": content})

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    
    return render(request, "encyclopedia/entry_form.html", {
        "form":form
    })


def random_entry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[title]))