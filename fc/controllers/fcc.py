from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
import sqlalchemy
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
from beaker.cache import CacheManager
from wakabaparse import WakabaParser
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from fc.lib.fileHolder import AngryFileHolder
from OrphieBaseController import OrphieBaseController
from mutagen.easyid3 import EasyID3


import logging
log = logging.getLogger(__name__)

def taglistcmp(a, b):
    return cmp(b.count, a.count) or cmp(a.board.tag, b.board.tag)

class FccController(OrphieBaseController):        
    def __before__(self):
        OrphieBaseController.__before__(self)
        #self.userInst = FUser(session.get('uidNumber', -1))
        c.userInst = self.userInst
        c.destinations = destinations
                                    
        c.currentURL = request.path_info
        if c.currentURL[-1] != '/':
            c.currentURL = c.currentURL + '/'
              
        if not self.userInst.isAuthorized():
            return redirect_to(c.currentURL+'authorize')
        if self.userInst.isBanned():
            #abort(500, 'Internal Server Error')     # calm hidden ban
            return redirect_to('/youAreBanned')
        c.canPost = self.userInst.canPost()
        if self.userInst.isAdmin() and not checkAdminIP():
            return redirect_to('/')
        self.initEnvironment()
        
    def selfBan(self, confirm):
        if g.OPT.spiderTrap:
            if confirm:
                self.banUser(meta.Session.query(User).filter(User.uidNumber == self.userInst.uidNumber()).first(), 2, _("[AUTOMATIC BAN] Security alert type 2"))
                redirect_to('/')
            else:
                return self.render('selfBan')
        else:
            return redirect_to('/')
            
    def buildFilter(self, url):
        def buildMyPostsFilter():
            list  = []  
            posts = self.sqlAll(meta.Session.query(Post).filter(Post.uidNumber==self.userInst.uidNumber()))
                    
            for p in posts:
                if p.parentid == -1 and not p.id in list:
                    list.append(p.id)
                elif p.parentid > -1 and not p.parentid in list:
                    list.append(p.parentid)
            return Post.id.in_(list)
            
        def buildArgument(arg):
            if not isinstance(arg, sqlalchemy.sql.expression.ClauseElement):
                if arg == '@':
                    return (buildMyPostsFilter(), [])
                elif arg == '~':
                    return (not_(Post.tags.any(Tag.id.in_(self.userInst.homeExclude()))), [])
                else:
                    return (Post.tags.any(tag=arg), [arg])
            else:
                return arg
         
        #log.debug(self.userInst.homeExclude())
        operators = {'+':1, '-':1, '^':2, '&':2}
        url = url.replace('&amp;', '&')
        filter = meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==-1)
        filteringExpression = False
        tagList = []
        RPN = getRPN(url,operators)
        stack = []
        for i in RPN:
            if i in operators:
                # If operator is not provided with 2 arguments, we silently ignore it. (for example '- b' will be just 'b')
                if len(stack)>= 2:
                    arg2 = stack.pop()
                    arg1 = stack.pop()
                    if i == '+':
                        f = or_(arg1[0],arg2[0])
                        for t in arg2[1]:
                            if not t in arg1[1]:
                                arg1[1].append(t)
                        stack.append((f,arg1[1]))
                    elif i == '&' or i == '^':
                        f = and_(arg1[0],arg2[0])
                        for t in arg2[1]:
                            if not t in arg1[1]:
                                arg1[1].append(t)
                        stack.append((f,arg1[1])) 
                    elif i == '-':
                        f = and_(arg1[0],not_(arg2[0]))
                        for t in arg2[1]:
                            if t in arg1[1]:
                                arg1[1].remove(t)
                        stack.append((f,arg1[1]))                      
            else:
                stack.append(buildArgument(i))
        if stack and isinstance(stack[0][0],sqlalchemy.sql.expression.ClauseElement):
            cl = stack.pop()
            filteringExpression = cl[0]
            filter = filter.filter(filteringExpression)
            tagList = cl[1]
        return (filter, tagList, filteringExpression)
        
    def paginate(self, count, page, tpp):
        if count > 1:
            p = divmod(count, tpp)
            c.pages = p[0]
            if p[1]:
                c.pages += 1
            if (page + 1) > c.pages:
                page = c.pages - 1
            c.page = page

            if c.pages>15:
                c.showPagesPartial = True
                if c.page-5>1:
                    c.leftPage = c.page-5 
                else:
                    c.leftPage=2
                    
                if c.page+5<c.pages-2:
                    c.rightPage = c.page+5 
                else:
                    c.rightPage=c.pages-2   
        elif count == 1:
            c.page  = False
            c.pages = False
        elif count == 0:
            c.page  = False
            c.pages = False   
        c.count = count      
                  
    def excludeHiddenTags(self, filter):
        adminTagsLine = g.settingsMap['adminOnlyTags'].value
        forbiddenTags = getTagsListFromString(adminTagsLine)

        if not self.userInst.isAdmin():
            blocker = Post.tags.any(Tag.id.in_(forbiddenTags))
            filter = filter.filter(not_(
                                   or_(blocker,
                                        Post.parentPost.has(blocker),
                                   )))
            
        return filter         
        
    def showPosts(self, threadFilter, tempid='', page=0, board='', tags=[], tagList=[]):
        if isNumber(page):
            page = int(page)
        else:
            page = 0
        
        c.board = board
        c.uidNumber = self.userInst.uidNumber()
        c.enableAllPostDeletion = self.userInst.canDeleteAllPosts()
        c.isAdmin = self.userInst.isAdmin()

        #TODO: ?move into GLOBAL object
        extensions = self.sqlAll(meta.Session.query(Extension))
        extList = []
        for ext in extensions:
            extList.append(ext.ext)
        c.extLine = ', '.join(extList)
        
        #settingsMap = c.settingsMap
        threadFilter = self.excludeHiddenTags(threadFilter)
        #threadFilter = threadFilter.filter(not_(Post.id.in_(self.userInst.hideThreads())))
                        
        count = self.sqlCount(threadFilter)
        tpp = self.userInst.threadsPerPage()
        
        if page*tpp >= count and count > 0:
            c.errorText = _("Incorrect page")
            return self.render('error')
        
        self.paginate(count, page, tpp)
        #log.debug("count: %d" % count)
        
        if count > 1:
            c.threads = self.sqlSlice(threadFilter.order_by(Post.bumpDate.desc()), (page * tpp), (page + 1)* tpp)
            if self.userInst.mixOldThreads():
                oldThread = self.sqlFirst(threadFilter.filter(Post.bumpDate < c.threads[-1].bumpDate).order_by(sqlalchemy.func.random()))
                #log.debug(oldThread)
                if oldThread:
                    oldThread.mixed = True
                    c.threads.insert(1, oldThread)
                    
        elif count == 1:
            c.threads = [self.sqlOne(threadFilter)]
        elif count == 0:
            c.threads = []
        
        if tagList and len(tagList) == 1 and tags:
            currentBoard = tags[0]
            c.boardName = currentBoard.options and currentBoard.options.comment or ("/" + currentBoard.tag + "/")
            c.tagLine   = currentBoard.tag
        elif not tagList and tags:
            names = []
            rawNames = []
            for t in tags:
                names.append(t.options and t.options.comment or ("/" + t.tag + "/"))
                rawNames.append(t.tag)
            c.boardName = " + ".join(names)
            c.tagLine ="+".join(rawNames)
        else:
            c.boardName = board
            c.tagLine = c.boardName
            if board == '~':
                c.boardName = _('Overview')
            if board == '@':
                c.boardName = _('Related threads')
                
        c.boardOptions = self.conjunctTagOptions(tags)
        c.tagList = ' '.join(tagList)
            
        hiddenThreads = self.userInst.hideThreads()
        for thread in c.threads:
            thread.hidden = (str(thread.id) in hiddenThreads)
            if thread.hidden:
                tl = []
                for tag in thread.tags:
                    tl.append(tag.tag)
                thread.tagLine = ', '.join(tl)     
                            
            if count > 1:
                replyCount = thread.replyCount #meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==thread.id).count()
                #if not isNumber(replyCount):
                    #replyCount = 0
                    #log.debug("WARNING!!!" + str(thread.id) + "::" + str(replyCount)  )            
                
                replyLim   = replyCount - self.userInst.repliesPerThread() 
                if replyLim < 0:
                    replyLim = 0
                thread.omittedPosts = replyLim
                
                thread.Replies = self.sqlSlice(meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==thread.id).order_by(Post.id.asc()), replyLim)
            else:
                thread.Replies = self.sqlAll(meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==thread.id).order_by(Post.id.asc()))
                thread.omittedPosts = 0
                thread.hidden = False
                       
            #log.debug(thread.id)
            #log.debug(self.userInst.hideThreads())
            #log.debug(str(thread.id) in self.userInst.hideThreads())
            #log.debug(thread.hidden)
                
        if tempid:  
            oekaki = self.sqlFirst(meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid))
            c.oekaki = oekaki
        else:
            c.oekaki = False
        
        #c.returnTo = session.get('returnTo', False)
        c.curPage = page
        return self.render('posts')
        
    def __tagListFromString(self, tagstr):
            tags = []
            tagsl= []
            if tagstr:
                tagstr = tagstr.replace('&amp;', '&')
                regex = re.compile(r"""([^,@~\#\+\-\&\s\/\\\(\)<>'"%\d][^,@~\#\+\-\&\s\/\\\(\)<>'"%]*)""")
                tlist = regex.findall(tagstr)
                for t in tlist:
                    if not t in tagsl:
                        tag = self.sqlFirst(meta.Session.query(Tag).filter(Tag.tag==t))
                        
                        if tag:
                            tags.append(tag)
                        else:
                            tags.append(Tag(t))
                        tagsl.append(t)      
            return tags
        
    def GetThread(self, post, tempid):  
        thePost = self.sqlFirst(meta.Session.query(Post).options(eagerload('file')).filter(Post.id==post))
        
        #if thePost isn't op-post, redirect to op-post instead
        if thePost and thePost.parentid != -1:
            if isNumber(tempid) and not int(tempid) == 0:
                redirect_to('/%d/%d' % (thePost.parentid, int(tempid)))
            else:
                redirect_to('/%d#i%d' % (thePost.parentid, thePost.id))
            #thePost = meta.Session.query(Post).options(eagerload('file')).filter(Post.id==thePost.parentid).first()
            
        if not thePost:
            c.errorText = _("No such post exist.")
            return self.render('error')
            
        filter = meta.Session.query(Post).options(eagerload('file')).filter(Post.id==thePost.id)
        c.PostAction = thePost.id
        
        return self.showPosts(threadFilter=filter, tempid=tempid, page=0, board='', tags=thePost.tags)

    def GetBoard(self, board, tempid, page=0):
        if board == '!':
            def getTotalPosts():
                return meta.Session().query(Post).count() #.execute("select count(id) from posts")
                #return result.fetchone()[0]
            
            def mainStats():
                boards = self.sqlAll(meta.Session.query(Tag).options(eagerload('options')))
                ret = empty()
                ret.boards=[]
                ret.tags=[]
                ret.totalBoardsThreads = 0
                ret.totalTagsThreads = 0
                ret.totalBoardsPosts = 0
                ret.totalTagsPosts = 0
                for b in boards:
                    if not b.tag in forbiddenTags:
                        bc = empty()
                        bc.count = b.threadCount
                        bc.postsCount = b.replyCount
                        bc.board = b

                        if b.options and b.options.persistent:
                            ret.boards.append(bc)
                            ret.totalBoardsThreads += bc.count
                            ret.totalBoardsPosts += bc.postsCount
                        else:
                            ret.tags.append(bc)
                            ret.totalTagsThreads += bc.count
                            ret.totalTagsPosts += bc.postsCount

                        """
                        result = meta.Session().execute("select count(p.id) from posts as p, tagsToPostsMap as m where (p.id = m.postId and m.tagId = :ctid)", {'ctid':b.id})                                        
                        #filter = self.buildFilter(b.tag)                                        
                        #bc.count = filter[0].count()
                        bc.count = result.fetchone()[0]
                        result = meta.Session().execute("select count(p.id) from posts as p, tagsToPostsMap as m where ((p.id = m.postId or p.parentId = m.postId)and m.tagId = :ctid)", {'ctid':b.id})                    
                        bc.postsCount = result.fetchone()[0]
                        if b.options and b.options.persistent:
                            ret.boards.append(bc)
                            ret.totalBoardsThreads += bc.count
                            ret.totalBoardsPosts += bc.postsCount
                        else:
                            ret.tags.append(bc)
                            ret.totalTagsThreads += bc.count
                            ret.totalTagsPosts += bc.postsCount
                        """
                return ret
            
            def vitalSigns():
                ret = empty()
                tpc = c.totalPostsCount
                uniqueUidsExpr = meta.Session().query(Post.uidNumber).distinct()
                ret.last1KUsersCount = uniqueUidsExpr.filter(and_(Post.id <= tpc, Post.id >= tpc - 1000)).count()
                ret.prev1KUsersCount = uniqueUidsExpr.filter(and_(Post.id <= tpc - 1000, Post.id >= tpc - 2000)).count()
            
                currentTime = datetime.datetime.now()
                firstBnd = currentTime - datetime.timedelta(days=7)
                secondBnd = currentTime - datetime.timedelta(days=14)
                ret.lastWeekMessages = meta.Session().query(Post.id).filter(Post.date >= firstBnd).count()
                ret.prevWeekMessages = meta.Session().query(Post.id).filter(and_(Post.date <= firstBnd, Post.date >= secondBnd)).count()
                """
                result = meta.Session().execute("select count(distinct uidNumber) from posts where id <= :maxid and id >= :minid", {'maxid' : tpc, 'minid' : tpc - 1000})
                ret.last1KUsersCount = result.fetchone()[0]
                result = meta.Session().execute("select count(distinct uidNumber) from posts where id <= :maxid and id >= :minid", {'maxid' : tpc - 1000, 'minid' : tpc - 2000})
                ret.prev1KUsersCount = result.fetchone()[0]
                result = meta.Session().execute("select count(id) from posts where DATE_SUB(NOW(), INTERVAL 7 DAY) <= date")
                ret.lastWeekMessages = result.fetchone()[0]
                result = meta.Session().execute("select count(id) from posts where DATE_SUB(NOW(), INTERVAL 7 DAY) >= date and DATE_SUB(NOW(), INTERVAL 14 DAY) <= date")
                ret.prevWeekMessages = result.fetchone()[0]
                """
                return ret
            
            adminTagsLine = g.settingsMap['adminOnlyTags'].value
            forbiddenTags = adminTagsLine.split(',')   
            
            if g.OPT.devMode:
                ct = time.time()
            
            c.totalPostsCount = 0
            mstat = False
            vts = False
            chTime = g.OPT.statsCacheTime
            
            if chTime > 0: 
                cm = CacheManager(type='memory')
                #cch = cache.get_cache('home_stats')
                cch = cm.get_cache('home_stats')
                c.totalPostsCount = cch.get_value(key="totalPosts", createfunc=getTotalPosts, expiretime=chTime)
                mstat = cch.get_value(key="mainStats", createfunc=mainStats, expiretime=chTime)
                vts = cch.get_value(key="vitalSigns", createfunc=vitalSigns, expiretime=chTime)
            else:
                c.totalPostsCount = getTotalPosts()
                mstat = mainStats()
                vts = vitalSigns()
            
            c.boards = sorted(mstat.boards, taglistcmp)
            c.tags = sorted(mstat.tags, taglistcmp)
            c.totalBoardsThreads = mstat.totalBoardsThreads
            c.totalTagsThreads = mstat.totalTagsThreads
            c.totalBoardsPosts = mstat.totalBoardsPosts
            c.totalTagsPosts = mstat.totalTagsPosts
            
            c.last1KUsersCount = vts.last1KUsersCount
            c.prev1KUsersCount = vts.prev1KUsersCount
            c.lastWeekMessages = vts.lastWeekMessages
            c.prevWeekMessages = vts.prevWeekMessages
            
            c.boardName = _('Home')
            
            if g.OPT.devMode:
                c.log.append("home: " + str(time.time() - ct))
            return self.render('home') 
            
        board = filterText(board)
        c.PostAction = board
        
        if isNumber(page):
            page = int(page)
        else:
            page = 0        
        
        filter = self.buildFilter(board)  
        tags = self.sqlAll(meta.Session.query(Tag).options(eagerload('options')).filter(Tag.tag.in_(filter[1])))
        return self.showPosts(threadFilter=filter[0], tempid=tempid, page=int(page), board=board, tags=tags, tagList=filter[1])
    
    def makeThumbnail(self, source, dest, maxSize):
        sourceImage = Image.open(source)
        size = sourceImage.size
        if sourceImage:
           sourceImage.thumbnail(maxSize,Image.ANTIALIAS)
           sourceImage.save(dest)
           return size + sourceImage.size
        else:
           return []
               
    def processFile(self, file, thumbSize=250):
        if isinstance(file, cgi.FieldStorage) or isinstance(file,FieldStorageLike):
           # We should check whether we got this file already or not
           # If we dont have it, we add it
           name = str(long(time.time() * 10**7))
           ext  = file.filename.rsplit('.', 1)[:0:-1]
           
           if ext:
              ext = ext[0].lstrip(os.sep).lower()
           else:
              # Panic, no extention found
              ext = ''
              return ''
          
           # Make sure its something we want to have

           extParams = self.sqlFirst(meta.Session.query(Extension).filter(Extension.ext==ext))
           
           if not extParams:
              return [_(u'Extension "%s" is disallowed') % ext, False]

           localFilePath = os.path.join(g.OPT.uploadPath, name + '.' + ext)
           localFile = open(localFilePath,'w+b')
           shutil.copyfileobj(file.file, localFile)
           localFile.seek(0)
           md5 = hashlib.md5(localFile.read()).hexdigest()
           file.file.close()
           localFile.close()

           pic = self.sqlFirst(meta.Session.query(Picture).filter(Picture.md5==md5))

           if pic:
               os.unlink(localFilePath)
               return [pic, False]

           try:
                if extParams.type == 'image':
                   thumbFilePath = name + 's.' + ext
                   size = self.makeThumbnail(localFilePath, os.path.join(g.OPT.uploadPath,thumbFilePath), (thumbSize,thumbSize))
                else:
                   if extParams.type == 'image-jpg':
                      thumbFilePath = name + 's.jpg'
                      size = self.makeThumbnail(localFilePath, os.path.join(g.OPT.uploadPath,thumbFilePath), (thumbSize,thumbSize))
                   else:
                     thumbFilePath = extParams.path
                     size = [0, 0, extParams.thwidth, extParams.thheight]
           except:
                return [_(u"Broken picture. Maybe it is interlaced PNG?"), AngryFileHolder(localFilePath)]
              
           pic = Picture()
           pic.path = name + '.' + ext
           pic.thumpath = thumbFilePath
           pic.width = size[0]
           pic.height = size[1]
           pic.thwidth = size[2]
           pic.thheight = size[3]
           pic.extid = extParams.id
           pic.size = os.stat(localFilePath)[6]
           pic.md5 = md5
           meta.Session.add(pic)
           meta.Session.commit()
           return [pic, AngryFileHolder(localFilePath, pic)]
        else:
           return False
                   
    def processPost(self, postid=0, board=u''):
        fileHolder = False
        
        if not self.userInst.canPost():
            c.errorText = _("Posting is disabled")
            return self.render('error')
                
        if postid:
            thePost = self.sqlFirst(meta.Session.query(Post).filter(Post.id==postid))
         
            if not thePost:
                c.errorText = _("Can't post into non-existent thread")
                return self.render('error')           
                 
            # ???
            if thePost.parentid != -1: 
                thread = self.sqlOne(meta.Session.query(Post).filter(Post.id==thePost.parentid))         
            else:
               thread = thePost
            tags = thread.tags
        else:        
            tagstr = request.POST.get('tags', False)
            tags = self.__tagListFromString(tagstr)
            if not tags:
                c.errorText = _("You should specify at least one board")
                return self.render('error') 
            
            maxTagsCount = int(g.settingsMap['maxTagsCount'].value)
            maxTagLen = int(g.settingsMap['maxTagLen'].value)
            disabledTagsLine = g.settingsMap['disabledTags'].value
            
            if len(tags) > maxTagsCount:
                c.errorText = _("Too many tags. Maximum allowed: %s") % (maxTagsCount)
                return self.render('error') 
                
            tagsPermOk = True
            problemTags = []
            disabledTags = disabledTagsLine.lower().split(',')
            for tag in tags:
                tagLengthProblem = ((not tag.options) or (tag.options and not tag.options.persistent)) and len(tag.tag)>maxTagLen
                tagDisabled = tag.tag.lower() in disabledTags
                if (tagLengthProblem or tagDisabled):
                    tagsPermOk = False
                    errorMsg = _("Too long. Maximal length: %s" % maxTagLen)
                    if tagDisabled:
                        errorMsg = _("Disabled")
                    problemTags.append(tag.tag + " [%s]" % errorMsg)
                    
            if not tagsPermOk:
                c.errorText = _("Tags restrictions violations:<br/> %s") % ('<br/>'.join(problemTags))
                return self.render('error') 
                
        options = self.conjunctTagOptions(tags)
        if not options.images and ((not options.imagelessThread and not postid) or (postid and not options.imagelessPost)):
            c.errorText = "Unacceptable combination of tags"
            return self.render('error')
        
        post = Post()
        #tempid = request.POST.get('tempid', False)
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        post.message = filterText(request.POST.get('message', u'')).replace('&gt;','>') #XXX: TODO: this must be fixed in parser
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        # VERY-VERY BIG CROCK OF SHIT !!!!!!!
        
        tempid = request.POST.get('tempid', False)        
        painterMark = False # TODO FIXME : move into parser
        if tempid: 
           oekaki = self.sqlFirst(meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid))

           file = FieldStorageLike(oekaki.path,os.path.join(g.OPT.uploadPath, oekaki.path))
           painterMark = u'<span class="postInfo">Drawn with <b>%s</b> in %s seconds</span>' % (oekaki.type, str(int(oekaki.time/1000)))
           if oekaki.source:
              painterMark += ", source " + self.formatPostReference(oekaki.source) #<a href="">&lt;&lt;%s</a>" % oekaki.source
           meta.Session.delete(oekaki) # TODO: Is it really needed to destroy oekaki IDs?
        else:
           file = request.POST.get('file',False)
        if painterMark:
            if post.messageInfo:
                post.messageInfo += painterMark
            else:
                post.messageInfo = painterMark
        if post.message:
           if len(post.message) <= 15000:
               parser = WakabaParser(g.OPT.markupFile)
               maxLinesInPost = int(g.settingsMap['maxLinesInPost'].value)
               cutSymbols = int(g.settingsMap["cutSymbols"].value)
               parsedMessage = parser.parseWakaba(post.message,self,lines=maxLinesInPost,maxLen=cutSymbols)
               fullMessage = parsedMessage[0]
               
               post.messageShort = parsedMessage[1]
               #FIXME: not best solution
               #if not fullMessage[5:].startswith(post.message):
               if (not post.message in fullMessage) or post.messageShort:
                   post.messageRaw = post.message
                   
               post.message = fullMessage
           else:
               c.errorText = _('Message is too long')
               return self.render('error') 
        
        post.title = filterText(request.POST.get('title', u''))
        post.date = datetime.datetime.now()
        
        fileDescriptors = self.processFile(file, options.thumbSize)    
        pic = False  
        if fileDescriptors:
            pic = fileDescriptors[0]
            fileHolder = fileDescriptors[1] # Object for file auto-removing
        
        if pic:
            if isinstance(pic, basestring) or isinstance(pic, unicode):
                c.errorText = pic
                return self.render('error')
            if pic.size > options.maxFileSize:
                c.errorText = _("File size (%d) exceeds the limit (%d)") % (pic.size, options.maxFileSize)
                return self.render('error') 
            if pic.height and (pic.height < options.minPicSize or pic.width < options.minPicSize):
                c.errorText = _("Image is too small. At least one side should be %d or more pixels.") % (options.minPicSize)
                return self.render('error') 
            if not options.images:
                c.errorText = _("Files are not allowed on this board")
                return self.render('error') 
            post.picid = pic.id
            
            try:
                if fileHolder:
                    audio = EasyID3(fileHolder.path())
                    trackInfo = '<span class="postInfo">Id3 info:</span><br/>'
                    for tag in audio.keys():
                        #log.debug(tag)
                        #log.debug(audio[tag])
                        value = audio[tag]
                        if value and isinstance(value, list) and tag in id3FieldsNames.keys():
                            value = ' '.join(value) 
                            trackInfo += u'<span class="postInfo"><b>%s</b>: %s</span><br/>' % (filterText(id3FieldsNames[tag]), filterText(value))
                    
                    if not post.messageInfo:
                        post.messageInfo = trackInfo
                    else:
                        post.messageInfo += '<br/>%s' % trackInfo
            except:
                pass
            #try:
            #except:
            #    pass
            
        post.uidNumber = self.userInst.uidNumber()
        
        if not post.message and not post.picid and not post.messageInfo:
            c.errorText = "At least message or file should be specified"
            return self.render('error') 
        
        if options.enableSpoilers:
            post.spoiler = request.POST.get('spoiler', False)  
            
        if postid:
            if not post.picid and not options.imagelessPost:
                c.errorText = _("Replies without image are not allowed")
                return self.render('error') 
                
            post.parentid = thread.id
            thread.replyCount += 1
            post.sage = request.POST.get('sage', False)
            if not post.sage:
                thread.bumpDate = datetime.datetime.now()
        else:
            if not post.picid and not options.imagelessThread:
                c.errorText = "Threads without image are not allowed"
                return self.render('error')
            post.parentid = -1
            post.replyCount = 0
            post.bumpDate = datetime.datetime.now()
            post.tags = tags
        
        newThread = True
        taglist = post.tags
        if not taglist:
            taglist = thread.tags
            newThread = False
            
        for tag in taglist:
            tag.replyCount += 1
            if newThread:
                tag.threadCount += 1
            
        if fileHolder:
            fileHolder.disableDeletion()
        meta.Session.add(post)
        meta.Session.commit()
        self.gotoDestination(post, postid)
        
    def gotoDestination(self, post, postid):        
        tagLine = request.POST.get('tagLine', '~')
        
        dest = int(request.POST.get('goto', 0))
        if isNumber(dest):
            dest = int(dest)
        else:
            dest = 0
            
        curPage = request.POST.get('curPage', 0)
        if isNumber(curPage):
            curPage = int(curPage)
        else:
            curPage = 0
              
        ##log.debug('%s %s %s' % (tagLine, str(dest), str(curPage)))
        redirectAddr = '~'
        
        if dest == 4: # destination board
            if post.parentid == -1:           
                tags = []
                for tag in post.tags:
                    tags.append(tag.tag)
                postTagline = "+".join(tags)
                                        
                redirectAddr = '%s/' % (postTagline) 
            else:
                dest = 1    
        
        if dest == 0: #current thread
            if postid:
                return redirect_to(action='GetThread', post=post.parentid, board=None)
            else:
                return redirect_to(action='GetThread', post=post.id, board=None)              
        elif dest == 1 or dest == 2: # current board
            if  tagLine:
                if dest == 1:
                    curPage = 0
                redirectAddr = "%s/page/%d" % (tagLine, curPage)          
        elif dest == 3: # overview
            pass
        elif dest == 5: #referrer
            return redirect_to(request.headers.get('REFERER', str(tagLine)))
        
        ##log.debug(redirectAddr)
        return redirect_to(str('/%s' % redirectAddr.encode('utf-8')))    
        


    def PostReply(self, post):
        return self.processPost(postid=post)

    def PostThread(self, board):
        return self.processPost(board=board)            

    def oekakiDraw(self,url):
        if not self.userInst.canPost():
            c.errorText = _("Posting is disabled")
            return self.render('error')
                                            
        c.url = url
        c.canvas = False
        c.width  = request.POST.get('oekaki_x','300')
        c.height = request.POST.get('oekaki_y','300')
        enablePicLoading = not (request.POST.get('oekaki_type','Reply') == 'New');        
        if not (isNumber(c.width) or isNumber(c.height)) or (int(c.width)<=10 or int(c.height)<=10):
           c.width = 300
           c.height = 300            
        c.tempid = str(long(time.time() * 10**7))
        oekaki = Oekaki()
        oekaki.tempid = c.tempid
        oekaki.picid = -1
        oekaki.time = -1
        oekaki.timeStamp = datetime.datetime.now()
        if request.POST.get('oekaki_painter','shiNormal') == 'shiNormal':
            oekaki.type = 'Shi normal'
            c.oekakiToolString = 'normal';
        else:
            oekaki.type = 'Shi pro'
            c.oekakiToolString = 'pro'
        oekaki.uidNumber = session['uidNumber']
        oekaki.path = ''        
        oekaki.source = 0
        if isNumber(url) and enablePicLoading: 
           post = self.sqlOne(meta.Session.query(Post).filter(Post.id==url))

           if post.picid:
              pic = self.sqlFirst(meta.Session.query(Picture).filter(Picture.id==post.picid))
               
              if pic and pic.width:
                 oekaki.source = post.id
                 c.canvas = h.modLink(pic.path, c.userInst.secid(), g.OPT.secureLinks)
                 c.width  = pic.width
                 c.height = pic.height
        meta.Session.add(oekaki)
        meta.Session.commit()
