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

                    <a target="_blank" href="${g.OPT.filesPathWeb + h.modLink(p.file.path, c.userInst.secid())}">${h.modLink(p.file.path, c.userInst.secid())}</a> 
                    (<em>${'%.2f' % (p.file.size / 1024.0)} Kbytes, ${p.file.width}x${p.file.height}</em>)</span>
                    <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
                    <a target="_blank" href="${g.OPT.filesPathWeb + h.modLink(p.file.path, c.userInst.secid())}">
                    %if p.spoiler:
                        <img src="${g.OPT.filesPathWeb}../images/spoiler.png" class="thumb"/>
                    %elif not '..' in p.file.thumpath:                                     
                        <img src="${g.OPT.filesPathWeb + h.modLink(p.file.thumpath, c.userInst.secid())}" width="${p.file.thwidth}" height="${p.file.thheight}" class="thumb" />
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