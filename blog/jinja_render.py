from jinja2 import Environment, PackageLoader, select_autoescape

def jinja_render(template_name, **kwargs):
    environment = Environment(
        loader=PackageLoader('blog', 'templates')
    )
    template = environment.get_template(f'{template_name}.j2.html')
    return template.render(**kwargs)
