from django.forms.util import flatatt
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.forms.widgets import ChoiceFieldRenderer, RadioChoiceInput

class StarRadioFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = RadioChoiceInput
    def render(self):
    	return mark_safe(u'\n%s\n' % u'\n'.join([u'%s' % force_unicode(w) for w in self]))

class StarRadioInput(RadioChoiceInput):
    def __init__(self, *args, **kwargs):
        msg = "RadioInput has been deprecated. Use RadioChoiceInput instead."
        warnings.warn(msg, PendingDeprecationWarning, stacklevel=2)
        super(RadioInput, self).__init__(*args, **kwargs)

    def tag(self):
    	if 'id' in self.attrs:
    		self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        	final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
    	if self.is_checked():
    		final_attrs['checked'] = 'checked'
    	return mark_safe(u'<input%s />' % flatatt(final_attrs))

