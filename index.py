'''


   ▄█    █▄       ▄████████  ▄█        ▄██████▄      ███     
  ███    ███     ███    ███ ███       ███    ███ ▀█████████▄ 
  ███    ███     ███    █▀  ███       ███    ███    ▀███▀▀██ 
 ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███    ███     ███   ▀ 
▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███    ███     ███     
  ███    ███     ███    █▄  ███       ███    ███     ███     
  ███    ███     ███    ███ ███▌    ▄ ███    ███     ███     
  ███    █▀      ██████████ █████▄▄██  ▀██████▀     ▄████▀   
                            ▀                                

VIRTUAL ASSISTANT FOR AADITYARENGARAJAN // FREELANCER
BY AADITYA RENGARAJAN

CREATION TIMESTAMP : 9:57PM FRIDAY 10 SEPTEMBER 2021



[TO-DO]

[DONE] View All Projects
[DONE] Launch Dolphin Folder on Click
[DONE] Change Status from Complete-Incomplete
[DONE] View Complete and Incomplete Projects Separately
- New Project (Support for Flask, Blank, HTML, Python Script)
- New from GitHub to "git clone"
- Custom Thumbnail file on Project Index JSON
- Automatc Thumbnail Generation and Copyright Document Generation
- Allow for Licenses from GitHub for License Generation Every Project including EULAs for private projects
[DONE] Add Auto-Generated Documentation Comments on header of Python Codes with cursive ASCII for heading
- Add Python Sections like :

auto-index and add
#!! SAMPLE OUTPUT
#/-
for every defined function
and, function definition syntax :
def function():

    # documentation

    code

in case of Flask add

- Smart Assistant
- "Share Project" automatically ZIPs and uploads to MediaFire and opens link
- Statistics Page
- Automatically Index All Code Using and add Credits Comment to all HTML ( Select "Credited" and "Ghost" projects on interface [add to Project Index JSON] )
- Automatically Index All Python code and add shebang on Line 1 for every ".py" code
- Auto-Generate requirements.txt on Code Creation
- Add Creation and Completion Timestamps
- Add Code Report Generation to show # of Lines of Code, and automatic pricing calculator based on Suggested Base Price + Multiplier x # of Lines of Code
- Port 2708
'''





from flask import redirect, render_template, Flask, request, url_for, send_file
from modules.index import *
import datetime, json, os, dateutil, requests, subprocess
import glob

os.chdir(os.path.split(__file__)[0])

app = Flask(__name__)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    return (datetime.datetime.strptime(date,"%d/%m/%Y")).strftime('%B %d, %Y')

@app.route('/favicon.ico')
def favicon():
	return redirect(url_for('static',filename='images/icon.png'))

@app.route('/')
def index():
    projects = []
    for directory in os.listdir('..'):
        with open(f"../{directory}/project.index.json") as jsonfile:
            project = json.loads(jsonfile.read())
            projects.append(project)
    stats = {"completed":0,
             "upcoming":0,
             "total":0}
    for project in projects:
        if project["completed"]=="true":
            stats["completed"]+=1
        else:
            stats["upcoming"]+=1
        stats["total"]+=1
    return render_template('index.html',
                            projects=projects,
                            formatteddate=datetime.datetime.now().strftime("%B %d"),
                            stats=stats)

@app.route('/new')
def new_project():
    return render_template('new.html',
                            type=request.args.get("k"))

@app.route('/dolphin')
def dolphin():
    route = request.args.get("k")
    for x in os.listdir(".."):
        if route in x:
            route = x
            break
    os.system(f'dolphin "/home/aaditya/Desktop/Coding/{route}"')
    return "<script>javascript:window.close()</script>"

