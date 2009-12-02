# -*- coding: utf-8 -*-
<%page args="thread, post"/>

<table id="quickReplyNode${post.id}"><tbody><tr>
<td class="doubledash">&gt;&gt;</td>
<td
%if g.OPT.memcachedPosts and not(c.userInst.isAdmin()):
  class="reply"
%else:
  %if post.uidNumber != c.uidNumber or not c.userInst.hlOwnPosts:
  class="reply"
  %else:
  class="reply myreply"
  %endif
%endif
id="reply${post.id}">
  <div class="postheader">
    <a name="i${post.id}"></a>
    &nbsp;<a href="javascript:void(0)" onclick="showDeleteBoxes()"><img src="${g.OPT.staticPathWeb}images/delete.gif" border="0" alt="x" title="Del" /></a>
    <span style="display:none" class="delete">
    %if g.OPT.memcachedPosts and not(c.userInst.isAdmin()):
      <input type="checkbox" name="delete-${post.id}" value="${post.id}" />
    %else:
      %if post.uidNumber == c.uidNumber or (thread.selfModeratable() and c.uidNumber == thread.uidNumber) or c.enableAllPostDeletion:
          <input type="checkbox" name="delete-${post.id}" value="${post.id}" />
          %if post.uidNumber != c.uidNumber and (thread.selfModeratable() and c.uidNumber == thread.uidNumber):
          <i>${_('[REMOVABLE]')}</i>
          %endif
      %endif
      ${h.postPanelCallback(thread, post, c.userInst)}
    %endif
    &nbsp;
    </span>
    %if post.sage:
        <img src="${g.OPT.staticPathWeb}images/sage.png" alt="Sage"/>
    %endif
    %if post.title:
        <span class="replytitle">${post.title}</span>
    %endif

     ${h.tsFormat(post.date)}

    <span class="reflink"> \
    %if c.board:
        <a href="${h.postUrl(thread.id, post.id)}">#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a> \
    %else:
        <a href="javascript:insert('&gt;&gt;${post.id}')">#${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a> \
    %endif
    ${h.postHeaderCallback(thread, post, c.userInst)}
    </span>

    &nbsp;
    </div>
    <%include file="wakaba.fileBlock.mako" args="post=post,opPost=None,searchMode=None,newsMode=None" />

    <blockquote class="postbody" id="postBQId${post.id}">
  %if g.OPT.memcachedPosts and not(c.userInst.isAdmin()):
        %if (c.count > 1) and post.messageShort and getattr(thread, 'enableShortMessages', True):
            ${post.messageShort}
            <br />
            ${_('Comment is too long.')} <a href="${h.postUrl(thread.id, post.id)}" onclick="getFullText(event,${thread.id},${post.id});" class="expandPost">${_('Full version')}</a>
        %else:
            ${post.message}
        %endif
  %else:
        %if (c.count > 1) and post.messageShort and c.userInst.hideLongComments and getattr(thread, 'enableShortMessages', True):
            ${post.messageShort}
            <br />
            ${_('Comment is too long.')} <a href="${h.postUrl(thread.id, post.id)}" onclick="getFullText(event,${thread.id},${post.id});" class="expandPost">${_('Full version')}</a>
        %else:
            ${post.message}
        %endif
    %endif
    %if post.messageInfo:
        <div>${post.messageInfo}</div>
    %endif
    </blockquote>
</td></tr></tbody></table>
