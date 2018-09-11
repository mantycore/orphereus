# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

%if c.currentUserCanPost:
<%include file="noema.postForm.mako" />
%endif

<form action="${h.url_for('process', board=c.currentRealm)}" method="post">
    <div><input type="hidden" name="tagLine" value="${c.tagLine}"></div>
    %for thread in c.threads:
    <div
            %if getattr(thread, 'mixed', False):
            class="thread mixed"
            %else:
            class="thread"
            %endif
            id="thread${thread.id}"
            data-id="${thread.id}">
        <%include file="noema.postOp.mako" args="thread=thread"/>
        <%include file="noema.replies.mako" args="thread=thread"/>
    </div>
    %endfor
    <div id="controlPanel">
        <div>
            <input type="hidden" name="task" value="delete">
            <input name="task_delete" type="submit"
                value="Удалить отмеченные посты">
        </div>
        %if c.isAdmin:
        <div>
            <label for="deleteReason">Причина:</label>
            <input type="text" name="reason" id="deleteReason">
        </div>
        %endif
        <div>
            <input type="checkbox" id="deleteFilesOnly"
                name="fileonly" value="on">
            <label for="deleteFilesOnly">только файлы</label>
        </div>
    </div>
</form>

<%include file="noema.paginator.mako" args="routeName='board', kwargDict={'board' : c.board}" />

<div class="post-wrapper" id="replyWrapper">
    <form id="reply" action="/1" method="post" enctype="multipart/form-data">
        <div><textarea name="message"></textarea></div>
        <div class="options">
            <span class="option">
                <label for="replyFile">Файл:</label>
                <input type="file" id="replyFile" name="file_0">
            </span>
            <span class="option">
                <input type="checkbox" id="replySage" name="sage">
                <label for="replySage">сажа</label>
            </span>
        </div>
        <div id="replyActions">
            <input type="submit" value="Вот так">
            <button id="replyCancel">Не надо</button>
            <input type="hidden" name="tagLine" value="">
            <input type="hidden" name="curPage" value="">
            <input type="hidden" name="task" value="post">
            <input type="hidden" name="title" value="">
            <input type="hidden" name="goto" value="${c.userInst.defaultGoto}">
        </div>
    </form>
</div>

<div class="post-wrapper" id="hoverWrapper"></div>