#        return render('/spainter.mako')
        return self.render('spainter')
        
    def DeletePost(self, board):
        fileonly = 'fileonly' in request.POST
        redirectAddr = board
             
        opPostDeleted = False
        reason = filterText(request.POST.get('reason', '???'))
        
        retest = re.compile("^\d+$")
        for i in request.POST:
            if retest.match(request.POST[i]):
                res = self.processDelete(request.POST[i], fileonly, True, reason)
                opPostDeleted = opPostDeleted or res 
     
        tagLine = request.POST.get('tagLine', False)
        if opPostDeleted: 
            if tagLine:
                redirectAddr = tagLine
            else:   
                redirectAddr = '~'
                
        return redirect_to(str('/%s' % redirectAddr.encode('utf-8')))
    
    def Anonimyze(self, post):
        postid = request.POST.get('postId', False)
        batch = request.POST.get('batchFA', False)
        if postid and isNumber(postid):
            c.FAResult = self.processAnomymize(int(postid), batch)
        else:
            c.boardName = _('Final Anonymization')
            c.FAResult = False
            c.postId = post
        return self.render('finalAnonymization')
    
    def processAnomymize(self, postid, batch):
        if not g.OPT.enableFinalAnonymity:
            return _("Final Anonymity is disabled")
        
        result = []
        post = self.sqlGet(meta.Session.query(Post), postid)
        if post:
            posts = []
            if not batch:
                posts = [post]
            else:
                posts = self.sqlAll(meta.Session.query(Post).filter(and_(Post.uidNumber == self.userInst.uidNumber(), Post.date <= post.date)))
            for post in posts:
                if post.uidNumber != self.userInst.uidNumber():
                    result.append(_("You are not author of post #%s") % post.id)
                else:
                    delay = g.OPT.finalAHoursDelay
                    timeDelta = datetime.timedelta(hours=delay)
                    if post.date < datetime.datetime.now() - timeDelta:
                        post.uidNumber = 0
                        result.append(_("Post #%d successfully anonymized") % post.id)
                    else:
                        params = (post.id, str(h.modifyTime(post.date, self.userInst, g.OPT.secureTime) + timeDelta), str(datetime.datetime.now()))
                        result.append(_("Can't anomymize post #%d now, it will be allowed after %s (now: %s)" % params))
            meta.Session.commit()
        else:
            result = [_("Nothing to anonymize")]
        
        return result
        
    def showProfile(self):
        if self.userInst.Anonymous:
            c.errorText = _("Profile is not avaiable to Anonymous users.")
            return self.render('error')
                                            
        c.templates = g.OPT.templates #['wakaba'] # TODO FIXME: init from settingsMap
        c.styles    = g.OPT.styles #['photon']
        c.profileChanged = False
        c.boardName = _('Profile')
        if request.POST.get('update', False):
            template = request.POST.get('template', self.userInst.template())
            if template in c.templates:
                self.userInst.template(template)
            style = filterText(request.POST.get('style', self.userInst.style()))
            if style in c.styles:
                self.userInst.style(style)
            gotodest = filterText(request.POST.get('defaultGoto', self.userInst.defaultGoto()))
            if isNumber(gotodest) and (int(gotodest) in destinations.keys()):
                #log.debug(gotodest)
                self.userInst.defaultGoto(int(gotodest))                
            threadsPerPage = request.POST.get('threadsPerPage',self.userInst.threadsPerPage())
            if isNumber(threadsPerPage) and (0 < int(threadsPerPage) < 30):
                self.userInst.threadsPerPage(threadsPerPage)
            repliesPerThread = request.POST.get('repliesPerThread',self.userInst.repliesPerThread())
            if isNumber(repliesPerThread) and (0 < int(repliesPerThread) < 100):
                self.userInst.repliesPerThread(repliesPerThread)
            self.userInst.hideLongComments(request.POST.get('hideLongComments',False))
            self.userInst.useAjax(request.POST.get('useAjax', False))
            self.userInst.mixOldThreads(request.POST.get('mixOldThreads', False))
            homeExcludeTags = self.__tagListFromString(request.POST.get('homeExclude', u''))
            homeExcludeList = []
            for t in homeExcludeTags:
                homeExcludeList.append(t.id)
            self.userInst.homeExclude(homeExcludeList)

            c.profileMsg = _('Password was NOT changed.')
            
            key = request.POST.get('key','').encode('utf-8')
            key2 = request.POST.get('key2','').encode('utf-8')
            currentKey = request.POST.get('currentKey', '').encode('utf-8')
            
            # XXX: temporary code. Methods from OrphieBaseController must be moved into model
            passwdRet = self.passwd(key, key2, False, currentKey)
            if passwdRet != True and passwdRet != False:
                return passwdRet
            
            c.profileChanged = True 
            c.profileMsg += _(' Profile was updated.')           
            meta.Session.commit()
            
        homeExcludeTags = self.sqlAll(meta.Session.query(Tag).filter(Tag.id.in_(self.userInst.homeExclude())))
        homeExcludeList = []
        for t in homeExcludeTags:
            homeExcludeList.append(t.tag)
        c.homeExclude = ', '.join(homeExcludeList)
        c.hiddenThreads = self.sqlAll(meta.Session.query(Post).options(eagerload('file')).options(eagerload('tags')).filter(Post.id.in_(self.userInst.hideThreads())))
        for t in c.hiddenThreads:
            tl = []
            for tag in t.tags:
                tl.append(tag.tag)
            t.tagLine = ', '.join(tl)
        c.userInst = self.userInst
        return self.render('profile')
        
    def viewLog(self,page):
        #settingsMap = c.settingsMap    
        if g.settingsMap['usersCanViewLogs'].value == 'true':
            c.boardName = 'Logs'
            page = int(page)
            count = self.sqlCount(meta.Session.query(LogEntry).filter(not_(LogEntry.event.in_(disabledEvents))))
            p = divmod(count, 100)
            c.pages = p[0]
            if p[1]:
                c.pages += 1
            if (page + 1) > c.pages:
                page = c.pages - 1
            c.page = page        
            c.logs = meta.Session.query(LogEntry).filter(not_(LogEntry.event.in_(disabledEvents))).options(eagerload('user')).order_by(LogEntry.date.desc())[page*100:(page+1)*100]
            rv = re.compile('(\d+\.){3}\d+')
            for log in c.logs:
                log.entry = rv.sub('<font color="red">[IP REMOVED]</font>', log.entry)
            return self.render('logs')
        else:
            return redirect_to('/')
        
    def search(self, text, page = 0):
        rawtext = text
        if not text:
            rawtext = request.POST.get('query', u'')
            text = filterText(rawtext)

        if not text or len(rawtext) < 3:
            c.boardName = _('Error')
            c.errorText = _("Query too short (minimal length: 3)")
            return self.render('error')
        
        if isNumber(page):
            page = int(page)
        else:
            page = 0
            
        pp = self.userInst.threadsPerPage()
        c.boardName = _("Search")        
        c.query = text
        
        tagfilter = False
        filteredQueryRe = re.compile("^(([^:]+):){1}(.+)$").match(text)
        if filteredQueryRe:
            groups = filteredQueryRe.groups()
            filterName = groups[1]
            text = groups[2]
            tagfilter = self.buildFilter(filterName)[2]
            
        base = meta.Session.query(Post)
        if tagfilter:
            base = meta.Session.query(Post)
            
            base = base.filter(or_(tagfilter,
                                        Post.parentPost.has(tagfilter),
                                   ))
        
        filter = self.excludeHiddenTags(base)
        filter = filter.filter(Post.message.like('%%%s%%' % text))
            
        adminTagsLine = g.settingsMap['adminOnlyTags'].value
        forbiddenTags = getTagsListFromString(adminTagsLine)
        
        count = self.sqlCount(filter)
        #log.debug(count)  
        self.paginate(count, page, pp)
        posts = self.sqlSlice(filter.order_by(Post.date.desc()), (page * pp), (page + 1)* pp)
        
        c.posts = []
        for p in posts:
            parent = p
            if not p.parentid == -1: 
                parent = p.parentPost #self.sqlFirst(meta.Session.query(Post).filter(Post.id == p.parentid))
                
            pt = []
            pt.append(p)
            if p.parentid == -1:
                pt.append(p)
            else:
               pt.append(parent)
            c.posts.append(pt)
        
        return self.render('search')
        
