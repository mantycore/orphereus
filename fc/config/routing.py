"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE
    # Special routes
    #map.connect('', controller='fcc', action='GetOverview')
    map.connect('/auth', controller='fcc', action='authorize', url='', conditions=dict(method=['POST']))
    map.connect('/:url/auth', controller='fcc', action='authorize', url='', conditions=dict(method=['POST']))
    map.connect('/register/:invite', controller='fcc', action='register')
    # Oekaki
    map.connect('/:url/oekakiDraw', controller='fcc', action='oekakiDraw', url='')
    map.connect('/:url/oekakiSave/:tempid', controller='fcc', action='oekakiSave', url='',requirements=dict(tempid='\d+'))
    map.connect('/:url/oekakiFinish/:tempid', controller='fcc', action='oekakiFinish', url='',requirements=dict(tempid='\d+'))
    
    # User subsystem
    map.connect('/userProfile', controller='fcc', action='showProfile')
    map.connect('/userProfile/messages', controller='fcc', action='showMessages')
    # Admin subsystem
    map.connect('/holySynod', controller='fca', action='index')
    map.connect('/holySynod/makeInvite', controller='fca', action='makeInvite')
    map.connect('/holySynod/manageSettings', controller='fca', action='manageSettings')
    map.connect('/holySynod/manageBoards', controller='fca', action='manageBoards')
    map.connect('/holySynod/manageBoards/edit/:tag', controller='fca', tag='', action='editBoard')
    map.connect('/holySynod/manageUsers', controller='fca', action='manageUsers')
    map.connect('/holySynod/manageQuestions', controller='fca', action='manageQuestions')
    map.connect('/holySynod/manageApplications', controller='fca', action='manageApplications')
    map.connect('/holySynod/viewLog/:page', controller='fca', action='viewLog', page=0, requirements=dict(page='\d+'))
    # Threads
    map.connect('/:post', controller='fcc', action='PostReply',conditions=dict(method=['POST']),requirements=dict(post='\d+'))
    map.connect('/:post/delete', controller='fcc', action='DeletePost',conditions=dict(method=['POST']))
    map.connect('/:post/:tempid', controller='fcc', action='GetThread', tempid=0, requirements=dict(post='\d+',tempid='\d+'))
    map.connect('/:board', controller='fcc', action='PostThread',conditions=dict(method=['POST']))
    # Special filters
    #map.connect('/~/:tempid', controller='fcc', action='GetOverview', tempid=0, requirements=dict(tempid='\d+'))
    #map.connect('/~/page/:page', controller='fcc', action='GetOverview', tempid=0, page=0, requirements=dict(page='\d+'))
    #map.connect('/@/:tempid', controller='fcc', action='GetMyThreads', tempid=0, requirements=dict(tempid='\d+'))
    #map.connect('/@/page/:page', controller='fcc', action='GetMyThreads', tempid=0, page=0, requirements=dict(page='\d+'))
    # Generic filter
    map.connect('/:board/:tempid', controller='fcc', action='GetBoard', board = '~', tempid=0, requirements=dict(tempid='\d+'))
    map.connect('/:board/page/:page', controller='fcc', action='GetBoard', tempid=0, page=0, requirements=dict(page='\d+'))

    map.connect('*url', controller='fcc', action='UnknownAction')

    return map
