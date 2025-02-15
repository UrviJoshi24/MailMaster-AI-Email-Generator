from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import SubjectLineForm
from .models import SubjectLine
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json
from .models import EmailReply  # Import your EmailReply model


@login_required  # Ensure only logged-in users can access saved replies
def get_saved_replies(request):
    if request.method == "GET":
        saved_replies = EmailReply.objects.filter(user=request.user).values(
            'id', 'ai_generated_reply', 'edited_reply', 'email_body', 'tone', 'writing_style', 'save_as'
        )

        return JsonResponse({"saved_replies": list(saved_replies)}, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt  # Only use this if CSRF protection is not handled elsewhere
@login_required  # Ensure the user is logged in
def save_edited_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Extract data from the request
        ai_generated_reply = data.get('ai_generated_reply')
        edited_reply = data.get('edited_reply')
        email_body = data.get('email_body')
        tone = data.get('tone')
        writing_style = data.get('writing_style')
        save_as = data.get('save_as')

        # Create or update the EmailReply instance
        email_reply, created = EmailReply.objects.update_or_create(
            user=request.user,  # Associate with the logged-in user
            save_as=save_as,  # Use 'save_as' to identify unique replies
            defaults={
                'ai_generated_reply': ai_generated_reply,
                'edited_reply': edited_reply,
                'email_body': email_body,
                'tone': tone,
                'writing_style': writing_style
            }
        )
        # Return a success response
        return JsonResponse({"success": True, "email_reply_id": email_reply.id})

    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def get_subject_lines(request):
    subject_lines = SubjectLine.objects.filter(user=request.user)
    subjects_data = [
        {
            'id': subject.id,
            'content': subject.content,
            'ai_generated': subject.ai_generated,
            'edited_subject': subject.edited_subject,
            'save_as': subject.save_as,
        }
        for subject in subject_lines
    ]
    return JsonResponse(subjects_data, safe=False)

@login_required
def get_subject(request, subject_id):
    try:
        subject = SubjectLine.objects.get(id=subject_id, user=request.user)
        subject_data = {
            'id': subject.id,
            'content': subject.content,
            'ai_generated': subject.ai_generated,
            'edited_subject': subject.edited_subject,
        }
        return JsonResponse(subject_data)
    except SubjectLine.DoesNotExist:
        return JsonResponse({"error": "Subject line not found"}, status=404)

@csrf_exempt
def generate_reply_email_writer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email_body = data.get('content')
        reply_tone = data.get('reply')
        writing_style = data.get('writing_style')

        # Logic to generate AI reply email based on body, tone, and writing style
        ai_generated_reply = f"AI-generated reply for: {email_body} with tone {reply_tone} and style {writing_style}"  
        # Replace with your actual AI logic or model
        return JsonResponse({"ai_generated_reply": ai_generated_reply})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def generate_subject_line(request):
    if request.method == "POST":
        data = json.loads(request.body)
        subject = data.get('subject')

        # Logic to generate AI subject line
        ai_generated_subject = f"AI generated for: {subject}"  # Replace this with actual AI logic

        return JsonResponse({"ai_generated_subject": ai_generated_subject})

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt  # Consider using CSRF protection for security
@login_required  # Ensure the user is logged in to save data
def save_edited_subject(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        # Extract data from the request
        content = data.get('content')  # Original content entered by the user
        ai_generated = data.get('ai_generated')  # AI-generated subject line
        edited_subject = data.get('edited_subject')  # User-edited subject line
        saveas = data.get('save_as')

        # Create or update the subject line instance
        subject_line, created = SubjectLine.objects.update_or_create(
            user=request.user,  # Link to the current user
            content=content,  
            save_as = saveas,  # Original content
            defaults={
                'ai_generated': ai_generated,
                'edited_subject': edited_subject
            }
        )

        # Return success response
        return JsonResponse({"success": True, "subject_line_id": subject_line.id})

    return JsonResponse({"error": "Invalid request method"}, status=400)

def index(request):
    return render(request, 'myapp/index.html')

def dashboard(request):
    return render(request, 'myapp/dashboard.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        # Create a new user
        user = User(username=username, password=make_password(password), email=email)
        user.save()

        messages.success(request, "Registration successful! You can now login.")
        return redirect('/')

    return render(request, 'myapp/index.html')

# Handle user login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        user = authenticate(username=username, password=password)
        print(password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/')

# Handle user logout
def logout_view(request):
    print("hello   ")
    # Django's logout function clears the session
    logout(request)
    # Redirect to the login page after logout
    return redirect('/')  # Replace 'index' with your login page URL name

def trash_view(request):
    return render(request, 'myapp/trash.html')

def version_control(request):
    return render(request, 'myapp/versioncontrol.html')

@login_required
def account_view(request):
    user = request.user  # Get logged-in user
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
    }
    return render(request, 'myapp/account.html', context)


def generate_email(request):
    response_text = ""
    if request.method == 'POST':
        topic = request.POST.get('emailTopic', '')
        tone = request.POST.get('tone', 'neutral')
        writing_style = request.POST.get('writing-style', 'casual')
        recipient = request.POST.get('name','')
        additional_details = request.POST.get('details', '')
        print(topic)

        # Prepare the prompt based on the form data
        prompt = f'''
        Generate an email based on the following parameters:
        1. Topic: {topic}
        2. Tone: {tone}
        3. Writing Style: {writing_style}
        4. Additional Details: {additional_details}
        5. Recipient: {recipient}

        Please create a well-structured email that aligns with these inputs in detail of 3 paragraphs.
        '''
        api_url = "https://00d9-35-232-82-179.ngrok-free.app/generate"
        api_response = requests.post(api_url, json={"prompt": prompt})

        if api_response.status_code == 200:
            response_text = api_response.json()['response']
            email_start_index = response_text.find("Dear")
    
            if email_start_index != -1:
                response_text = response_text[email_start_index:]
            
            start_index = response_text.find("Respected")
            if start_index != -1:
                response_text = response_text[start_index:]
        else:
            response_text = "Error generating email."
        
        print(response_text)
        return JsonResponse({'response_text': response_text})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def generate_subject(request):
    response_text = ""
    if request.method == 'POST':
        content = request.POST.get('subject', '')
        print(content)

        prompt=f'''Generate a formal and clear subject line based on the following email content:

        Email Content:{content}

        Please provide the subject line below:
        '''
        api_url = "https://00d9-35-232-82-179.ngrok-free.app/generate"
        api_response = requests.post(api_url, json={"prompt": prompt})

        if api_response.status_code == 200:
            response_text = api_response.json()['response']
            print(response_text)
            start_index = response_text.find("below:")
            if start_index != -1:
                response_text = response_text[start_index+6:]
        else:
            response_text = "Error generating subject."
        
        print(response_text)
        return JsonResponse({'response_text': response_text})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def generate_reply_email(request):
    response_text = ""
    if request.method == 'POST':
        topic = request.POST.get('emailBody', '')
        tone = request.POST.get('replytone', 'neutral')
        writing_style = request.POST.get('replywriting-style', 'casual')
        print(topic)

        # Prepare the prompt based on the form data
        prompt = f'''
        Generate a reply email based on the following parameters:

        Email Content: {topic}
        Tone: {tone}
        Writing Style: {writing_style}

        Please provide email below:
        Dear/Respected 
        '''
        api_url = "https://00d9-35-232-82-179.ngrok-free.app/generate"
        api_response = requests.post(api_url, json={"prompt": prompt})

        if api_response.status_code == 200:
            response_text = api_response.json()['response']
            print(response_text)
            email_start_index = response_text.find("Dear")
            second_index = response_text.find('Dear', email_start_index + 1)
    
            if second_index != -1:
                response_text = response_text[second_index:]
            
            start_index = response_text.find("Respected")
            s_index = response_text.find('Respected', start_index + 1)
            if s_index != -1:
                response_text = response_text[s_index:]
        else:
            response_text = "Error generating email."
        
        return JsonResponse({'response_text': response_text})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)