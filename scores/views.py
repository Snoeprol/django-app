from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from scores.forms import DateRange, EditUserForm
from scores.models import Score, TotalScore, User


# Create your views here.
def home(request):
    #Check if post
    if request.method == 'POST':
        form = DateRange(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['date1']
            end_date = form.cleaned_data['date2']

            # Filter scores by date
            scores = Score.objects.filter(date__range=[start_date, end_date])
            total_scores = {}
            high_scores = {}
            
            # Get total scores and high scores per user
            for score in scores:
                if score.user in total_scores:
                    total_scores[score.user] += score.score
                else:
                    total_scores[score.user] = score.score
                if score.user in high_scores:
                    if score.score > high_scores[score.user]:
                        high_scores[score.user] = score.score
                else:
                    high_scores[score.user] = score.score
                

            return render(request, 'home.html', {'form' : form, 'total_scores' : total_scores, 'high_scores' : high_scores})
        
    # Form for the date input
    form = DateRange()
    return render(request, 'home.html', {'form' : form})
    
def display_members(request):
    # Get all users
    users = User.objects.all()
    
    return render(request, 'display.html', {'users' : users})

def auth(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Login the user
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            # Redirect to edit members page
            return render(request, 'succes.html', {'form' : form})

    # Login form
    form = AuthenticationForm()
    
    return render(request, 'sorry.html', {'form' : form})

def edit_members(request):
    if request.user.is_superuser:
        users = [user.username for user in User.objects.all()]
        
        # Check if there are any users
        if len(users) == 0:
            return render(request, 'no_users.html')
        
        return render(request, 'list_members.html', {'users' : users})
    else:
        return render(request, 'not_super.html')
def user_page(request, user):
    # Make sure user is superuser
    if request.user.is_superuser:
            
        if request.method == 'POST':
            form = EditUserForm(request.POST)
            if form.is_valid():
                # Extract data from form
                date = form.cleaned_data['date']
                score = form.cleaned_data['score']
                score = Score.create(user=user, date=date, score=score)
                score.save()

        
        form = EditUserForm()
        return render(request, 'edit_member.html', {'form' : form, 'user' : user})
    else:
        return render(request, 'not_super.html')