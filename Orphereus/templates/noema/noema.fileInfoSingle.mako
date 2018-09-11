<%page args="attachment"/>

%if attachment.attachedFile and (attachment.attachedFile.pictureInfo or attachment.relationInfo):
<div class="extra-file-info">
    %if attachment.attachedFile.pictureInfo:
    ${attachment.attachedFile.pictureInfo}
    %endif
    %if attachment.relationInfo:
    ${attachment.relationInfo}
    %endif
</div>
%endif
