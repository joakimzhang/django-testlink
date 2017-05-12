#coding:utf8
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class user_info(models.Model):
    server_name = models.CharField(max_length=1000)
    user_name = models.CharField(max_length=100)
    rent_time = models.DateTimeField(
        'use end time', default=timezone.now)


class RentDB(models.Model):
    d_type = models.CharField(max_length=100)
    d_id = models.CharField(max_length=100)
    d_pic = models.ImageField(upload_to='img')
    p_name = models.CharField(max_length=100)

class TestlinkBuild(models.Model):
    build_name = models.CharField(max_length=100, null=True)
    def __str__(self):
        #return "TestlinkDB33"
        return self.build_name
    def type_name(self):
        return "TestlinkBuild"
class TestlinkReport(models.Model):
    
    test_case = models.ForeignKey('TestlinkCase',related_name='case_report',null=True)
    build_name = models.ForeignKey('TestlinkBuild', related_name='case_report',null=True)
    result_choice = (('Pass', 'pass'), ('Fail', 'fail'), ('Untest', 'untest'),('Block','block'))
    test_result = models.CharField(max_length=100, choices=result_choice, default='Untest')
    result_description = models.TextField(max_length=4000, null=True, blank=True)
    result_pic = models.ImageField(upload_to='img', null=True,blank=True)
    result_video = models.FileField(upload_to='video',null=True,blank=True)
    result_log = models.FileField(upload_to='log',null=True,blank=True)

class TestlinkDB(models.Model):
    # parent_suite_name = models.CharField(max_length=100)
    parent_suite_name = models.ForeignKey(
        'self',  related_name='children',blank=True,null=True,)
    suite_name = models.CharField(max_length=100,null=True, blank=True)
    suite_detail = models.TextField(default='null',blank=True)
    suite_id = models.CharField(max_length=100)

    def __str__(self):
        #return "TestlinkDB33"
        return self.suite_name
    def type_name(self):
        return "TestlinkDB"


class TestlinkCase(models.Model):
    case_name = models.CharField(
        max_length=100,null=True, blank=True)
    case_sum = models.TextField(null=True, default='null')
    case_step = models.TextField(max_length=4000, null=True, blank=True)
    case_except = models.TextField(null=True, blank=True)
    case_suite = models.ForeignKey('TestlinkDB',
                                   blank=True, null=True,
                                   related_name='children_case')
    internalid = models.CharField(max_length=1000,default='null')

    def __str__(self):
        return self.case_name
    
    def type_name(self):
        return "TestlinkCase"

class BlogComment(models.Model):
    user_name = models.CharField('评论者名字',max_length=100)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间',auto_now_add=True)
    ariticle = models.ForeignKey('TestlinkCase', verbose_name='评论所属文章',on_delete=models.CASCADE)
    def __str__(self):
        return self.body[:20]
