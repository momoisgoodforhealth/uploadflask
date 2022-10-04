import os
from flask import Flask, flash, request, redirect,render_template, url_for, send_file
from werkzeug.utils import secure_filename
import shutil
import random

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
testdata=["helo","helo","helo","helo","helo"]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

rel_directory=os.path.realpath('.')
rnd=str(random.randint(0, 10000))+"/"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


idnum=0
store=[]
@app.route('/', methods=['GET', 'POST'])
def rider():
    if request.method == 'POST':
        text = request.form['id']
        processed_text = text.upper()
        folder=processed_text+"/"
        UPLOAD_FOLDER3=os.path.join(app.root_path,'uploads/', folder)
        if os.path.isdir(UPLOAD_FOLDER3):
            f = open("uploads/"+processed_text+"/"+processed_text+".txt", "r")
            lines=f.readlines()
            for line in lines:
                cnt=0
                length=len(line)
                for i in line:
                    if i=="=":
                        value=line[cnt+1:length]
                        store.append(value)
                    cnt=cnt+1
            #idno=f.read(10)
            #idnum=idno[7:10]
            return redirect('/form')
        else:
            return redirect('/form')
    return render_template("rideid.html")


@app.route('/form',methods=['GET', 'POST'])
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
                eventcountmax=request.form['eventcountmax'].upper()
                eventcountmin=request.form['eventcountmin'].upper()
                eventcountinterval=request.form['eventcountinterval'].upper()
                airtemp=request.form['airtemp'].upper()
                humidity=request.form['humidity'].upper()
                atmospressure=request.form['atmospressure'].upper()
                disposition=request.form['disposition'].upper()


                folder=processed_text+"/"
                UPLOAD_FOLDER2=os.path.join(app.root_path,'uploads/',folder,rnd)
                UPLOAD_FOLDER3=os.path.join(app.root_path,'uploads/', folder)

                #if os.path.isdir(UPLOAD_FOLDER3):
                #    f = open(processed_text+".txt", "r")
                #    print(f.read())
                #    with open() as f:
                #      lines=f.readline()
                #testdata=[text,processed_text,ridetype,restraint,headrest]

                if not os.path.isdir(UPLOAD_FOLDER2):
                    os.makedirs(UPLOAD_FOLDER2)
                if not os.path.isdir(UPLOAD_FOLDER3):
                    os.makedirs(UPLOAD_FOLDER3)
                
                app.config['UPLOAD_FOLDER2']=UPLOAD_FOLDER2
                filer.save(os.path.join(UPLOAD_FOLDER2, filename))
                #textfile = open("b.txt", "w")
                textfile = open("b.txt", "w")
                textfile.write(processed_text+"\n"+ridetype+"\n"+restraint+"\n"+date+"\n"+filterfreq+"\n"+rate+"\n"+ginterval+"\n"+airtemp+"\n"+humidity+"\n"+atmospressure+"\n"+disposition)

                
                #shutil.copy('b.txt',processed_text+".txt")
                #textfile2 = open(processed_text+".txt", "w")
                #textfile2.write(str(count))
           
                #shutil.copy('/home/momoisgoodforhealth/Flask_upload/b.txt', '/home/momoisgoodforhealth/Flask_upload/'+folder+processed_text+".txt")
                #textfile2 = open("/home/momoisgoodforhealth/Flask_upload/"+folder+processed_text+".txt", "w")
                shutil.copy('b.txt', UPLOAD_FOLDER3+processed_text+".txt")
                textfile2 = open(UPLOAD_FOLDER3+processed_text+".txt", "w")
                textfile2.write("RIDEID="+processed_text+"\n"+"RIDETYPE="+ridetype+"\n"+"RESTRAINT="+restraint+"\n"+"HEADREST="+headrest+"\n"+"256HZ="+hz256+"\n"+"INJURIES="+injuries+"\n"+"DATE="+date+"\n"+"FILTER FREQUENCY="+filterfreq+"\n"+"RATE="+rate+"\n"+"G INTERVAL="+ginterval+"\n"+"EVENT COUNT MAX="+eventcountmax+"\n"+"EVENT COUNT MIN="+eventcountmin+"\n"+"EVENT COUNT INT="+eventcountinterval+"\n"+"AIR TEMPERATURE="+airtemp+"\n"+"HUMIDITY="+humidity+"\n"+"ATMOSPHERIC PRESSURE="+atmospressure+"\n"+"DISPOSITION="+disposition)
                #return redirect(url_for('download_file', name=filename))


        return render_template("upload_success.html")

    #<input type=text name="id"><br>n
    return render_template("home.html", data=store)


from flask import send_from_directory
dir_path = "/uploads/"
rideids=[]
for path in os.listdir(os.path.join(app.root_path,'uploads/')):
        rideids.append(path)

for rideid in rideids:
    shutil.make_archive(rideid+'zip','zip','uploads/'+rideid)

@app.route('/downloads/', methods = ['GET', 'POST'])
def list_folders():
    #shutil.make_archive('69zip','zip','uploads/69/')
    #return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    return render_template("list.html", data=rideids)

#@app.route('/static/69/', methods = ['GET', 'POST'])
#def download_file():
#    return send_file("69zip.zip", as_attachment=True)


@app.route('/static/<id>/', methods = ['GET', 'POST'])
def testing(id=rideid):
    return send_file(id+"zip.zip", as_attachment=True)

@app.route('/test/', methods = ['GET', 'POST'])
def test():
    return render_template("test.html",data=testdata)