# -*- coding: utf-8 -*-
<%page args="thread"/>

%if thread.file:
<span class="filesize">
    <a target="_blank" href="${g.OPT.filesPathWeb + h.modLink(thread.file.path, c.userInst.secid(), g.OPT.secureLinks)}">${h.modLink(thread.file.path, c.userInst.secid(),g.OPT.secureLinks)}</a>            
    (<em>${'%.2f' % (thread.file.size / 1024.0)} Kbytes, ${thread.file.width}x${thread.file.height}</em>)
</span>
<span class="thumbnailmsg"></span><br />                       
<a target="_blank" href="${g.OPT.filesPathWeb + h.modLink(thread.file.path, c.userInst.secid(), g.OPT.secureLinks)}">
%if thread.spoiler:
    <img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb" alt="Spoiler"/>
%elif not '..' in thread.file.thumpath:
    <img src="${g.OPT.filesPathWeb + h.modLink(thread.file.thumpath, c.userInst.secid(),g.OPT.secureLinks)}" width="${thread.file.thwidth}" height="${thread.file.thheight}" class="thumb"  alt="Preview" />             
%else:
    <img src="${g.OPT.staticPathWeb+thread.file.thumpath}" width="${thread.file.thwidth}" height="${thread.file.thheight}" class="thumb" alt="Preview"/>             
%endif   
</a>
%elif thread.picid == -1:
    <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
    <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb" alt="Removed"/>             
%endif
<a name="i${thread.id}"></a>
<label>
    &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src="${g.OPT.staticPathWeb}images/delete.gif" border="0" alt="x" title="Delete"/></a>
    <span style="display:none" class="delete">       
    %if thread.uidNumber == c.uidNumber or c.enableAllPostDeletion:
        <input type="checkbox" name="delete-${thread.id}" value="${thread.id}" />
        %if g.OPT.enableFinalAnonymity:
            <a href="/${thread.id}/anonymize">[FA]</a>
        %endif
    %endif
    %if c.isAdmin:
        <a href="/holySynod/manageUsers/editAttempt/${thread.id}">[User]</a>
        <a href="/holySynod/manageMappings/show/${thread.id}">[Tags]</a>                     
    %endif
    </span>
    <span class="filetitle">${thread.title}</span>
</label>

    <span 
    %if getattr(thread, 'mixed', False):
     style="color: red;"
    %endif
    >
    ${h.modTime(thread, c.userInst, g.OPT.secureTime)}
    </span>
    <span class="reflink">
    %if c.board:
        <a href="/${thread.id}#i${thread.id}" ${c.canPost and """onClick="doQuickReplyForm(event,%s,%s)" """ % (thread.id,thread.id) or ""}>#${g.OPT.secondaryIndex and thread.secondaryIndex or thread.id}</a>
    %else:
        <a href="javascript:insert('&gt;&gt;${thread.id}')" ${c.canPost and """onClick="doQuickReplyForm(event,%s,%s)" """ % (thread.id,thread.id) or ""}>#${g.OPT.secondaryIndex and thread.secondaryIndex or thread.id}</a>
    %endif
    </span> 
    %if g.OPT.hlAnonymizedPosts and thread.uidNumber == 0:
        <b class="signature"><a href="/static/finalAnonymity" target="_blank">FA</a></b>
    %endif    

    &nbsp;
    ${_('Posted in')}:
%for t in thread.tags:
    <a href="/${t.tag}/" 
    %if tag.options:
        title="${t.options.comment}"
    %endif
    >/${t.tag}/</a>
%endfor


&nbsp;
%if not c.userInst.Anonymous:
[<a href="/ajax/hideThread/${thread.id}/${c.PostAction}${c.curPage and '/page/'+str(c.curPage) or ''}">${_('Hide Thread')}</a>]
<!-- </span> -->
%endif

<!-- <span class="replytothread"> -->
    %if c.canPost:
    %if thread.file and thread.file.width:
     [<a href="/${thread.id}/oekakiDraw">Draw</a>]
    %endif
    [<a href="/${thread.id}">Reply</a>]
    %else:
    [<a href="/${thread.id}">View thread</a>]
    %endif
<!-- </span>-->


<blockquote class="postbody" id="quickReplyNode${thread.id}">
    %if (c.count > 1) and thread.messageShort and c.userInst.hideLongComments():
        ${h.modMessage(thread.messageShort, c.userInst, g.OPT.secureText)}
        <br />
        ${_('Comment is too long.')} <a href="/${thread.id}#i${thread.id}" onClick="getFullText(event,${thread.id},${thread.id});" class="expandPost">${_('Full version')}</a>
    %else:
        ${h.modMessage(thread.message, c.userInst, g.OPT.secureText)}
    %endif
</blockquote>
%if 'omittedPosts' in dir(thread) and thread.omittedPosts:
    <span class="omittedposts">${_('%s posts omitted.') % thread.omittedPosts } </span>
%endif