@app.route('/toggle/<code>')
def toggle_status(code):
    for directory in os.listdir('..'):
        if code in directory:
            with open(f"../{directory}/project.index.json") as jsonfile:
                project = json.loads(jsonfile.read())
                if project["completed"]=="true":
                    project.update({"completed":"false"})
                else:
                    project.update({"completed":"true"})
            with open(f"../{directory}/project.index.json","w") as jsonfile:
                json.dump(project,jsonfile, indent=4)
            subfolders, files = run_fast_scandir(f"../{directory}", [".py"])

            pymods = []

            for i in files:
                with open(i) as pyfile:
                    project = pyfile.readlines()
                    for line in project:
                        if checkX(line,
                            ["#","*","!","@","$","%","^","&","(",")","-","=","+","~","`","'",'"',"[","]"],
                            ["import "]):
                            if "from " not in line:
                                for x in line.split("import ")[-1].replace("import ","").split(" as ")[0].split(","):
                                    for y in x.strip().split(" "):
                                        pymods.append(y)
                            else:
                                for x in line.split("from ")[-1].split("import  ")[0].replace("from ","").replace("import ","").split(","):
                                    for y in x.strip().split(" "):
                                        pymods.append(y)
            case_filter = []
            python_modules = []
            for i in pymods:
                if i.lower() not in case_filter:
                    case_filter.append(i.lower())
                    python_modules.append(i)

            reqmts = []
            for mod in python_modules:
                result = subprocess.getoutput(f'pip freeze | grep {mod}')
                for out in result.split("\n"):
                    if f"-{mod.lower()}" in out.split("=")[0].lower()\
                    or f"{mod.lower()}-" in out.split("=")[0].lower()\
                    or f"-{mod.lower()}-" in out.split("=")[0].lower()\
                    or f"={mod.lower()}" in out.split("=")[0].lower()\
                    or mod.lower() == out.split("=")[0].lower():
                        reqmts.append(out.replace("\n",""))

            with open(f"../{directory}/requirements.txt","w") as reqmtfile:
                reqmtfile.write("\n".join(reqmts))

    return redirect(url_for("index"))

