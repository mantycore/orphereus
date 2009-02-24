from sqlalchemy import MetaData

__all__ = ['engine', 'metadata', 'Session', 'globj']
engine = None
Session = None
metadata = MetaData()
globj = None
