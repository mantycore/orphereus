# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

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
    <input type="hidden" name="task" value="post" />
    <input type="hidden" name="akane" />   
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
                %if c.returnToThread:
                    <label><input type="radio" name="gb2" value="board" />board</label>
                    <label><input type="radio" name="gb2" value="thread" checked="checked" />${_('thread')}</label>
                %else:
                    <label><input type="radio" name="gb2" value="board" checked="checked" />${_('board')}</label>
                    <label><input type="radio" name="gb2" value="thread" />thread</label>                
                %endif
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
            
<td class="adminMenu">
<div id="smallFont">
${_('On this board:')}
<ul class="nomargin">
<li>${_('Minimal picture size')}: ${c.boardOptions.minPicSize}<sup>2</sup></li>
<li>${_('Maximal file size')}: ${'%.2f' % (c.boardOptions.maxFileSize / 1024.0)} Kbytes</li>
<li>${_('Thumbnail size')}: ${c.boardOptions.thumbSize}<sup>2</sup></li>
<li>${_('Images')}:  ${not c.boardOptions.images and _('not') or ''} allowed</li>
<li>${_('Imageless threads')}:  ${not c.boardOptions.imagelessThread and _('not') or ''} ${_('allowed')}</li>
<li>${_('Imageless posts')}:  ${not c.boardOptions.imagelessPost and _('not') or ''} ${_('allowed')}</li>
<li>${_('Spoiler alerts')}:  ${not c.boardOptions.enableSpoilers and _('not') or ''} ${_('allowed')}</li>
<li>${_('Enabled extensions')}:  ${c.extLine}</li>
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
                <img src="${c.uploadPathWeb + c.oekaki.path}">
            </div>
