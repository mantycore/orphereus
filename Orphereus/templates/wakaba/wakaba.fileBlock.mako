<%page args="post,opPost,searchMode,newsMode"/>

%if post.attachments:
%if len(post.attachments) > 1:
  %for attachmentId, attachment in enumerate(post.attachments):
    %if attachment.attachedFile and attachment.attachedFile.id != 0:
      <div class="file_thread">
      %if not newsMode:
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
                %if g.OPT.memcachedPosts and not(c.userInst.isAdmin()):
                    [<a href="${h.url_for('oekakiDraw', url=post.id, sourceId = attachmentId)}">${_('Draw')}</a>]
                %elif c.currentUserCanPost:
                    [<a href="${h.url_for('oekakiDraw', url=post.id, selfy=c.userInst.oekUseSelfy and '+selfy' or '-selfy', anim=c.userInst.oekUseAnim and '+anim' or '-anim', tool=c.userInst.oekUsePro and 'shiPro' or 'shiNormal', sourceId = attachmentId)}">${_('Draw')}</a>]
                %endif

                %if attachment.animpath:
                  [<a href="${h.url_for('viewAnimation', source=post.id, animid = attachmentId)}" target="_blank">${_('Animation')}</a>]
                %endif
            %else:
                ${_('Kbytes')}</em>)
            %endif

            %if attachment.attachedFile.pictureInfo or attachment.relationInfo:
              <a class="linkWithPopup" id="link-${attachment.postId}-${attachment.fileId}">[?]</a>
            %endif
          </span><br />

          <span class="filesize" style="display: none">
          <!-- Quick & dirty JS fix -->
          <em>${attachment.attachedFile.width}x${attachment.attachedFile.height}</em>
          </span>
      %endif

          <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}" \
          %if attachment.attachedFile.extension.newWindow:
              target="_blank" \
          %endif
          >

          <%include file="wakaba.thumbnail.mako" args="post=post,attachment=attachment,attachmentId=attachmentId" />

          </a>

          %if attachment.attachedFile.pictureInfo or attachment.relationInfo:
          <div id="filePopup-link-${attachment.postId}-${attachment.fileId}" class="popupDiv highlight reply" style="display: none;">
            %if attachment.attachedFile.pictureInfo:
              ${attachment.attachedFile.pictureInfo}
            %endif
            %if attachment.relationInfo:
              ${attachment.relationInfo}
            %endif
          </div>
          %endif
            </div>
    %else:
          <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb" alt="Removed"/>
    %endif
  %endfor
<br style="clear: both" />
%else: # len(attachments) == 1
  %for attachmentId, attachment in enumerate(post.attachments):
    %if attachment.attachedFile and attachment.attachedFile.id != 0:
        %if not newsMode:
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
                %if g.OPT.memcachedPosts and not(c.userInst.isAdmin()):
                    [<a href="${h.url_for('oekakiDraw', url=post.id, sourceId = attachmentId)}">${_('Draw')}</a>]
                %elif c.currentUserCanPost:
                    [<a href="${h.url_for('oekakiDraw', url=post.id, selfy=c.userInst.oekUseSelfy and '+selfy' or '-selfy', anim=c.userInst.oekUseAnim and '+anim' or '-anim', tool=c.userInst.oekUsePro and 'shiPro' or 'shiNormal', sourceId = attachmentId)}">${_('Draw')}</a>]
                %endif

                %if attachment.animpath:
                  [<a href="${h.url_for('viewAnimation', source=post.id, animid = attachmentId)}" target="_blank">${_('Animation')}</a>]
                %endif
            %else:
                ${_('Kbytes')}</em>)
            %endif
            </span>

          %if not opPost:
            <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span>
          %endif

          <br />
        %endif

          <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}"
          %if attachment.attachedFile.extension.newWindow:
              target="_blank"
          %endif
          >

          <%include file="wakaba.thumbnail.mako" args="post=post,attachment=attachment,attachmentId=attachmentId" />

          </a>
    %else:
          <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
          <img src="${g.OPT.staticPathWeb}images/picDeleted.png" class="thumb" alt="Removed"/>
    %endif
  %endfor
%endif
%endif
