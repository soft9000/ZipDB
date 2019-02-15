#!/usr/bin/env python3

# Mission: Opportunity to create an externalizable, database-style, record.
# The default row shall provide us with a consistent set of values, as well
# as the ability to specify an unlimited set of asymetrical user values.

# Status: Testing Success
# Date Created: 2019-02-15

import time
from collections import OrderedDict

class RowOne:
    '''
    This data record ("RowOne") has an immutable & unique id, a mutable subject,
    time, as well as body (or "payload.") Support includes the ability to add
    user-defined fields. The list of user-changeable fields is returned by
    the .key_setters(). The key_setter keys are used by .set().  
    '''
    reserved = ['time', 'id'] # Fields that cannot be .set() directly by the user.

    def __init__(self, time=None):
        self._data = OrderedDict()
        self.reset()
        if time:
            try:
                self._data['time'] = int(time)
            except:
                pass # ignore it

    def keys(self):
        ''' Return the list of keys for all data. '''
        return list(self._data.keys())

    def key_setters(self):
        ''' Return the list of .set() / user-changable keys for all columns / fields. '''
        results = list()
        for key in self._data:
            if key in RowOne.reserved:
                continue
            results.append(key)
        return results

    def reset(self):
        ''' Re-generate all key fields, including the id. PRESERVE user-data, if present. '''
        import uuid
        self._data['id'] = str(uuid.uuid1())
        self._data['time'] = time.time()
        self._data['subject'] = ''
        self._data['data'] = ''

    def reset_all(self):
        ''' Re-generate all fields, REMOVING any user data.'''
        self._data = OrderedDict()
        self.reset()

    def set(self, key, value):
        ''' Create / update a user-defined key + value. True upon success. False on error. '''
        if key in RowOne.reserved:
            return False
        self._data[key] = value
        return True

    def get(self, key):
        ''' Return the value for a key. None if not found ... or if key is set to same.
        None on error. '''
        if key in self._data:
            return self._data[key]
        return None

    def hack(self):
        self._data['time'] = time.time()

    def time_info(self, local=False):
        ''' Return this row's tm structure for either the local, or global (GMT) lime zone.
        False on error. '''
        try:
            if local:
                return time.localtime(self._data['time'])
            else:
                return time.gmtime(self._data['time'])
        except:
            ''' Safe coding is no accident ... :-) '''
            return False

    def time_string(self, local=False):
        ''' Format up a classic, user-displayable, time-string. False on error. '''
        try:
            return time.asctime(self.time_info(local))
        except:
            ''' Safe coding is no accident ... :-) '''
            return False

    @property
    def id(self):
        ''' The definitive id. Read-only. '''
        return self._data['id']

    @property
    def time(self):
        ''' The time. User maintainable. '''
        return self._data['time']

    @property
    def subject(self):
        ''' The subject. User maintainable. '''
        return self._data['subject']

    @property
    def data(self):
        ''' The payload. User maintainable. '''
        return self._data['data']

    @time.setter
    def time(self, value):
        try:
            self._data['time'] = int(value)
            return True
        except:
            return False

    @subject.setter
    def subject(self, value):
        self._data['subject'] = value
        return True

    @data.setter
    def data(self, value):
        self._data['data'] = value
        return True

    def __str__(self):
        return str(self._data)

    def __iter__(self):
        for key in self._data:
            yield key, self._data[key]

    @staticmethod
    def FromString(string):
        ''' Populate a Row from a dictionary. Note that the dictionary does
        not necessarily have to be a Row, to have the default RowOne() properies added.
        Strategy allows for unique data values to be provided. Note also that if the
        time key is not integral, then the present time will be used. Returns
        False on error.        '''
        try:
            obj = eval(string)
            result = RowOne()
            for key in obj:
                result._data[key] = obj[key]
            try:
                if float(result._data['time']):
                    pass # all is well!
            except:
                result.hack()
            return result
        except:
            return False

    @staticmethod
    def ToString(instance):
        ''' Convert an instance of RowOne into a string. Returns False on error. '''
        if isinstance(instance, RowOne):
            return repr(instance._data)
        else:
            return False


if __name__ == '__main__':
    # Test basic time set / get
    row = RowOne(time=1234567890)
    assert(row.time_string(local=True) == 'Fri Feb 13 18:31:30 2009')
    assert(row.time_string(local=False) == 'Fri Feb 13 23:31:30 2009')
    try:
        row.id = 123
        raise Exception("Error: The ID should never change.")
    except:
        pass
    # Test properties:
    row.data    = "my data"
    row.subject = "my\nsubject"
    assert(row.data == "my data")
    assert(row.subject == "my\nsubject")
    assert(row.data != "my")
    assert(row.subject != "subject")
    # Test user-modifiable values (defaults)
    keys = row.key_setters()
    for key in keys:
        assert(row.set(key, 'z' + key))
        assert(row.get(key) == 'z'+ key)
    # Test user-modifiable values (superset)
    keys = row.key_setters()
    keys.append('shazam')
    keys.append('mazsham')
    keys.append('key\tplan')
    for key in keys:
        assert(row.set(key, 'z' + key))
        assert(row.get(key) == 'z'+ key)
    # Test stringification save / restore:
    row2 = RowOne.FromString(RowOne.ToString(row))
    for key in keys:
        assert(row.get(key) == row2.get(key))
    assert(row2.time_string(local=True) == 'Fri Feb 13 18:31:30 2009')
    assert(row2.time_string(local=False) == 'Fri Feb 13 23:31:30 2009')
    # Test new iteration:
    for key in row2.key_setters():
        assert(row2.set(key, 'zz' + key))
        assert(row2.get(key) == 'zz'+ key)
    # Test reserved-key rejections
    for key in RowOne.reserved:
        assert(row2.set(key, 123) == False)
    # Test all-value interation
    keys = dict(zip(row2.keys(), row2.keys()))
    for key, value in row2:
        keys[key] = None
    for key in keys:
        assert(keys[key] == None)
    # Enforce reset + reset_all expectations
    row2.reset()
    assert(len(row.keys())      == len(row2.keys()))
    row2.reset_all()
    assert(len(row.keys())      != len(row2.keys()))
    assert(len(RowOne().keys()) == len(row2.keys()))
    print("Testing Success")

        
    
