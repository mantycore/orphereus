# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<b>Found:</b> ${c.count}

<br/>
<form action="/search" method="post">
    <input type="text" name="query" size="20" value="${c.query}"/>
    <input value="Search again" type="submit" />
    [<a href="/static/markup#search" target="_blank">Help</a>]
</form>

<%include file="wakaba.paginator.mako" args="baselink='search/%s' % c.query"/>

%for pt in c.posts:
<table id="quickReplyNode${pt[0].id}">
    <tbody>
        <tr>
            <td class="doubledash">&gt;&gt;</td>
            <td class="reply" id="reply${pt[0].id}">
            	&nbsp;  
                <a name="i${pt[0].id}"></a>
                <label>
                    %if pt[0].sage:
                        <img src='${g.OPT.staticPathWeb}images/sage.png'>
                    %endif
                    <span class="replytitle">${pt[0].title}</span>
                    ${pt[0].date}
                </label>
                <span class="reflink">
                    <a href="/${pt[1].id}#i${pt[0].id}">#${g.OPT.secondaryIndex and pt[0].secondaryIndex or pt[0].id}</a>;                 
                                                 
					${_('Thread')}
					<a href="/${pt[1].id}#i${pt[1].id}">#${g.OPT.secondaryIndex and pt[1].secondaryIndex or pt[1].id}</a>
					${_('from')}:
					%for t in pt[1].tags:
					    <a href="/${t.tag}/">/${t.tag}/</a> 
					%endfor
				</span>         
				&nbsp;       
                %if pt[0].file:
                    <br /><span class="filesize">${_('File:')}     

                    <a target="_blank" href="${g.OPT.filesPathWeb + h.modLink(pt[0].file.path, c.userInst.secid(), g.OPT.secureLinks)}">${h.modLink(pt[0].file.path, c.userInst.secid(), g.OPT.secureLinks)}</a> 
                    (<em>${'%.2f' % (pt[0].file.size / 1024.0)} Kbytes, ${pt[0].file.width}x${pt[0].file.height}</em>)</span>
                    <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
                    <a target="_blank" href="${g.OPT.filesPathWeb + h.modLink(pt[0].file.path, c.userInst.secid(), g.OPT.secureLinks)}">
                    %if pt[0].spoiler:
                        <img src="${g.OPT.staticPathWeb}images/spoiler.png" class="thumb"/>
                    %elif not '..' in pt[0].file.thumpath:                                     
                        <img src="${g.OPT.filesPathWeb + h.modLink(pt[0].file.thumpath, c.userInst.secid(), g.OPT.secureLinks)}" width="${pt[0].file.thwidth}" height="${pt[0].file.thheight}" class="thumb" />
                    %else:  
                        <img src="${g.OPT.filesPathWeb + pt[0].file.thumpath}" width="${pt[0].file.thwidth}" height="${pt[0].file.thheight}" class="thumb" />                                
                    %endif 
                    </a>
                    %elif pt[0].picid == -1:
                        <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
                        <img src='${g.OPT.staticPathWeb}images/picDeleted.png' class="thumb">                                    
                    %endif
                <blockquote class="postbody" id="postBQId${pt[0].id}">
                        ${h.modMessage(pt[0].message, c.userInst, g.OPT.secureText)}
                </blockquote> 
            </td>
        </tr>
    </tbody>
</table>
	 
%endfor 

<br/>
<form action="/search" method="post">
    <input type="text" name="query" size="20" value="${c.query}"/>
    <input value="Search again" type="submit" />
</form>

%if c.userInst.useAjax():
	<script>popup_posts({ajax: true});</script>
%endif   

<%include file="wakaba.paginator.mako" args="baselink='search/%s' % c.query"/>
