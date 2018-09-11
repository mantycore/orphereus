<%page args="post,attachment,attachmentId"/>

%if h.overrideThumbnail(post, c, attachment):
<%include file="${'noema.thumbnail.%s.mako' % c.currentThumbnailHook.thumbnailForPost(post, c, attachment)}" args="post=post,attachment=attachment,attachmentId=attachmentId" />
%else:
%if attachment.spoiler:
<img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb" alt="Спойлер!">
%elif 'image' in attachment.attachedFile.extension.type:
<img src="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.thumpath, c.userInst.secid())}" class="thumb" alt="Превью">
%else:
<img src="${g.OPT.staticPathWeb + h.modLink(attachment.attachedFile.thumpath, c.userInst.secid())}" class="thumb" alt="Превью">
%endif
%endif

