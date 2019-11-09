from flask import Flask, render_template #Need render_template() to render HTML pages
from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import dataframe
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font='IPAGothic')
import numpy as np
import statsmodels.api as sm

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
    df = df_season.to_frame()
    df['Stock']=stock_name
    # fig = res.plot()
    # fig.set_figheight(8)
    # fig.set_figwidth(15)
    # plt.show()

    #render_template('Simple.html',  tables=[df.head().to_html(header="true", table_id="table")], titles=df.columns.values)
    return render_template("Simple.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)
    #return df.head().to_html(header="true", table_id="table")

if __name__ == '__main__':
  app.run(debug=True) # Enable reloader and debugger