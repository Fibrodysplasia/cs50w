from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task", max_length=20, min_length=3)
    priority = forms.ChoiceField(choices=((1, "Low"), (2, "Medium"), (3, "High")))

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
        })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })