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
    map.connect('/authorize', controller='fcp', action='authorize', url='')
    map.connect('/captcha/:cid', controller='fcp', action='captchaPic', cid=0)
    map.connect('/logout', controller='fcp', action='logout', url='')
    map.connect('/*url/authorize', controller='fcp', action='authorize', url='')
    map.connect('/register/:invite', controller='fcp', action='register')
    map.connect('/youAreBanned', controller='fcp', action='banned')
    map.connect('/Join', controller='fcp', action='showStatic', page = 'Join')    

    # Oekaki
    map.connect('/:url/oekakiDraw', controller='fcc', action='oekakiDraw', url='')
    map.connect('/:url/oekakiSave/:tempid', controller='fcp', action='oekakiSave', url='',requirements=dict(tempid='\d+'))
    
    # User subsystem
    map.connect('/userProfile', controller='fcc', action='showProfile')
    #map.connect('/userProfile/messages', controller='fcc', action='showMessages')
    map.connect('/viewLog/:page', controller='fcc', action='viewLog', page=0, requirements=dict(page='\d+'))

    # Admin subsystem
    map.connect('/holySynod', controller='fca', action='index')
    map.connect('/holySynod/invitePage', controller='fca', action='invitePage')
    map.connect('/holySynod/makeInvite', controller='fca', action='makeInvite')
    map.connect('/holySynod/manageSettings', controller='fca', action='manageSettings')
    map.connect('/holySynod/manageExtensions', controller='fca', action='manageExtensions')
    map.connect('/holySynod/manageExtensions/edit/:ext', controller='fca', ext='', action='editExtension')
    map.connect('/holySynod/manageBoards', controller='fca', action='manageBoards')
    map.connect('/holySynod/manageBoards/edit/:tag', controller='fca', tag='', action='editBoard')
    map.connect('/holySynod/manageUsers', controller='fca', action='manageUsers')
    map.connect('/holySynod/manageUsers/editAttempt/:pid', controller='fca', action='editUserAttempt', requirements=dict(pid='\d+'))    
    map.connect('/holySynod/manageUsers/editUserByPost/:pid', controller='fca', action='editUserByPost', requirements=dict(pid='\d+'))        
    map.connect('/holySynod/manageUsers/edit/:uid', controller='fca', action='editUser', requirements=dict(uid='\d+'))
    map.connect('/holySynod/manageQuestions', controller='fca', action='manageQuestions')
    map.connect('/holySynod/manageApplications', controller='fca', action='manageApplications')
    map.connect('/holySynod/viewLog/:page', controller='fca', action='viewLog', page=0, requirements=dict(page='\d+'))
    map.connect('/holySynod/manageMappings/:act/:id/:tagid', controller='fca', action='manageMappings', act='show', id=0, tagid=0, requirements=dict(id='\d+', tagid='\d+'))        

    # Maintenance
    map.connect('/holySynod/service/:actid/:secid', controller='fcm', actid='', secid='', action='mtnAction')    
    
    # AJAX
    map.connect('/ajax/getPost/:post', controller='fcajax', action='getPost', requirements=dict(post='\d+'))
    map.connect('/ajax/getRenderedPost/:post', controller='fcajax', action='getRenderedPost', requirements=dict(post='\d+'))
    map.connect('/ajax/editUserFilter/:fid/:filter', controller='fcajax', action='editUserFilter', requirements=dict(fid='\d+'))
    map.connect('/ajax/deleteUserFilter/:fid', controller='fcajax', action='deleteUserFilter', requirements=dict(fid='\d+'))
    map.connect('/ajax/addUserFilter/:filter', controller='fcajax', action='addUserFilter')
    
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
    map.connect('/:board/:tempid', controller='fcc', action='GetBoard', board = '!', tempid=0, requirements=dict(tempid='\d+'))
    map.connect('/:board/page/:page', controller='fcc', action='GetBoard', tempid=0, page=0, requirements=dict(page='\d+'))
    
    map.connect('/static/:page', controller='fcc', action='showStatic', page = 'Rules')

    map.connect('*url', controller='fcp', action='UnknownAction')

    return map
