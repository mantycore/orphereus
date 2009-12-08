# -*- coding: utf-8 -*-
<%page args="thread"/>
%if thread.attachments and (len(thread.attachments) == 1):
<%include file="wakaba.fileBlock.mako" args="post=thread,opPost=True,searchMode=None,newsMode=None" />
%endif

<a name="i${thread.id}"></a>
&nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src="${g.OPT.staticPathWeb}images/delete.gif" border="0" alt="x" title="Delete"/></a>
%if thread.pinned:
<img src="${g.OPT.staticPathWeb}images/pin.png" border="0" alt="!" title="Pinned"/>
%endif
<span style="display:none" class="delete">
%if thread.uidNumber == c.uidNumber or c.enableAllPostDeletion:
    <input type="checkbox" name="delete-${thread.id}" value="${thread.id}" />
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
${h.threadHeaderCallback(thread, c.userInst)}
</span>

%if not(c.minimalRender):
    &nbsp;
    ${_('Posted in')}:
%for t in thread.tags:
    <a href="${h.url_for('boardBase', board=t.tag)}" \
    title="${t.comment}" \
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
    [<a href="${h.url_for('thread', post=thread.id)}">${_('Reply')}</a>]
%else:
    [<a href="${h.postUrl(thread.id, thread.id)}">${_('Read')}</a>]
%endif

${h.threadInfoCallback(thread, c.userInst)}<br />
%endif

%if thread.attachments and (len(thread.attachments) > 1):
<%include file="wakaba.fileBlock.mako" args="post=thread,opPost=True,searchMode=None,newsMode=None" />
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
    %if thread.attachments and len(thread.attachments) == 1:
      <%include file="wakaba.fileInfoSingle.mako" args="attachment=thread.attachments[0]" />
    %endif
</blockquote>
%if 'omittedPosts' in dir(thread) and thread.omittedPosts:
    <span class="omittedposts"><span>${ungettext('%s post omitted.', '%s posts omitted.', thread.omittedPosts) % thread.omittedPosts}</span> <a href="${h.postUrl(thread.id, thread.id)}">${_('Expand thread')}</a> </span>
%endif
