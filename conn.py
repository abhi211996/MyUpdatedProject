from flask import Flask, render_template, request, redirect,url_for
# from flask_mysqldb import MySQL
# import yaml
import pyaudio
import wave
import MySQLdb
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('RegForm1.html')

@app.route("/reg", methods=['GET', 'POST'])
def reg():

    name = request.form['name']
    roll = request.form['roll']
    email = request.form['email']
    clgname = request.form['clgname']
    bnch = request.form['bnch']
    Qualification = request.form['Qualification']
    ph = request.form['ph']

    db = MySQLdb.connect(user='root', password='', host='localhost', database='student')
    query = "INSERT INTO registration(name,roll,email,clgname,bnch,Qualification,ph) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    val = (name, roll, email, clgname, bnch, Qualification, ph)
    ob = db.cursor()
    ob.execute(query, val)
    db.commit()
    ob.close()
    return render_template("Result.html")




@app.route('/student')
def users():
    cur = MySQLdb.connection.cursor()
    resultValue = cur.execute("SELECT * FROM registration")
   if resultValue > 0:
        userDetails = cur.fetchall()

        return render_template('student.html',userDetails=userDetails)

@app.route('/starttest')
def starttest():
    return render_template('starttest.html')

@app.route('/Question')
def Question():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5

    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        dat = frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # import numpy as np
    # import cv2
    # cap = cv2.VideoCapture(0)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    #
    # while (cap.isOpened()):
    #     ret, frame = cap.read()
    #     if ret == True:
    #         frame = cv2.flip(frame, 180)
    #         out.write(frame)
    #
    #         # cv2.imshow('frame',frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     else:
    #         break
    #         RECORD_SECONDS = 5
    # cap.release()
    # out.release()
    # cv2.destroyAllWindows()
    # cv2.close()

    return render_template('Question.html',dm =dat)

@app.route('/done')
def done():

    return render_template('Done.html')

if __name__ == '__main__':
    app.run(debug=True)
