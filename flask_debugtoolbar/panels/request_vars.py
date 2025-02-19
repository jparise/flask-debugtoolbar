from flask_debugtoolbar.panels import DebugPanel

_ = lambda x: x

class RequestVarsDebugPanel(DebugPanel):
    """
    A panel to display request variables (POST/GET, session, cookies).
    """
    name = 'RequestVars'
    has_content = True

    def nav_title(self):
        return _('Request Vars')

    def title(self):
        return _('Request Vars')

    def url(self):
        return ''

    def process_request(self, request):
        self.request = request
        self.view_func = None
        self.view_args = []
        self.view_kwargs = {}

    def process_view(self, request, view_func, view_kwargs):
        self.view_func = view_func
        self.view_kwargs = view_kwargs

    def content(self):
        context = self.context.copy()
        context.update({
            'get': [(k, self.request.args.getlist(k)) for k in self.request.args],
            'post': [(k, self.request.form.getlist(k)) for k in self.request.form],
            'cookies': [(k, self.request.cookies.get(k)) for k in self.request.cookies],
            'view_func': '%s.%s' % (self.view_func.__module__, self.view_func.__name__) if self.view_func else '[unknown]',
            'view_args': self.view_args,
            'view_kwargs': self.view_kwargs or {}
        })
        if hasattr(self.request, 'session'):
            context.update({
                'session': [(k, self.request.session.get(k)) for k in self.request.session.iterkeys()]
            })

        return self.render('panels/request_vars.html', context)

