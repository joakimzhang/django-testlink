from django.contrib import admin

# Register your models here.
from .models import TestlinkCase, TestlinkDB, TestlinkReport, TestlinkBuild,BlogComment

#admin.site.register(TestlinkCase)


from django.contrib.admin.options import *
from django.utils.translation import (
    override as translation_override, string_concat, ugettext as _, ungettext,
)
 
class TestlinkAdmin(admin.ModelAdmin):
    exclude = ('case_sum','internalid','suite_id')
    """aaa"""
    def get_id(self, request):
        return request.GET['id']
    def formfield_for_dbfield(self, db_field,**kwargs):
        field =  super(TestlinkAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'test_case':
        #    if kwargs:
            try:
                field.initial = kwargs['request'].GET['id']
            except:
                pass
        if db_field.name == 'case_suite':
        #    if kwargs:
            try:
                field.initial = kwargs['request'].GET['id']
            except:
                pass
        if db_field.name == 'parent_suite_name':
        #    if kwargs:
            try:
                field.initial = kwargs['request'].GET['id']
            except:
                pass
                
        #print "aaaaaaaaaaaaaaaaaaaaaa",field,"aaaaaaaaaaaaa",db_field,"aaaaaaaaaaaa",kwargs
        return field
    
    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)
        obj_url = reverse(
            'admin:%s_%s_change' % (opts.app_label, opts.model_name),
            args=(quote(pk_value),),
            current_app=self.admin_site.name,
        )
        # Add a link to the object's change form if the user can edit the obj.
        if self.has_change_permission(request, obj):
            obj_repr = format_html('<a href="{}">{}</a>', urlquote(obj_url), obj)
        else:
            obj_repr = force_text(obj)
        msg_dict = {
            'name': force_text(opts.verbose_name),
            'obj': obj_repr,
        }
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.

        if IS_POPUP_VAR in request.POST:
            to_field = request.POST.get(TO_FIELD_VAR)
            if to_field:
                attr = str(to_field)
            else:
                attr = obj._meta.pk.attname
            value = obj.serializable_value(attr)
            popup_response_data = json.dumps({
                'value': six.text_type(value),
                'obj': six.text_type(obj),
            })
            return SimpleTemplateResponse('admin/popup_response.html', {
                'popup_response_data': popup_response_data,
            })

        elif "_continue" in request.POST or (
                # Redirecting after "Save as new".
                "_saveasnew" in request.POST and self.save_as_continue and
                self.has_change_permission(request, obj)
        ):
            msg = format_html(
                _('The {name} "{obj}" was added successfully. You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            if post_url_continue is None:
                post_url_continue = obj_url
            post_url_continue = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts},
                post_url_continue
            )
            return HttpResponseRedirect(post_url_continue)

        elif "_addanother" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was added successfully. You may add another {name} below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(
                _('The {name} "{obj}" was added successfully.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            #return self.response_post_save_add(request, obj)
            #return HttpResponseRedirect("/testlink")
        
            if opts.model_name == "testlinkdb":
                #return HttpResponseRedirect("/testcase/%s"%(pk_value))
                return HttpResponseRedirect("/testsuite/%s"%(request.GET['id']))
            elif opts.model_name == "testlinkreport":
                return HttpResponseRedirect("/testreport/%s"%(request.GET['id']))  
            else:        
                return HttpResponseRedirect("/testcase/%s"%(pk_value)) 
        
        
        
    
    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
	print "response change"
        if IS_POPUP_VAR in request.POST:
            to_field = request.POST.get(TO_FIELD_VAR)
            attr = str(to_field) if to_field else obj._meta.pk.attname
            # Retrieve the `object_id` from the resolved pattern arguments.
            value = request.resolver_match.args[0]
            new_value = obj.serializable_value(attr)
            popup_response_data = json.dumps({
                'action': 'change',
                'value': six.text_type(value),
                'obj': six.text_type(obj),
                'new_value': six.text_type(new_value),
            })
            return SimpleTemplateResponse('admin/popup_response.html', {
                'popup_response_data': popup_response_data,
            })

        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {
            'name': force_text(opts.verbose_name),
            'obj': format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
        }
        if "_continue" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully. You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        elif "_saveasnew" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was added successfully. You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        elif "_addanother" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully. You may add another {name} below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_add' %
                                   (opts.app_label, opts.model_name),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            #return self.response_post_save_change(request, obj)
            print "up!!!!!",self.admin_site.name,opts.model_name,opts.app_label,type(opts)
            if opts.model_name == "testlinkdb":
                #return HttpResponseRedirect("/testcase/%s"%(pk_value))
                return HttpResponseRedirect("/testlink")
            elif opts.model_name == "testlinkreport":
                return HttpResponseRedirect("/testreport/%s"%(request.GET['id']))  
            else:        
                return HttpResponseRedirect("/testcase/%s"%(pk_value))    
            


    def response_delete(self, request, obj_display, obj_id):
        opts = self.model._meta
        if IS_POPUP_VAR in request.POST:
            popup_response_data = json.dumps({
                'action': 'delete',
                'value': str(obj_id),
            })
            return SimpleTemplateResponse('admin/popup_response.html', {
                'popup_response_data': popup_response_data,
            })

        self.message_user(
            request,
            _('The %(name)s "%(obj)s" was deleted successfully.') % {
                'name': force_text(opts.verbose_name),
                'obj': force_text(obj_display),
            },
            messages.SUCCESS,
        )

        if self.has_change_permission(request, None):
            post_url = reverse(
                'admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, post_url
            )
            post_url = "/testlink"
            #if opts.model_name == "testlinkdb":
                #return HttpResponseRedirect("/testcase/%s"%(pk_value))
            #    post_url = "/testlink"
            #elif opts.model_name == "testlinkreport":
            #    post_url = ("/testreport/%s"%(request.GET['id']))  
            #else:        
            #    post_url = ("/testcase/%s"%(pk_value))  
            
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)













admin.site.register(TestlinkDB, TestlinkAdmin)
admin.site.register(TestlinkCase, TestlinkAdmin)

admin.site.register(TestlinkReport, TestlinkAdmin)
admin.site.register(TestlinkBuild, TestlinkAdmin)
admin.site.register(BlogComment, TestlinkAdmin)


