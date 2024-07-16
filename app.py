from flask import Flask,render_template,request,redirect
import pickle
import numpy as np
model = pickle.load(open('model.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))
location = sorted(df['location'].unique())
bhk = sorted(df['BHK'].unique())
bath = sorted(df['bath'].unique())


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',locations=location,bhks=bhk,baths=bath)

@app.route("/predict",methods=['POST'])
def predict():
    location = request.form.get('location')
    bath = request.form.get('bath')
    sqft = request.form.get('sqft')
    bhk = request.form.get('bhk')
    respones = np.exp(model.predict([[location,float(sqft),float(bath),int(bhk)]]))[0]
    lower = round((respones - respones*0.05),2)
    upper = round((respones + respones*0.05),2)
    return render_template('index.html', message=f"Your Home Price is Between {lower} to {upper} Lakhs")

if __name__ == "__main__":
    app.run(debug=True)