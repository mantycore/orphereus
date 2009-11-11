<%page args="post,attachment"/>

%if post.spoiler:
    <img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb" alt="Spoiler"/>
%elif 'image' in attachment.extension.type:
    <img src="${g.OPT.filesPathWeb +  h.modLink(attachment.thumpath, c.userInst.secid())}" width="${attachment.thwidth}" height="${attachment.thheight}" class="thumb"  alt="Preview" />
%else:
    <img src="${g.OPT.staticPathWeb +  h.modLink(attachment.thumpath, c.userInst.secid())}" width="${attachment.thwidth}" height="${attachment.thheight}" class="thumb"  alt="Preview" />
%endif
