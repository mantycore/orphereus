# -*- coding: utf-8 -*-
<%page args="thread"/>

<%include file="wakaba.fileBlock.mako" args="post=thread,opPost=True,searchMode=None" />

<a name="i${thread.id}"></a>
&nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src="${g.OPT.staticPathWeb}images/delete.gif" border="0" alt="x" title="Delete"/></a>
%if thread.pinned:
<img src="${g.OPT.staticPathWeb}images/pin.png" border="0" alt="!" title="Pinned"/>
%endif
<span style="display:none" class="delete">
%if thread.uidNumber == c.uidNumber or c.enableAllPostDeletion:
    <input type="checkbox" name="delete-${thread.id}" value="${thread.id}" />
    %if g.OPT.enableFinalAnonymity and not c.userInst.Anonymous and thread.uidNumber == c.uidNumber:
        <a href="${h.url_for('anonymize', post=thread.id)}">[FA]</a>
    %endif
%endif
${h.threadPanelCallback(thread, c.userInst)}
&nbsp;
</span>
%if thread.title:
    <span class="filetitle">${thread.title}</span>
%endif


<span \
%if getattr(thread, 'mixed', False):
 style="color: red;" \
%elif thread.pinned:
 style="font-weight: bold;" \
%endif
> \
${h.tsFormat(thread.date)} \
</span>
<span class="reflink"> \
%if c.board:
    <a href="${h.postUrl(thread.id, thread.id)}">#${g.OPT.secondaryIndex and thread.secondaryIndex or thread.id}</a> \
%else:
    <a href="javascript:insert('&gt;&gt;${thread.id}')">#${g.OPT.secondaryIndex and thread.secondaryIndex or thread.id}</a> \
%endif
%if g.OPT.hlAnonymizedPosts and thread.uidNumber == 0:
    <b class="signature"><a href="${h.url_for('static', page='finalAnonymity')}" target="_blank">FA</a></b> \
%endif
</span>

%if not(c.minimalRender):
    &nbsp;
    ${_('Posted in')}:
%for t in thread.tags:
    <a href="${h.url_for('boardBase', board=t.tag)}" \
    %if t.options:
        title="${t.options.comment}" \
    %endif
    >/${t.tag}/</a>
%endfor


&nbsp;
%if not c.userInst.Anonymous or g.OPT.allowAnonProfile:
    %if not thread.hidden:
        [<a href="${h.url_for('ajHideThread', post=thread.id, redirect='board', realm=(not c.board and c.tagLine) and c.tagLine or unicode(c.currentRealm), page=c.curPage)}">${_('Hide')}</a>]
    %else:
        [<a href="${h.url_for('ajShowThread', post=thread.id, redirect=c.board and 'board' or 'thread', realm=unicode(c.currentRealm), page=c.curPage)}">${_('Unhide')}</a>]
    %endif
%endif

%if c.currentUserCanPost:
    %if thread.attachments and thread.attachments[0] and thread.attachments[0].attachedFile.width:
        [<a href="${h.url_for('oekakiDraw', url=thread.id, selfy=c.userInst.oekUseSelfy and '+selfy' or '-selfy', anim=c.userInst.oekUseAnim and '+anim' or '-anim', tool=c.userInst.oekUsePro and 'shiPro' or 'shiNormal')}">${_('Draw')}</a>]
    %endif
    [<a href="${h.url_for('thread', post=thread.id)}">${_('Reply')}</a>]
%else:
    [<a href="${h.postUrl(thread.id, thread.id)}">${_('Read')}</a>]
%endif

${h.threadInfoCallback(thread, c.userInst)}
%endif

<blockquote class="postbody" id="quickReplyNode${thread.id}">
    %if (c.count > 1) and thread.messageShort and c.userInst.hideLongComments:
        ${thread.messageShort}
        <br />
        ${_('Comment is too long.')} <a href="${h.postUrl(thread.id, thread.id)}" onclick="getFullText(event,${thread.id},${thread.id});" class="expandPost">${_('Full version')}</a>
    %else:
        ${thread.message}
    %endif
    %if thread.messageInfo:
        <div>${thread.messageInfo}</div>
    %endif
    %if thread.attachments and thread.attachments[0] and thread.attachments[0].attachedFile.animpath:
        [<a href="${h.url_for('viewAnimation', source=thread.id)}" target="_blank">${_('Animation')}</a>]
    %endif
</blockquote>
%if 'omittedPosts' in dir(thread) and thread.omittedPosts:
    <span class="omittedposts"><span>${ungettext('%s post omitted.', '%s posts omitted.', thread.omittedPosts) % thread.omittedPosts}</span> <a href="#">${_('Expand thread')}</a> </span>
%endif
