import logging

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
from wakabaparse import WakabaParser
from fc.lib.fuser import FUser

class FieldStorageLike(object):
    def __init__(self,filename,filepath):
        self.filename = filename
        self.file = open(filepath,'rb')

def isNumber(n):
    if n and isinstance(n, basestring):
        if re.match("^[-+]?[0-9]+$", n):
            return True
        else:
            return False
    else:
        return False

log = logging.getLogger(__name__)
hashSecret = 'paranoia' # We will hash it by sha512, so no need to have it huge
uploadPath = 'fc/public/uploads/'
uploadPathWeb = '/uploads/'
class FccController(BaseController):
    def __before__(self):
        self.userInst = FUser(session.get('uid_number',-1))
        c.userInst = self.userInst
        
    def authorize(self, url):
        if url:
            c.currentURL = '/' + str(url.encode('utf-8')) + '/'
        else:
            c.currentURL = '/'
        if request.POST['code']:
            code = hashlib.sha512(request.POST['code'] + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
            user = meta.Session.query(User).options(eagerload('options')).filter(User.uid==code).first()
            if user:
                self.login(user)
                redirect_to(c.currentURL)
        return render('/wakaba.login.mako')
    def login(self, user):
        isNumber(True)
        session['uid_number'] = user.uid_number
        session.save()
    def initEnvironment(self):
        settingsDef = {
            "title" : "FailChan",
            "uploadPathLocal" : 'fc/public/uploads/',
            "uploadPathWeb" :  '/uploads/'
        }
        settings = meta.Session.query(Setting).all()
        settingsMap = {}
        if settings:
            for s in settings:
                if s.name in settingsDef:
                    settingsMap[s.name] = s
        for s in settingsDef:
            if not s in settingsMap:
                settingsMap[s] = Setting()
                settingsMap[s].name = s
                settingsMap[s].value = settingsDef[s]
                meta.Session.save(settingsMap[s])
                meta.Session.commit()        
        c.title = settingsMap['title'].value
        boards = meta.Session.query(Tag).join('options').filter(TagOptions.persistent==True).order_by(TagOptions.section_id).all()
        c.boardlist = []
        section_id = 0
        section = []
        for b in boards:
            if not section_id:
                section_id = b.options.section_id
                section = []
            if section_id != b.options.section_id:
                c.boardlist.append(section)
                section_id = b.options.section_id
                section = []
            section.append(b.tag)
        if section:
            c.boardlist.append(section)
    def getRPN(self,text,operators):
        whitespace = [' ',"\t","\r","\n","'",'"','\\','<','>']
        stack = []
        temp  = []
        result= []
        for i in text:
            if i == '(':
                if temp:
                    result.append(''.join(temp))
                    temp = []
                stack.append('(')
            elif i == ')':
                if temp:
                    result.append(''.join(temp))
                    temp = []                
                while (stack and stack[-1] != '('):
                    result.append(stack.pop())
                if stack:
                    stack.pop()
            elif i in operators:
                if temp:
                    result.append(''.join(temp))
                    temp = []
                while (stack and (stack[-1] in operators) and (operators[i] <= operators[stack[-1]])):
                    result.append(stack.pop())
                stack.append(i)
            elif not i in whitespace:
                temp.append(i)
        if temp:
            result.append(''.join(temp))
            temp = []
        while stack:
            result.append(stack.pop())
        return result
    def buildFilter(self,url):
        def buildMyPostsFilter():
            list  = []
            posts = meta.Session.query(Post).filter(Post.uid_number==self.userInst.uidNumber()).all()
            for p in posts:
                if p.parentid == -1 and not p.id in list:
                    list.append(p.id)
                elif p.parentid > -1 and not p.parentid in list:
                    list.append(p.parentid)
            return Post.id.in_(list)
            
        def buildArgument(arg):
            if not isinstance(arg,sqlalchemy.sql.expression.ClauseElement):
                if arg == '@':
                    return buildMyPostsFilter()
                elif arg == '~':
                    return Post.parentid==-1
                else:
                    return Post.tags.any(tag=arg)
            else:
                return arg
         
        operators = {'+':1,'-':1,'^':2,'&':2}
        filter = meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==-1)
        RPN = self.getRPN(url,operators)
        stack = []
        for i in RPN:
            if i in operators:
                # If operator is not provided with 2 arguments, we silently ignore it. (for example '- b' will be just 'b')
                if len(stack)>= 2:
                    arg2 = stack.pop()
                    arg1 = stack.pop()
                    if i == '+':
                        stack.append(or_(arg1,arg2))
                    elif i == '&' or i == '^':
                        stack.append(and_(arg1,arg2))
                    elif i == '-':
                        stack.append(and_(arg1,not_(arg2)))
            else:
                stack.append(buildArgument(i))
        if stack and isinstance(stack[0],sqlalchemy.sql.expression.ClauseElement):
            cl = stack.pop()
            filter = filter.filter(cl)
        return filter
    def showPosts(self, threadFilter, tempid='', page=0, board=''):
        self.initEnvironment()
        c.board = board
        c.uploadPathWeb = uploadPathWeb
        c.uid_number = self.userInst.uidNumber()
        c.enableAllPostDeletion = self.userInst.canDeleteAllPosts()
        count = threadFilter.count()
        
        c.showSpoilerCheckbox = True
        if board and board != '~':
            currentBoard = meta.Session.query(Tag).filter(Tag.tag==board).first()
            if currentBoard and currentBoard.options and currentBoard.options.comment:
                c.boardName = currentBoard.options.comment
                c.showSpoilerCheckbox = currentBoard.options.enableSpoilers
            else:
                c.boardName = '/%s/' % board               

        if count > 1:
            p = divmod(count, self.userInst.threadsPerPage())
            c.pages = p[0]
            if p[1]:
                c.pages += 1
            if (page + 1) > c.pages:
                page = c.pages - 1
            c.page = page
            c.threads = threadFilter.order_by(Post.last_date.desc())[(page * self.userInst.threadsPerPage()):(page + 1)* self.userInst.threadsPerPage()]
        elif count == 1:
            c.page  = False
            c.pages = False
            c.threads = [threadFilter.one()]
        elif count == 0:
            c.page  = False
            c.pages = False
            c.threads = []

        for thread in c.threads:
            if count > 1:
                replyCount = meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==thread.id).count()
                replyLim   = replyCount - self.userInst.repliesPerThread() 
                if replyLim < 0:
                    replyLim = 0
                thread.omittedPosts = replyLim
                thread.Replies = meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==thread.id).order_by(Post.id.asc())[replyLim:]
            else:
                thread.Replies = meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==thread.id).order_by(Post.id.asc()).all()
                thread.omittedPosts = 0
                
        if tempid:
            oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
            c.oekaki = oekaki
        else:
            c.oekaki = False
        
        try:            
            c.returnToThread = session['returnToThread']
        except KeyError: 
            pass
             
        return render('/%s.posts.mako' % self.userInst.template())
        
    def getParentID(self, id):
        post = meta.Session.query(Post).filter(Post.id==id).first()
        if post:
           return post.parentid
        else:
           return False
    
    def isPostOwner(self, id):
        post = meta.Session.query(Post).filter(Post.id==id).first()
        if post and post.uid_number == self.userInst.uidNumber():
           return post.parentid
        else:
           return False

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
        if isinstance(file,cgi.FieldStorage) or isinstance(file,FieldStorageLike):
           # We should check whether we got this file already or not
           # If we dont have it, we add it
           name = str(long(time.time() * 10**7))
           ext  = file.filename.rsplit('.',1)[:0:-1]
           if ext:
              ext = ext[0].lstrip(os.sep)
           else:
              # Panic, no extention found
              ext = ''
              return ''
           # Make sure its something we want to have
           extParams = meta.Session.query(Extension).filter(Extension.ext==ext).first()
           if not extParams:
              return ''

           localFilePath = os.path.join(uploadPath,name + '.' + ext)
           localFile = open(localFilePath,'w+b')
           shutil.copyfileobj(file.file, localFile)
           localFile.seek(0)
           md5 = hashlib.md5(localFile.read()).hexdigest()
           file.file.close()
           localFile.close()

           pic = meta.Session.query(Picture).filter(Picture.md5==md5).first()
           if pic:
               os.unlink(localFilePath)
               return pic

           if extParams.type == 'image':
              thumbFilePath = name + 's.' + ext
              size = self.makeThumbnail(localFilePath, os.path.join(uploadPath,thumbFilePath), (thumbSize,thumbSize))
           else:
               if extParams.type == 'image-jpg':
                  thumbFilePath = name + 's.jpg'
                  size = self.makeThumbnail(localFilePath, os.path.join(uploadPath,thumbFilePath), (thumbSize,thumbSize))
               else:
                  thumbFilePath = extParams.path
                  size = [0,0,extParams.thwidth,extParams.thheight]
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
           meta.Session.save(pic)
           meta.Session.commit()
           return pic
        else:
           return None
    def conjunctTagOptions(self, tags):
        options = TagOptions()
        options.imageless_thread = True
        options.imageless_post   = True
        options.images   = True
        options.max_fsize = 2621440
        options.min_size = 50
        options.thumb_size = 250
        for t in tags:
            if t.options:
                options.imageless_thread = options.imageless_thread & t.options.imageless_thread
                options.imageless_post = options.imageless_post & t.options.imageless_post
                options.images = options.images & t.options.images
                if t.options.max_fsize < options.max_fsize:
                    options.max_fsize = t.options.max_fsize
                if t.options.min_size > options.min_size:
                    options.min_size = t.options.min_size
                if t.options.thumb_size < options.thumb_size:
                    options.thumb_size = t.options.thumb_size                   
        return options
    def processPost(self, postid=0, board=u''):
        if postid:
            thePost = meta.Session.query(Post).filter(Post.id==postid).first()
            if thePost.parentid != -1:
               thread = meta.Session.query(Post).filter(Post.id==thePost.parentid).one()
            else:
               thread = thePost
            tags = thread.tags
        else:
            tags = []
            tagsl= []
            #maintag = request.POST.get('maintag',False)
            #if maintag and maintag != '~':
            #    tag = meta.Session.query(Tag).filter(Tag.tag==maintag).first()
            #    if tag:
            #        tags.append(tag)
            #    else:
            #        tags.append(Tag(maintag))
            #    tagsl.append(maintag)
            tagstr = request.POST.get('tags',False)
            if tagstr:
                regex = re.compile(r"""([^,@~\+\-\&\s\/\\\(\)<>'"%\d][^,@~\+\-\&\s\/\\\(\)<>'"%]*)""")
                tlist = regex.findall(tagstr)
                for t in tlist:
                    if not t in tagsl:
                        tag = meta.Session.query(Tag).filter(Tag.tag==t).first()
                        if tag:
                            tags.append(tag)
                        else:
                            tags.append(Tag(t))
                        tagsl.append(t)
            if not tags:
                c.errorText = "You should specify at least one board"
                return render('/wakaba.error.mako')
        options = self.conjunctTagOptions(tags)
        if not options.images and ((not options.imageless_thread and not postid) or (postid and not options.imageless_post)):
            c.errorText = "Unacceptable combination of tags"
            return render('/wakaba.error.mako')
        
        post = Post()
        tempid = request.POST.get('tempid',False)
        post.message = request.POST.get('message', '')
        tempid = request.POST.get('tempid',False)
        if tempid:
           oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
           file = FieldStorageLike(oekaki.path,os.path.join(uploadPath,oekaki.path))
           post.message += "\r\nDrawn with **%s** in %s seconds" % (oekaki.type,str(int(oekaki.time/1000)))
           if oekaki.source:
              post.message += ", source >>%s" % oekaki.source
        else:
           file = request.POST.get('file',False)
        if post.message:
           parser = WakabaParser()
           post.message = parser.parseWakaba(post.message,self)     
        post.title = request.POST['title']
        post.date = datetime.datetime.now()
        pic = self.processFile(file,options.thumb_size)
        if pic:
            if pic.size > options.max_fsize:
                c.errorText = "File size exceeds the limit"
                return render('/wakaba.error.mako')
            if pic.height and (pic.height < options.min_size or pic.width < options.min_size):
                c.errorText = "Image is too small"
                return render('/wakaba.error.mako')
            post.picid = pic.id
        post.uid_number = self.userInst.uidNumber()
        
        if not post.message and not post.picid:
            c.errorText = "At least message or file should be specified"
            return render('/wakaba.error.mako')
        
        if options.enableSpoilers:
            post.spoiler = request.POST.get('spoiler', False)        
            
        if postid:
            if not post.picid and not options.imageless_post:
                c.errorText = "Replies without image are not allowed"
                return render('/wakaba.error.mako')
            post.parentid = thread.id
            post.sage = request.POST.get('sage', False)
            if not post.sage:
                thread.last_date = datetime.datetime.now()
        else:
            if not post.picid and not options.imageless_thread:
                c.errorText = "Threads without image are not allowed"
                return render('/wakaba.error.mako')        
            post.parentid = -1
            post.last_date = datetime.datetime.now()
            post.tags = tags
        meta.Session.save(post)
        meta.Session.commit()
        returnTo = request.POST.get('gb2', 'board')
        #response.set_cookie('returnTo', returnTo, expires=3600000)
        session['returnToThread'] = not (returnTo == 'board')
        session.save()
        if returnTo == 'board':             
            rboard = u'/'+tags[0].tag+u'/'
            redirect_to(rboard.encode('utf-8'))
        else:
            if postid:
                return redirect_to(action='GetThread',post=post.parentid,board=None)
            else:
                return redirect_to(action='GetThread',post=post.id,board=None)          

    def GetOverview(self, page=0, tempid=''):
        c.currentURL = '/~/'
        if not self.userInst.isAuthorized():
            return render('/wakaba.login.mako')
        c.currentTag = ''
        c.allowTags = True
        c.PostAction = '~'
        return self.showPosts(threadFilter=meta.Session.query(Post).options(eagerload('file')).filter(Post.parentid==-1), tempid=tempid, page=int(page), board='~')

    def GetMyThreads(self, page=0, tempid=''):
        c.currentURL = '/@/'
        if not self.userInst.isAuthorized():
            return render('/wakaba.login.mako')
        c.currentTag = ''
        c.allowTags = True
        c.PostAction = '@'
        filter = meta.Session.query(Post).options(eagerload('file')).filter(Post.uid_number==self.userInst.uidNumber())
        return self.showPosts(threadFilter=filter, tempid=tempid, page=int(page), board='@')
        

    def GetThread(self, post, tempid):
        c.currentURL = request.path_info + '/'
        if c.currentURL == '/': 
           c.currentURL = ''
        if not self.userInst.isAuthorized():
           return render('/wakaba.login.mako')

        c.currentTag = ''
        c.allowTags = False
        
        ThePost = meta.Session.query(Post).options(eagerload('file')).filter(Post.id==post).first()
        if not ThePost:
            c.errorText = "No such post exist."
            return render('/wakaba.error.mako')
                            
        if ThePost.parentid != -1:
           filter = meta.Session.query(Post).options(eagerload('file')).filter(Post.id==ThePost.parentid)
           c.PostAction = ThePost.parentid
        else:
           filter = meta.Session.query(Post).options(eagerload('file')).filter(Post.id==post)
           c.PostAction = ThePost.id

        return self.showPosts(threadFilter=filter, tempid=tempid, page=0, board='')

    def GetBoard(self, board, tempid, page=0):
        c.currentURL = request.path_info.decode('utf-8') + '/'
        if c.currentURL == '//':
           c.currentURL = '/~/'
        if not self.userInst.isAuthorized():
           return render('/wakaba.login.mako')
        c.PostAction = board
        
        c.currentTag = board
        c.allowTags = True
        
        return self.showPosts(threadFilter=self.buildFilter(board), tempid=tempid, page=int(page), board=board)

    def PostReply(self, post):
        c.currentURL = request.path_info + '/'
        if not self.userInst.isAuthorized():
           return render('/wakaba.login.mako')
        return self.processPost(postid=post)

    def PostThread(self, board):
        c.currentURL = request.path_info + '/'
        if not self.userInst.isAuthorized():
           return render('/wakaba.login.mako')
        return self.processPost(board=board)
            
    def register(self,invite):
        if 'invite' not in session:
            invite_q = meta.Session.query(Invite).filter(Invite.invite==invite).first()
            if invite_q:
                meta.Session.delete(invite_q)
                meta.Session.commit()
                session['invite'] = invite
                session.save()
            else:
                c.currentURL = '/'
                return render('/wakaba.login.mako')
        key = request.POST.get('key','')
        key2 = request.POST.get('key2','')
        if key:
            if len(key)>=24 and key == key2:
               uid = hashlib.sha512(key + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
               user = User()
               user.uid = uid
               meta.Session.save(user)
               meta.Session.commit()
               del session['invite']
               self.login(user)
               redirect_to('/')
        return render('/wakaba.register.mako')
    def oekakiDraw(self,url):
        c.currentURL = request.path_info + '/'
        if not self.userInst.isAuthorized():
           return render('/wakaba.login.mako')
        c.url = url
        c.uploadPathWeb = uploadPathWeb
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
        if request.POST.get('oekaki_painter','shiNormal') == 'shiNormal':
            oekaki.type = 'Shi normal'
            c.oekakiToolString = 'normal';
        else:
            oekaki.type = 'Shi pro'
            c.oekakiToolString = 'pro'
        oekaki.uid_number = session['uid_number']
        oekaki.path = ''        
        oekaki.source = 0
        if isNumber(url) and enablePicLoading:
           post = meta.Session.query(Post).filter(Post.id==url).one()
           if post.picid:
              pic = meta.Session.query(Picture).filter(Picture.id==post.picid).first()
              if pic and pic.width:
                 oekaki.source = post.id
                 c.canvas = pic.path
                 c.width  = pic.width
                 c.height = pic.height
        meta.Session.save(oekaki)
        meta.Session.commit()
        return render('/spainter.mako')
    def oekakiSave(self, environ, start_response, url, tempid):
        start_response('200 OK', [('Content-Type','text/plain'),('Content-Length','2')])
        oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
        cl = int(request.environ['CONTENT_LENGTH'])
        if oekaki and cl:
           id = request.environ['wsgi.input'].read(1)
           if id == 'S':
              headerLength = int(request.environ['wsgi.input'].read(8))
              header = request.environ['wsgi.input'].read(headerLength)
              bodyLength = int(request.environ['wsgi.input'].read(8))
              request.environ['wsgi.input'].read(2)
              body = request.environ['wsgi.input'].read(bodyLength)
              headers = header.split('&')
              type = headers[0].split('=')[1]
              time = headers[1].split('=')[1]
              localFilePath = os.path.join(uploadPath, tempid + '.' + type)
              localFile = open(localFilePath,'wb')
              localFile.write(body)
              localFile.close()
              oekaki.time = time
              oekaki.path = tempid + '.' + type
              meta.Session.commit()
        return ['ok']
    def DeletePost(self, post):
        if not self.userInst.isAuthorized():
           return render('/wakaba.login.mako')
        fileonly = 'fileonly' in request.POST
        for i in request.POST:
            if re.compile("^\d+$").match(request.POST[i]):
                self.processDelete(request.POST[i],fileonly)
        return redirect_to(str('/%s' % post.encode('utf-8')))
    def processDelete(self, postid, fileonly=False, checkOwnage=True):
        p = meta.Session.query(Post).get(postid)
        if p:
            if checkOwnage and not (p.uid_number == self.userInst.uidNumber() or self.userInst.canDeleteAllPosts()):
                # print some error stuff here
                return
            if p.parentid == -1 and not fileonly:
                for post in meta.Session.query(Post).filter(Post.parentid==p.id).all():
                    self.processDelete(postid=post.id,checkOwnage=False)
            pic = meta.Session.query(Picture).filter(Picture.id==p.picid).first()
            if pic and meta.Session.query(Post).filter(Post.picid==p.picid).count() == 1:
                filePath = os.path.join(uploadPath,pic.path)
                thumPath = os.path.join(uploadPath,pic.thumpath)
                if os.path.isfile(filePath): os.unlink(filePath)
                ext = meta.Session.query(Extension).filter(Extension.id==pic.extid).first()
                if not ext.path:
                    if os.path.isfile(thumPath): os.unlink(thumPath)
                meta.Session.delete(pic)
            if fileonly: p.picid = None
            else: meta.Session.delete(p)
        meta.Session.commit()
    def showProfile(self):
        if not self.userInst.isAuthorized():
            return render('/wakaba.login.mako')
        self.initEnvironment()
        c.templates = ['wakaba']
        c.styles    = ['photon']
        c.profileChanged = False
        if request.POST:
            template = request.POST.get('template',self.userInst.template())
            if template in c.templates:
                self.userInst.template(template)
            style = request.POST.get('style',self.userInst.style())
            if style in c.styles:
                self.userInst.style(style)
            threadsPerPage = request.POST.get('threadsPerPage',self.userInst.threadsPerPage())
            if isNumber(threadsPerPage) and (0 < int(threadsPerPage) < 100):
                self.userInst.threadsPerPage(threadsPerPage)
            repliesPerThread = request.POST.get('repliesPerThread',self.userInst.repliesPerThread())
            if isNumber(repliesPerThread) and (0 < int(repliesPerThread) < 100):
                self.userInst.repliesPerThread(repliesPerThread)
            c.profileChanged = True
            meta.Session.commit()
        c.userInst = self.userInst
        return render('/wakaba.profile.mako')
    def UnknownAction(self):      
        c.errorText = "Excuse me, WTF are you?"
        return render('/wakaba.error.mako')

