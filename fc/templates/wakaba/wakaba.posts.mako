# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<%include file="wakaba.postForm.mako" />

<form action="/${c.PostAction}/delete" method="post">
<input type="hidden" name="tagLine" value="${c.tagLine}">
%for thread in c.threads:
    <div id="thread-${thread.id}">
        %if thread.file:
        <span class="filesize">
            <a target="_blank" href="${g.OPT.filesPathWeb + c.modLink(thread.file.path, c.userInst.secid())}">${c.modLink(thread.file.path, c.userInst.secid())}</a>            
            (<em>${'%.2f' % (thread.file.size / 1024.0)} Kbytes, ${thread.file.width}x${thread.file.height}</em>)
        </span>
        <span class="thumbnailmsg"></span><br />                       
        <a target="_blank" href="${g.OPT.filesPathWeb + c.modLink(thread.file.path, c.userInst.secid())}">
        %if thread.spoiler:
            <img src="${g.OPT.filesPathWeb}../images/spoiler.png" class="thumb"/>
        %elif not '..' in thread.file.thumpath:
            <img src="${g.OPT.filesPathWeb + c.modLink(thread.file.thumpath, c.userInst.secid())}" width="${thread.file.thwidth}" height="${thread.file.thheight}" class="thumb" />             
        %else:
            <img src="${g.OPT.filesPathWeb+thread.file.thumpath}" width="${thread.file.thwidth}" height="${thread.file.thheight}" class="thumb" />             
        %endif   
        </a>
        %elif thread.picid == -1:
            <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
            <img src='${g.OPT.filesPathWeb}../images/picDeleted.png' class="thumb" >             
        %endif
        <a name="i${thread.id}"></a>
        <label>
            &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src='${g.OPT.filesPathWeb}../images/delete.gif' border=0 alt='x' title='Delete'></a>
            <div style="display:none" class="delete">       
            %if thread.uidNumber == c.uidNumber or c.enableAllPostDeletion:
                <input type="checkbox" name="delete-${thread.id}" value="${thread.id}" />
            %endif
            %if c.isAdmin:
                <a href="/holySynod/manageUsers/editAttempt/${thread.id}">[User]</a>
                <a href="/holySynod/manageMappings/${thread.id}">[Tags]</a>                     
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
                                &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src='${g.OPT.filesPathWeb}../images/delete.gif' border=0 alt='x' title='Del'></a>
                                <div style="display:none" class="delete">
                                %if p.uidNumber == c.uidNumber or c.enableAllPostDeletion:
                                    <input type="checkbox" name="delete-${p.id}" value="${p.id}" />
                                %endif                              
                                %if c.isAdmin:
                                    <a href="/holySynod/manageUsers/editAttempt/${p.id}">[User]</a>     
                                    <a href="/holySynod/manageMappings/${p.id}">[Tags]</a>
                                %endif
                                </div>
                                %if p.sage:
                                    <img src='${g.OPT.filesPathWeb}../images/sage.png'>
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

                                <a target="_blank" href="${g.OPT.filesPathWeb + c.modLink(p.file.path, c.userInst.secid())}">${c.modLink(p.file.path, c.userInst.secid())}</a> 
                                (<em>${'%.2f' % (p.file.size / 1024.0)} Kbytes, ${p.file.width}x${p.file.height}</em>)</span>
                                <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
                                <a target="_blank" href="${g.OPT.filesPathWeb + c.modLink(p.file.path, c.userInst.secid())}">
                                %if p.spoiler:
                                    <img src="${g.OPT.filesPathWeb}../images/spoiler.png" class="thumb"/>
                                %elif not '..' in p.file.thumpath:                                     
                                    <img src="${g.OPT.filesPathWeb + c.modLink(p.file.thumpath, c.userInst.secid())}" width="${p.file.thwidth}" height="${p.file.thheight}" class="thumb" />
                                %else:  
                                    <img src="${g.OPT.filesPathWeb + p.file.thumpath}" width="${p.file.thwidth}" height="${p.file.thheight}" class="thumb" />                                
                                %endif 
                                </a>
                                %elif p.picid == -1:
                                    <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
                                    <img src='${g.OPT.filesPathWeb}../images/picDeleted.png' class="thumb">                                    
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
    %for pg in range(0,2):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
        %endif
    %endfor
    %if c.leftPage and c.leftPage>2:
    ...
    %endif
    %if c.leftPage and c.rightPage:
        %for pg in range(c.leftPage,c.rightPage):
            %if pg == c.page:
                [${pg}]
            %else:
                [<a href='/${c.board}/page/${pg}/'>${pg}</a>]
            %endif
        %endfor    
        %if  c.rightPage<c.pages-2:
            ...
        %endif
    %endif   
    %for pg in range(c.pages-2,c.pages):
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
