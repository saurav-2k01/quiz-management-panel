import string
import random

from django.db import models
from tinymce.models import HTMLField


class QuestionBank(models.Model):
    question_hin = models.TextField(blank=True, null=True)
    question_eng = models.TextField(blank=True, null=True)
    option1_hin = models.TextField(blank=True, null=True)
    option1_eng = models.TextField(blank=True, null=True)
    option2_hin = models.TextField(blank=True, null=True)
    option2_eng = models.TextField(blank=True, null=True)
    option3_hin = models.TextField(blank=True, null=True)
    option3_eng = models.TextField(blank=True, null=True)
    option4_hin = models.TextField(blank=True, null=True)
    option4_eng = models.TextField(blank=True, null=True)
    option5_hin = models.TextField(blank=True, null=True)
    option5_eng = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    chapter = models.TextField(blank=True, null=True)
    previous_of = models.CharField(max_length=45, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    solution_hin = models.TextField(blank=True, null=True)
    solution_eng = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=45, blank=True, null=True)
    section_type = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    batch_id = models.CharField(max_length=45, blank=True, null=True)
    class_id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question_bank'


class Chapters(models.Model):
    batch_id = models.IntegerField()
    subject_id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=555, blank=True, null=True)
    image = models.CharField(max_length=555, blank=True, null=True)
    status = models.IntegerField()
    sorting_params = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_At', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chapters'

class BatchesSubjects(models.Model):
    batch_id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=555, blank=True, null=True)
    image = models.CharField(max_length=555, blank=True, null=True)
    status = models.IntegerField()
    sorting_params = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_At', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'batches_subjects'


class Quiz(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    secret_key = models.CharField(max_length=20)
    questions = models.ManyToManyField(QuestionBank,  related_name='quizzes', blank=True)
    chapter = models.CharField(max_length=250, blank=True, null=True)
    subject = models.CharField(max_length=250, blank=True, null=True)
    classes = models.CharField(max_length=250, blank=True, null=True)
    questions_count = models.IntegerField(default=0)
    promotion = HTMLField(null=True, blank=True)



    class Meta:
        managed = True
        db_table = 'quiz_quiz'

    def save(self, *args, **kwargs):
        if not self.secret_key:  # Only generate if secret_key is not set
            self.secret_key = self._generate_unique_secret_key()
        super().save(*args, **kwargs)

    def _generate_unique_secret_key(self):
        """
        Generates a unique 20-character random string for the secret key.
        Ensures uniqueness by checking existing keys in the database.
        """
        while True:
            random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            if not Quiz.objects.filter(secret_key=random_key).exists():
                return random_key





