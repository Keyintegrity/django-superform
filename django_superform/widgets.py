from django import forms


class TemplateWidget(forms.Widget):
    """
    Template based widget. It renders the ``template_name`` set as attribute
    which can be overriden by the ``template_name`` argument to the
    ``__init__`` method.
    """

    field = None
    template_name = None
    value_context_name = None

    def __init__(self, *args, **kwargs):
        template_name = kwargs.pop('template_name', None)
        if template_name is not None:
            self.template_name = template_name
        super(TemplateWidget, self).__init__(*args, **kwargs)

    def get_context_data(self):
        return {}

    def format_value(self, value):
        return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        widget_context = context['widget']
        context.update({
            'name': widget_context['name'],
            'hidden': widget_context['is_hidden'],
            'required': widget_context['required'],
            # In our case ``value`` is the form or formset instance.
            'value': widget_context['value'],
            'attrs': widget_context['attrs'],
        })

        if self.value_context_name:
            context[self.value_context_name] = widget_context['value']

        context.update(self.get_context_data())

        return context


class FormWidget(TemplateWidget):
    template_name = 'superform/formfield.html'
    value_context_name = 'form'


class FormSetWidget(TemplateWidget):
    template_name = 'superform/formsetfield.html'
    value_context_name = 'formset'
