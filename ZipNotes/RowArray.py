#!/usr/bin/env python3

# Mission: Opportunity to create an externalizable, database-style, storage
# manager. The default row shall provide us with a consistent set of values,
# as well as the ability to specify an unlimited set of asymetrical user
# values, as well.

# Status: Testing Success
# Date Created: 2019-02-15
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from collections import OrderedDict

from ZipNotes.Row import RowOne

class RowArray:

    def __init__(self):
        self._db = OrderedDict()

    def clear(self):
        ''' Remove all items from the databases. '''
        self._db.clear()

    def pack(self):
        ''' Remove any items marked for deletion from the database. '''
        datum = OrderedDict()
        for key in self._db:
            if self._db[key]:
                datum[key] = self._db[key]
        self._db = datum

    def count(self):
        ''' Count the number of ACTIVE (not deleted) items in the database. '''
        tally = 0
        for key in self._db:
            if self._db[key]:
                tally += 1
        return tally

    def count_deleted(self):
        ''' Count the number of DELETED (not active) items in the database. '''
        tally = 0
        for key in self._db:
            if not self._db[key]:
                tally += 1
        return tally

    def create(self):
        ''' Create a new row in the database. '''
        result = RowOne()
        self._db[result.id] = result
        return result

    def exists(self, row):
        ''' Check to see if a row / row's ID is in the database. '''
        if not isinstance(row, RowOne):
            return False
        return row.id in self._db

    def append(self, row, unique=False):
        ''' Add a new row to the database. Return True if all went well, else False.
        Use "unique" to manage append / update checking. '''
        if not isinstance(row, RowOne):
            return False
        if unique and row.id in self._db:
            return False
        self._db[row.id] = row
        return True

    def get_subjects(self):
        ''' Get the id and subject for all database rows. '''
        results = OrderedDict()
        for key in self._db:
            results[key] = self._db[key].subject
        return results

    def lookup(self, key):
        ''' Retrieve a database row by id ('key'.) Return None if not found. '''
        if isinstance(key, RowOne):
            return self.lookup(key.id)
        if key in self._db:
            return self._db[key]
        return None

    def read(self, row):
        ''' Re-retrieve a database row. Return None if not found. '''
        if not isinstance(row, RowOne):
            return None
        if row.id in self._db:
            return self._db[row.id]
        return None

    def update(self, row):
        ''' Use the Id to update the database row. False if the row was not
        found, else True when updated. Use .append() to add external records. '''
        if not isinstance(row, RowOne):
            return False
        if row.id in self._db:
            self._db[row.id] = row
            return True
        else:
            return False

    def delete(self, row):
        ''' Use the row's .id to mark it for database removal. Row
        identifier will remain in the database until the next .pack()
        operation. This function returns False if the row was not found,
        else True when the row has been tagged for removal. '''
        if not isinstance(row, RowOne):
            return False
        if row.id in self._db:
            self._db[row.id] = None
            return True
        else:
            return False

    @staticmethod
    def FromString(string):
        ''' Create & populate a RowArray from the result of its prior ToString()
        operation. '''
        results = RowArray()
        try:
            values = eval(string)
            for value in values:
                zobj = RowOne.FromString(value)
                if zobj:
                    results.append(zobj)
            return results
        except:
            return False

    @staticmethod
    def ToString(instance):
        ''' Create a string representing of the entire database. Items marked for
        deletion WILL be omitted from the final string representation. This operation
        returns False on error. '''
        if not isinstance(instance, RowArray):
            return False
        results = list()
        for key in instance._db:
            value = instance._db[key]
            if value:
                results.append(RowOne.ToString(value))
        return str(results)
        


if __name__ == '__main__':
    # Test counting, instance creation / lookup / reading operations:
    db = RowArray()
    assert(db.count() == 0)
    assert(db.count_deleted() == 0)
    row = db.create()
    assert(db.count() == 1)
    assert(db.count_deleted() == 0)
    row2 = db.create()
    assert(db.count() == 2)
    assert(db.count_deleted() == 0)
    assert(len(db.get_subjects()) == 2)
    row.subject = "row subject 1"
    row2.subject = "row subject 2"
    assert(db.read(row).subject == row.subject)
    assert(db.read(row2).subject == row2.subject)
    assert(db.lookup(row.id).subject == row.subject)
    assert(db.lookup(row).subject == row.subject)
    assert(db.lookup(row).subject != row2.subject)
    values = tuple(db.get_subjects())
    assert(db.lookup(values[0]).subject == row.subject)
    assert(db.lookup(values[1]).subject == row2.subject)
    # Test stringification:
    db2 = RowArray.FromString(RowArray.ToString(db))
    assert(db2.count() == db.count())
    assert(db2.lookup(values[0]).subject == row.subject)
    assert(db2.lookup(values[1]).subject == row2.subject)
    # Test cleanup:
    db2.delete(row)
    assert(db2.count() != db.count())
    assert(db2.count() == 1)
    assert(db2.count_deleted() == 1)
    db2.delete(row2)
    assert(db2.count() == 0)
    assert(db2.count_deleted() == 2)
    db2.pack()
    assert(db2.count() == 0)
    assert(db2.count_deleted() == 0)
    db2 = RowArray.FromString(RowArray.ToString(db))
    assert(db2.count() == db.count())
    db2.clear()
    assert(db2.count() == 0)
    assert(db2.count_deleted() == 0)
    # Test append and update:
    db2 = RowArray.FromString(RowArray.ToString(db))
    zrow = RowOne()
    assert(db2.exists(zrow) == False)
    assert(db2.update(zrow) == False)
    assert(db2.append(zrow) == True)
    assert(db2.exists(zrow) == True)
    assert(db2.count() == 3)
    zrow.data = "My Data"
    assert(db2.lookup(zrow).data == "My Data")
    zrow.subject = "My Subject"
    assert(db2.lookup(zrow).subject == "My Subject")
    print("Testing Success")
   
    
    
    
    
