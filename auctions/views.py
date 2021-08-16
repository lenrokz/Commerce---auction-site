from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Listing, Bid, Comment, Watchlist

listing = Listing.objects.all()

CHOICES = (
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Home', 'Home'),
        ('Vehicles', 'Vehicles'),
    )

class Comment_form(forms.Form):
    content = forms.CharField(max_length=100)

class Bid_form(forms.Form):
    addbid = forms.DecimalField(max_digits=6, decimal_places=2)

class Listing_form(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=64)
    image = forms.URLField(max_length=200)
    starting_price = forms.DecimalField(max_digits=6, decimal_places=2)
    category = forms.ChoiceField(widget=forms.Select, choices = CHOICES)




def index(request):
    return render(request, "auctions/index.html", {
        "listings":Listing.objects.filter(closed = False)
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

@login_required
def create_listing(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        form = Listing_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            starting_price = form.cleaned_data["starting_price"]
            listing = Listing(title=title, description=description, category=category, image=image, starting_price=starting_price)
            listing.user = user
            listing.save()
            return HttpResponseRedirect(reverse('listing_page', args=(listing.id,)))
        else:
            return render(request, "auctions/create_listing.html", {
        "form":Listing_form()   
            }) 
    return render(request, "auctions/create_listing.html", {
        "form":Listing_form()   
            }) 

@login_required
def listing_page(request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(id=listing_id)
    if "watchlist" not in request.session:
        request.session["watchlist"] = []
    if request.method == "POST":
        if request.POST.get("watchbutton") == 'Watchlist':
            watched = listing_id
            if not watched in request.session["watchlist"]:
                request.session["watchlist"] += [watched]
                return render(request, "auctions/watchlist.html", {
                    "watchlist": request.session["watchlist"]
                })
            else:
                 request.session["watchlist"].remove(watched)
                 return render(request, "auctions/watchlist.html", {
                    "watchlist": request.session["watchlist"]
                })   



        if not listing.closed:
            if request.POST.get("closebutton") == 'Close':
                listing.closed = True
                listing.save()
        commentform = Comment_form(request.POST)
        if commentform.is_valid():
            content = commentform.cleaned_data["content"]
            comment = Comment(content=content)
            comment.user = user
            comment.save()
            listing.comment.add(comment)
            listing.save()
            return HttpResponseRedirect(reverse('listing_page', args=(listing.id,)))
        bidform = Bid_form(request.POST)
        if bidform.is_valid():
            addbid = bidform.cleaned_data["addbid"]
            added = float(request.POST["addbid"])
            if addbid < listing.starting_price:
                return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "bidform": Bid_form(),
            "commentform": Comment_form(),
            "bidmassage": "Invalid bid, try again."
            })
            else:
                bids = Bid(addbid=addbid)
                bids.user = user
                bids.save()
                listing.bids.add(bids)
                listing.starting_price = added
                listing.save()
                return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "bidform": Bid_form(),
                "commentform": Comment_form(),
                "bidmassage": "Your bid is the highest."
            })    
        else:        
            return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "bidform": Bid_form(),
            "commentform": Comment_form(),
            "bidmassage": ""
            })
            
    else:        
            return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "bidform": Bid_form(),
            "commentform": Comment_form(),
            "bidmassage": ""
            })
@login_required
def watchlist_page(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.session["watchlist"]
    })


@login_required
def categories(request):
    return render(request, 'auctions/categories.html', {
        "categories": CHOICES
    })
@login_required
def category_listings(request, category):
    items = Listing.objects.filter(category=category)
    return render(request, 'auctions/category_listings.html', {
        "items":items,
        "category": category
    })
