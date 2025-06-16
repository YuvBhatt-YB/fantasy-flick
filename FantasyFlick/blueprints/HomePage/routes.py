from flask  import render_template,Blueprint


HomePage = Blueprint("HomePage",__name__,template_folder="templates")

@HomePage.route("/")
def index():
    return render_template("HomePage/index.html")