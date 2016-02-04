from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import  Boolean,REAL, Integer, Unicode,FLOAT
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import and_

Base = declarative_base()
dt = DATETIME(storage_format="%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(minute)02d:%(second)02d",
                                               regexp=r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})",)

class sqliteConnector:
    def __init__(self, pathToEngine, extenssion_path):
        self.engine=  create_engine("sqlite:///" + pathToEngine, echo = False)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

        @event.listens_for(self.engine, "connect")
        def connect(dbapi_connection, connection_rec):
            dbapi_connection.enable_load_extension(True)
            dbapi_connection.execute('SELECT load_extension("%s")'%(extenssion_path))
            dbapi_connection.enable_load_extension(False)

        Base.metadata.create_all(self.engine)

    def getPostsList(self,window_start,window_end):
        postsList = self.session.query(Post).filter(and_(Post.date>=window_start,Post.date<=window_end)).all()
        return postsList

#########################
## DB entities classes ##
#########################
class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True)
    author = Column(Unicode,default=None)
    guid = Column(Unicode, unique=True,default=None)
    title = Column(Unicode,default=None)
    url = Column(Unicode,unique=True,default=None)
    date = Column(dt,default=None)
    content = Column(Unicode,default=None)
    is_detailed = Column(Boolean,default=True)
    is_LB = Column(Boolean,default=False)
    domain = Column(Unicode,default=None)
    author_guid = Column(Unicode,default=None)

    def __repr__(self):
        return "<Post(post_id='%s', guid='%s', title='%s', url='%s', date='%s', content='%s', author='%s', is_detailed='%s',  is_LB='%s',domain='%s',author_guid='%s')>" % (self.post_id, self.guid, self.title,self.url,self.date,self.content,self.author,self.is_detailed,self.is_LB, self.domain,self.author_guid)

class Post_citation(Base):
    __tablename__ = 'post_citations'

    post_id_from = Column(Integer,ForeignKey('posts.post_id',ondelete="CASCADE"),primary_key=True)
    post_id_to = Column(Integer,ForeignKey('posts.post_id',ondelete="CASCADE"),primary_key=True)
    url_from = Column(Unicode,index=True)
    url_to = Column(Unicode,index=True)

    def __repr__(self):
        return "<Post_citation(post_id_from='%s', post_id_to='%s', url_from='%s', url_to='%s')>" % ( self.post_id_from, self.post_id_to, self.url_from, self.url_to)