%endif     
</div>
</div>
<hr />
<form action="/${c.PostAction}/delete" method="post">
<input type="hidden" name="tagLine" value="${c.tagLine}">
%for thread in c.threads:
    <div id="thread-${thread.id}">
        %if thread.file:
        <span class="filesize">
            <a target="_blank" href="${c.uploadPathWeb + thread.file.path}">${thread.file.path}</a>
            (<em>${thread.file.size}, ${thread.file.width}x${thread.file.height}</em>)
        </span>
        <span class="thumbnailmsg"></span><br />                       
        <a target="_blank" href="${c.uploadPathWeb + thread.file.path}">
        %if thread.spoiler:
            <img src="/images/spoiler.png" class="thumb"/>
        %else:
            <img src="${c.uploadPathWeb + thread.file.thumpath}" width="${thread.file.thwidth}" height="${thread.file.thheight}" class="thumb" />             
        %endif                             
        </a>
        %elif thread.picid == -1:
            <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
            <img src='/images/picDeleted.png' class="thumb" >             
        %endif
        <a name="i${thread.id}"></a>
        <label>
            &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src='/images/delete.gif' border=0 alt='x' title='Delete'></a>
            <div style="display:none" class="delete">       
            %if thread.uidNumber == c.uidNumber or c.enableAllPostDeletion:
                <input type="checkbox" name="delete-${thread.id}" value="${thread.id}" />
            %endif
            %if c.isAdmin:
                <a href="/holySynod/manageUsers/editAttempt/${thread.id}">[User]</a>                   
            %endif
            </div>
            <span class="filetitle">${thread.title}</span>  
            <span class="postername"></span>
            ${thread.date}
        </label>
        <span class="reflink">
            %if c.board:
                <a href="/${thread.id}#i${thread.id}" onClick="doQuickReplyForm(event,${thread.id},${thread.id})">#${thread.id}</a>
            %else:
                <a href="javascript:insert('&gt;&gt;${thread.id}')" onClick="doQuickReplyForm(event,${thread.id},${thread.id})">#${thread.id}</a>
            %endif 
        </span>
        &nbsp;
        <span class="replytothread">
            [<a href="/${thread.id}">Reply</a>]
            %if thread.file and thread.file.width:
             [<a href="/${thread.id}/oekakiDraw">Draw</a>]
            %endif
        </span>
        <span>${_('Posted in')} :
        %for t in thread.tags:
            <a href="/${t.tag}/">/${t.tag}/</a> 
        %endfor
        </span>
        <blockquote class="postbody" id="quickReplyNode${thread.id}">
            %if (c.count > 1) and thread.messageShort and c.userInst.hideLongComments():
                ${thread.messageShort}
                <br />
                ${_('Comment is too long.')} <a href="/${thread.id}#i${thread.id}" onClick="getFullText(event,${thread.id},${thread.id});">${_('Full version')}</a>
            %else:
                ${thread.message}
            %endif
        </blockquote>
        %if thread.omittedPosts:
            <span class="omittedposts">${_('%s posts omitted.') % thread.omittedPosts } </span>
        %endif
        %for p in thread.Replies:
            <table id="quickReplyNode${p.id}">
                <tbody>
                    <tr>
                        <td class="doubledash">&gt;&gt;</td>
                        <td class="reply" id="reply${p.id}">
                            <a name="i${p.id}"></a>
                            <label>
                                &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src='/images/delete.gif' border=0 alt='x' title='Del'></a>
                                <div style="display:none" class="delete">
                                %if p.uidNumber == c.uidNumber or c.enableAllPostDeletion:
                                    <input type="checkbox" name="delete-${p.id}" value="${p.id}" />
                                %endif                              
                                %if c.isAdmin:
                                    <a href="/holySynod/manageUsers/editAttempt/${p.id}">[User]</a>                                    
                                %endif
                                </div>
                                %if p.sage:
                                    <img src='/images/sage.png'>
                                %endif
                                <span class="replytitle">${p.title}</span>
                                <span class="commentpostername"></span>
                                ${p.date}
                            </label>
                            <span class="reflink">
                                %if c.board:
                                    <a href="/${thread.id}#i${p.id}" onClick="doQuickReplyForm(event,${thread.id},${p.id})">#${p.id}</a>
                                %else:
                                    <a href="javascript:insert('&gt;&gt;${p.id}')" onClick="doQuickReplyForm(event,${thread.id},${p.id})">#${p.id}</a>
                                %endif 
                                %if p.file and p.file.width:
                                    [<a href="/${p.id}/oekakiDraw">Draw</a>]
                                %endif                                                      
                            </span>
                            &nbsp;  
                            %if p.file:
                                <br /><span class="filesize">${_('File:')} 
                                <a target="_blank" href="${c.uploadPathWeb + p.file.path}">${p.file.path}</a> 
                                (<em>${p.file.size}, ${p.file.width}x${p.file.height}</em>)</span>
                                <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
                                <a target="_blank" href="${c.uploadPathWeb + p.file.path}">
                                %if p.spoiler:
                                    <img src="/images/spoiler.png" class="thumb"/>
                                %else:     
                                    <img src="${c.uploadPathWeb + p.file.thumpath}" width="${p.file.thwidth}" height="${p.file.thheight}" class="thumb" />
                                %endif 
                                </a>
                                %elif p.picid == -1:
                                    <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
                                    <img src='/images/picDeleted.png' class="thumb">                                    
                                %endif
                            <blockquote class="postbody" id="postBQId${p.id}">
                                %if (c.count > 1) and p.messageShort and c.userInst.hideLongComments():
                                    ${p.messageShort}
                                    <br />
                                    ${_('Comment is too long.')} <a href="/${thread.id}#i${p.id}"' onClick="getFullText(event,${thread.id},${p.id});">${_('Full version')}</a>
                                %else:
                                    ${p.message}
                                %endif                            
                            </blockquote> 
                        </td>
                    </tr>
                </tbody>
            </table>
        %endfor
    </div>
    <br clear="left" />
    <hr />
%endfor
<table class="userdelete">
    <tbody>
        <tr><td> 
            <input type="hidden" name="task" value="delete" />Delete post [<label><input type="checkbox" name="fileonly" value="on" />Only file</label>]
            <br />
            <input value="Delete" type="submit" />
        </td></tr>
    </tbody>
</table>
</form>
%if c.pages:
<table border="1"><tbody><tr><td>
%if not c.showPagesPartial:
    %for pg in range(0,c.pages):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor
%else:
    %for pg in range(0,4):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor
    ...
    %if c.leftPage and c.rightPage:
        %for pg in range(c.leftPage,c.rightPage):
            %if pg == c.page:
                [${pg}]
            %else:
                [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
            %endif
        %endfor    
        ...
    %endif
    %for pg in range(c.pages-5,c.pages):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor    
%endif
</td></tr></tbody></table>
%endif
<br clear="all" />
