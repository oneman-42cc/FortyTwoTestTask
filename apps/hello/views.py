from django.shortcuts import render


def home(request):

    """A view for home page. Renders user's profile."""

    return render(request, "hello/home.html", {})
