# coding:utf8
'''
Created on 2016年8月3日

@author: zhangq
'''

from django.conf.urls import url
from Ts_app import views
urlpatterns = [
    url(r'^$', views.homeview),
    url(r'^ts_app/$', views.indexview),
    url(r'^ajax_radio/', views.radioview),
    url(r'^equipment/$', views.rentview),
    url(r'^testlink/$', views.testlinkview),
    url(r'^testcase/(\d+)$', views.test_case_view),
    url(r'^testsuite/(\d+)$', views.test_suite_view),
    url(r'^testreport/(.+)', views.test_report_view),
    url(r'^testbuild/(\d+)', views.test_build_view),
    url(r'^testbuild/result/(\d+)', views.test_result_view),
    url(r'^editcase/', views.edit_case_view),
    url(r'^editsuite/', views.edit_suite_view),
    url(r'^ajax_list/', views.ajaxview),
    url(r'^ajax_dic/', views.ajaxdicview),
    url(r'^create_excel/(\d+)$', views.excelview),
    url(r'^testcase/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
    ]
