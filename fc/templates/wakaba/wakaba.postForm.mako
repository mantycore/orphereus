# -*- coding: utf-8 -*-

%if not c.board and c.tagLine:
    [<a href="${h.url_for('boardBase', board=c.tagLine)}">${_('Back')}</a>]
    <hr/>
%endif

<div class="theader">
<a style="cursor:pointer; display: block;" onclick="toggle_div('newThreadPlaceholder');">
%if not c.board:
    ${_('Reply')}
%else:
    ${_('New thread')}
%endif
</a>
</div>

<div id="newThreadPlaceholder" ${c.userInst.useTitleCollapse() and 'style="display:none"' or ""}>
<div class="postarea" id="postFormDiv">

<table>
<tr>
<td>
    <form id="postform" action="/${c.PostAction}" method="post" enctype="multipart/form-data">
    <input type="hidden" name="tagLine" value="${c.tagLine}" />
    <input type="hidden" name="curPage" value="${c.curPage}" />
    <input type="hidden" name="task" value="post" />
    %if c.boardOptions.images and c.oekaki:
        <input type="hidden" name="tempid" value="${c.oekaki.tempid}" />
    %endif
    <table>
        <tbody >
    %if not c.board:
        <tr id="trsage">
            <td class="postblock">${_('Sage')}</td>
            <td><input type="checkbox" name="sage" /></td>
        </tr>
    %endif

    %if c.boardOptions.enableSpoilers:
        <tr id="trspoiler">
            <td class="postblock">${_('Spoiler')}</td>
            <td><input type="checkbox" name="spoiler" /></td>
        </tr>
    %endif
        <tr id="trsubject">
            <td class="postblock">${_('Title')}</td>
            <td>
                <input type="text" name="title" size="35" />
                <input type="submit" value="${_('Post')}" />
            </td>
        </tr>
        <tr id="trcomment">
            <td class="postblock">${_('Text')}</td>
            <td><textarea id="replyText" name="message" cols="60" rows="6"></textarea></td>
        </tr>
        %if c.board:
            <tr id="trtags">
                <td class="postblock">${_('Boards')}</td>
                <td>
                    <input type="text" name="tags" size="35" value="${c.tagList}" />
                </td>
            </tr>
        %endif

        %if c.captcha:
            <tr id="trcaptcha">
                <td class="postblock">${_('Captcha')}</td>
                <td>
                    <img src="${h.url_for('captcha', cid=c.captcha.id)}" alt="Captcha" onclick="update_captcha(this)"/><br/>
                    <input type="text" name="captcha" size="35"/>
                </td>
            </tr>
        %endif
        %if c.userInst.Anonymous:
            <tr id="trrempass">
                <td class="postblock">${_('Password')}</td>
                <td>
                    <input type="password" name="remPass" size="35" value="${c.remPass}" />
                </td>
            </tr>
        %endif

        %if c.boardOptions.images and not c.oekaki:
            <tr id="trfile">
                <td class="postblock">${_('File')}</td>
                <td><input type="file" name="file" size="35" /></td>
            </tr>
        %endif

        <tr id="trgetback">
            <td class="postblock">${_('Go to')}</td>
            <td>
                <select name="goto">
                    %for dest in c.destinations.keys():
                      %if dest != 3 or g.OPT.allowOverview:
                          <option value="${dest}"
                          %if dest == c.userInst.defaultGoto():
                            selected="selected"
                          %endif
                          >
                          ${_(c.destinations[dest])}
                          %if dest == 1 or dest == 2:
                            (${c.tagLine}
                            %if dest == 2:
                              /page/${c.curPage}
                            %endif
                            )
                          %endif
                          </option>
                      %endif
                    %endfor
                </select>
            </td>
        </tr>
    </tbody>
    </table>
    </form>
    %if c.boardOptions.images and not c.oekaki:
            <form method="post" action="${h.url_for('oekakiDraw', url=c.PostAction)}">
                <table style="display: block;">
                <tr id="troekaki">
                   <td class="postblock">${_('Oekaki')}</td>
                   <td>
                    <select name="oekaki_painter">
                        <option value="shiNormal" ${not c.userInst.oekUsePro() and 'selected="selected"' or ""}>Shi Normal</option>
                        <option value="shiPro" ${c.userInst.oekUsePro() and 'selected="selected"' or ""}>Shi Pro</option>
                    </select>

                    ${_('Size')}:
                    <input type="text" value="300" size="3" name="oekaki_x"/>
                    &#215;
                    <input type="text" value="300" size="3" name="oekaki_y"/>

                    <label><input type="checkbox" name="selfy" ${c.userInst.oekUseSelfy() and 'checked="checked"' or ""} /> ${_('Selfy')}</label>
                    <label><input type="checkbox" name="animation" ${c.userInst.oekUseAnim() and 'checked="checked"' or ""} /> ${_('Animation')}</label>

                    <input type="hidden" value="New" name="oekaki_type"/>
                    <input type="submit" value="${_('Draw')}"/>

                    </td>
                </tr>
               </table>
            </form>
    %endif

