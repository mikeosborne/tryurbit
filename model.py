
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import DateTime
from database import Base
from globals import CometStatus

class AppGlobals(Base):
    __tablename__ = "app_globals"
    
    min_mined_comets    = Column(Integer, primary_key=True)
    min_ready_comets    = Column(Integer)
    max_assigned_comets = Column(Integer)
    max_time            = Column(Integer) 
    
    def __init__(self, min_mined_comets, min_ready_comets, max_assigned_comets, max_time):
        self.min_mined_comets = min_mined_comets
        self.min_ready_comets = min_ready_comets
        self.max_assigned_comets = max_assigned_comets
        self.max_time = max_time
 
    def __repr__(self):
        return '<Min Mined: {}, Min Ready: {}, Max Assigned: {}, Max Time: {}>'.format(self.min_mined_comets, self.min_ready_comets, self.max_assigned_comets, self.max_time)
    
           
    

class Comet(Base):
    __tablename__ = "comet"
    
    id          = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name        = Column(String(64))
    code        = Column(String(64))
    status      = Column(Integer)
    assigned    = Column(Integer)
    pier        = Column(String(64))
    pid         = Column(Integer)
    port        = Column(String(64))
    mined_ts    = Column(DateTime)
    ready_ts    = Column(DateTime)
    assigned_ts = Column(DateTime)
    dropped_ts  = Column(DateTime)
    
    def __init__(self, name, code, pier):
        self.name = name
        self.code = code
        self.status = CometStatus.MINED
        self.assigned = None
        self.pier = pier
        self.pid = None
        self.port = None
        self.mined_ts = datetime.now()
        self.ready_ts = None
        self.assigned_ts = None
        self.dropped_ts = None
        
    def __repr__(self):
        return '<Comet {}>'.format(self.name)
        

class Users(Base):
    __tablename__ = "users"
    
    id    = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name  = Column(String(64))
    email = Column(String(64))
    group = Column(String(64))
    optin = Column(Boolean)
    
    def __init__(self, name, email, init_group=None, optin=False):
        self.name = name
        self.email = email
        self.init_group = group
        self.optin = optin
        
    def __repr__(self):
        return '<User {}>'.format(self.name)
    

class Admins(Base):
    __tablename__ = "admins"
    
    name            = Column(String(255), primary_key=True, index=True)
    email           = Column(String(255))
    notice_daily    = Column(Boolean)
    alert_low_mined = Column(Boolean)
    alert_low_ready = Column(Boolean)
    alert_max_users = Column(Boolean)
 
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.notice_daily = True
        self.alert_low_mined = False
        self.alert_low_ready = False
        self.alert_max_users = False   
        
    def __repr__(self):
        return '<Admin {}>'.format(self.name)
     
    
class Ports(Base):
    __tablename__ = 'ports'
    
    port      = Column(String(16), primary_key=True)
    available = Column(Boolean)
    
    def __init_(self, port):
        self.port = port
        self.available = True
        
    def __repr__(self):
        return '<Port {}>'.format(self.port)