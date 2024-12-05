from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Question, Choice, Vote
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, ProfileEditForm, UserProfileForm, QuestionForm, ChoiceFormSet
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def home(request):
    return render(request, 'basic.html')



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('polls:profile-edit')

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'registration/profile.html',{'user_profile': user_profile })



@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('polls:basic')


    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'registration/profile_edit.html', {'form': form})

@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Ваш аккаунта был удален.')
        return redirect('polls:basic')

    return render(request, 'registration/delete_profile.html', {'user': user})





class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        # # Проверка, активен ли вопрос
        # if question.end_date <= timezone.now():
        #     context['is_active'] = True
        # else:
        #     context['is_active'] = False

        # Проверка, проголосовал ли пользователь
        if self.request.user.is_authenticated:
            try:
                Vote.objects.get(user=self.request.user, question=question)
                context['has_voted'] = True
            except Vote.DoesNotExist:
                context['has_voted'] = False
        return context



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)


    if question.end_date <= timezone.now():
        print("Голосование завершено")
    else:
        print("Голосование не завершено")
    # Проверка, завершено ли голосование
    if not question.end_date <= timezone.now():
        return redirect('polls:results', pk=question.id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        # Проверка, не проголосовал ли уже пользователь
        if Vote.objects.filter(user=request.user, question=question).exists():
            messages.error(request, 'Вы уже проголосовали в этот опрос.')
            return redirect('polls:results', pk=question.id)
        Vote.objects.create(user=request.user, question=question, choice=selected_choice)
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save()

            for form in choice_formset:
                choice = form.save(commit=False)
                if choice.choice_text:
                    choice.question = question
                    choice.save()
            return redirect('polls:index')
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()

    return render(request, 'polls/create_question.html',
                  {'question_form': question_form, 'choice_formset': choice_formset})