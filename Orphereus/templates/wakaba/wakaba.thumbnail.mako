<%page args="post,attachment"/>

%if h.overrideThumbnail(post, c, attachment):
  <%include file="${'wakaba.thumbnail.%s.mako' % c.currentThumbnailHook.thumbnailForPost(post, c, attachment)}" args="post=post,attachment=attachment" />
%else:
  %if attachment.spoiler:
      <img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb" alt="Spoiler"/>
  %elif 'image' in attachment.attachedFile.extension.type:
      <img src="${g.OPT.filesPathWeb +  h.modLink(attachment.attachedFile.thumpath, c.userInst.secid())}" width="${attachment.attachedFile.thwidth}" height="${attachment.attachedFile.thheight}" class="thumb"  alt="Preview" />
  %else:
      <img src="${g.OPT.staticPathWeb +  h.modLink(attachment.attachedFile.thumpath, c.userInst.secid())}" width="${attachment.attachedFile.thwidth}" height="${attachment.attachedFile.thheight}" class="thumb"  alt="Preview" />
  %endif
%endif
