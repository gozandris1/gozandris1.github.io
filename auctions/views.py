from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ValidationError

from .models import User, Category, Listing

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(
        max_length=256, 
        widget=forms.Textarea(),
        help_text='Write here your message!')
    startingbid = forms.IntegerField()
    picture = forms.URLField(label='Picture url', required=False)
    categorytype = forms.ModelChoiceField(queryset=Category.objects.all())
#    owner = forms.IntegerField(widget=forms.HiddenInput())

#    def __init__(self, *args, **kwargs):
#        self.request = kwargs.pop("request")
#        super(NewListingForm,self).__init__(*args, **kwargs)
#        self.fields['startingbid'].initial = self.request.user.id

    def clean_startingbid(self):
        startingbid = int(self.cleaned_data["startingbid"])
        if startingbid > 9999:
            raise forms.ValidationError('Kisebb értéket adj meg ennél')
        return startingbid

class BidForm(forms.Form):
    newbid = forms.IntegerField()
    initialbid = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        # Get 'initial' argument if any
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
              # We have initial arguments, fetch 'listing' placeholder variable if any
              listing = initial_arguments.get('listing',None)
              # Now update the form's initial values if listing
              if listing:
                    updated_initial['newbid'] = getattr(listing, 'actualbid', None)
                    updated_initial['initialbid'] = getattr(listing, 'actualbid', None)
        kwargs.update(initial=updated_initial)
        super(BidForm, self).__init__(*args, **kwargs)

    def clean(self):
        newbid = int(self.cleaned_data["newbid"])
        initialbid = int(self.cleaned_data["initialbid"])
        currentbid = initialbid
        if newbid <= currentbid:
            message = "Nagyobb értéket adj meg ennél"
            self.add_error('newbid', message)
        

class CommentForm(forms.Form):
    name = forms.CharField(label='Your name')
    comment = forms.CharField()

def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createlisting(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        
        if form.is_valid():
            addlisting=Listing()
            addlisting.title = form.cleaned_data['title']
            addlisting.description = form.cleaned_data['description']
            addlisting.startingbid = form.cleaned_data['startingbid']
            addlisting.picture = form.cleaned_data['picture']
            addlisting.categorytype = form.cleaned_data['categorytype']
            addlisting.owner = request.user
            addlisting.save()

            return render(request, "auctions/newlisting.html",{
                "categories" : Category.objects.all(),
                "form" : NewListingForm(),
                "message" : "form kitöltve"
            })
        else:
            return render(request,"auctions/newlisting.html",{
                "categories" : Category.objects.all(),
                "message" : "form hibára futott",
                "form" : form
            })
    else:
        return render(request, "auctions/newlisting.html",{
            "categories" : Category.objects.all(),
            "form" : NewListingForm()
        })


def categorypage(request):
    pass

def whatchlistpage(request):
    pass

def listingpage(request, listing_id):
    if request.method == "POST":
        listing= Listing.objects.get(pk=listing_id)
        bidform = BidForm(request.POST)
        if bidform.is_valid():
            listing.actualbid = bidform.cleaned_data['newbid']
            listing.save()
            message = 'Successfull bid'
            bidform = BidForm(initial={'listing':listing,})
            return render(request, "auctions/listing.html",{
            "listing" : listing,
            "bidform": bidform,
            "message":message
            })
        else:
            message = "The form is not valid"
            #bidform = BidForm(initial={'listing':listing,})
            return render(request, "auctions/listing.html",{
            "listing" : listing,
            "message" : message,
            "bidform" : bidform
            })
    else:
        listing= Listing.objects.get(id=listing_id)
        bidform = BidForm(initial={'listing':listing,})
        return render(request, "auctions/listing.html",{
            "listing" : listing,
            "bidform": bidform
        })
