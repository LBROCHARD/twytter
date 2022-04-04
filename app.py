from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import redirect
from datetime import datetime
import emoji
import os
from werkzeug.utils import secure_filename
import json
app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd() + "/static/img/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def gethashtag(message):

    wordarray = message.split()
    message = ""
    messagearray = []
    messageAndhashtags = [messagearray]
    hashtags = []
    ishashtag = False

    for i in range(len(wordarray)):
        if wordarray[i][0] == "#":

            if message != "":

                if ishashtag == False:
                    dico = {
                        "type": "text",
                        "content": message
                    }
                    messagearray.append(dico)
                    message = ""

            dico = {
                "type": "hashtag",
                "content": wordarray[i]
            }
            hashtags.append(wordarray[i])
            messagearray.append(dico)
            ishashtag = True


        elif i == len(wordarray)-1 and wordarray[i][0] != "#":
            dico = {
                "type": "text",
                "content": wordarray[i]
            }
            messagearray.append(dico)
            message = ""

        else:
            message += wordarray[i] + " "
            ishashtag = False



    messageAndhashtags = [messagearray, hashtags]

    return messageAndhashtags


"""with open('twyts.json', 'r') as reader:
    twyts = json.loads(reader.read())"""


@app.route('/')
def mainPage():
    with open('twyts.json', 'r') as reader:
        twyts = json.loads(reader.read())

    return render_template('index.html', twyts=twyts)


@app.route('/new')
def pageNew():
    return render_template('new.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/add', methods=['POST'])
def new_twyts():
    with open('twyts.json', 'r') as reader:
        twyts = json.loads(reader.read())

    if request.form['Name']:
        name = request.form['Name'].upper()

    else:
        name = "ANONYMOUS"


    timedate = datetime.now()
    dtwithoutseconds = timedate.strftime("%d %B %Y, %H:%M")
    timestring = str(dtwithoutseconds)

    message = request.form['newMessage']
    messageAndhashtags = gethashtag(message)

    message = messageAndhashtags[0]
    hashtags = messageAndhashtags[1]

    print("=========LOG=========(hashtags:)")             #=====LOG
    print(message)

    print("=========LOG=========(hashtags:)")             #=====LOG
    print(hashtags)

    dictionary = {}

    if request.files:

        image = request.files["image"]

        print("=========LOG=========(image:)")           # =====LOG
        print(image)

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            dictionary = {
                "name": name,
                "message": message,
                "time": timestring,
                "like": "unliked",
                "image": filename,
                "hashtag": hashtags,
                "awnser": []
            }


        else:
            dictionary = {
                "name": name,
                "message": message,
                "time": timestring,
                "like": "unliked",
                "image": "",
                "hashtag": hashtags,
                "awnser": []
            }

    newTab = [dictionary]

    print("=========LOG=========(hashtags:)")  # =====LOG
    print(newTab)

    for i in range(len(twyts)):
        newTab.append(twyts[i])


    """tab = twyts"""
    """tab.append(dictionary)"""

    with open("twyts.json", "w") as outfile:
        dico_json = json.dumps(newTab, indent=2)
        outfile.write(dico_json)


    return redirect(url_for('mainPage'))


@app.route('/like', methods=['POST'])
def like():
    with open('twyts.json', 'r') as reader:
        twyts = json.loads(reader.read())

    wichButton = request.form['likeButton']

    if twyts[int(wichButton)]['like'] == "liked":
        twyts[int(wichButton)]['like'] = "unliked"

    else:
        twyts[int(wichButton)]['like'] = "liked"

    with open("twyts.json", "w") as outfile:
        newjson = json.dumps(twyts, indent=2)
        outfile.write(newjson)

    return redirect(url_for('mainPage'))


@app.route('/awnser', methods=['POST'])
def awnser():
    with open('twyts.json', 'r') as reader:
        twyts = json.loads(reader.read())

    wichMessage = request.form['awnserButton']

    timedate = datetime.now()
    dtwithoutseconds = timedate.strftime("%d %B %Y, %H:%M")
    timestring = str(dtwithoutseconds)

    dictionary = {
         "name": request.form['NameAwnser'].upper(),
         "message": request.form['MessageAwnser'],
         "time": timestring
    }

    awnserTab = twyts[int(wichMessage)]['awnser']
    awnserTab.append(dictionary)

    twyts[int(wichMessage)]['awnser'] = awnserTab

    with open("twyts.json", "w") as outfile:
        newjson = json.dumps(twyts, indent=2)
        outfile.write(newjson)

    return redirect(url_for('mainPage'))


@app.route('/clear', methods=['POST'])
def clear():
    with open('twyts.json', 'r') as reader:
        twyts = json.loads(reader.read())

    wichMessage = request.form['clearButton']

    twyts[int(wichMessage)]['awnser'] = []

    with open("twyts.json", "w") as outfile:
        newjson = json.dumps(twyts, indent=2)
        outfile.write(newjson)

    return redirect(url_for('mainPage'))


@app.route('/hashtag', methods=['POST'])
def hashtag():
    with open('twyts.json', 'r') as reader:
        twyts = json.loads(reader.read())

    hashtwyts = []
    hashtagsearch = request.form['hashtag'].lower()
    rawhashtag = hashtagsearch

    if hashtagsearch == "":
        nothing = "*blank*"
        return render_template('notfound.html', hash=nothing)

    elif hashtagsearch[0] != "#":
        hashtagsearch = "#" + hashtagsearch

    print("hashtagsearch=" + hashtagsearch)

    for i in range(len(twyts)):

        for parts in twyts[i]["message"]:

            if parts["type"] == "hashtag":

                if parts["content"] == hashtagsearch:
                    hashtwyts.append(twyts[i])

    if  hashtwyts == []:
        return render_template('notfound.html', hash=rawhashtag)
    else:
        return render_template('index.html', twyts=hashtwyts)





#to run : flask run --no-reload