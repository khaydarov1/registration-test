from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewUserForm, QuestionForm
from .models import Question, Choice


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registation successful. ")
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration.Invalid information")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now login in as{username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password. ")
    else:
        messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def index(request):
    print(request.user)
    savollar = Question.objects.all()
    return render(request, 'users/index.html', {'savollar': savollar})


def savol_detail(request, id):
    savol = get_object_or_404(Question, id=id)
    return render(request, 'users/detail.html', {"savol": savol})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_question(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:home")
    return render(request, 'users/question_form.html', {"form": form})


def check_answer(request, id):
    variant = get_object_or_404(Choice, id=id)
    # to'g'rimi yo'qmi tekshirib, natijalar tablitsasiga saqlaymiz
    question_ids = list(Question.objects.values_list('id', flat=True))
    try:
        next_question_id = question_ids[question_ids.index(variant.question.id) + 1]
    except Exception as e:
        print(e)
        next_question_id = None
    if next_question_id:
        return redirect("users:savol_detail", id=next_question_id)

        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (total * 10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'users/result.html', context)
    else:
        questions = Question.objects.all()
        context = {
            'questions': questions
        }
        return render(request, 'users/checked.html', {'correct': variant.is_correct})
