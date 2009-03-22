# -*- coding: utf-8 -*-
<%page args="thread"/>

%if thread.file:
<span class="filesize">
    <a href="${g.OPT.filesPathWeb + h.modLink(thread.file.path, c.userInst.secid())}"
    %if thread.file.extension.newWindow:
        target="_blank"
    %endif
    >
    ${h.modLink(thread.file.path, c.userInst.secid(), True)}</a>

    (<em>${'%.2f' % (thread.file.size / 1024.0)}
    %if thread.file.width and thread.file.height:
        ${_('Kbytes')}, ${thread.file.width}x${thread.file.height}</em>)
    %else:
        ${_('Kbytes')}</em>)
    %endif
</span>

<br />
<a href="${g.OPT.filesPathWeb + h.modLink(thread.file.path, c.userInst.secid())}"
%if thread.file.extension.newWindow:
    target="_blank"
%endif
>

<%include file="wakaba.thumbnail.mako" args="post=thread" />

</a>
%elif thread.picid == -1:
    <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
    <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb" alt="Removed"/>
%endif
<a name="i${thread.id}"></a>
&nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src="${g.OPT.staticPathWeb}images/delete.gif" border="0" alt="x" title="Delete"/></a>
<span style="display:none" class="delete">
%if thread.uidNumber == c.uidNumber or c.enableAllPostDeletion:
    <input type="checkbox" name="delete-${thread.id}" value="${thread.id}" />
    %if g.OPT.enableFinalAnonymity and not c.userInst.Anonymous and thread.uidNumber == c.uidNumber:
        <a href="${h.url_for('anonymize', post=thread.id)}">[FA]</a>
    %endif
%endif
%if c.userInst.isAdmin() and c.userInst.canManageUsers():
    <a href="${h.url_for('hsUserEditAttempt', pid=thread.id)}">[User]</a>
%endif
%if c.userInst.isAdmin() and c.userInst.canManageMappings():
    <a href="${h.url_for('hsMappings', act='show', id=thread.id)}">[Tags]</a>
%endif
&nbsp;
</span>
%if thread.title:
    <span class="filetitle">${thread.title}</span>
%endif


<span
%if getattr(thread, 'mixed', False):
 style="color: red;"
%endif
>
${h.modTime(thread, c.userInst, g.OPT.secureTime)}
</span>
<span class="reflink">
%if c.board:
    <a href="${h.postUrl(thread.id, thread.id)}">#${g.OPT.secondaryIndex and thread.secondaryIndex or thread.id}</a>
%else:
    <a href="javascript:insert('&gt;&gt;${thread.id}')">#${g.OPT.secondaryIndex and thread.secondaryIndex or thread.id}</a>
%endif
%if g.OPT.hlAnonymizedPosts and thread.uidNumber == 0:
    <b class="signature"><a href="${h.url_for('static', page='finalAnonymity')}" target="_blank">FA</a></b>
%endif
</span>

    &nbsp;
    ${_('Posted in')}:
%for t in thread.tags:
    <a href="${h.url_for('boardBase', board=t.tag)}"
    %if t.options:
        title="${t.options.comment}"
    %endif
    >/${t.tag}/</a>
%endfor


&nbsp;
%if not c.userInst.Anonymous or g.OPT.allowAnonProfile:
    %if not thread.hidden:
        [<a href="${h.url_for('ajHideThread', post=thread.id, redirect=u'%s%s' % ((not c.board and c.tagLine) and c.tagLine or unicode(c.PostAction), c.curPage and '/page/'+str(c.curPage) or '') )}">${_('Hide')}</a>]
    %else:
        [<a href="${h.url_for('ajShowThread', post=thread.id, redirect=u'%s%s' % (unicode(c.PostAction), c.curPage and '/page/'+str(c.curPage) or '') )}">${_('Unhide')}</a>]
    %endif
%endif

%if c.currentUserCanPost:
    %if thread.file and thread.file.width:
        [<a href="${h.url_for('oekakiDraw', url=thread.id, selfy=c.userInst.oekUseSelfy() and '+selfy' or '-selfy', anim=c.userInst.oekUseAnim() and '+anim' or '-anim', tool=c.userInst.oekUsePro() and 'shiPro' or 'shiNormal')}">Draw</a>]
    %endif
    [<a href="${h.url_for('thread', post=thread.id)}">${_('Reply')}</a>]
%else:
    [<a href="${h.postUrl(thread.id, thread.id)}">${_('Read')}</a>]
%endif

<blockquote class="postbody" id="quickReplyNode${thread.id}">
    %if (c.count > 1) and thread.messageShort and c.userInst.hideLongComments():
        ${h.modMessage(thread.messageShort, c.userInst, g.OPT.secureText)}
        <br />
        ${_('Comment is too long.')} <a href="${h.postUrl(thread.id, thread.id)}" onclick="getFullText(event,${thread.id},${thread.id});" class="expandPost">${_('Full version')}</a>
    %else:
        ${h.modMessage(thread.message, c.userInst, g.OPT.secureText)}
    %endif
    %if thread.messageInfo:
        ${thread.messageInfo}
    %endif
    %if thread.file and thread.file.animpath:
        [<a href="${h.url_for('viewAnimation', source=thread.id)}" target="_blank">${_('Animation')}</a>]
    %endif
</blockquote>
%if 'omittedPosts' in dir(thread) and thread.omittedPosts:
    <span class="omittedposts"><span>${_('%s posts omitted.') % thread.omittedPosts }</span> <a href="#">${_('Expand thread')}</a> </span>
%endif
