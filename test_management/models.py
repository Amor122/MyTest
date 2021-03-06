from hashlib import md5
from django.db import models
from django.conf import settings

import human_management.models
from human_management.models import HumanCommon, Human, Organization


class Question(HumanCommon):
    class Meta:
        db_table = 'questions'
        verbose_name = verbose_name_plural = '题库'

    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, verbose_name='所属科目', null=True, blank=True)
    difficulty = models.ForeignKey('Difficulty', on_delete=models.SET_NULL, verbose_name='难度', null=True, blank=True)
    question_type_choices = ((0, '单选题'), (1, '多选题'), (2, '填空题'), (3, '判断题'), (4, '解答题'))
    question_type = models.IntegerField(choices=question_type_choices, verbose_name='题目类型')
    knowledge_node = models.CharField(max_length=100, verbose_name='知识点')
    question_main = models.CharField(max_length=300, verbose_name='题干')
    question_answer = models.CharField(max_length=500, verbose_name='参考答案')

    def __str__(self):
        return self.question_main


class Subject(HumanCommon):
    """科目，语文数学英语之类的"""

    class Meta:
        db_table = 'subjects'
        verbose_name = verbose_name_plural = '科目'

    subject_name = models.CharField(max_length=30, verbose_name='科目名称', unique=True)

    def __str__(self):
        return self.subject_name


class Difficulty(HumanCommon):
    """题目的难度层级，高一上、下、高二上下之类的"""

    class Meta:
        db_table = 'difficulties'
        verbose_name = verbose_name_plural = '难度'

    difficulty_name = models.CharField(max_length=30, verbose_name='难度层级', unique=True)

    def __str__(self):
        return self.difficulty_name


class Test(HumanCommon):
    class Meta:
        db_table = 'tests'
        verbose_name = verbose_name_plural = '考试'

    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, verbose_name='所属科目', null=True, blank=True)
    difficulty = models.ForeignKey('Difficulty', on_delete=models.SET_NULL, verbose_name='难度', null=True, blank=True)

    test_name = models.CharField(max_length=30, verbose_name='考试名称', unique=True)
    start_time = models.DateTimeField(verbose_name='开考时间')
    duration = models.IntegerField(verbose_name='考试时长', default=150)
    # 考试的删除涉及过多，不建议直接去除数据，这里将它的状态标识为删除，我们在查看时不再显示
    delete_status = models.BooleanField(verbose_name='删除状态',default=False)
    # 考生信息，有权限才能参加考试，不是吗
    test_examinee = models.ManyToManyField(Human, db_table='test_examinee', related_name='student_tests',
                                           verbose_name='考试考生关联信息', null=True)
    # 组织信息用于在配置时将整个组的人加到考试里，组织的退出和加入都会涉及到整个组织的人员的变动。处理逻辑会处理组织的类型问题，以便不把老师加到考试里。
    # 或者就是想把老师加到考试里，不做特别处理也行
    test_organization = models.ManyToManyField(Organization, db_table='test_organization',
                                               related_name='organization_tests',
                                               verbose_name='考试组织关联信息', null=True)
    # 监考人信息
    # test_invigilator = models.ManyToManyField(Human, db_table='test_invigilator', related_name='invigilate_tests',
    #                                           verbose_name='考试监考人信息', null=True)

    def __str__(self):
        return self.test_name


class Invigilator(HumanCommon):
    class Meta:
        db_table = 'invigilator'
        verbose_name = verbose_name_plural = '监考信息'

    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='考试')
    location = models.CharField(max_length=30, verbose_name='监考地点')
    invigilator = models.ForeignKey(human_management.models.Human, on_delete=models.CASCADE, verbose_name='监考人')


class Paper(HumanCommon):
    """因为有可能随机组卷，所以考试试卷单独建立模型"""

    class Meta:
        db_table = 'papers'
        verbose_name = verbose_name_plural = '试卷'

    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='所属考试')


class PaperQuestion(HumanCommon):
    class Meta:
        db_table = 'paper_questions'
        verbose_name = verbose_name_plural = '试卷题目信息'

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, verbose_name='所属试卷')
    paper_number = models.IntegerField(unique=True, verbose_name='卷内编号')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='考题')
    score = models.IntegerField(verbose_name='分数')


class PaperAnswer(HumanCommon):
    class Meta:
        db_table = 'paper_answers'
        verbose_name = verbose_name_plural = '试卷题目回答'

    examinee = models.ForeignKey(human_management.models.Human, on_delete=models.CASCADE, verbose_name='考生')
    paper_question = models.ForeignKey(PaperQuestion, on_delete=models.CASCADE, verbose_name='题目')
    my_answer = models.CharField(max_length=500, verbose_name='题目回答')
    score_get = models.IntegerField(verbose_name='得分', null=True, blank=True)
