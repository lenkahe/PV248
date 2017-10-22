import re # regular expressions
import sqlite3

# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).

class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if ( self.id is None ):
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.name = re.sub('\([0-9+-]+\)', '', string )
        self.born = self.died = None
        year1 = re.search('\((\d{4})', string)
        if year1:
            self.born = int(year1.group(1))
        year2 = re.search('(\d{4})\)', string)
        if year2:
            self.died = int(year2.group(1))


    def fetch_id( self ):
        self.cursor.execute( "select id from person where name = ?", (self.name,) )
        self.id = self.cursor.fetchone()

    def do_store( self ):
        self.cursor.execute( "insert into person (born, died, name) values (?,?,?)", (self.born, self.died, self.name) )


class Score( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.genre = self.key = self.incipit =  self.year = None


    def do_store( self ):
        self.cursor.execute( "insert into score (genre, key, incipit, year) values (?,?,?,?)", (self.genre, self.key, self.incipit, self.year) )


conn = sqlite3.connect('scorelib.dat')
rx = re.compile(r"(.*): (.*)")
for line in open('scorelib.txt', 'r', encoding = 'utf-8'):
    m = rx.match(line)
    if m is None: continue
    k = m.group(1)
    v = m.group(2)
    if k == 'Composer':
        for c in v.split(';'):
            p = Person(conn, c.strip())
            p.store()
conn.commit()
