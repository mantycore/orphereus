import logging
import datetime

from paste.deploy import appconfig
from pylons import config
from Orphereus.model import *
import Orphereus.oldmodel as OM
import hashlib
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper

from Orphereus.config.environment import load_environment
import Orphereus.lib.app_globals as app_globals

from sqlalchemy import create_engine

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s: %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)
log.info("Migration")

userOptMembers = ["threadsPerPage",
"repliesPerThread",
"style",
"template",
"homeExclude",
"hideThreads",
"bantime",
"banreason",
"banDate",
"useFrame",
"hideLongComments",
"useAjax",
"expandImages",
"maxExpandWidth",
"maxExpandHeight",
"mixOldThreads",
"useTitleCollapse",
"hlOwnPosts",
"invertSortingMode",
"defaultGoto",
"oekUseSelfy",
"oekUseAnim",
"oekUsePro",
"isAdmin",
"canDeleteAllPosts",
"canMakeInvite",
"canChangeRights",
"canChangeSettings",
"canManageBoards",
"canManageUsers",
"canManageExtensions",
"canManageMappings",
"canRunMaintenance",
"lang",
"cLang", ]

tagOptMembers = ["comment",
"sectionId",
"persistent",
"service",
"imagelessThread",
"imagelessPost",
"images",
"maxFileSize",
"minPicSize",
"thumbSize",
"enableSpoilers",
"canDeleteOwnThreads",
"specialRules",
"selfModeration",
"showInOverview",
"bumplimit", ]

banMembers = ["ip",
"mask",
"type",
"reason",
"date",
"period",
"enabled", ]

extMembers = ["path",
"thwidth",
"thheight",
"ext",
"type",
"enabled",
"newWindow",
]

oekakiMembers = ["tempid",
"time",
"uidNumber",
"type",
"path",
"timeStamp",
"selfy",
"animPath",
]

postMembers = ["id",
"secondaryIndex",
"parentid",
"message",
"messageShort",
"messageRaw",
"title",
"sage",
"uidNumber",
"date",
"bumpDate",
"replyCount",
"removemd5",
"ip",
"pinned",
]

def copyMembers(membersList, source, target):
    for member in membersList:
        setattr(target, member, getattr(source, member))

