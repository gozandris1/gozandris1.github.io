from django.shortcuts import render
from django import forms
from . import util
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2


class NewTaskForm(forms.Form):
    searchtext = forms.CharField(label="Search")

class CreateNewPage(forms.Form):
    text = forms.CharField(label="Textarea")
    title = forms.CharField(label="Title")

class EditPage(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}),label="TextArea")

def index(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            searchtext = form.cleaned_data["searchtext"]
            #itt csinálunk keresést
            entries = util.list_entries()
            searchresult = []
            for entry in entries:
                if searchtext == entry:
                    return loadpage(request,entry)
                elif searchtext.lower() in entry.lower():
                    searchresult.append(entry)
            if not searchresult:
                searchresult.append(f"No result for {searchtext}")
            return search(request,searchresult)
        else:
            return render(request, "encyclopedia/index.html",{
                "form":NewTaskForm()
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":NewTaskForm()
    })

def loadpage(request,pagename):
    content=markdown2.markdown(util.get_entry(pagename))
    return render(request, "encyclopedia/page.html", {
        "content":content,
        "title":pagename,
        "form":NewTaskForm()
    })

def createpage(request):
    if request.method == "POST":
        form = CreateNewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text1= f"#{title} \n"
            text2 = form.cleaned_data["text"]
            text= text1 + text2

            if exist(title):
                util.save_entry(title,text)
                return HttpResponseRedirect(f"wiki/{title}")
            else:
                return render(request,"encyclopedia/newpage.html",{
                "form":NewTaskForm(),
                "createform":CreateNewPage(),
                "errormessage":"The page already exists, try to modify"
                })
        else:
            return render(request,"encyclopedia/newpage.html",{
            "form":NewTaskForm(),
            "createform":CreateNewPage()
        })
    return render(request,"encyclopedia/newpage.html",{
        "form":NewTaskForm(),
        "createform":CreateNewPage()
    })

def search(request,list):
        return render(request, "encyclopedia/search.html",{
        "entries":list,
        "form":NewTaskForm()
        })

def exist(title):
    entries = util.list_entries()
    if title in entries:
        return False
    else:
        return True

def randpage(request):
    entries = util.list_entries()
    numberofentries = int(len(entries))
    getthisnumber = random.randint(0,numberofentries-1)
    try:
        item = entries[getthisnumber]
        print(getthisnumber)
    except:
        print(getthisnumber)
    return HttpResponseRedirect(f"wiki/{item}")

def editpage(request,pagename):
    content=util.get_entry(pagename)
    return render(request, "encyclopedia/edit.html", {
        "editform":EditPage(),
        "content":content,
        "title":pagename,
        "form":NewTaskForm()
    })

def savepage(request,pagename):
    form = EditPage(request.POST)
    if form.is_valid():
        content = form.cleaned_data["textarea"]
        util.save_entry(pagename,content)
        return editpage(request,pagename)
