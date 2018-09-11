# -*- coding: utf-8 -*-
<%page args="thread"/>


<div class="post-wrapper" id="postWrapper${thread.id}">
    <div
            %if not (c.userInst.hlOwnPosts and c.userInst.ownPost(thread)):
            class="post original-post"
            %else:
            class="post original-post own"
            %endif
            id="i${thread.id}"
            data-id="${thread.id}">
        <div class="post-head">
            <span class="post-control">
                <a class="pseudo-link" title="Управление постом" data-id="${thread.id}">×</a>
                %if c.userInst.ownPost(thread) or c.enableAllPostDeletion:
                <input type="checkbox" class="delete" 
                    name="delete-${thread.id}" value="${thread.id}">
                %endif
            </span>
            %if thread.pinned:
            <img src="${g.OPT.staticPathWeb}images/pin.png" border="0" alt="!" title="Тред прикреплён">
            %endif
            <a class="post-id" href="${h.postUrl(thread.id, thread.id)}">#${g.OPT.secondaryIndex and thread.secondaryIndex or thread.id}</a>
            <span class="post-date"> ${h.tsFormat(thread.date)}</span>
            <span class="post-action reply-action"><a href="${h.url_for('thread', post=thread.id)}">ответить</a></span>
            <span class="post-boards">
                Доски:
                %for t in thread.tags:
                <a href="${h.url_for('boardBase', board=t.tag)}" title="${t.comment}">/${t.tag}/</a>
                %endfor
            </span>
            
            %if hasattr(thread, 'hidden') and thread.hidden:
            <span class="post-action"><a href="${h.url_for('ajShowThread', post=thread.id, redirect='board', realm=unicode(c.currentRealm), page=c.curPage)}">показать</a></span>
            %else:
            <span class="post-action"><a href="${h.url_for('ajHideThread', post=thread.id, redirect='board', realm=(not c.board and c.tagLine) and c.tagLine or unicode(c.currentRealm), page=c.curPage)}">скрыть</a></span>
            %endif
            
            %if thread.attachments and (len(thread.attachments) == 1):
            %for attachment in thread.attachments:
            <span class="post-file-info">
                Файл:
                <a href="${g.OPT.filesPathWeb + h.modLink(attachment.attachedFile.path, c.userInst.secid())}">${attachment.attachedFile.path.split('.')[-1]}</a>,
                ${'%.2f' % (attachment.attachedFile.size / 1024.0)} К
                %if attachment.attachedFile.width and attachment.attachedFile.height:
                — ${attachment.attachedFile.width}×${attachment.attachedFile.height}
                %endif
            </span>
            %endfor
            %endif
            
            <!--span class="post-action"><a href="#/ololo/12">рисовать</a></span-->
        </div>
        
        %if not (hasattr(thread, 'hideFromBoards') and thread.hideFromBoards):
        %if thread.attachments:
        <%include file="noema.fileBlock.mako" args="post=thread,opPost=True,searchMode=None,newsMode=None" />
        %endif
        
        <div class="post-text">
            %if thread.title:
            <h2>${thread.title}</h2>
            %endif
            <div class="real-post-text">
                %if (c.count > 1) and thread.messageShort and c.userInst.hideLongComments:
                ${thread.messageShort}
                <a class="post-cut" href="${h.postUrl(thread.id, thread.id)}" data-id="${thread.id}">дальше →</a>
                %else:
                ${thread.message}
                %endif
                %if thread.messageInfo:
                <div>${thread.messageInfo}</div>
                %endif
                %if thread.attachments and len(thread.attachments) == 1:
                <%include file="noema.fileInfoSingle.mako" args="attachment=thread.attachments[0]" />
                %endif
            </div>
        </div>
        %endif
    </div>
</div>

%if not (hasattr(thread, 'hideFromBoards') and thread.hideFromBoards):
<div id="tail${thread.id}">
%if hasattr(thread, 'omittedPosts') and thread.omittedPosts:
    <div class="post-wrapper">
        <div class="skipped">
            %if thread.omittedPosts == 1:
            <a class="pseudo-link" data-id="${thread.id}">${thread.omittedPosts} сообщением</a> позже...
            %else:
            <a class="pseudo-link" data-id="${thread.id}">${thread.omittedPosts} сообщениями</a> позже...
            %endif
        </div>
    </div>
%endif
%endif
