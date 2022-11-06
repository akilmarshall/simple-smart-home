import hug
from jinja2 import Template


@hug.get('/', output=hug.output_format.html)
def home():
    # Get File Content in String
    jinja2_template_string = open('pages/home.html', 'r').read()

    # Create Template Object
    template = Template(jinja2_template_string)

    # Render HTML Template String
    html_template_string = template.render()

    return html_template_string


@hug.get('/services', output=hug.output_format.html)
def services():
    jinja2_template_string = open('pages/services.html', 'r').read()
    template = Template(jinja2_template_string)
    html_template_string = template.render()

    return html_template_string
