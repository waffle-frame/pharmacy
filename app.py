from models import *
import jinja2.ext as jinja
from flask import redirect


from flask import Flask
from blueprints.login import bp as LoginBlueprint
from blueprints.admin import bp as AdminBlueprint
from blueprints.selller import bp as SelllerBlueprint
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aoaoaoaooaoaoaoaoao'

app.register_blueprint(SelllerBlueprint, url_prefix='/selller')
app.register_blueprint(LoginBlueprint, url_prefix='/login') 
app.register_blueprint(AdminBlueprint, url_prefix='/admin')
jinja2_extensions = jinja.do, jinja.i18n, jinja.loopcontrols


@app.route('/') 
def checker():
    return(redirect('/login/'))


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port='5010', debug=True)