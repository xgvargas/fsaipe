#-*- coding: utf-8 -*-

from flask import Blueprint, render_template, url_for, redirect
from flask import make_response, abort
from flask import request
# from flask import g
# import datetime
import os
from functools import wraps
from slugify import slugify
# from form import FormFromPeewee


current_dir = os.path.dirname(__file__)


class SaipeConfig(object):

    exclude = []
    readonly = []
    where = ''

    def __init__(self, model, caption):
        self.model = model
        self.caption = caption
        # self.modelForm = FormFromPeewee(model)

    def get_name(self):
        return slugify(self.model.__name__)

    def get_urls(self):
        return [( '/ajax/<op>', self.ajax )]

    def get_caption(self, row):
        return {'id': row.id, 'caption': self.caption.format(**row.__dict__)}

    def ajax(self, op):
        if request.is_xhr:
            if request.method == 'GET':
                if op == 'list':
                    rows = []
                    for r in self.model.query.all():
                        rows.append(self.get_caption(r))
                    return render_template('list.html', name=self.get_name(), rows=rows)

                abort(404)

            elif request.method == 'POST':
                if op == 'add':
                    abort(401)

                abort(404)

        abort(403)

    def do_query(self, page):
        if self.where:
            d = self.model.select().where(self.where).page(page)
        else:
            d = self.model.select().page(page)
        return d

    def do_foreing_query(self, model):
        return model.select()

    def on_save(self, obj):
        obj.save()

    def get_config(self, **kwargs):
        # form = self.ModelForm()
        form = {}
        return {'name': self.get_name(), 'form':form}



class Saipe(object):

    def __init__(self, app, getUser, bp_name='fsaipe', url_prefix='/saipe'):
        self.blueprint = Blueprint(bp_name,
                                   __name__,
                                   # static_folder=os.path.join(current_dir, 'static'),
                                   static_folder='static',
                                   # template_folder=os.path.join(current_dir, 'templates'),
                                   template_folder='templates',
                                   # static_url_path='/edp'
                                   )
        self.app = app
        self.getUser = getUser
        self.url_prefix = url_prefix
        self._models = {}

        app.register_blueprint(self.blueprint)

    def register(self, model, caption='{id}', model_config=SaipeConfig):
        m = model_config(model, caption)
        self._models[model] = m

    def auth_required(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = self.getUser()

            if not user:
                # login_url = url_for('%s.login' % self.auth.blueprint.name, next=get_next())
                login_url = url_for('%s.login' % self.auth.blueprint.name)
                return redirect(login_url)

            # if not self.check_user_permission(user):
            #     abort(403)

            return func(*args, **kwargs)
        return inner

    # def index(self):
    #     return render_template('edpeewee/index.html')

    def setup(self):
        # self.blueprint.route('/', methods=['GET', 'POST'])(self.auth_required(self.index))

        for model in self._models.values():

            name = model.get_name()
            for url, cb in model.get_urls():
                self.blueprint.add_url_rule(
                    '/'+name+url,
                    '%s_%s' % (name, cb.__name__),
                    self.auth_required(cb),
                    methods=['GET', 'POST'],
                )

        self.app.register_blueprint(self.blueprint, url_prefix=self.url_prefix)

    def get_config(self, model, **kwargs):
        return self._models[model].get_config(**kwargs)
