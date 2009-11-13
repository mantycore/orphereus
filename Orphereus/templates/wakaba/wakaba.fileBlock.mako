<%page args="post,opPost,searchMode"/>

%if post.attachments:
%if len(post.attachments) > 1:
  %for attachment in post.attachments:
    %if attachment.attachedFile.id != 0:
      <div class="file_thread">
            <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
            %if attachment.attachedFile.extension.newWindow:
                target="_blank" \
            %endif
            > \
            ${h.modLink(attachment.attachedFile.path, c.userInst.secid(), True)}</a>
               <br />
          <span class="fileinfo">
            (<em>${'%.2f' % (attachment.attachedFile.size / 1024.0)} \
            %if attachment.attachedFile.width and attachment.attachedFile.height:
                ${_('Kbytes')}, ${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>)
            %else:
                ${_('Kbytes')}</em>)
            %endif
          </span><br />

          <span class="filesize" style="display: none">
          <!-- Quick & dirty JS fix -->
          <em>${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>
          </span>
          <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}"
          %if attachment.attachedFile.extension.newWindow:
              target="_blank"
          %endif
          >
                  
          <%include file="wakaba.thumbnail.mako" args="post=post,attachment=attachment" />
    
               </a>
            </div>
    %else:
          <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb" alt="Removed"/>
    %endif
  %endfor
<br style="clear: both" />
%else: # len(attachments) == 1
  %for attachment in post.attachments:
    %if attachment.attachedFile.id != 0:
          %if not opPost:
          <!-- <br /> -->
          %endif
          <span class="filesize">
          %if not opPost:
          ${_('File:')}
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
          <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span>
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
