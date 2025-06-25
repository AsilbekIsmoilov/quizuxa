from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import InternCreationForm
import random
import time
from django.utils.timezone import now
from datetime import timedelta
from collections import defaultdict
import json
from django.shortcuts import render, get_object_or_404


@login_required
def create_intern_view(request):
    if not request.user.is_trainer:
        return redirect('forbidden')  

    if request.method == 'POST':
        form = InternCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Intern.objects.create(user=user, trainer=request.user.trainer)
            return redirect('app:trainer_interns')
    else:
        form = InternCreationForm()

    context = {
        'form':form,
        "title":"Создать Стажера"
    }
    return render(request, 'app/create_intern.html', context)


@login_required
def trainer_interns_view(request):
    if not request.user.is_trainer:
        return redirect('forbidden')

    trainer = request.user.trainer
    interns = trainer.interns.all().select_related('user')
    results_qs = TestResult.objects.filter(intern__in=interns)
    results_dict = {r.intern.pk: r for r in results_qs}
    return render(request, 'app/trainer_interns.html', {
        'interns': interns,
        'results': results_dict,
        "title":"Главная Страница"
    })

@login_required
def intern_dashboard(request):
    if not request.user.is_intern:
        return redirect('forbidden')

    intern = request.user.intern
    results = TestResult.objects.filter(intern=intern).order_by('-created_at')
    last_result = results.first()

    test_done = False
    can_retry_time = None
    current_time = now()

    total_questions = Question.objects.count()
    wrong_answers = None 

    if last_result:
        total_questions = last_result.total_questions
        wrong_answers = total_questions - last_result.score

        retry_delay = timedelta(minutes=5)
        can_retry_time = last_result.created_at + retry_delay
        if current_time < can_retry_time:
            test_done = True

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        if full_name and (not test_done or (can_retry_time and current_time >= can_retry_time)):
            request.session['full_name'] = full_name
            return redirect('app:start_test')

    return render(request, 'app/intern_dashboard.html', {
        'test_done': test_done,
        'can_retry_time': can_retry_time,
        'now': current_time,
        'results': results,
        'result': last_result,
        'total_questions': total_questions,
        'wrong_answers': wrong_answers,
        'title': f"Стажер: {request.user.username}",
    })


@login_required
def start_test_view(request):
    if not request.user.is_intern:
        return redirect('forbidden')

    intern = request.user.intern

    if request.method == 'POST':
        total = 0
        correct = 0
        try:
            start_time = float(request.POST.get('start_time', '').replace(',', '.'))
        except ValueError:
            return redirect('app:intern_dashboard')

        end_time = time.time()
        duration_seconds = int(end_time - start_time)

        for key, value in request.POST.items():
            if key.startswith('question_'):
                answer_id = value
                try:
                    answer = Answer.objects.get(id=answer_id)
                except Answer.DoesNotExist:
                    continue
                InternAnswer.objects.create(intern=intern, answer=answer)
                total += 1
                if answer.is_correct:
                    correct += 1

        full_name = request.session.get('full_name', '')

        if duration_seconds >= 60:
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            duration_display = f"{minutes:02d}:{seconds:02d} мин"
        else:
            duration_display = f"{duration_seconds} сек"

        TestResult.objects.create(
            intern=intern,
            score=correct,
            duration_minutes=duration_display,
            full_name=full_name
        )

        request.session.pop('start_time', None)
        request.session.pop('question_ids', None)
        request.session.pop('full_name', None)

        return redirect('app:intern_dashboard')

    else:
        if 'question_ids' not in request.session:
            questions = list(Question.objects.all())
            if len(questions) >= 10:
                selected_questions = random.sample(questions, 10)
            else:
                random.shuffle(questions)
                selected_questions = questions

            request.session['question_ids'] = [q.id for q in selected_questions]
        else:
            selected_questions = list(Question.objects.filter(id__in=request.session['question_ids']))

        for q in selected_questions:
            answers = list(q.answers.all())
            random.shuffle(answers)
            q.randomized_answers = answers

        start_time = time.time()
        request.session['start_time'] = start_time
        full_name = request.session.get('full_name', '')

        return render(request, 'app/start_test.html', {
            'questions': selected_questions,
            'start_time': start_time,
            'full_name': full_name,
            "title":f"Стажер: {full_name}"
        })


@login_required
def intern_detail(request):
    if not request.user.is_trainer:
        return redirect('forbidden')

    trainer = request.user.trainer
    interns = trainer.interns.all().select_related('user')
    results_qs = TestResult.objects.filter(intern__in=interns).order_by('-created_at')

    results_by_intern = defaultdict(list)
    for r in results_qs:
        results_by_intern[r.intern.pk].append(r)

    return render(request, 'app/intern_detail.html', {
        'interns': interns,
        'results': results_by_intern,
        "title":"Список"
    })

@login_required
def intern_test_detail(request, pk):
    result = get_object_or_404(TestResult, pk=pk)
    intern = result.intern  
    user = intern.user

    total_questions = result.total_questions or 10
    score = result.score or 0
    wrong_answers = total_questions - score

    referer = request.META.get('HTTP_REFERER', '/')

    intern_answers = InternAnswer.objects.filter(intern=intern).select_related('answer__question')

    user_answers = {}
    for ia in intern_answers:
        question_id = ia.answer.question.id
        user_answers[question_id] = ia.answer.id

    question_ids = user_answers.keys()
    questions = Question.objects.filter(id__in=question_ids)
    for q in questions:
        q.randomized_answers = Answer.objects.filter(question=q)

    return render(request, 'app/intern_test_detail.html', {
        'result': result,
        'wrong_answers': wrong_answers,
        'total_questions': total_questions,
        'user': user,
        'referer': referer,
        'questions': questions,
        'user_answers': user_answers
    })


