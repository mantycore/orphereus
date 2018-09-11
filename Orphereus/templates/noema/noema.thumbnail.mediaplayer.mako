<%page args="post,attachment,attachmentId"/>
</a>

<table class="thumb">
<tr><td>

<a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
%if attachment.attachedFile.extension.newWindow:
    target="_blank" \
%endif
>
<img src="${g.OPT.staticPathWeb +  h.modLink(attachment.attachedFile.thumpath, c.userInst.secid())}" width="${attachment.attachedFile.thwidth}" height="${attachment.attachedFile.thheight}" class="thumb"  alt="Preview" />
</a>

<br />
</td></tr><tr><td>
<object type="application/x-shockwave-flash"
        data="${g.OPT.staticPathWeb}player.swf?file=${g.OPT.filesPathWeb +  h.modLink(attachment.attachedFile.path, c.userInst.secid())}"
        width="150" height="15">
  <param name="movie" value="${g.OPT.staticPathWeb}player.swf?file=${g.OPT.filesPathWeb +  h.modLink(attachment.attachedFile.path, c.userInst.secid())}" />
</object>
</td></tr>
</table>

<a href="#" style="display: none">


