from DataSource import DataSource
from decorate import log
from decorate import value_check
import sys
import urllib2
import datetime as dt

class YahooDataSource(DataSource):
    
    __ls_price_data = []

    def __init__(self):
        return

    def fetchData(self, symbol):
        """
        Fetches most recent day's price data for a particular symbol
        Args:
          symbol (str): An exchange trading symbol such as 'IBM'.

        Returns:
          list: list of price data. 

        Raises:
            RuntimeError - If price data is not formatted as expected
        """   
 
        #prepare data stucture by deleting any previous lists
        del self.__ls_price_data[:]

        #Yahoo will produce 1 minute granularity of price data
        #for 1 day price data
        num_of_periods = 1   
        period_type = 'd'

        urlForData = self._createURL(symbol, num_of_periods, period_type)
        
        price_data = urllib2.urlopen(urlForData).read()

        #The price data always begins after
        self.__ls_price_data = price_data.split('\n')

        for day_index in xrange(0,len(self.__ls_price_data)):
            test = self.__ls_price_data[day_index].split(':')[0]
            if 'volume' in test:
                day_index+=1
                break;

        if day_index == len(self.__ls_price_data):
            raise RuntimeError("Price data not formatted as expected")

        #drop the meta data
        self.__ls_price_data = self.__ls_price_data[day_index:]

        if('d' == period_type):
            #convert unix timestamp to stadard form
            for day_index in xrange(0, len(self.__ls_price_data)):
                #make sure the data looks like a unix timestamp
                s_my_date = self.__ls_price_data[day_index][:10]
                if (10 == len(s_my_date)):
                    if s_my_date.isdigit():
                        self.__ls_price_data[day_index] = \
                        dt.datetime.fromtimestamp(float(s_my_date)).strftime('%Y:%m:%d:%H:%M:%S') \
                        +self.__ls_price_data[day_index][10:]
                    else:
                        raise RuntimeError("Price data not formatted as expected, timestamp contained non digits")
                else:
                    if 0 != len(s_my_date):
                        #len == 0 at last line of file
                        raise RuntimeError("Price data not formatted as expected, could not convert timestamp")

        return self.__ls_price_data

    def _createURL(self, symbol, num_of_periods, period_type):
        """
        Forms the restful API for pulling data from a 
        particular concrete data source.

        Ex. _createURL(GPBUSD=X, 5, d)
        This will pull the 5 day price data for GPBUSD=X. 

        Args:
          symbol (str): An exchange trading symbol such as 'IBM'.
          num_of_periods(int): Number of periods to retrieve. Periods
            returned may not equal periods requested.
          period_type(unicode): 'd' for day, 'y' for year, 'm' for month

        Returns:
          URL (str): Formatted URL to be used to fetch data

        Raises:
            ValueError: raised if period_type not set to 'd','m', or 'y'
        """   

        #check for invalid parameter values
        if period_type not in ["d","m","y"]:
            raise ValueError("'d','m','y' was not passed in for period_type")

        urlForData = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+ \
        symbol+'/chartdata;type=quote;range='+str(num_of_periods)+period_type+'/csv'      
        print 'url is ',urlForData
        #Example of API to just retrieve the current (real-time) price:
        #http://download.finance.yahoo.com/d/quotes.csv?s=USDGBP%3DX&f=k1&e=.csv

        return urlForData
