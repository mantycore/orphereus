# -*- coding: utf-8 -*-
<%page args="thread, post"/>

    %if post.sage:
        <img src="${g.OPT.staticPathWeb}images/sage.png" alt="Sage"/>
    %endif
    %if post.title:
        <span class="replytitle">${post.title}</span>
    %endif

     ${h.modTime(post, c.userInst, g.OPT.secureTime)}
     <a href="${h.url_for('thread', post=post.id)}">#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a>

    &nbsp;
    %if post.file:
        <br />
        <span class="filesize">${_('File:')}
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
        <br />
        <a href="${g.OPT.filesPathWeb + h.modLink(post.file.path, c.userInst.secid())}"
        %if post.file.extension.newWindow:
            target="_blank"
        %endif
        >

        <%include file="std.thumbnail.mako" args="post=post" />
        </a>
    %elif post.picid == -1:
        <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
        <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb"  alt="Removed" />
    %endif
    <blockquote class="postbody" id="postBQId${post.id}">
        ${h.modMessage(post.message, c.userInst, g.OPT.secureText)}
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

