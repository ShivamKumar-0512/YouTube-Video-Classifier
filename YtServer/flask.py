from flask import Flask, render_template, request, url_for, redirect
import pickle
from flask_cors import CORS
from forms import PredictForm
from googleapiclient.discovery import build

api_key = "Your_API"
youtube = build('youtube', 'v3', developerKey=api_key)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c1088081fcafcfbe2f8cbd109fce3fe4'
CORS(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    pred_form = PredictForm()
    if pred_form.validate_on_submit():
        if "youtube" in pred_form.url.data and "?v=" in pred_form.url.data:
            video_id = pred_form.url.data.split("=")[1]
            title_tag = [get_video_details(youtube, video_id)[1]]
            print(title_tag)
            vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
            model = pickle.load(open('premodel.model', 'rb'))
            result = model.predict(vectorizer.transform(title_tag))
            print(result)
            if result == 1:
                return redirect(url_for('educational', youtube_id=video_id))
            else:
                return redirect(url_for('entertainment', youtube_id=video_id))
        else:
            return redirect(url_for("invalid_page"))
    return render_template('home.html', form=pred_form, title="Prediction")


@app.route('/about')
def about():
    return render_template("about.html", title="About")


@app.route('/educational/<string:youtube_id>')
def educational(youtube_id):
    video_title = get_video_details(youtube, youtube_id)[0]
    return render_template("educational.html", title='Educational', id=youtube_id, title_tag=video_title)


@app.route("/invalid")
def invalid_page():
    return render_template("invalid.html", title='Invalid')


@app.route('/entertainment/<string:youtube_id>')
def entertainment(youtube_id):
    video_title = get_video_details(youtube, youtube_id)[0]
    return render_template("entertainment.html", title='Entertainment', id=youtube_id, title_tag=video_title)


@app.route('/predict',methods=['POST'])
def predict():
    features = [request.form["Title"]] #for get method
    vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    model = pickle.load(open('premodel.model', 'rb'))
    result = model.predict(vectorizer.transform(features))

    if result[0]==0:
        type = "Non-Educatonal"
    else:
        type = "Educational"
    return type


def get_video_details(youtube, video_id):
    request = youtube.videos().list(part='snippet,statistics', id=video_id)
    response = request.execute()['items'][0]
    title = response['snippet'].get('title')
    tags = response['snippet'].get('tags')
    tag = ' '.join(tags)
    merge = title + tag
    return title ,merge


if __name__ == "__main__":
    app.run(debug=False)
