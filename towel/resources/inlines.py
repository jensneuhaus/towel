"""
This is mostly equivalent with Django's inline formsets mechanism, but
used together with editlive.
"""

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from towel.utils import changed_regions
from .base import DetailView, FormView


class ChildFormView(FormView):
    base_template = 'modal.html'
    parent_attr = 'parent'

    def get_parent_class(self):
        return self.model._meta.get_field(self.parent_attr).rel.to

    def get_parent_queryset(self):
        return self.get_parent_class()._default_manager.all()

    def get_parent(self):
        return get_object_or_404(self.get_parent_queryset(),
            pk=self.kwargs[self.parent_attr])

    def get_form_kwargs(self, **kwargs):
        kwargs['prefix'] = self.model.__name__.lower()
        return super(ChildFormView, self).get_form_kwargs(**kwargs)

    def form_valid(self, form):
        setattr(form.instance, self.parent_attr, self.parent)

        self.object = form.save()

        regions = DetailView.render_regions(self,
            model=self.parent.__class__,
            object=self.parent,
            )
        return HttpResponse(
            json.dumps(changed_regions(regions, [
                '%s_set' % self.model.__name__.lower(),
                ])),
            content_type='application/json')


class ChildAddView(ChildFormView):
    def get(self, request, *args, **kwargs):
        if not self.allow_add(silent=False):
            return redirect(self.url('list'))
        self.parent = self.get_parent()
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        if not self.allow_add(silent=False):
            return redirect(self.url('list'))
        self.parent = self.get_parent()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class ChildEditView(ChildFormView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.parent = getattr(self.object, self.parent_attr)
        if not self.allow_edit(self.object, silent=False):
            return redirect(self.object)
        form = self.get_form()
        context = self.get_context_data(form=form, object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.parent = getattr(self.object, self.parent_attr)
        if not self.allow_edit(self.object, silent=False):
            return redirect(self.object)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(self, form)
