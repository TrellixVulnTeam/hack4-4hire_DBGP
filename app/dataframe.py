import pandas as pd


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


def createDataStore():
    '''Final DF'''

    try:
        stocks = ['INFY', 'HDFC', 'TCS', 'WIT']
        finalDf = pd.DataFrame()
        #print(finalDf)
        for sName in stocks:
            df = pd.read_csv(getDataFileS3Bucket(sName))
            #print(df)
            finalDf = finalDf.append(df)

        if finalDf.empty:
            raise Exception('Unable to retrieve data from AWS S3')

        return finalDf
    except:
        raise


def createMainDashboard():
    '''Main Dashboard'''

    df = createDataStore()
    #print(df.head())
    return df.head()


def downloadTrends():
    '''Download Stock Trends'''

    df = createDataStore()
    df.to_csv('DataTrend.csv')
