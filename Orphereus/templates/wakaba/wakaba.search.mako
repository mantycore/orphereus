# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<b>${_('Found')}:</b> ${c.count}

<br/>
<form action="${h.url_for('searchBase')}" method="post">
    <input type="text" name="query" size="20" value="${c.query}"/>
    <input value="${_('Search again')}" type="submit" />
    [<a href="${h.url_for('static', page='markup', anchor='search')}" target="_blank">${_('Help')}</a>]
</form>

<%include file="wakaba.paginator.mako" args="routeName='search', kwargDict={'text' : c.query}"/>

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
                    %if pt[0].title:
                        <span class="replytitle">${pt[0].title}</span>
                    %endif
                    ${pt[0].date}
                </label>
                <span class="reflink">
                    <a href="${h.postUrl(pt[1].id, pt[0].id)}">#${g.OPT.secondaryIndex and pt[0].secondaryIndex or pt[0].id}</a>;

          ${_('Thread')}
          <a href="${h.postUrl(pt[1].id, pt[1].id)}">#${g.OPT.secondaryIndex and pt[1].secondaryIndex or pt[1].id}</a>
          ${_('from')}:
          %for t in pt[1].tags:
              <a href="${h.url_for('boardBase', board=t.tag)}">/${t.tag}/</a>
          %endfor
        </span>
        &nbsp;
                %if pt[0].file:
                    <br /><span class="filesize">${_('File:')}

                    <a href="${g.OPT.filesPathWeb + h.modLink(pt[0].file.path, c.userInst.secid())}"
                    %if pt[0].file.extension.newWindow:
                        target="_blank"
                    %endif
                    >
                    ${h.modLink(pt[0].file.path, c.userInst.secid(), True)}</a>
                    (<em>${'%.2f' % (pt[0].file.size / 1024.0)} Kbytes, ${pt[0].file.width}x${pt[0].file.height}</em>)</span>
                    <span class="thumbnailmsg">${_('This is resized copy. Click it to view original image')}</span><br />
                    <a href="${g.OPT.filesPathWeb + h.modLink(pt[0].file.path, c.userInst.secid())}"
                    %if pt[0].file.extension.newWindow:
                        target="_blank"
                    %endif
                    >

                    <%include file="wakaba.thumbnail.mako" args="post=pt[0]" />

                    </a>
                    %elif pt[0].picid == -1:
                        <span class="thumbnailmsg">${_('Picture was removed by user or administrator')}</span><br/>
                        <img src='${g.OPT.staticPathWeb}images/picDeleted.png' class="thumb">
                    %endif
                <blockquote class="postbody" id="postBQId${pt[0].id}">
                %if pt[0].id in c.highlights:
                    ${c.highlights[pt[0].id][1]}
                %else:
                    ${pt[0].message}
                %endif
                </blockquote>
            </td>
        </tr>
    </tbody>
</table>

%endfor

<br/>
<form action="${h.url_for('searchBase')}" method="post">
    <input type="text" name="query" size="20" value="${c.query}"/>
    <input value="${_('Search again')}" type="submit" />
</form>

<%include file="wakaba.jsService.mako" />

<%include file="wakaba.paginator.mako" args="routeName='search', kwargDict={'text' : c.query}"/>
