<%page args="post,opPost,searchMode,newsMode"/>

%if post.attachments:
<div
        %if len(post.attachments) == 1:
        class="post-files single"
        %else:
        class="post-files multiple"
        %endif
        >
    %for i, attachment in enumerate(post.attachments):
    <div class="file">
        %if len(post.attachments) > 1:
        <div class="file-info">
            <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}">${attachment.attachedFile.path.split('.')[-1]}</a>,
            ${'%.2f' % (attachment.attachedFile.size / 1024.0)} К
            %if attachment.attachedFile.width and attachment.attachedFile.height:
            — ${attachment.attachedFile.width}×${attachment.attachedFile.height}
            %endif
        </div>
        %endif
        <a class="file-tile" href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}"
                %if attachment.attachedFile.extension.newWindow:
                target="_blank"
                %endif
                %if attachment.attachedFile.width:
                data-width="${attachment.attachedFile.width}"
                %endif
                %if attachment.attachedFile.height:
                data-height="${attachment.attachedFile.height}"
                %endif
                >
            <%include file="noema.thumbnail.mako" args="post=post,attachment=attachment,attachmentId=i" />
        </a>
    </div>
    %endfor
</div>
%endif

