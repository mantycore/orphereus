# -*- coding: utf-8 -*-
<%page args="thread, post"/>

%if post.sage:
    <img src="${g.OPT.staticPathWeb}images/sage.png" alt="Sage"/>
%endif
%if post.title:
    <span class="replytitle">${post.title}</span>
%endif

 ${h.tsFormat(post.date)}
 <a href="${h.url_for('thread', post=post.id)}">#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a>

&nbsp;
%if post.attachments:
%for attachment in post.attachments:
%if attachment.attachedFile.id != 0:
    <br />
    <span class="filesize">${_('File:')}
    <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
    %if attachment.attachedFile.extension.newWindow:
        target="_blank" \
    %endif
    >
    ${h.modLink(attachment.attachedFile.path, c.userInst.secid(), True)}</a>

    (<em>${'%.2f' % (attachment.attachedFile.size / 1024.0)} \
    %if attachment.attachedFile.width and attachment.attachedFile.height:
        ${_('Kbytes')}, ${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>) \
    %else:
        ${_('Kbytes')}</em>)
    %endif

    </span>
    <br />
    <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
    %if attachment.attachedFile.extension.newWindow:
        target="_blank" \
    %endif
    >

    <%include file="std.thumbnail.mako" args="post=post,attachment=attachment" />
    </a>
%else:
    <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
    <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb"  alt="Removed" />
%endif
%endfor
%endif
<blockquote class="postbody" id="postBQId${post.id}">
    ${post.message}
    %if post.messageInfo:
        ${post.messageInfo}
    %endif
    %if post.file and post.file.animpath:
        [<a href="${h.url_for('viewAnimation', source=post.id)}" target="_blank">${_('Animation')}</a>]
    %endif
</blockquote>
%if post.replies != None:
    <i>${_('Replies: %s') % post.replies }</i>
%endif

