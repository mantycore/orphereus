# -*- coding: utf-8 -*-
<%page args="thread, post"/>

<table id="quickReplyNode${post.id}"><tbody><tr>
<td class="doubledash">&gt;&gt;</td>
<td class="reply" id="reply${post.id}">
    <a name="i${post.id}"></a>
    &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src="${g.OPT.staticPathWeb}images/delete.gif" border="0" alt="x" title="Del" /></a>
    <span style="display:none" class="delete">
    %if post.uidNumber == c.uidNumber or (thread.selfModeratable() and c.uidNumber == thread.uidNumber) or c.enableAllPostDeletion:
        <input type="checkbox" name="delete-${post.id}" value="${post.id}" />
        %if post.uidNumber != c.uidNumber and (thread.selfModeratable() and c.uidNumber == thread.uidNumber):
        <i>${_('[REMOVABLE]')}</i>
        %endif
        %if g.OPT.enableFinalAnonymity and not c.userInst.Anonymous and post.uidNumber == c.uidNumber:
            <a href="${h.url_for('anonymize', post=post.id)}">[FA]</a>
        %endif
    %endif
    %if c.userInst.isAdmin() and c.userInst.canManageUsers():
        <a href="${h.url_for('hsUserEditAttempt', pid=post.id)}">[User]</a>
	    <a href="${h.url_for('hsIpBanAttempt', pid=thread.id)}">[Ban]</a>
    %endif
    &nbsp;
    </span>
    %if post.sage:
        <img src="${g.OPT.staticPathWeb}images/sage.png" alt="Sage"/>
    %endif
    %if post.title:
        <span class="replytitle">${post.title}</span>
    %endif

     ${post.date}

    <span class="reflink">
    %if c.board:
        <a href="${h.postUrl(thread.id, post.id)}">#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a>
    %else:
        <a href="javascript:insert('&gt;&gt;${post.id}')">#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a>
    %endif
    %if c.currentUserCanPost and post.file and post.file.width:
        [<a href="${h.url_for('oekakiDraw', url=post.id, selfy=c.userInst.oekUseSelfy() and '+selfy' or '-selfy', anim=c.userInst.oekUseAnim() and '+anim' or '-anim', tool=c.userInst.oekUsePro() and 'shiPro' or 'shiNormal')}">Draw</a>]
    %endif

    %if g.OPT.hlAnonymizedPosts and post.uidNumber == 0:
        <b class="signature"><a href="${h.url_for('static', page='finalAnonymity')}" target="_blank">FA</a></b>
    %endif
    </span>

    &nbsp;
    %if post.file:
        <br /><span class="filesize">${_('File:')}
        <a href="${g.OPT.filesPathWeb + h.modLink(post.file.path, c.userInst.secid())}"
        %if post.file.extension.newWindow:
            target="_blank"
        %endif
        >
        ${h.modLink(post.file.path, c.userInst.secid(), True)}</a>

        (<em>${'%.2f' % (post.file.size / 1024.0)}
        %if post.file.width and post.file.height:
            ${_('Kbytes')}, ${post.file.width}x${post.file.height}</em>)
        %else:
            ${_('Kbytes')}</em>)
        %endif

        </span>
        <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
        <a href="${g.OPT.filesPathWeb + h.modLink(post.file.path, c.userInst.secid())}"
        %if post.file.extension.newWindow:
            target="_blank"
        %endif
        >

        <%include file="wakaba.thumbnail.mako" args="post=post" />
        </a>
    %elif post.picid == -1:
        <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
        <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb"  alt="Removed" />
    %endif
    <blockquote class="postbody" id="postBQId${post.id}">
        %if (c.count > 1) and post.messageShort and c.userInst.hideLongComments() and getattr(thread, 'enableShortMessages', True):
            ${post.messageShort}
            <br />
            ${_('Comment is too long.')} <a href="${h.postUrl(thread.id, post.id)}" onclick="getFullText(event,${thread.id},${post.id});" class="expandPost">${_('Full version')}</a>
        %else:
            ${post.message}
        %endif
        %if post.messageInfo:
            <div>${post.messageInfo}</div>
        %endif
        %if post.file and post.file.animpath:
            [<a href="${h.url_for('viewAnimation', source=post.id)}" target="_blank">${_('Animation')}</a>]
        %endif
    </blockquote>
</td></tr></tbody></table>
