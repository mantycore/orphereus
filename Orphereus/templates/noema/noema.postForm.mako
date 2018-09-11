# -*- coding: utf-8 -*-

<!-- FIXME: back link -->

<div id="newPost">
    <a class="pseudo-link" id="newPostToggle">
    %if c.board:
    создать новый тред ↓
    %else:
    ответить ↓
    %endif
    </a>
    <form class="post-content" action="${c.PostAction}" method="post" enctype="multipart/form-data" onsubmit="return checkForTagNames();">
        <div class="help">
            <a href="${h.url_for('static', page='markup')}" target="_blank" title="Язык разметки и другие плюшки">Пояснения</a>
        </div>
        <div>
            <label for="postSubject">Тема:</label>
            <input type="text" id="postSubject" name="title">
            
            %if c.board:
            <label for="postBoards">Доски:</label>
            <input type="text" id="postBoards" name="tags" value="${c.tagList}">
            %else:
            <input type="checkbox" name="sage" id="postSage">
            <label for="postSage">сажа</label>
            %endif
            
            <input type="hidden" name="newThread" value="${c.board and 'yes' or ''}">
            <input type="hidden" name="tagsChecked" value="">
            <input type="hidden" name="tagLine" value="${c.tagLine}">
            <input type="hidden" name="curPage" value="${c.curPage}">
            <input type="hidden" name="goto" value="${c.userInst.defaultGoto}">
            %if c.boardOptions.images and c.oekaki:
            <input type="hidden" name="tempid" value="${c.oekaki.tempid}">
            %endif

            <input type="hidden" id="additionalFilesCount" value="${c.boardOptions.allowedAdditionalFiles}">
            <input type="hidden" id="createdRows" value="0">
            <input type="hidden" id="nextRowId" value="0">
        </div>
        <div>
            <textarea name="message"></textarea>
        </div>
        <div>
            <table class="attaches">
                <tr id="fileRow0">
                    <td><label for="firstAttach">Файл:</label></td>
                    <td>
                        %if c.boardOptions.images and not c.oekaki:
                        <input type="file" name="file_0" id="firstAttach">
                        %if c.boardOptions.enableSpoilers:
                        <input type="checkbox" class="spoiler-toggle" name="spoiler_0">
                        <label>спойлер</label>
                        %endif
                        %elif c.oekaki:
                        <a href="${g.OPT.filesPathWeb + h.modLink(c.oekaki.path, c.userInst.secid())}" target="_blank">последнее оекаки</a>
                        %endif
                    </td>
                    %if c.boardOptions.allowedAdditionalFiles > 0:
                    <td><button class="add-file">ещё</button></td>
                    %endif
                </tr>
            </table>
        </div>
        <div>
            <input type="submit" value="Вот так">
        </div>
    </form>
    
    %if c.boardOptions.images and not c.oekaki:
    <form id="postOekaki" method="post" action="${h.url_for('oekakiDraw', url=c.currentRealm)}">
        <div>
            <label for="oekakiPainterSelect">Оекаки:</label>
            <select id="oekakiPainterSelect" name="oekaki_painter">
                <option value="shiNormal" ${not c.userInst.oekUsePro and 'selected="selected"' or ""}>Shi Normal</option>
                <option value="shiPro" ${c.userInst.oekUsePro and 'selected="selected"' or ""}>Shi Pro</option>
            </select>
            
            <label>Размер:</label>
            <input type="text" value="300" size="3" name="oekaki_x">
            ×
            <input type="text" value="300" size="3" name="oekaki_y">
            
            <input type="checkbox" name="selfy" ${c.userInst.oekUseSelfy and 'checked="checked"' or ""} id="oekakiSelfy">
            <label for="oekakiSelfy">Selfy</label>
            <input type="checkbox" name="animation" ${c.userInst.oekUseAnim and 'checked="checked"' or ""} id="oekakiAnimation">
            <label for="oekakiAnimation">анимация</label>
            
            <input type="hidden" name="oekaki_type" value="New">
            <input type="submit" value="Рисовать">
        </div>
    </form>
    %endif
    
    <div id="paramPlaceholderContent">
        <img alt="Загрузка..." src="${g.OPT.staticPathWeb}images/loading.gif">
    </div>
    <div id="additionalPostParameters">
        <div id="paramPlaceholder">
        &nbsp;
        </div>
        <button id="submitAgainButton">Давай</button>
        <button id="cancelPostingButton">Отменить</button>
    </div>
</div>

<br class="clearer">

