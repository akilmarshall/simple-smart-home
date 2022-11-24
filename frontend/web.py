import hug
from jinja2 import Template
from pathlib import Path


pages_path = Path('pages').absolute()

@hug.get('/', output=hug.output_format.html)
def home():
    # Get File Content in String
    jinja2_template_string = open(pages_path / 'home.html', 'r').read()

    # Create Template Object
    template = Template(jinja2_template_string)

    # Render HTML Template String
    html_template_string = template.render()

    return html_template_string

@hug.get('/services', output=hug.output_format.html)
def services():
    jinja2_template_string = open(pages_path / 'services.html', 'r').read()
    template = Template(jinja2_template_string)
    html_template_string = template.render()

    return html_template_string
