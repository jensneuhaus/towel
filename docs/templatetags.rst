.. _templatetags:

=============
Template tags
=============


ModelView detail tags
=====================

.. module:: towel.templatetags.modelview_detail

.. function:: model_details

   Yields a list of ``(verbose_name, value)`` tuples for all local model
   fields::

       {% load modelview_detail %}

       <table>
       {% for title, value in object|model_details %}
           <tr>
               <th>{{ title }}</th>
               <td>{{ value }}<td>
           </tr>
       {% endfor %}
       </table>


ModelView list tags
===================

.. module:: towel.templatetags.modelview_list

.. function:: model_row

   Requires a list of fields which should be shown in columns on a list page.
   The fields may also be callables. ForeignKey fields are automatically
   converted into links::

       {% load modelview_list %}

       <table>
       {% for object in object_list %}
           <tr>
               {% for title, value in object|model_row:"__unicode__,author %}
                   <td>{{ value }}</td>
               {% endfor %}
           </tr>
       {% endfor %}
       </table>


.. function:: pagination

   Uses ``towel/_pagination.html`` to display a nicely formatted pagination
   section.  An additional parameter may be provided if the pagination should
   behave differently depending on where it is shown; it is passed to
   ``towel/_pagination.html`` as ``where``::

       {% load modelview_list %}

       {% if paginator %}{% pagination page paginator "top" %}{% endif %}

       {# list / table code ... #}

       {% if paginator %}{% pagination page paginator "bottom" %}{% endif %}


   As long as ``paginate_by`` is set on the ModelView, a paginator object is
   always provided. The ``{% if paginator %}`` is used because you cannot
   be sure that pagination is used at all in a generic list template.

   This template tag needs the ``django.core.context_processors.request``
   context processor.


.. function:: querystring

   URL-encodes the passed ``dict`` in a format suitable for pagination. ``page``
   and ``all`` are excluded by default::

       {% load modelview_list %}

       <a href="?{{ request.GET|querystring }}&page=1">Back to first page</a>

       {# equivalent, but longer: #}
       <a href="?{{ request.GET|querystring:"page,all" }}&page=1">Back to first page</a>


.. function:: ordering_link

   Shows a table column header suitable for use as a link to change the
   ordering of objects in a list::

       {% ordering_link "" request title=_("Edition") %} {# default order #}
       {% ordering_link "customer" request title=_("Customer") %}
       {% ordering_link "state" request title=_("State") %}

   Required arguments are the field and the request. It is very much
   recommended to add a title too of course.

   ``ordering_link`` has an optional argument, ``base_url`` which is
   useful if you need to customize the link part before the question
   mark. The default behavior is to only add the query string, and nothing
   else to the ``href`` attribute.

   It is possible to specify a set of CSS classes too. The CSS classes
   ``'asc'`` and ``'desc'`` are added automatically by the code depending
   upon the ordering which would be selected if the ordering link were
   clicked (NOT the current ordering)::

       {% ordering_link "state" request title=_("State") classes="btn" %}

   The ``classes`` argument defaults to ``'ordering'``.


Batch tags
==========

.. module:: towel.templatetags.towel_batch_tags

.. function:: batch_checkbox

   Returns the checkbox for batch processing::

       {% load towel_batch_tags %}

       {% for object in object_list %}
           {# ... #}
           {% batch_checkbox batch_form object.id %}
           {# ... #}
       {% endfor %}


Form tags
=========

.. module:: towel.templatetags.towel_form_tags

.. function:: form_items

   Returns the concatenated result of running ``{% form_item field %}`` on every
   form field.


.. function:: form_item

   Uses ``towel/_form_item.html`` to render a form field. The default template
   renders a table row, and includes:

   * ``help_text`` after the form field in a ``p.help``
   * ``invalid`` and ``required`` classes on the row


.. function:: form_item_plain

   Uses ``towel/_form_item_plain.html`` to render a form field, f.e. inside a
   table cell. The default template puts the form field inside a ``<span>`` tag
   with various classes depending on the state of the form field such as
   ``invalid`` and ``required``.


.. function:: form_errors

   Shows form and formset errors using ``towel/_form_errors.html``. You can
   pass a list of forms, formsets, lists containing forms and formsets and
   dicts containing forms and formsets as values.

   Variables which do not exist are silently ignored::

       {% load towel_form_tags %}

       {% form_errors publisher_form books_formset %}


.. function:: form_warnings

   Shows form and formset warnings using ``towel/_form_warnings.html``. You can
   pass a list of forms, formsets, lists containing forms and formsets and
   dicts containing forms and formsets as values. Also shows a checkbox which
   can be used to ignore warnings. This template tag does not work with
   Django's standard forms because they have do not have support for warnings.
   Use :py:class:`~towel.forms.WarningsForm` instead.

   Variables which do not exist are silently ignored::

       {% load towel_form_tags %}

       {% form_warnings publisher_form books_formset %}


.. function:: dynamic_formset

   This is a very convenient block tag which can be used to build dynamic
   formsets, which means formsets where new forms can be added with
   javascript (jQuery)::

       {% load towel_form_tags %}

       <script type="text/javascript" src="PATH_TO_JQUERY.JS"></script>
       <script type="text/javascript" src="{{ STATIC_URL }}towel/towel.js"></script>
       <style type="text/css">.empty { display: none; }</style>

       <form method="post" action=".">{% csrf_token %}
           {% form_errors form formset %}

           <table>
           {% for field in form %}{% form_item field %}{% endfor %}
           </table>

           <h2>Formset</h2>

           <table>
               <thead><tr>
                   <th>Field 1</th>
                   <th>Field 2</th>
                   <th></th>
               </tr></thead>
               <tbody>
               {% dynamic_formset formset "formset-prefix" %}
                   <tr id="{{ form_id }}" {% if empty %}class="empty"{% endif %}>
                       <td>
                           {{ form.id }}
                           {% form_item_plain form.field1 %}
                       </td>
                       <td>{% form_item_plain form.field2 %}</td>
                       <td>{{ form.DELETE }}</td>
                   </tr>
               {% enddynamic_formset %}
               </tbody>
           </table>

           <button type="button" onclick="towel_add_subform('formset-prefix')">
               Add row to formset</button>

           <button type="submit">Save</button>
       </form>

   The formset-prefix must correspond to the prefix used when initializing
   the FormSet in your Python code. You should pass ``extra=0`` when creating
   the FormSet class; any additional forms are better created using
   ``towel_add_subform``.
