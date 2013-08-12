# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.template import Library, Node

DUOSHUO_SHORT_NAME = getattr(settings, "DUOSHUO_SHORT_NAME", None)
DUOSHUO_SECRET = getattr(settings, "DUOSHUO_SECRET", None)

register = Library()

class DuoshuoCommentsNode(Node):
    def __init__(self, short_name=DUOSHUO_SHORT_NAME, topic_id=None, topic_title=None, topic_user=None):
        self.short_name = short_name
        self.topic_id = topic_id
        self.topic_title = topic_title
        self.topic_user = topic_user

    def render(self, context):
        topci_id = self.topic_id.resolve(context, True)
        topic_title = self.topic_title.resolve(context, True)
        topic_user = self.topic_user.resolve(context, True)
        code = '''<!-- Duoshuo Comment BEGIN -->
        <div class="ds-thread" data-thread-key="%s" data-title="%s" data-author-key="%s"></div>
        <script type="text/javascript">
        var duoshuoQuery = {short_name:"%s"};
        (function() {
            var ds = document.createElement('script');
            ds.type = 'text/javascript';ds.async = true;
            ds.src = 'http://static.duoshuo.com/embed.js';
            ds.charset = 'UTF-8';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ds);
        })();
        </script>
        <!-- Duoshuo Comment END -->''' % (topci_id, topic_title, topic_user, self.short_name)
        return code

def duoshuo_comments(parser, token):
    duo_data = token.contents.split()
    if len(duo_data) == 4:
        topic_id = parser.compile_filter(duo_data[1])
        topic_title = parser.compile_filter(duo_data[2])
        topic_user = parser.compile_filter(duo_data[3])
        return DuoshuoCommentsNode(DUOSHUO_SHORT_NAME, topic_id, topic_title, topic_user)
    else:
        raise template.TemplateSyntaxError, "duoshuo_comments tag takes SHORT_NAME as exactly one argument"
duoshuo_comments = register.tag(duoshuo_comments)

# 生成remote_auth，使用JWT后弃用
# @register.filter
# def remote_auth(value):
#     user = value
#     duoshuo_query = ds_remote_auth(user.id, user.username, user.email)
#     code = '''
#     <script>
#     duoshuoQuery['remote_auth'] = '%s';
#     </script>
#     ''' % duoshuo_query
#     return code
# remote_auth.is_safe = True

