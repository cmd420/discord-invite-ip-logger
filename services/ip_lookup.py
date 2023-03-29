'''
Defines the abstract class used to 
'''
from abc import ABC, abstractclassmethod


class IpLookup(ABC):
    '''
    Abstract class for other ip lookup services
    '''
    @abstractclassmethod
    def lookup_ip(self):
        '''
        Looks up the ip and gets location (lat lon), country... etc.
        ### Returns
        - returns an embed field
        '''
        pass
