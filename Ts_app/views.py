# coding:utf-8
from django.shortcuts import render, get_object_or_404,HttpResponseRedirect
from django.http import JsonResponse
from Ts_app.form import AddForm, AddUser, StreamForm, RentForm, TestlinkForm, TestlinkForm_case, TestlinkForm_suite, BlogCommentForm
from Ts_app.models import user_info, RentDB, TestlinkDB, TestlinkCase, TestlinkReport, TestlinkBuild, BlogComment
from django.views.generic.edit import CreateView, FormView
from Ts_app.switch_stream_Worker import switch_stream_Worker
from datetime import datetime
from Ts_app.XML_CSV import XML_CSV
import markdown2
import xlwt,xlrd



import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def homeview(request):
    test = [('States',1), [('Kansas',2), [('Lawrence',3), ('Topeka',4), ('Illinois',5)]]]
    return render(request, 'Ts_app/home.html', {'test':test})

# Ts_app页面的逻辑函数
def indexview(request):
    if request.method == 'POST':  # 注释
        form = AddForm()
        form_user = AddUser()
        form_stream = StreamForm()
        user_obj = user_info.objects.all()
        if 'switch_file' in request.POST:
            form_stream = StreamForm(request.POST)
            if form_stream.is_valid():
                host_name = form_stream.cleaned_data['host_name']
                stream_path = form_stream.cleaned_data['stream_path']
                connect_obj = switch_stream_Worker()
                result_num = connect_obj.run_switch_one(
                    r"%s" % host_name, stream_path)
                return render(request, 'Ts_app/index.html', {
                    'form_stream': form_stream, 'form': form,
                    'result_num': result_num, 'form_user': form_user,
                    'user_obj': user_obj})
        if 'switch' in request.POST:
            form = AddForm(request.POST)
            if form.is_valid():
                host_name = form.cleaned_data['host_name']
                stream_path = form.cleaned_data['stream_path']
                modulation = form.cleaned_data['modulation']
                frame_mode = form.cleaned_data['frame_mode']
                code_rate = form.cleaned_data['code_rate']
                band_width = form.cleaned_data['bandwidth']
                connect_obj = switch_stream_Worker()
                result_num = connect_obj.run_switch(
                    r"%s" % host_name, stream_path, modulation,
                    frame_mode, code_rate, band_width)
                return render(request, 'Ts_app/index.html', {
                    'form_stream': form_stream, 'form': form,
                    'result_num': result_num, 'form_user': form_user,
                    'user_obj': user_obj})
        if 'rent' in request.POST:
            form_user = AddUser(request.POST)
            if form_user.is_valid():
                servername = form_user.cleaned_data['server_name']
                print servername
                try:
                    form_user = AddUser(
                        request.POST, instance=user_info.objects.get(
                            server_name=servername))
                except:
                    pass
                form_user.save()
                return render(request, 'Ts_app/index.html', {
                    'form_stream': form_stream, 'form': form,
                    'form_user': form_user, 'user_obj': user_obj})
        # 注释掉了，暂时不用
        if 'check_box_list_bak' in request.POST:
            print "fff"
            radio = request.POST.get('check_box_list')
            radio = int(radio)-1
            host_name = request.POST.get('host_name')
            print host_name
            modulation = ['3', '2', '3', '3', '3', '5', '4']
            frame_mode = ['1', '2', '1', '2', '3', '3', '2']
            code_rate = ['1', '3', '2', '3', '3', '2', '3']
            carrier_mode = ['1', '2', '1', '2', '1', '1', '2']
            print host_name, modulation[radio],\
                frame_mode[radio], code_rate[radio]
            connect_obj = switch_stream_Worker()
            result_num = connect_obj.run_switch_mode(
                r"%s" % host_name, modulation[radio],
                frame_mode[radio], code_rate[radio], carrier_mode[radio])
            return render(request, 'Ts_app/index.html', {
                'form_stream': form_stream, 'form': form,
                'result_num': result_num, 'form_user': form_user,
                'user_obj': user_obj})
    else:
        form = AddForm()
        form_stream = StreamForm()
        form_user = AddUser()
        user_obj = user_info.objects.all()
    return render(request, 'Ts_app/index.html', {
        'form_stream': form_stream, 'form': form,
        'form_user': form_user, 'user_obj': user_obj})


