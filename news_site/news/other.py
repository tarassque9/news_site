from bs4 import BeautifulSoup
import uuid
import re

def uuid_gen():
	return str(uuid.uuid4().hex)

def clear_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.text

class RequiredFieldsMixin():

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        fields_required = getattr(self.Meta, 'fields_required', None)

        if fields_required:
            for key in self.fields:
                if key not in fields_required:
                    self.fields[key].required = False

