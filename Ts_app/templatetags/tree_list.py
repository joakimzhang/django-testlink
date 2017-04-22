from django import template
register = template.Library()
from django.utils.safestring import SafeData, mark_safe

def li_tree(value):
    def walk_items(item_list):
        item_iterator = iter(item_list)
        try:
            item = next(item_iterator)
            
            while True:
                try:
                    next_item = next(item_iterator)
                except StopIteration:
                    yield item, None
                    break
                if not isinstance(next_item, tuple):
                    try:
                        iter(next_item)
                    except TypeError:
                        pass
                    else:
                        yield item, next_item
                        item = next(item_iterator)
                        continue
                yield item, None
                item = next_item
                
        except StopIteration:
            pass

    def list_formatter(item_list, tabs=1):
        indent = '\t' * tabs
        output = []
        for item, children in walk_items(item_list):
            sublist = ''
            if children:
                sublist = '\n%s<ul>\n%s\n%s</ul>\n%s' % (
                    indent, list_formatter(children, tabs + 1), indent, indent)
                #print item
                #output.append('%s<li><font color="black"><a>%s</a>%s</li>' % (indent, item[0], sublist))
                output.append('%s<li class="testlink_suite"><a href="/testsuite/%s">%s</a>%s</li>' % (indent,item[1], item[0], sublist))
            else:
                if item[2]==1:
                    #output.append('%s<div class="testlink_case"><a href="/testcase/%s">%s</a>%s</div>' % (indent, item[1], item[0], sublist))
                    if item[3] or item[4] != 0:
                        if item[3] == "Pass":
                            color = '<font style="font-weight:bold;" color="green">Pass</font>'
                        elif item[3] == "Fail":
                            color = '<font style="font-weight:bold;" color="red">Fail</font>'      
                        else:
                            color = ""                     
                        output.append('%s<div class="testlink_case"><a href="/testreport/%s">%s</a>  %s %s</div>' % (indent, item[1],item[0], color, sublist))
                        #output.append('<a> test result:%s</a>' % item[3])
                    else:
                        output.append('%s<div class="testlink_case"><a href="/testcase/%s">%s</a>%s</div>' % (indent, item[1], item[0], sublist))       
                           
                else:
                    #output.append('%s<li class="testlink_suite"><a href="/admin/Ts_app/testlinkdb/%s/change/">%s</a>%s</li>' % (indent, item[1], item[0], sublist))    
                    output.append('%s<li class="testlink_suite"><a href="/testsuite/%s">%s</a>%s</li>' % (indent, item[1], item[0], sublist))    

        return '\n'.join(output)
    return mark_safe(list_formatter(value))

register.filter("li_tree", li_tree)
