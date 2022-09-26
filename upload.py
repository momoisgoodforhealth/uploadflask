import os
from flask import Flask, flash, request, redirect,render_template, url_for, send_file
from werkzeug.utils import secure_filename
import shutil
import random

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

rel_directory=os.path.realpath('.')
rnd=str(random.randint(0, 10000))+"/"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    count=0
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for filer in files:   #added
            count=count+1

            #filename = secure_filename(filer.filename) 
            #filer.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'],filename))
            #text = request.form['id']
        #    if file.filename == '':
         #       flash('No selected file') 
          #      return redirect(request.url)
            if filer and allowed_file(filer.filename):
                filename = secure_filename(filer.filename)

               

                #filer.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
                text = request.form['id']
                processed_text = text.upper()
                ridetype= request.form['type'].upper()
                restraint=request.form['restraint'].upper()
                headrest=request.form['headrest'].upper()
                hz256=request.form['hz256'].upper()
                injuries=request.form['injuries'].upper()
                date=request.form['datadate'].upper()
                filterfreq=request.form['filter'].upper()
                rate=request.form['SampleRate'].upper()
                ginterval=request.form['Ginterval'].upper()
                lowext=request.form['lowextent'].upper()
                highext=request.form['highextent'].upper()
                eventcountmax=request.form['eventcountmax'].upper()
                eventcountmin=request.form['eventcountmin'].upper()
                eventcountinterval=request.form['eventcountinterval'].upper()


                folder=processed_text+"/"
                UPLOAD_FOLDER2=os.path.join(app.root_path,'uploads/',folder,rnd)
                UPLOAD_FOLDER3=os.path.join(app.root_path,'uploads/', folder)
                if not os.path.isdir(UPLOAD_FOLDER2):
                    os.makedirs(UPLOAD_FOLDER2)
                if not os.path.isdir(UPLOAD_FOLDER3):
                    os.makedirs(UPLOAD_FOLDER3)
                
                app.config['UPLOAD_FOLDER2']=UPLOAD_FOLDER2
                filer.save(os.path.join(UPLOAD_FOLDER2, filename))
                #textfile = open("b.txt", "w")
                textfile = open("b.txt", "w")
                textfile.write(processed_text+"\n"+ridetype+"\n"+restraint+"\n"+date+"\n"+filterfreq+"\n"+rate+"\n"+ginterval+"\n"+lowext+"\n"+highext)

                
                #shutil.copy('b.txt',processed_text+".txt")
                #textfile2 = open(processed_text+".txt", "w")
                #textfile2.write(str(count))
           
                #shutil.copy('/home/momoisgoodforhealth/Flask_upload/b.txt', '/home/momoisgoodforhealth/Flask_upload/'+folder+processed_text+".txt")
                #textfile2 = open("/home/momoisgoodforhealth/Flask_upload/"+folder+processed_text+".txt", "w")
                shutil.copy('b.txt', UPLOAD_FOLDER3+processed_text+".txt")
                textfile2 = open(UPLOAD_FOLDER3+processed_text+".txt", "w")
                textfile2.write("RIDEID="+processed_text+"\n"+"RIDETYPE="+ridetype+"\n"+"RESTRAINT="+restraint+"\n"+"HEADREST="+headrest+"\n"+"256HZ="+hz256+"\n"+"INJURIES="+injuries+"\n"+"DATE="+date+"\n"+"FILTER FREQUENCY="+filterfreq+"\n"+"RATE="+rate+"\n"+"G INTERVAL="+ginterval+"\n"+"LOW EXTENT="+lowext+"\n"+"HIGH EXTENT="+highext+"\n"+"EVENT COUNT MAX="+eventcountmax+"\n"+"EVENT COUNT MIN="+eventcountmin+"\n"+"EVENT COUNT INT="+eventcountinterval+"\n")
                #return redirect(url_for('download_file', name=filename))


        return 'Upload Success!'

    #<input type=text name="id"><br>n
    return render_template("home.html")


from flask import send_from_directory
dir_path = "/uploads/"
rideids=[]
#for path in os.listdir(dir_path):
       # rideids.append(path)
        
@app.route('/downloads/', methods = ['GET', 'POST'])
def list_folders():
    shutil.make_archive('/assets/789zip','zip','/home/momoisgoodforhealth/Flask_upload/uploads/789')
    #return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    return render_template("list.html", data=rideids)

@app.route('/static/789/', methods = ['GET', 'POST'])
def download_file():
    return send_file("/assets/789zip.zip", as_attachment=True)