</td>

<td class="reply" style="padding: 10px; vertical-align: top;">

%if h.templateExists(c.actuatorTest+'wakaba.postFormAdv.mako'):
    <%include file="${c.actuator+'wakaba.postFormAdv.mako'}" />
%endif

<div><a style="cursor:pointer" onclick="toggle_div('boardInfo');">
<b>${_('Board settings')}
%if c.tagLine:
<i>(${c.tagLine})</i>
%endif
</b>
</a>
</div>
<div class="smallFont" id="boardInfo" style="display:none">
<ul class="nomargin">
<li>${_('Minimum picture size')}: ${c.boardOptions.minPicSize}&#215;${c.boardOptions.minPicSize}</li>
<li>${_('Maximum file size')}: ${'%.2f' % (c.boardOptions.maxFileSize / 1024.0)} ${_('Kbytes')}</li>
<li>${_('Thumbnail size')}: ${c.boardOptions.thumbSize}&#215;${c.boardOptions.thumbSize}</li>
<li>${_('Images')}:  ${not c.boardOptions.images and _('not') or ''} ${_('allowed')}</li>
<li>${_('Imageless threads')}:  ${not c.boardOptions.imagelessThread and _('not') or ''} ${_('allowed')}</li>
<li>${_('Imageless posts')}:  ${not c.boardOptions.imagelessPost and _('not') or ''} ${_('allowed')}</li>
<li>${_('Spoiler alerts')}:  ${not c.boardOptions.enableSpoilers and _('not') or ''} ${_('allowed')}</li>
<li>${_('Op can delete thread')}:  ${c.boardOptions.canDeleteOwnThreads and _('yes') or _('no')}</li>
<li>${_('Op can moderate thread')}:  ${c.boardOptions.selfModeration and _('yes') or _('no')}</li>
</ul>
<b>${_('Additional information')}:</b>
<ul class="nomargin">
<li>${_('Enabled extensions')}:<br/>  ${c.extLine}</li>
<li>${_('Final Anonymity')}:  ${_('turned')} ${not g.OPT.enableFinalAnonymity and _('off') or _('on')}
${g.OPT.enableFinalAnonymity and g.OPT.hlAnonymizedPosts and _('(with marks)') or ''}
${g.OPT.enableFinalAnonymity and not g.OPT.hlAnonymizedPosts and _('(without marks)') or ''}
</li>
<li>${_('Board-wide prooflabels')}:  ${_('turned')} ${not g.OPT.boardWideProoflabels and _('off') or _('on')}</li>
<li>${_('IP logging')}:  ${not g.OPT.saveAnyIP and (g.OPT.allowAnonymous and _('only for anonymous') or _('disabled')) or _('for all users')}</li>
<li>${_('Invisible bumps')}:  ${not c.invisibleBumps and _('disabled') or _('enabled')}</li>
<li>${_('News site mode')}:  ${not g.OPT.newsSiteMode and _('off') or _('on')}
%if c.userInst.invertSortingMode():
${_('(but inverted in your profile)')}
%endif
</li>
<li><a href="${h.url_for('static', page='markup')}" target="_blank">${_('Markup and features')}</a></li>
</ul>
</div>
<br />
%if c.boardOptions.rulesList:
${_('Board-specific rules:')}
<ul class="nomargin">
    %for rule in c.boardOptions.rulesList:
        <li>${rule}</li>
    %endfor
</ul>
%endif
</td>

</tr>
</table>

%if c.oekaki:
            <div id="trfile" class="theader">
                <img src="${g.OPT.filesPathWeb + h.modLink(c.oekaki.path, c.userInst.secid())}" alt="Oekaki preview" />
            </div>
%endif

</div>
</div>