def migrate(targetConfig, sourceModelUrl):
    """Place any commands to setup Orphereus here"""
    conf = appconfig('config:' + os.path.abspath(targetConfig))
    load_environment(conf.global_conf, conf.local_conf, True)

    log.info("Dropping tables")
    meta.metadata.drop_all(bind = meta.engine)
    log.info("Successfully dropped")
    log.info("Creating tables")
    meta.metadata.create_all(bind = meta.engine)
    log.info("Successfully setup")

    init_globals(meta.globj, False)

    # Classes which doesn't need migration: FCCaptcha, LoginTracker
    log.info("=================================================================")
    log.info("Initializing old model")
    engine = create_engine(sourceModelUrl)
    OM.init_model(engine)
    log.info("-----------------------------------------------------------------")

    log.info("=================================================================")
    log.info("Migrating users...")
    log.info("-----------------------------------------------------------------")
    oldUsers = OM.User.query.all()
    log.info("Users count: %d" % len(oldUsers))

    for user in oldUsers:
        log.info("Creating [%d] %s" % (user.uidNumber, user.uid))
        newUser = User(user.uid, None)
        meta.Session.add(newUser)
        meta.Session.commit()
        newUser.uidNumber = user.uidNumber
        if user.options:
            log.info("Copying options for %d..." % newUser.uidNumber)
            newUser.options = UserOptions()
            copyMembers(userOptMembers, user.options, newUser.options)
            meta.Session.add(newUser.options)
        else:
            log.error("No options for user %d" % user.uidNumber)
        meta.Session.commit()
        log.info("Creating filters for %d..." % newUser.uidNumber)
        for filter in user.filters:
            newUser.addFilter(filter.filter)

    log.info("=================================================================")
    log.info("Migrating tags...")
    log.info("-----------------------------------------------------------------")
    oldTags = OM.Tag.query.all()
    log.info("Tags count: %d" % len(oldTags))

    for tag in oldTags:
        log.info("Creating /%s/" % (tag.tag,))
        newTag = Tag(tag.tag)
        newTag.replyCount = tag.replyCount
        newTag.threadCount = tag.threadCount
        if tag.options:
            log.info("Copying options for /%s/..." % tag.tag)
            copyMembers(tagOptMembers, tag.options, newTag.options)
        else:
            log.error("No options for tag /%s/" % tag.tag)
        meta.Session.add(newTag)
        meta.Session.commit()

    log.info("=================================================================")
    log.info("Migrating settings...")
    log.info("-----------------------------------------------------------------")
    oldSettings = OM.Setting.query.all()
    log.info("Settings count: %d" % len(oldSettings))

    for setting in oldSettings:
        log.info("Creating %s=%s" % (setting.name, setting.value))
        Setting.create(setting.name, setting.value)

    log.info("=================================================================")
    log.info("Migrating bans...")
    log.info("-----------------------------------------------------------------")
    oldBans = OM.Ban.query.all()
    log.info("Bans count: %d" % len(oldBans))

    for ban in oldBans:
        log.info("Creating ban for %d" % (ban.ip,))
        newBan = Ban(0, 0, 0, '', datetime.datetime.now(), 0, False)
        copyMembers(banMembers, ban, newBan)
        meta.Session.add(newBan)
        meta.Session.commit()

    log.info("=================================================================")
    log.info("Migrating extensions...")
    log.info("-----------------------------------------------------------------")
    oldExtensions = OM.Extension.query.all()
    log.info("Extensions count: %d" % len(oldExtensions))

    for ext in oldExtensions:
        log.info("Creating .%s" % (ext.ext,))
        newExt = Extension("", False, False, "", "", 0, 0)
        copyMembers(extMembers, ext, newExt)
        meta.Session.add(newExt)
        meta.Session.commit()

    log.info("=================================================================")
    log.info("Migrating invites...")
    log.info("-----------------------------------------------------------------")
    oldInvites = OM.Invite.query.all()
    log.info("Invites count: %d" % len(oldInvites))

    for invite in oldInvites:
        log.info("Creating %s" % (invite.invite,))
        newInvite = Invite(invite.invite)
        meta.Session.add(newInvite)
        meta.Session.commit()
        newInvite.date = invite.date
        newInvite.id = invite.id
        meta.Session.commit()

    log.info("=================================================================")
    log.info("Migrating logs...")
    log.info("-----------------------------------------------------------------")
    oldLog = OM.LogEntry.query
    log.info("Log records count: %d" % oldLog.count())

    for record in oldLog:
        log.info("Copying %d/%s" % (record.id, str(record.date),))
        newRecord = LogEntry(record.uidNumber, record.event, record.entry)
        meta.Session.add(newRecord)
        meta.Session.commit()
        newRecord.date = record.date
        newRecord.id = record.id
        meta.Session.commit()

    log.info("=================================================================")
    log.info("Migrating oekaki temporary IDs...")
    log.info("-----------------------------------------------------------------")
    oldOek = OM.Oekaki.query.all()
    log.info("Oekaki temporary IDs count: %d" % len(oldOek))

    for oek in oldOek:
        log.info("Copying %s" % (oek.tempid,))
        newOek = Oekaki('', 1, '', 0, 0, False)
        copyMembers(oekakiMembers, oek, newOek)
        newOek.sourcePicIdx = 0
        newOek.sourcePost = oek.source
        meta.Session.commit()

    def migratePosts(posts):
        for post in posts:
            log.info("Copying %d" % (post.id,))
            newPost = Post()
            copyMembers(postMembers, post, newPost)
            meta.Session.add(newPost)
            meta.Session.commit()
            newPost.id = post.id
            meta.Session.commit()
            # Picture
            pic = post.file
            if pic:
                log.info("%d has picture, copying..." % (post.id,))
                extension = Extension.getExtension(pic.extension.ext)
                additionalInfo = None
                relInfo = None
                if post.messageInfo:
                    if "ID3" in post.messageInfo:
                        additionalInfo = post.messageInfo
                    else:
                        relInfo = post.messageInfo
                newPic = Picture(pic.path,
                                     pic.thumpath,
                                     pic.size,
                                     [pic.width, pic.height, pic.thwidth, pic.thheight],
                                     extension.id,
                                     pic.md5,
                                     additionalInfo,
                                     )
                assoc = PictureAssociation(post.spoiler, relInfo, pic.animpath)
                meta.Session.add(assoc)
                assoc.attachedFile = newPic
                newPost.attachments.append(assoc)
            meta.Session.commit()
            # Tags
            if not newPost.parentid:
                log.info("Attaching tags to %d..." % (post.id,))
                for tag in post.tags:
                    log.info("Attaching /%s/ to %d..." % (tag.tag, post.id,))
                    newPost.tags.append(Tag.getTag(tag.tag))
                meta.Session.commit()
                # Usertags
                utags = OM.UserTag.query.filter(OM.UserTag.posts.any(OM.Post.id == post.id)).all()
                if utags:
                    log.info("Attaching usertags to %d..." % (post.id,))
                    for utag in utags:
                        log.info("Attaching /$%s/ to %d (userId == %d)..." % (utag.tag, post.id, utag.userId))
                        ns = meta.globj.pluginsDict['usertags'].pnamespace
                        newUtag = ns.UserTag(utag.tag, utag.comment, utag.userId)
                        newUtag.posts.append(newPost)
                        meta.Session.add(newUtag)
                    meta.Session.commit()

    log.info("=================================================================")
    log.info("Migrating OP-posts...")
    log.info("-----------------------------------------------------------------")
    oldOps = OM.Post.query.filter(OM.Post.parentid == None)
    log.info("Op posts count: %d" % oldOps.count())
    migratePosts(oldOps)

    log.info("=================================================================")
    log.info("Migrating replies...")
    log.info("-----------------------------------------------------------------")
    oldPosts = OM.Post.query.filter(not_(OM.Post.parentid == None))
    log.info("Replies posts count: %d" % oldPosts.count())
    migratePosts(oldPosts)

# migrate(NEWCONFIG, oldDBUrl)
# All tables from target database will be dropped!
migrate("development.ini", "mysql://root:@127.0.0.1/orphieold?use_unicode=0&charset=utf8")
