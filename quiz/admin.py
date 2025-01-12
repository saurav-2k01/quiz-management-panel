from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponseRedirect

from quiz.models import QuestionBank, Chapters, BatchesSubjects, Quiz
from tinymce.widgets import TinyMCE


# forms.py
from django import forms

class QuizCreationForm(forms.Form):
    title = forms.CharField(max_length=250, label="Quiz Title", widget=forms.TextInput(attrs={'size': '40'}))
    description = forms.CharField(max_length=500, label="Description", widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    classes = forms.CharField(max_length=250, label="Class", widget=forms.TextInput(attrs={'size': '40'}))
    # promotion = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))



class ChapterFilter(admin.SimpleListFilter):
    title = "chapter"
    parameter_name = "chapter"


    def lookups(self, request, model_admin):
        # chapters_with_questions = QuestionBank.objects.values('chapter').distinct()
        # chapters = Chapters.objects.filter(id__in=chapters_with_questions)
        # return [(chapter.id, chapter.name) for chapter in chapters]
        subject_id = request.GET.get("subject", None)
        if subject_id:
            chapters = Chapters.objects.filter(subject_id=subject_id)
        else:
            chapters = Chapters.objects.all()
        return [(chapter.id, chapter.name) for chapter in chapters]


    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(chapter = self.value())
        return queryset




class SubjectFilter(admin.SimpleListFilter):
    title = "subject"
    parameter_name = "subject"


    def lookups(self, request, model_admin):

        subjects_with_questions = QuestionBank.objects.values('subject').distinct()
        subjects = BatchesSubjects.objects.filter(id__in=subjects_with_questions)
        return [(subject.id, subject.name) for subject in subjects]


    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subject = self.value())
        return queryset







# class QuestionBankAdmin(admin.ModelAdmin):
#     list_display = ("question_hin", "option1_hin", "option2_hin", "option3_hin", "option4_hin", "option5_hin","answer")
#     list_filter = (SubjectFilter,ChapterFilter,)

class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ("question_hin", "option1_hin", "option2_hin", "option3_hin", "option4_hin", "option5_hin", "answer")
    list_filter = (SubjectFilter, ChapterFilter,)
    actions = ["redirect_to_quiz_form"]

    def redirect_to_quiz_form(self, request, queryset):
        """
        Redirect to a form to input quiz details.
        """
        if not queryset.exists():
            self.message_user(request, "No questions selected!", level="error")
            return

        # Store the selected questions in the session
        request.session['selected_questions'] = list(queryset.values_list('id', flat=True))
        return HttpResponseRedirect("create-quiz/")  # Redirect to the custom form URL

    redirect_to_quiz_form.short_description = "Create Quiz with selected questions"

    def create_quiz_form(self, request):
        """
        Display a form to collect quiz title and description.
        """
        if request.method == "POST":
            form = QuizCreationForm(request.POST)
            if form.is_valid():
                # Retrieve selected questions from the session
                selected_questions = request.session.pop('selected_questions', [])
                if not selected_questions:
                    messages.error(request, "No questions were selected.")
                    return redirect("..")

                # get chapter and subject
                sample_question_id = selected_questions[0]
                chapter_id = QuestionBank.objects.get(id=sample_question_id).chapter
                subject_id = QuestionBank.objects.get(id=sample_question_id).subject
                chapter = Chapters.objects.get(id=chapter_id).name
                subject = BatchesSubjects.objects.get(id=subject_id).name
                # Create a new quiz
                quiz = Quiz.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    classes=form.cleaned_data['classes'],
                )
                quiz.chapter = chapter
                quiz.subject = subject
                quiz.questions_count = len(selected_questions)




                quiz.questions.set(QuestionBank.objects.filter(id__in=selected_questions))
                quiz.save()

                messages.success(request, f"Quiz '{quiz.title}' created successfully!")
                return redirect("..")  # Redirect back to the QuestionBank list
        else:
            form = QuizCreationForm()

        return render(request, "admin/create_quiz_form.html", {"form": form})

    def get_urls(self):
        """
        Add a custom URL for the quiz creation form.
        """
        urls = super().get_urls()
        custom_urls = [
            path('create-quiz/', self.admin_site.admin_view(self.create_quiz_form), name='create_quiz_form'),
        ]
        return custom_urls + urls





class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "chapter", "subject", "created_at", "questions_count","classes")


admin.site.register(QuestionBank, QuestionBankAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(BatchesSubjects)
admin.site.register(Chapters)
admin.site.site_header = "Quiz Admin"
