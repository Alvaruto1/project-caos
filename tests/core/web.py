"""Provides the Flask App object to be used in the project"""
from os.path import abspath 
from flask import (
    Flask,
    Blueprint,
    render_template
)

def render_view(view_name, **context):
    """Renders a view with the given context.

    :param view_name: the name of the view to be
                      rendered, or an iterable with view names
                      the first one existing will be rendered
    :param context: the variables that should be available in the
                    context of the view.
    """
    return render_template(template_name_or_list=view_name, **context)


"""Main Flask app to be used in the project"""
app = Flask(__name__,
            static_folder=abspath("src/webapp/views/static"), 
            template_folder=abspath("src/webapp/views"),            
)



"""Register the Vendor Assets found in the core module"""
vendor_blueprint = Blueprint('vendor', __name__, static_url_path='/static/vendor', static_folder=abspath("src/core/html/vendor"))
app.register_blueprint(vendor_blueprint)
