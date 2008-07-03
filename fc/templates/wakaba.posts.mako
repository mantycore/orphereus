# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

%if not c.board:
    <div class="theader">${_('Reply')}</div>
%endif    

<div class="postarea">
    <table>
        <tbody>
    <form id="postform" action="/${c.PostAction}" method="post" enctype="multipart/form-data">
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
            <td><textarea name="message" cols="60" rows="6"></textarea></td>
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
            <tr id="trfile">
                <td colspan=2 class="theader"><input type="hidden" name="tempid" value="${c.oekaki.tempid}">
                <img src="${c.uploadPathWeb + c.oekaki.path}">
                </td>
            </tr>
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
</div>
<hr />
<form action="/${c.PostAction}/delete" method="post">
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
        %endif
        <a name="i${thread.id}"></a>
        <label>
			&nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src='/images/delete.gif' border=0 alt='x' title='Del'></a>
			<div style="display:none" class="delete">		
            %if thread.uidNumber == c.uidNumber or c.enableAllPostDeletion:
                <input type="checkbox" name="delete-${thread.id}" value="${thread.id}" />
            %endif
			</div>
            <span class="filetitle">${thread.title}</span>  
            <span class="postername"></span>
            ${thread.date}
        </label>
        <span class="reflink">
			%if c.board:
				<a href="/${thread.id}#i${thread.id}">#${thread.id}</a>
			%else:
				<a href="javascript:insert('&gt;&gt;${thread.id}')">#${thread.id}</a>
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
        <blockquote class="postbody">
            ${thread.message}
        </blockquote>
        %if thread.omittedPosts:
            <span class="omittedposts">${_('%s posts omitted.') % thread.omittedPosts } </span>
        %endif
        %for p in thread.Replies:
            <table>
                <tbody>
                    <tr>
                        <td class="doubledash">&gt;&gt;</td>
                        <td class="reply" id="reply${p.id}">
                            <a name="${p.id}"></a>
                            <label>
								&nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src='/images/delete.gif' border=0 alt='x' title='Del'></a>
								<div style="display:none" class="delete">
                                %if p.uidNumber == c.uidNumber or c.enableAllPostDeletion:
                                    <input type="checkbox" name="delete-${p.id}" value="${p.id}" />
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
									<a href="/${thread.id}#i${p.id}">#${p.id}</a>
								%else:
									<a href="javascript:insert('&gt;&gt;${p.id}')">#${p.id}</a>
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
                                <span class="thumbnailmsg">This is resized copy. Click it to view original image</span><br />
                                <a target="_blank" href="${c.uploadPathWeb + p.file.path}">
                                %if p.spoiler:
                                    <img src="/images/spoiler.png" class="thumb"/>
                                %else:
                                    <img src="${c.uploadPathWeb + p.file.thumpath}" width="${p.file.thwidth}" height="${p.file.thheight}" class="thumb" />
                                %endif
                                </a>
                            %endif
                            <blockquote class="postbody">
                                ${p.message}
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
    %for pg in range(0,c.pages):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor
</td></tr></tbody></table>
%endif
<br clear="all" />
