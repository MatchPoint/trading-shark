import abc

class DataSource:
    """
    This abstract class defines interfaces useful for retriving
    price data for equities and forex currencies.

    The granlarity of price data may vary based on the concrete
    data source. For example, Yahoo may return 5 day price data
    with 3 minute granularity where Google will return 5 day
    price data with 5 minute granularity.

    Some concrete implementations may behave differently. For example,
    Yahoo may return only 3 days worth of data when 5 days is requested
    while Google returns 5 days of data when 5 days is requests.

    Client modules should be aware of these inconsistencies and perform
    validation on all data received from classes derived from this class.
    """    
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def fetchData(self, symbol, start_date, end_date):
        """Fetches price data for a particular symbol and data range"""
        print 'Function not implemented ', sys._getframe().f_code.co_name
        return

    @abc.abstractmethod
    def fetchData(self, symbol):
        """
        Fetches most recent day's price data for a particular symbol
        Args:
          symbol (str): An exchange trading symbol such as 'IBM'.

        Returns:
          list: list of price data. 

        Raises:
            none
        """        
        print 'Function not implemented ', sys._getframe().f_code.co_name
        return        

    @abc.abstractmethod
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
            none        
        """             
        print 'Function not implemented ', sys._getframe().f_code.co_name
        return