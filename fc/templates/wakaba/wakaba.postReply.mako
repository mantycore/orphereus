# -*- coding: utf-8 -*-
<%page args="thread, post"/>

<table id="quickReplyNode${post.id}">
    <tbody>
        <tr>
            <td class="doubledash">&gt;&gt;</td>
            <td class="reply" id="reply${post.id}">
                <a name="i${post.id}"></a>
                <label>
                    &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src="${g.OPT.staticPathWeb}images/delete.gif" border="0" alt="x" title="Del" /></a>
                    <span style="display:none" class="delete">
                    %if post.uidNumber == c.uidNumber or c.enableAllPostDeletion:
                        <input type="checkbox" name="delete-${post.id}" value="${post.id}" />
                        %if g.OPT.enableFinalAnonymity and not c.userInst.Anonymous:
                            <a href="/${post.id}/anonymize">[FA]</a>
                        %endif
                    %endif
                    %if c.userInst.isAdmin() and c.userInst.canManageUsers():
                        <a href="/holySynod/manageUsers/editAttempt/${post.id}">[User]</a>
                    %endif
                    </span>
                    %if post.sage:
                        <img src="${g.OPT.staticPathWeb}images/sage.png" alt="Sage"/>
                    %endif
                    <span class="replytitle">${post.title}</span>
                </label>
                     ${h.modTime(post, c.userInst, g.OPT.secureTime)}

                    <span class="reflink">
                    %if c.board:
                        <a href="/${thread.id}#i${post.id}" ${c.canPost and """onclick="doQuickReplyForm(event,%s,%s)" """ % (thread.id,post.id) or ""}>#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a>
                    %else:
                        <a href="javascript:insert('&gt;&gt;${post.id}')" ${c.canPost and """onclick="doQuickReplyForm(event,%s,%s)" """ % (thread.id,post.id) or ""}>#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a>
                    %endif
                    %if c.canPost and post.file and post.file.width:
                        [<a href="/${post.id}/oekakiDraw">Draw</a>]
                    %endif

                    %if g.OPT.hlAnonymizedPosts and post.uidNumber == 0:
                        <b class="signature"><a href="/static/finalAnonymity" target="_blank">FA</a></b>
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
                    (<em>${'%.2f' % (post.file.size / 1024.0)} Kbytes, ${post.file.width}x${post.file.height}</em>)</span>
                    <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
                    <a href="${g.OPT.filesPathWeb + h.modLink(post.file.path, c.userInst.secid())}"
                    %if post.file.extension.newWindow:
                        target="_blank"
                    %endif
                    >
                    %if post.spoiler:
                        <img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb" alt="Spoiler"/>
                    %elif 'image' in post.file.extension.type:
                        <img src="${g.OPT.filesPathWeb + h.modLink(post.file.thumpath, c.userInst.secid())}" width="${post.file.thwidth}" height="${post.file.thheight}" class="thumb" alt="Preview"/>
                    %else:
                        <img src="${g.OPT.staticPathWeb + h.modLink(post.file.thumpath, c.userInst.secid())}" width="${post.file.thwidth}" height="${post.file.thheight}" class="thumb" alt="Preview"/>
                    %endif
                    </a>
                %elif post.picid == -1:
                    <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
                    <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb"  alt="Removed" />
                %endif
                <blockquote class="postbody" id="postBQId${post.id}">
                    %if (c.count > 1) and post.messageShort and c.userInst.hideLongComments() and getattr(thread, 'enableShortMessages', True):
                        ${h.modMessage(post.messageShort, c.userInst, g.OPT.secureText)}
                        <br />
                        ${_('Comment is too long.')} <a href="/${thread.id}#i${post.id}" onclick="getFullText(event,${thread.id},${post.id});" class="expandPost">${_('Full version')}</a>
                    %else:
                        ${h.modMessage(post.message, c.userInst, g.OPT.secureText)}
                    %endif
                    %if post.messageInfo:
                        ${post.messageInfo}
                    %endif
                </blockquote>
            </td>
        </tr>
    </tbody>
</table>
