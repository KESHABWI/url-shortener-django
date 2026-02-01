from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import ShortenedURL
from .forms import URLForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    urls = request.user.urls.all().order_by('-created_at')
    form = URLForm()
    return render(request, 'shortener/dashboard.html', {'urls': urls, 'form': form})

@login_required
def create_url(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_obj = form.save(commit=False)
            url_obj.user = request.user
            custom_code = form.cleaned_data.get('custom_code')
            if custom_code:
                url_obj.short_code = custom_code
            url_obj.save()
            messages.success(request, "URL shortened successfully!")
            return redirect('dashboard')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    return redirect('dashboard')

def redirect_url(request, short_code):
    url_obj = get_object_or_404(ShortenedURL, short_code=short_code)
    
    if url_obj.is_expired:
        return render(request, 'shortener/expired.html', status=410)
    
    url_obj.clicks += 1
    url_obj.save()
    return redirect(url_obj.long_url)

@login_required
def delete_url(request, pk):
    url_obj = get_object_or_404(ShortenedURL, pk=pk, user=request.user)
    if request.method == 'POST':
        url_obj.delete()
        messages.success(request, "URL deleted successfully!")
    return redirect('dashboard')

@login_required
def edit_url(request, pk):
    url_obj = get_object_or_404(ShortenedURL, pk=pk, user=request.user)
    if request.method == 'POST':
        form = URLForm(request.POST, instance=url_obj)
        if form.is_valid():
            url_obj = form.save(commit=False)
            custom_code = form.cleaned_data.get('custom_code')
            if custom_code:
                url_obj.short_code = custom_code
            url_obj.save()
            messages.success(request, "URL updated successfully!")
            return redirect('dashboard')
    else:
        form = URLForm(instance=url_obj, initial={'custom_code': url_obj.short_code})
    return render(request, 'shortener/edit.html', {'form': form, 'url': url_obj})

import qrcode
from io import BytesIO
from django.http import HttpResponse

def qr_code_view(request, short_code):
    url_obj = get_object_or_404(ShortenedURL, short_code=short_code)
    full_url = request.build_absolute_uri(url_obj.get_absolute_url())
    
    img = qrcode.make(full_url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
