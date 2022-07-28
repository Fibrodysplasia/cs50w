from django.shortcuts import render, redirect
import random
import markdown
import re
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(util.get_entry(title)),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "error": "Entry does not exist"
        })

def search(request):
    if request.method == "POST":
        query = str(request.POST.get("query"))
        entries = util.list_entries()
        pattern = re.compile(query, re.IGNORECASE)
        if query != "":
            results = []
            for entry in entries:
                if re.fullmatch(pattern, entry):
                    return render(request, "encyclopedia/entry.html", {
                        "entry": markdown.markdown(util.get_entry(entry)),
                        "title": query
                    })
                elif re.search(pattern, entry):
                    results.append(entry)
            if len(results) == 0:
                return render(request, "encyclopedia/error.html", {
                    "title": query,
                    "error": "No results found"
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "results": results,
                    "query": query
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
        
def create(request):
    if request.method == "POST":
        title = str(request.POST.get("title"))
        content = str(request.POST.get("content"))
        entries = util.list_entries()
        pattern = re.compile(title, re.IGNORECASE)
        for entry in entries:
            if re.fullmatch(pattern, entry):
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "error": "Entry already exists"
                })
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown.markdown(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/create.html")
    
def edit(request, title):
    if request.method == "POST":
        title = str(request.POST.get("title"))
        content = str(request.POST.get("content"))
        util.save_entry(title, content)
        return redirect(entry, title=title)
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })

def rngpage(request):
    entries = util.list_entries()
    title = entries[random.randint(0, len(entries) - 1)]
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown.markdown(util.get_entry(title))
    })