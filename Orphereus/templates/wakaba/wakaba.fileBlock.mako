<%page args="post,opPost,searchMode"/>

%if post.attachments:
%if len(post.attachments) > 1:
  %if opPost:
    %for attachment in post.attachments:
    %if attachment.attachedFile.id != 0:
    <span class="filesize">
        <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
        %if attachment.attachedFile.extension.newWindow:
            target="_blank" \
        %endif
        >
        ${h.modLink(attachment.attachedFile.path, c.userInst.secid(), True)}</a>

        (<em>${'%.2f' % (attachment.attachedFile.size / 1024.0)} \
        %if attachment.attachedFile.width and attachment.attachedFile.height:
            ${_('Kbytes')}, ${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>)
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

    <%include file="wakaba.thumbnail.mako" args="post=post,attachment=attachment" />

    </a>
    %else:
        <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
        <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb" alt="Removed"/>
    %endif
    %endfor
  %elif not searchMode:
      %for attachment in post.attachments:
      %if attachment.attachedFile.id != 0:
          <br /><span class="filesize">${_('File:')}
          <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
          %if attachment.attachedFile.extension.newWindow:
              target="_blank" \
          %endif
          > \
          ${h.modLink(attachment.attachedFile.path, c.userInst.secid(), True)}</a>

          (<em>${'%.2f' % (attachment.attachedFile.size / 1024.0)} \
          %if attachment.attachedFile.width and attachment.attachedFile.height:
              ${_('Kbytes')}, ${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>)</span>
          %else:
              ${_('Kbytes')}</em>)</span>
          %endif

          <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
          <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
          %if attachment.attachedFile.extension.newWindow:
              target="_blank" \
          %endif
          >

          <%include file="wakaba.thumbnail.mako" args="post=post,attachment=attachment" />
          </a>
      %else:
          <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
          <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb"  alt="Removed" />
      %endif
      %endfor
  %else:
    %for attachment in post.attachments:
    %if attachment.attachedFile.id != 0:
        <br /><span class="filesize">${_('File:')}

        <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}"
        %if attachment.attachedFile.extension.newWindow:
            target="_blank"
        %endif
        >
        ${h.modLink(attachment.attachedFile.path, c.userInst.secid(), True)}</a>
        (<em>${'%.2f' % (attachment.attachedFile.size / 1024.0)} Kbytes, ${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>)</span>
        <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
        <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}"
        %if attachment.attachedFile.extension.newWindow:
            target="_blank"
        %endif
        >

        <%include file="wakaba.thumbnail.mako" args="post=pt,attachment=attachment" />

        </a>
        %else:
            <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
            <img src='${g.OPT.staticPathWeb}images/picDeleted.png' class="thumb">
        %endif
      %endfor
  %endif
%else: # len(attachments) == 1
  %for attachment in post.attachments:
  %if attachment.attachedFile.id != 0:
        %if not opPost:
        <br />
        %endif
        <span class="filesize">
        %if not opPost:
        ${_('Filez:')}
        %endif

          <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
          %if attachment.attachedFile.extension.newWindow:
              target="_blank" \
          %endif
          > \
          ${h.modLink(attachment.attachedFile.path, c.userInst.secid(), True)}</a>

          (<em>${'%.2f' % (attachment.attachedFile.size / 1024.0)} \
          %if attachment.attachedFile.width and attachment.attachedFile.height:
              ${_('Kbytes')}, ${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>)
          %else:
              ${_('Kbytes')}</em>)
          %endif
          </span>

        %if not opPost:
        <span class="thumbnailmsg">${_('This is resized copy. Click it to view original imagez')}</span>
        %endif

        <br />
        <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}"
        %if attachment.attachedFile.extension.newWindow:
            target="_blank"
        %endif
        >

        <%include file="wakaba.thumbnail.mako" args="post=post,attachment=attachment" />

        </a>
  %else:
        <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
        <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb" alt="Removed"/>
  %endif
  %endfor
%endif
%endif
