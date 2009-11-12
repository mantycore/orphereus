<%page args="post,attachment"/>

%if h.overrideThumbnail(post, c, attachment):
  <%include file="${'wakaba.thumbnail.%s.mako' % c.currentThumbnailHook.thumbnailForPost(post, c, attachment)}" args="post=post,attachment=attachment" />
%else:
  %if False and post.spoiler:
      <img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb" alt="Spoiler"/>
  %elif 'image' in attachment.extension.type:
      <img src="${g.OPT.filesPathWeb +  h.modLink(attachment.thumpath, c.userInst.secid())}" width="${attachment.thwidth}" height="${attachment.thheight}" class="thumb"  alt="Preview" />
  %else:
      <img src="${g.OPT.staticPathWeb +  h.modLink(attachment.thumpath, c.userInst.secid())}" width="${attachment.thwidth}" height="${attachment.thheight}" class="thumb"  alt="Preview" />
  %endif
%endif
