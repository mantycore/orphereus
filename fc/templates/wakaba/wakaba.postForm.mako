# -*- coding: utf-8 -*-

%if not c.board:
    <div class="theader">${_('Reply')}</div>
%else:
    <div class="theader">${_('New thread')}</div>
%endif

<div id="newThreadPlaceholder">
<div class="postarea" id="postFormDiv">
<table>
<tr>
<td>
    <table>
        <tbody >
    <form id="postform" action="/${c.PostAction}" method="post" enctype="multipart/form-data">
    <input type="hidden" name="tagLine" value="${c.tagLine}">
    <input type="hidden" name="curPage" value="${c.curPage}">
    <input type="hidden" name="task" value="post" />
    %if not c.board:
        <tr id="tremail">
            <td class="postblock">${_('Sage')}</td>
            <td><input type="checkbox" name="sage" /></td>
        </tr>
    %endif
    
    %if c.boardOptions.enableSpoilers:
        <tr id="tremail">
            <td class="postblock">${_('Spoiler')}</td>
            <td><input type="checkbox" name="spoiler" /></td>
        </tr> 
    %endif   
        <tr id="trsubject">
            <td class="postblock">${_('Title')}</td>
            <td>
                <input type="text" name="title" size="35" />
                <input type="submit" value="Post" />
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
                    <input type="text" name="tags" size="35" value='${c.tagList}' />
                </td>
            </tr>
        %endif
        <tr id="trgetback">
            <td class="postblock">${_('Go to')}</td>
            <td>
                <select name='goto'>
                    %for dest in c.destinations.keys():
                    	<option value="${dest}" 
                    	%if dest == c.userInst.defaultGoto(): 
                    		selected
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
                    %endfor    
                </select>                 
            </td>
        </tr>        
        %if c.oekaki:
            <input type="hidden" name="tempid" value="${c.oekaki.tempid}">        
            </form>            
        %elif c.boardOptions.images:
            <tr id="trfile">
                <td class="postblock">${_('File')}</td>
                <td><input type="file" name="file" size="35" /></td>
            </tr>   
         </form>       
         
        <form method="post" action="/${c.PostAction}/oekakiDraw">
            <tr id="tremail">
               <td class="postblock">${_('Oekaki')}</td>
               <td>   
     
                <select name="oekaki_painter">   
                    <option selected="selected" value="shiNormal">Shi Normal</option>      
                <option value="shiPro">Shi Pro</option>     
                </select>
                Width: 
                <input type="text" value="300" size="3" name="oekaki_x"/>                
                Height: 
                <input type="text" value="300" size="3" name="oekaki_y"/>
                <input type="hidden" value="New" name="oekaki_type"/>
                <input type="submit" value="${_('Draw Oekaki')}"/>    
                
                </td> 
            </tr>
        </form>            
        %else:
        </form>
        %endif
            </tbody>
            </table>         
            </td>
            
<td class="reply" style="padding: 10px; vertical-align: top;">
<p>Маленькое объявление:</p>
<p>jabber-сборища, результатом деятельности которых и стал этот чан, продолжают существовать.
Новый адрес: <b>aconf@conference.jabber.ru</b>, пароль - <b>oblavobla</b>. За доступом обращайтесь на rusanon@jabber.org либо 
johan.liebert@jabber.ru</p>
<div id="smallFont">
${_('On this board:')}
<ul class="nomargin">
<li>${_('Minimal picture size')}: ${c.boardOptions.minPicSize}<sup>2</sup></li>
<li>${_('Maximal file size')}: ${'%.2f' % (c.boardOptions.maxFileSize / 1024.0)} ${_('Kbytes')}</li>
<li>${_('Thumbnail size')}: ${c.boardOptions.thumbSize}<sup>2</sup></li>
<li>${_('Images')}:  ${not c.boardOptions.images and _('not') or ''} ${_('allowed')}</li>
<li>${_('Imageless threads')}:  ${not c.boardOptions.imagelessThread and _('not') or ''} ${_('allowed')}</li>
<li>${_('Imageless posts')}:  ${not c.boardOptions.imagelessPost and _('not') or ''} ${_('allowed')}</li>
<li>${_('Spoiler alerts')}:  ${not c.boardOptions.enableSpoilers and _('not') or ''} ${_('allowed')}</li>
<li>${_('Op can delete thread')}:  ${c.boardOptions.canDeleteOwnThreads and _('yes') or _('no')}</li>
<li>${_('Enabled extensions')}:<br/>  ${c.extLine}</li>
</ul>
</div>
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
                <img src="${g.OPT.filesPathWeb + c.oekaki.path}">
            </div>
%endif     
</div>
</div>

<hr />