@app.route('/new/create',methods=['POST'])
def create_new():
    if request.form.get("type") == "flask":
        name = request.form["title"]
        modules = request.form["modules"].split(',')
        fmodules = []
        for i in modules:
            fmodules.append(i.strip())
        modules = fmodules
        description = request.form["description"]
        code = str(name)[:2].upper()+"-"+(datetime.datetime.now().strftime('%d%m%Y-%H%M%S'))
        project = {
                    "name" : name,
                    "description" : description,
                    "created" : datetime.datetime.now().strftime("%d/%m/%Y"),
                    "completed" : "false",
                    "modules" : modules,
                    "hosting" : {"hosted" : "false"},
                    "code" : code
                  }
        os.mkdir(f"../{name.replace(' ','_')}_({code})")
        with open(f"../{name.replace(' ','_')}_({code})/project.index.json","w") as jsonfile:
            json.dump(project,jsonfile, indent=4)
        with open(f"../{name.replace(' ','_')}_({code})/index.py","w") as indexpy:
            indexpy.write("import "+str(", ".join(modules))+"\n")
        if "flask" in modules:
            modules.remove("flask")
        with open(f"../{name.replace(' ','_')}_({code})/index.py","w") as indexpy:
            indexpy.write(f'''
{requests.get(f"https://artii.herokuapp.com/make?text={name}&font=block").text}


{description}
BY AADITYA RENGARAJAN

CREATION TIMESTAMP : {datetime.datetime.now().strftime("%H:%M %D %d %m %Y")}

#==============IMPORTING MODULES======================================================
#/- see 'requirements.txt' to install extra modules via pip
''')
            if 'bs4' in modules:
                indexpy.write('#/- note : bs4 requires html5lib parser\n')
            indexpy.write("from flask import redirect, render_template, Flask, request, url_for, send_file\n")
            indexpy.write("import "+str(", ".join(modules))+"\n")
            indexpy.write('''
#==============DEFINING BASIC FUNCTIONS======================================================



app = Flask(__name__)


#==============ROUTES======================================================
#/- routes are defined by @app.route decorator

@app.route('/')
def index():
    return render_template("index.html")




#==============ERROR HANDLING======================================================
#/- custom error handling using custom template to get fancy ;)

@app.errorhandler(404)
def page_not_found(e):
    return str((render_template('error.html',
                code="404",
                type="Not Found",
                content="Sorry, this page was not found!"))), 404

@app.errorhandler(500)
def internal_server_error(e):
    return str((render_template('error.html',
                code="500",
                type="Internal Server Error",
                content=f"Oh No! Something Went Wrong!<br/>{e}"))), 500

@app.errorhandler(410)
def gone(e):
    return str((render_template('error.html',
                code="410",type="Gone",
                content="Sorry, this page is has mysteriously vanished!"))), 410

@app.errorhandler(403)
def forbidden(e):
    return str((render_template('error.html',
                code="403",
                type="Forbidden",
                content="Sorry, you are not allowed to access this page!"))), 403

@app.errorhandler(401)
def unauthorized(e):
    return str((render_template('error.html',
                code="401",
                type="Unauthorized",
                content="Sorry, you are not authorized to access this page!"))), 401

#==============PROGRAM RUN======================================================


if __name__=="__main__":

    #/- note : remove debuggers and change port respectively
    #/- on production deployment.

    app.run(
        debug=True,
        use_reloader=True,
        use_debugger=True,
        port=8080,
        use_evalex=True,
        threaded=True,
        passthrough_errors=False
        )


#==============END OF WEBAPP======================================================''')
        os.mkdir(f"../{name.replace(' ','_')}_({code})/templates")

        os.mkdir(f"../{name.replace(' ','_')}_({code})/static")
        os.mkdir(f"../{name.replace(' ','_')}_({code})/static/scripts")
        with open(f"../{name.replace(' ','_')}_({code})/static/scripts/scripts.js","w") as scriptsjs:
            pass
        with open(f"../{name.replace(' ','_')}_({code})/static/scripts/jquery.min.js","w") as jsfile:
                jsfile.write(str((requests.get('https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js', allow_redirects=True)).text))
        os.mkdir(f"../{name.replace(' ','_')}_({code})/static/styles")
        with open(f"../{name.replace(' ','_')}_({code})/static/styles/styles.css","w") as stylescss:
            pass
        os.mkdir(f"../{name.replace(' ','_')}_({code})/static/images")
        os.mkdir(f"../{name.replace(' ','_')}_({code})/data")

        framework = request.form["framework"]

        if framework=='none':

            with open(f"../{name.replace(' ','_')}_({code})/templates/index.html","w") as indexhtml:
                indexhtml.write('''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <link rel='stylesheet' href="{{url_for('static',filename='styles/styles.css')}}"/>
    '''+f"<title>{name.replace(' ','_')}_({code})</title>"+'''
  </head>
  <body>
  <script src="{{url_for('static',filename='scripts/jquery.min.js')}}"></script>
  <script src="{{url_for('static',filename='scripts/scripts.js')}}"></script>
  </body>
</html>''')
        else:
            links = {"bs": {"js":"https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js",
                            "css":"https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"},
                     "mat":{"js":"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js",
                            "css":"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"},
                     "mdl":{"js":"https://code.getmdl.io/1.3.0/material.min.js",
                            "css":"https://code.getmdl.io/1.3.0/material.indigo-pink.min.css"},
                     "mdb":{"js":"https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/3.3.0/mdb.min.js",
                            "css":"https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/3.3.0/mdb.min.css"}}
            files = links[framework]
            jsfilename = files['js'].split('/')[-1]
            cssfilename = files['css'].split('/')[-1]
            with open(f"../{name.replace(' ','_')}_({code})/static/scripts/{jsfilename}","w") as jsfile:
                jsfile.write(str((requests.get(files['js'], allow_redirects=True)).text))
            with open(f"../{name.replace(' ','_')}_({code})/static/styles/{cssfilename}","w") as cssfile:
                cssfile.write(str((requests.get(files['css'], allow_redirects=True)).text))
            with open(f"../{name.replace(' ','_')}_({code})/templates/index.html","w") as indexhtml:
                indexhtml.write('''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <link rel='stylesheet' href="{{url_for('static',filename='styles/styles.css')}}"/>
    <link rel='stylesheet' href="{{url_for('static',filename='styles/'''+cssfilename+'''')}}"/>
    '''+f"<title>{name.replace(' ','_')}_({code})</title>"+'''
  </head>
  <body>
  <script src="{{url_for('static',filename='scripts/jquery.min.js')}}"></script>
  <script src="{{url_for('static',filename='scripts/scripts.js')}}"></script>
  <script src="{{url_for('static',filename='scripts/'''+jsfilename+'''')}}"></script>
  </body>
</html>''')

if __name__=="__main__":
    app.run(
        debug=True,
        use_reloader=True,
        use_debugger=True,
        port=2708,
        host='0.0.0.0',
        use_evalex=True,
        threaded=True,
        passthrough_errors=False
        ) 
