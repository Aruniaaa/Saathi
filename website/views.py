from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .llm import process
import markdown
from supabase import Client, create_client
import os
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import Profile
from dotenv import load_dotenv
from functools import wraps
from markdown_it import MarkdownIt
from mdit_py_plugins.texmath import texmath_plugin

load_dotenv()


url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(url, key)

def login_required(view_func):
    """Custom decorator to require Supabase auth before accessing a feature"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def home(request):
    username = request.session.get("username")

    if username:
     return render(request, "website/home.html", {"username" : username})
    else:
        return render(request, "website/home.html", {})

@login_required
def chat(request):
    return render(request, "website/chat.html", {})

def contact(request):
    return render(request, "website/contacts.html", {})


@method_decorator(csrf_exempt, name='dispatch')
class ChatAPI(View):

    def post(self, request):

        try:

            # Try to parse JSON
            data = json.loads(request.body)
            print("Parsing the input...")


            query = data.get('query', '').strip()
            print("Got the query!!")


            if not query:
                return JsonResponse({
                    'error': 'No query provided'
                }, status=400)


            bot_response = process(query)

            md = MarkdownIt().use(texmath_plugin)
            bot_response = md.render(bot_response)

            return JsonResponse({
                'response': bot_response,
                'status': 'success'
            })

        except json.JSONDecodeError as e:
            return JsonResponse({
                'error': 'Invalid JSON in request'
            }, status=400)

        except Exception as e:

            return JsonResponse({
                'error': 'An error occurred processing your request',
                'details': str(e),
                'type': type(e).__name__
            }, status=500)

@login_required
def quiz_gen(request):
    pass

@login_required
def progress(request):
    pass




def login(request):
    if request.method == "GET":
        return render(request, "website/login.html", {})
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            response = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
        except Exception as e:
            return render(request, "website/login.html", {"message": str(e)})

        if response.user:
            user_id = response.user.id

            try:
                user = Profile.objects.get(supabase_id=user_id)
                username = user.username
            except Profile.DoesNotExist:
                username = email.split("@")[0]

            request.session["user_id"] = user_id
            request.session["username"] = username

            return redirect("home")



def signup(request):

    if request.method == "GET":
        return render(request, "website/signup.html", {})
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )

            user = response.user

            if not user:
                return render(request, "website/signup.html", {"message": "Signup failed. Try again!"})

            if user:
                new_user = Profile.objects.create(
                    supabase_id=user.id,
                    username=username,
                    email=email
                )
                new_user.save()

                request.session["user_id"] = user.id
                request.session["username"] = username

                return redirect("home")
        except Exception as e:
            return render(request, "website/signup.html", {"message" : str(e)})

def logout_view(request):
    request.session.flush()
    supabase.auth.sign_out()
    return redirect("home")
