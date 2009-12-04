<%page args="attachment"/>

%if attachment.attachedFile.pictureInfo or attachment.relationInfo:
<!-- hr/ -->
<div>
  %if attachment.attachedFile.pictureInfo:
    ${attachment.attachedFile.pictureInfo}
  %endif
  %if attachment.relationInfo:
    ${attachment.relationInfo}
  %endif
</div>
%endif
