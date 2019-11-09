from flask import Flask, render_template #Need render_template() to render HTML pages
from flask import Flask, request, flash, url_for, redirect, render_template, session, send_file
from flask_sqlalchemy import SQLAlchemy
import dataframe
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font='IPAGothic')
import numpy as np
import statsmodels.api as sm
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import datetime as dt
from pyramid.arima import auto_arima


app = Flask(__name__)

@app.route('/')
def about():
  return render_template('welcome.html')
  """Render an HTML template and return"""
   # HTML file to be placed under sub-directory templates

@app.route('/home', methods = ['GET', 'POST'] )
def home():
  return render_template('home.html')

def getDataFileS3Bucket(stockName):
    '''Create S3 Bucket to download csv'''

    try:
        import boto
        from boto.s3.key import Key

        keyId = "AKIARWXZ333LUXA7HNM6"
        sKeyId = "VJdj3bNTXxEbNuL6UjQcMz44ok5IJ9rGWXC9aU3a"
        srcFileName = "{0}.csv".format(stockName)
        destFileName = "s3_{0}".format(stockName)
        bucketName = "dah2-h2h-table44"

        conn = boto.connect_s3(keyId, sKeyId)
        bucket = conn.get_bucket(bucketName)

        # Get the Key object of the given key, in the bucket
        k = Key(bucket, srcFileName)

        # Get the contents of the key into a file
        k.get_contents_to_filename(destFileName)

        return destFileName

    except Exception as e:
        raise e


def createDataStore(stock):
    '''Final DF'''

    try:
        #stocks = ['INFY', 'HDFC', 'TCS', 'WIT']
        stocks = [stock]
        finalDf = pd.DataFrame()

        #df = pd.read_csv(getDataFileS3Bucket(sName))
        df = pd.read_csv(getDataFileS3Bucket(stock), parse_dates=['Date'], index_col='Date')
        finalDf = df


        if finalDf.empty:
            raise Exception('Unable to retrieve data from AWS S3')

        return finalDf
    except:
        raise

@app.route('/trade/<stock_name>', methods=("POST", "GET"))
def createMainDashboard(stock_name):
    df = createDataStore(stock_name)
    print(df)
    df=df.dropna()

    res = sm.tsa.seasonal_decompose(df.Close, freq=365)
    print(type(res))
    df_season = res.seasonal
    #df = df_season.to_frame()
    #df['Stock']=stock_name
    #df=df[['Stock','Close']]
    fig = res.plot()
    fig.set_figheight(4)
    fig.set_figwidth(8)

    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)

    return send_file(img,mimetype='image/png')

    #return render_template("graph.html", name =plt.show())

    #return render_template("Simple.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)


@app.route('/data/<stock_name>', methods=("POST", "GET"))
def createdata(stock_name):
    df = createDataStore(stock_name)
    print(df)
    df=df.dropna()

    res = sm.tsa.seasonal_decompose(df.Close, freq=365)

    df_season = res.seasonal
    df = df_season.to_frame()
    df['Stock']=stock_name
    df=df[['Stock','Close']]


    return render_template("Simple.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

@app.route('/pre/<stock_name>', methods=("POST", "GET"))
def predata(stock_name):
    df = createDataStore(stock_name)
    print(df)
    df=df.dropna()

    stepwise_model = auto_arima(df.Close, start_p=1, start_q=1,max_p=3, max_q=3, m=12,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True,stepwise=True)
    stepwise_model.fit(df)
    future_forecast = stepwise_model.predict(n_periods=len(df.Close) + 365)
    date = pd.date_range(start=dt.strptime(str(max(df.index)).split(" ")[0], "%Y-%m-%d").strftime("%d-%m-%Y"),end='09-11-2020', freq='D')
    predection = future_forecast[len(df.Close) - 1:]
    print(predection)
    future_forecast = pd.DataFrame(predection, index=date, columns=['Prediction'])
    df=future_forecast
    print(future_forecast)
    return render_template("Simple.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)
if __name__ == '__main__':
  #app.run(debug=True) # Enable reloader and debugger
  app.run(host='0.0.0.0')