# equipment页面的逻辑函数
def rentview(request):
    rent_obj = RentDB.objects.all()
    if request.method == 'POST':
        print "b"
        form2 = RentForm()
        if 'rent' in request.POST:
            print "c"
            form2 = RentForm(request.POST or None, request.FILES)
            if form2.is_valid():
                device_id = form2.cleaned_data['d_id']
                try:
                    form2 = RentForm(
                        request.POST, request.FILES,
                        instance=RentDB.objects.get(d_id=device_id))
                except:
                    pass
                form2.save()
                return render(request, 'Ts_app/rent.html', {
                    'form2': form2, 'rent_obj': rent_obj})

    else:
        form2 = RentForm()

    return render(request, 'Ts_app/rent.html', {
        'form2': form2, 'rent_obj': rent_obj})

def excelview(request,suite_id,build_id):
    test_suite_root = TestlinkDB.objects.get(id=int(suite_id))
    #test_suite_root = TestlinkDB.objects.filter(suite_name="AIrBee")
    test_case_list = get_case_list(test_suite_root,test_suite_root.suite_name,build_id)
    #print test_case_list
    print test_suite_root
    print "aaaaa"
    return render(request, 'Ts_app/testlink.html')

    
    


# 用ajax请求动态内容的逻辑函数
def ajaxview(request):
    a = range(30)
    return JsonResponse(a, safe=False)


