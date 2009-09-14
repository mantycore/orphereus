<%page args="post"/>

%if h.overrideThumbnail(post, c):
  <%include file="${'wakaba.thumbnail.%s.mako' % c.currentThumbnailHook.thumbnailForPost(post, c)}" args="post=post" />
%else:
  %if post.spoiler:
      <img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb" alt="Spoiler"/>
  %elif 'image' in post.file.extension.type:
      <img src="${g.OPT.filesPathWeb +  h.modLink(post.file.thumpath, c.userInst.secid())}" width="${post.file.thwidth}" height="${post.file.thheight}" class="thumb"  alt="Preview" />
  %else:
      <img src="${g.OPT.staticPathWeb +  h.modLink(post.file.thumpath, c.userInst.secid())}" width="${post.file.thwidth}" height="${post.file.thheight}" class="thumb"  alt="Preview" />
  %endif
%endif
