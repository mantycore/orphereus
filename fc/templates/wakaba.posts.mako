# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="postarea">
    <form id="postform" action="/${c.PostAction}" method="post" enctype="multipart/form-data">
    <input type="hidden" name="task" value="post" />
    <input type="hidden" name="akane" />
    <table>
        <tbody>
        <tr id="tremail">
            <td class="postblock">Sage</td>
            <td><input type="checkbox" name="sage" /></td>
        </tr>
        <tr id="trsubject">
            <td class="postblock">Title</td>
            <td>
                <input type="text" name="title" size="35" />
                <input type="submit" value="Post" />
            </td>
        </tr>
        <tr id="trcomment">
            <td class="postblock">Text</td>
            <td><textarea name="message" cols="60" rows="6"></textarea></td>
        </tr>
        %if c.oekaki:
            <tr id="trfile">
                <td colspan=2><input type="hidden" name="tempid" value="${c.oekaki.tempid}"><img src="${c.uploadPathWeb + c.oekaki.path}"></td>
            </tr>
        %else:
            <tr id="trfile">
                <td class="postblock">File</td>
                <td><input type="file" name="file" size="35" /></td>
            </tr>
        %endif
        <tr id="trgetback">
            <td class="postblock">Gb2 :</td>
            <td>
                <label><input type="radio" name="gb2" value="board" />board</label>
                <label>
                    <input type="radio" name="gb2" value="thread" checked="checked" /> 
                    thread
                </label>
            </td>
        </tr>
        </tbody>
    </table>
    </form>
</div>
<hr />
<form>
%for thread in c.threads:
    <div id="thread-${thread.id}">
        %if thread.file:
        <span class="filesize">
            <a target="_blank" href="${c.uploadPathWeb + thread.file.path}">${thread.file.path}</a>
            (<em>${thread.file.size}, ${thread.file.width}x${thread.file.height}</em>)
        </span>
        <span class="thumbnailmsg"></span><br />
        <a target="_blank" href="${c.uploadPathWeb + thread.file.path}">
            <img src="${c.uploadPathWeb + thread.file.thumpath}" class="thumb" />
        </a>
        %endif
        <a name="i${thread.id}"></a>
        <label>
            %if thread.uid_number == c.uid_number:
                <input type="checkbox" name="delete" value="${thread.id}" />
            %endif
            <span class="filetitle">${thread.title}</span>  
            <span class="postername"></span>
            ${thread.date}
        </label>
        <span class="reflink">
            <a href="/${thread.id}#i${thread.id}">#${thread.id}</a>
        </span>
        &nbsp;
        <span class="replytothread">
            [<a href="/${thread.id}#i${thread.id}">Reply</a>]
            %if thread.file and thread.file.width:
             [<a href="/${thread.id}/oekakiDraw">Draw</a>]
            %endif
        </span>
        <blockquote class="postbody">
            ${thread.message}
        </blockquote>
        %if thread.omittedPosts:
            <span class="omittedposts">${thread.omittedPosts} posts omitted.</span>
        %endif
        %for p in thread.Replies:
            <table>
                <tbody>
                    <tr>
                        <td class="doubledash">&gt;&gt;</td>
                        <td class="reply" id="reply${p.id}">
                            <a name="i${p.id}"></a>
                            <label>
                                %if p.uid_number == c.uid_number:
                                    <input type="checkbox" name="delete" value="${p.id}" />
                                %else:
                                    <input type="checkbox" name="delete" disabled/>
                                %endif
                                %if p.sage:
                                    <img src='/images/sage.png'>
                                %endif
                                <span class="replytitle">${p.title}</span>
                                <span class="commentpostername"></span>
                                ${p.date}
                            </label>
                            <span class="reflink">
                                <a href="/${p.id}#i${p.id}">#${p.id}</a>
                                %if p.file and p.file.width:
                                    [<a href="/${p.id}/oekakiDraw">Draw</a>]
                                %endif                                                      
                            </span>
                            &nbsp;  
                            %if p.file:
                                <br /><span class="filesize">File: 
                                <a target="_blank" href="${c.uploadPathWeb + p.file.path}">${p.file.path}</a> 
                                (<em>${p.file.size}, ${p.file.width}x${p.file.height}</em>)</span>
                                <span class="thumbnailmsg"></span><br />
                                <a target="_blank" href="${c.uploadPathWeb + p.file.path}">
                                <img src="${c.uploadPathWeb + p.file.thumpath}" width="${p.file.thwidth}" height="${p.file.thheight}" class="thumb" /></a>
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