def ajaxdicview(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': datetime.now()}
    return JsonResponse(name_dict)


def radioview(request):
        # print request.GET['radio_id']
        if request.method == 'GET':
            radio = int(request.GET['radio_id'])-1
            host_name = request.GET['host_id']
            modulation = ['3', '2', '3', '3', '3', '5', '4']
            frame_mode = ['1', '2', '1', '2', '3', '3', '2']
            code_rate = ['1', '3', '2', '3', '3', '2', '3']
            carrier_mode = ['1', '2', '1', '2', '1', '1', '2']
            connect_obj = switch_stream_Worker()
            result_num = connect_obj.run_switch_mode(
                r"%s" % host_name, modulation[radio],
                frame_mode[radio], code_rate[radio], carrier_mode[radio])
            print 1
            return JsonResponse(result_num, safe=False)
        else:
            print "no find check box in request"
            print request.method

def get_case_list(root_node,suite_name,build_id):
    exl_obj = xlwt.Workbook()
    num = 1
    i = root_node
    sheet_1 = exl_obj.add_sheet(suite_name, cell_overwrite_ok=False)
    raw_0 = ["suite_name","case_name","test_step","test_except","test_result","result_description"]
    for j in range(6):
        sheet_1.write(0,j,raw_0[j])
    print i.suite_name
    sheet_1.write(num,0,i.suite_name)
    num = num + 1
    # 目录的case子节点
    child_case = i.children_case.all()
    for l in child_case:
        #sheet_1.write(num,1,l.case_name)
        #sheet_1.write(num,2,l.case_step)
        #sheet_1.write(num,3,l.case_except)
        if int(build_id):
            m = l.case_report.filter(build_name=build_id).order_by('-id')
            if m:
                _test_result = m[0].test_result
                _result_description = m[0].result_description
                sheet_1.write(num,4,_test_result)
                sheet_1.write(num,5,_result_description)
                if _test_result:
                    sheet_1.write(num,1,l.case_name)
                    sheet_1.write(num,2,l.case_step)
                    sheet_1.write(num,3,l.case_except)
                    #sheet_1.write(num,4,l.case)
                    num = num + 1
        else:
            sheet_1.write(num,1,l.case_name)
            sheet_1.write(num,2,l.case_step)
            sheet_1.write(num,3,l.case_except)
            #sheet_1.write(num,4,l.case)
            num = num + 1
        
    # 目录的目录子节点
    children = i.children.all()
    for k in children:
        sheet_1.write(num,0,k.suite_name)
        num = num + 1
        for l in k.children_case.all():
            #sheet_1.write(num,1,l.case_name)
            #sheet_1.write(num,2,l.case_step)
            #sheet_1.write(num,3,l.case_except)
            if int(build_id):
                m = l.case_report.filter(build_name=build_id).order_by('-id')
                if m:
                    _test_result = m[0].test_result
                    _result_description = m[0].result_description
                    sheet_1.write(num,4,_test_result)
                    sheet_1.write(num,5,_result_description)
                    if _test_result:
                        sheet_1.write(num,1,l.case_name)
                        sheet_1.write(num,2,l.case_step)
                        sheet_1.write(num,3,l.case_except)
                        num = num + 1
            else:
                sheet_1.write(num,1,l.case_name)
                sheet_1.write(num,2,l.case_step)
                sheet_1.write(num,3,l.case_except)
                #sheet_1.write(num,4,l.case)
                num = num + 1
    exl_obj.save("/var/www/public_html/test_case.xls")
    #return play_list

#excel生成
def get_case_list_bak(root_node,suite_name):
    exl_obj = xlwt.Workbook()
    num = 1
    #for i in root_node:
    #    if i.type_name() == "TestlinkDB":
    i = root_node
    sheet_1 = exl_obj.add_sheet(suite_name, cell_overwrite_ok=False)
    raw_0 = ["suite_name","case_name","test_step","test_except","test_result"]
    for j in range(5):
        sheet_1.write(0,j,raw_0[j])
    print i.suite_name
    sheet_1.write(num,0,i.suite_name)
    num = num + 1
    # 目录的case子节点
    child_case = i.children_case.all()
    for l in child_case:
        sheet_1.write(num,1,l.case_name)
        sheet_1.write(num,2,l.case_step)
        sheet_1.write(num,3,l.case_except)
        #sheet_1.write(num,4,l.case)
        num = num + 1
        
    # 目录的目录子节点
    children = i.children.all()
    for k in children:
        sheet_1.write(num,0,k.suite_name)
        num = num + 1
        for l in k.children_case.all():
            sheet_1.write(num,1,l.case_name)
            sheet_1.write(num,2,l.case_step)
            sheet_1.write(num,3,l.case_except)
            #sheet_1.write(num,4,l.case)
            num = num + 1
    exl_obj.save("/var/www/public_html/test_case.xls")
    #return play_list
#测试报告界面
def get_suite_list(root_node,build_id):
    #print "get_suite_list"
    play_list = []
    for i in root_node:
        #print i.type_name()
        #if str(i) == "TestlinkDB":
        if i.type_name() == "TestlinkDB":
            #print "suit"
            play_list.append((i.suite_name,i.id,0,build_id))
            # 目录的目录子节点
            child_case = i.children_case.all()
            # 目录的case子节点
            children = i.children.all()
            #if len(child_case) > 0 and len(children) > 0:
            # 目录子节点和case子节点都加入列表
            play_list.append(
                get_suite_list(children,build_id)+get_suite_list(child_case,build_id))
            #elif len(children) > 0:
            #    play_list.append(get_suite_list(children))
            #elif len(child_case) > 0:
            #    play_list.append(get_suite_list(child_case))
        # 当是case的时候，把case加入list
        #elif str(i) == "TestlinkCase":
        if i.type_name() == "TestlinkCase":
            j = i.case_report.filter(build_name=build_id).order_by('-id')
            if j:
                _test_result = j[0].test_result
            else:
                _test_result = ""
            play_list.append((i.case_name,i.id,1,_test_result,build_id))

            #print "case"
    print play_list
    return play_list
#测试结果,只包括有结果的项
def get_result_list(root_node,build_id):
    print "get_result_list"
    play_list = []
    for i in root_node:
        #print i.type_name()
        if i.type_name() == "TestlinkDB":
            # 目录的目录子节点
            child_case = i.children_case.all()
            # 目录的case子节点
            children = i.children.all()
            # 目录子节点和case子节点都加入列表
            if children:
                if get_result_list(children,build_id):
                    play_list.append((i.suite_name,i.id,0,build_id))
                    play_list.append(get_result_list(children,build_id))
                else:
                    pass
            else:
                if get_result_list(child_case,build_id):
                    play_list.append((i.suite_name,i.id,0,build_id))
                    play_list.append(get_result_list(child_case,build_id))
                else:
                    pass
        if i.type_name() == "TestlinkCase":
            j = i.case_report.filter(build_name=build_id).order_by('-id')
            if j:
                _test_result = j[0].test_result
                play_list.append((i.case_name,i.id,1,_test_result,build_id))
            else:
                _test_result = ""
    print play_list
    if len(play_list):
        return play_list
    else:
        return None


def get_build_suite_list(root_node):
    play_list = []
    for i in root_node:
        print i.type_name()
        #if str(i) == "TestlinkDB":
        if i.type_name() == "TestlinkDB":
            #print "suit"
            play_list.append((i.suite_name,i.id,0,build_id))
            # 目录的目录子节点
            child_case = i.children_case.all()
            # 目录的case子节点
            children = i.children.all()
            #if len(child_case) > 0 and len(children) > 0:
            # 目录子节点和case子节点都加入列表
            play_list.append(
                get_suite_list(children)+get_suite_list(child_case))
            #elif len(children) > 0:
            #    play_list.append(get_suite_list(children))
            #elif len(child_case) > 0:
            #    play_list.append(get_suite_list(child_case))
        # 当是case的时候，把case加入list
        #elif str(i) == "TestlinkCase":
        if i.type_name() == "TestlinkCase":
            play_list.append((i.case_name,i.id,1,i.case_report))
            j = i.case_report.filter(build_name=build_id)
            if j:
                print j[0].test_result
            
            #print "case"
    #print play_list
    return play_list



def edit_case_view(request):
    test_suite_root = TestlinkDB.objects.filter(parent_suite_name=None)
    test_suite_list = get_suite_list(test_suite_root)
    if "add_case" in request.POST:  
        form_obj_2 = TestlinkForm_case(request.POST)  
        form_obj_2.save()
        #if "add_case" in request.post:
        return render(request, 'Ts_app/editcase.html',{'test_suite_list':test_suite_list, "form_obj_2":form_obj_2})
    else:
        form_obj_2 = TestlinkForm_case() 
        return render(request, 'Ts_app/editcase.html',{'test_suite_list':test_suite_list, "form_obj_2":form_obj_2})

def edit_suite_view(request):
    form_obj_3 = TestlinkForm_suite(request.POST)
    test_suite_root = TestlinkDB.objects.filter(parent_suite_name=None)
    test_suite_list = get_suite_list(test_suite_root)
    if "add_suite" in request.POST:    
        form_obj_3.save()
        #if "add_case" in request.post:
        return render(request, 'Ts_app/editsuite.html',{'test_suite_list':test_suite_list, "form_obj_3":form_obj_3})
    return render(request, 'Ts_app/editsuite.html',{'test_suite_list':test_suite_list, "form_obj_3":form_obj_3})
#测试报告页面
def test_build_view(request, _build_id):

    test_build_list = TestlinkBuild.objects.filter(id=str(_build_id))
    test_suite_root = TestlinkDB.objects.filter(parent_suite_name=None)
    #test_case_list = TestlinkCase.objects.all()
    test_suite_list = get_suite_list(test_suite_root,_build_id)
    if request.method == 'POST':
        pass
    
    #return render(request, 'Ts_app/testbuild.html',{'test_build_list': test_build_list})
    return render(request, 'Ts_app/testlink.html',
                  {'test_suite_list':test_suite_list,'test_build_list': test_build_list})
#已完成报告页面
def test_result_view(request, _build_id):

    test_build_list = TestlinkBuild.objects.filter(id=str(_build_id))
    test_suite_root = TestlinkDB.objects.filter(parent_suite_name=None)
    #test_case_list = TestlinkCase.objects.all()
    test_suite_list = get_result_list(test_suite_root,_build_id)
    print test_suite_list
    if request.method == 'POST':
        pass
    
    #return render(request, 'Ts_app/testbuild.html',{'test_build_list': test_build_list})
    return render(request, 'Ts_app/testresult.html',
                  {'test_suite_list':test_suite_list,'test_build_list': test_build_list})
#测试目录的已完成
def test_result_suite_view(request, _build_id, suite_number):
    print "test_result_suite_view"
    test_build_list = TestlinkBuild.objects.filter(id=str(_build_id))
    test_suite_root = TestlinkDB.objects.filter(id=int(suite_number))
    test_suite_list = get_result_list(test_suite_root,_build_id)
    return render(request, 'Ts_app/resultsuite.html',
                  {'suite_id':int(suite_number),'build_id':int(_build_id),'test_suite_list':test_suite_list,'test_build_list': test_build_list})
def test_case_view(request, case_num):
    test_case_list = TestlinkCase.objects.filter(id=int(case_num))
    comment_list = BlogComment.objects.filter(ariticle=int(case_num))
    form = BlogCommentForm()
    return render(request, 'Ts_app/testcase.html',{'test_case_list': test_case_list,'comment_list':comment_list,'form':form})
#测试目录页面
def test_suite_view(request, suite_num):
    test_suite_queryset = TestlinkDB.objects.filter(id=int(suite_num))
    test_suite_list = get_suite_list(test_suite_queryset, 0)
    return render(request,'Ts_app/testsuite.html',{'suite_id':int(suite_num),'test_suite_list':test_suite_list})

def test_report_view(request, case_num):
    #build_id = request.GET['id']
    test_case_list = TestlinkCase.objects.filter(id=int(case_num))
    for i in test_case_list:
        if i.id:
            num = i.id
            report_obj = i.case_report.all()
            #report_obj = i.case_report.filter(build_name=build_id)

    #print test_case_list
    print report_obj
    for j in report_obj:
        pass
        print j.test_result
        print j.result_description
    
    return render(request, 'Ts_app/testreport.html',{'test_case_list': test_case_list},{'report_obj':report_obj})




def testlinkview(request):
    
    test_case_list = TestlinkCase.objects.all()
    for i in test_case_list:
        #print i.case_step
        try:
            i.case_step = markdown2.markdown(i.case_step)
            print i.case_step
        except Exception, e:
            print e
    test_suite_root = TestlinkDB.objects.filter(parent_suite_name=None)
    test_suite_list = get_suite_list(test_suite_root,0)
    #print test_suite_list
    test_suite_list_2 = TestlinkDB.objects.all()
    test_build_list = TestlinkBuild.objects.all()

    if request.method == 'POST':
        if "delete" in request.POST.values():
            for i in request.POST:
                if request.POST[i] == "delete":
                    print i 
                    fileter_o = TestlinkCase.objects.filter(id=i).delete()
        if "delete_suite" in request.POST.values():
            for i in request.POST:
                if request.POST[i] == "delete_suite":
                    print i 
                    fileter_o = TestlinkDB.objects.filter(id=i).delete()


        
        form_obj = TestlinkForm(request.POST, request.FILES)
        form_obj_2 = TestlinkForm_case(request.POST)
        form_obj_3 = TestlinkForm_suite(request.POST)
        #if form_obj_2.isvalid():
        if "add_case" in request.POST:    
            form_obj_2.save()
            #if "add_case" in request.post:
            return render(request, 'Ts_app/testlink.html',
              {'form_obj': form_obj, 'test_case_list': test_case_list,
               'test_suite_root': test_suite_root, 'test_suite_list':test_suite_list, "form_obj_2":form_obj_2})
        if "add_suite" in request.POST:    
            form_obj_3.save()
            #if "add_case" in request.post:
            return render(request, 'Ts_app/testlink.html',
              {'form_obj': form_obj, 'test_case_list': test_case_list,
               'test_suite_root': test_suite_root, 'test_suite_list':test_suite_list, "form_obj_3":form_obj_3})
        

        
        if form_obj.is_valid():
            file_name = form_obj.cleaned_data['filepath']
            #print file_name
            # 返回一个文件对象
            file_obj = request.FILES['filepath']
            #print file_obj
            # print file_obj.read()
            print hasattr(file_obj, "read")
            xml_obj = XML_CSV()
            test_case = xml_obj.read_xml(file_obj)
            #print test_case
            for suite in test_case[0]:
                if suite[0] == "root_node":
                    TestlinkDB.objects.get_or_create(
                        parent_suite_name=None, suite_name=suite[1],
                        suite_detail=suite[2], suite_id=suite[3])
                    continue
                print "~~~~~~~~~~~~~~~\n%s\n~~~~~~~~~~~~~~~~~~~" % suite[0]
                suite_ins = TestlinkDB.objects.get(suite_id=suite[0])
                TestlinkDB.objects.get_or_create(
                    parent_suite_name=suite_ins, suite_name=suite[1],
                    suite_detail=suite[2], suite_id=suite[3])
            for case in test_case[1]:
                suite_ins = TestlinkDB.objects.get(suite_id=case[0])
                if TestlinkCase.objects.filter(internalid=case[5]):
                    # print case[1]
                    # print "get !!!!!!!!!!"
                    TestlinkCase.objects.filter(internalid=case[5]).update(
                        case_name=case[1], case_sum=case[2],
                        case_step=case[3], case_except=case[4],
                        internalid=case[5], case_suite=suite_ins)
                else:
                    # print case[1]
                    # print case[4]
                    # print "not find!!!!!"
                    TestlinkCase.objects.create(
                        case_name=case[1], case_sum=case[2],
                        case_step=case[3], case_except=case[4],
                        internalid=case[5], case_suite=suite_ins)
            return render(request, 'Ts_app/testlink.html',
                          {'form_obj': form_obj, 'file_name': file_name,
                           'test_case_list': test_case_list,
                           'test_suite_root': test_suite_root,
                           'test_suite_list': test_suite_list,
                           'test_build_list': test_build_list
                           })

    else:
        form_obj = TestlinkForm()
        form_obj_2 = TestlinkForm_case()
        form_obj_3 = TestlinkForm_suite()
    return render(request, 'Ts_app/testlink.html',
                  {'form_obj': form_obj, 'test_case_list': test_case_list,
                   'test_suite_root': test_suite_root, 'test_suite_list':test_suite_list,'test_suite_list_2':test_suite_list_2,  "form_obj_2":form_obj_2, "form_obj_3":form_obj_3, 'test_build_list': test_build_list})

class CommentPostView(FormView):
    form_class = BlogCommentForm # 指定使用的是哪个form
    template_name = 'Ts_app/testcase.html' 
    # 指定评论提交成功后跳转渲染的模板文件。
    # 我们的评论表单放在detail.html中，评论成功后返回到原始提交页面。

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""
        print "提交的数据验证合法"
        # 首先根据 url 传入的参数（在 self.kwargs 中）获取到被评论的文章
        target_article = get_object_or_404(TestlinkCase, pk=self.kwargs['article_id'])
        print "target article",target_article,"a",self.kwargs['article_id'],type(self.kwargs['article_id'])
        # 调用ModelForm的save方法保存评论，设置commit=False则先不保存到数据库，
        # 而是返回生成的comment实例，直到真正调用save方法时才保存到数据库。
        comment = form.save(commit=False)
        print "==========================="

        # 把评论和文章关联
        #comment.article = 65
        #comment.ariticle = int(self.kwargs['article_id'])
        comment.ariticle = target_article
        comment.save()
        print "==========================="

        # 评论生成成功，重定向到被评论的文章页面，get_absolute_url 请看下面的讲解。
        #self.success_url = target_article.get_absolute_url()
        self.success_url = "/testcase/%s" % int(self.kwargs['article_id'])
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        """提交的数据验证不合法后的逻辑"""
        print "提交的数据验证不合法"
        target_article = get_object_or_404(TestlinkCase, pk=self.kwargs['article_id'])

        # 不保存评论，回到原来提交评论的文章详情页面
        return render(self.request, 'Ts_app/testcase.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.BlogComment_set.all(),
        })
