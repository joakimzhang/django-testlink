# -*- coding:utf-8 -*-
from django import forms
from Ts_app.models import user_info, RentDB, TestlinkCase, TestlinkDB,BlogComment


class StreamForm(forms.Form):
    host_name_choice = (
        ('bjdittest', u"bjdittest"),
        ('bjdlise2', u"bjdlise2"),
        ('bjdqa150804', u"bjdqa150804"),
    )
    host_name = forms.ChoiceField(
        label=(u"HostName"), required=True, choices=host_name_choice)
    stream_path = forms.Field(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'input the stream path',
            'aria-describedby': "sizing-addon1",
            }),)


class AddForm(forms.Form):
    # choice字段需要设置每个字段的可选值
    host_name_choice = (
        ('bjdittest', u"bjdittest"),
        ('bjdlise2', u"bjdlise2"),
        ('bjdqa150804', u"bjdqa150804"),
        )
    modulation_choice = (
         (5, u"64QAM"),
         (1, u"4QAM-NR"),
         (2, u"4QAM"),
         (3, u"16QAM"),
         (4, u"32QAM"),
         )
    frame_mode_choice = (
        (1, u"mode3"),
        (2, u"mode2"),
        (3, u"mode1"),
        )
    code_rate_choice = (
        (3, u"0.8"),
        (2, u"0.6"),
        (1, u"0.4"),
        )
    frequency_choice = (
        (2, u"578"),
        (1, u"474"),
        )
    bandwidth_choice = (
        (4, u"8M"),
        (3, u"6M"),
        (2, u"4M"),
        (1, u"2M"),
        )

    host_name = forms.ChoiceField(label=(u"HostName"),
                                  required=True, choices=host_name_choice)
    modulation = forms.ChoiceField(label=(u"modulation"),
                                   required=True, choices=modulation_choice)
    frame_mode = forms.ChoiceField(label=(u"frame_mode"),
                                   required=True, choices=frame_mode_choice)
    code_rate = forms.ChoiceField(label=(u"code_rate"),
                                  required=True, choices=code_rate_choice)
    frequency = forms.ChoiceField(label=(u"frequency"),
                                  required=True, choices=frequency_choice)
    bandwidth = forms.ChoiceField(label=(u"bandwidth"),
                                  required=True, choices=bandwidth_choice)
    # 设置一些html的标签属性
    stream_path = forms.Field(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'input the stream path',
            'aria-describedby': "sizing-addon1",
            }),)


# 用户借用码流卡的表单
class AddUser(forms.ModelForm):
    server_name_choice = (
        ('bjdittest', u"bjdittest"),
        ('bjdlise2', u"bjdlise2"),
        ('bjdqa150804', u"bjdqa150804"),
        )
    server_name = forms.ChoiceField(label=(u"HostName"),
                                    required=True, choices=server_name_choice)

    # 设置使用哪个数据库的表作为表单内容
    class Meta:
        model = user_info
        fields = ['server_name', 'user_name', 'rent_time']


class RentForm(forms.ModelForm):
    d_type_choice = (('usb', u'usb'), ('disk', u'disk'))
    d_type = forms.ChoiceField(label=(u"device type"),
                               required=True, choices=d_type_choice)

    class Meta:
        model = RentDB
        fields = '__all__'


class TestlinkForm(forms.Form):
    filepath = forms.FileField()


class TestlinkForm_case(forms.ModelForm):
    #d_type_choice = (('usb', u'usb'), ('disk', u'disk'))
    #d_type = forms.ChoiceField(label=(u"device type"),
    #                           required=True, choices=d_type_choice)
    
    class Meta:
        model = TestlinkCase
        fields = ['case_name', 'case_step', 'case_except', 'case_suite']

class TestlinkForm_suite(forms.ModelForm):
    #d_type_choice = (('usb', u'usb'), ('disk', u'disk'))
    #d_type = forms.ChoiceField(label=(u"device type"),
    #                           required=True, choices=d_type_choice)

    class Meta:
        model = TestlinkDB
        fields = ['suite_name', 'parent_suite_name']
class BlogCommentForm(forms.ModelForm):
    class Meta:
        """指定一些 Meta 选项以改变 form 被渲染后的样式"""
        model = BlogComment # form 关联的 Model

        fields = ['user_name',  'body']
        # fields 表示需要渲染的字段，这里需要渲染user_name、user_email、body
        # 这样渲染后表单会有三个文本输入框，分别是输入user_name、user_email、body的输入框

        widgets = {
            # 为各个需要渲染的字段指定渲染成什么html组件，主要是为了添加css样式。
            # 例如 user_name 渲染后的html组件如下：
            # <input type="text" class="form-control" placeholder="Username" aria-describedby="sizing-addon1">

            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入昵称",
                'aria-describedby': "sizing-addon1",
            }),
            'body': forms.Textarea(attrs={'placeholder': '我来评两句~'}),
        }
