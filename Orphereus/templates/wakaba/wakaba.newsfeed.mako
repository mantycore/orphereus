%if c.newsFeed:
<h3 class="theader"><a style="cursor:pointer; display: block;" onclick="toggle_div('lastNews');">${_('Latest news')}</a></h3>
<div align="center">
<div id="lastNews" style="width: 90%; text-align: left;" >
    %for post in c.newsFeed:
    <div style="border: 1px dashed gray; padding: 0px 4px 0px 4px; margin-bottom: 15px;" id="thread-${post.id}" class="thread">
        <span class="adminMenu" style="text-align: center; display: block;">
        %if post.title:
            <span class="filetitle">${post.title}</span>
        %endif
        <span>${post.date}</span>
        </span>
        %if post.file:
            <a href="${g.OPT.filesPathWeb + h.modLink(post.file.path, c.userInst.secid())}"
            %if post.file.extension.newWindow:
                target="_blank"
            %endif
            >
            <%include file="wakaba.thumbnail.mako" args="post=post" />
            </a>
        %endif
        <blockquote class="postbody" id="quickReplyNode${post.id}">${post.message}</blockquote>
            <br clear="all" />
        <a class="adminMenu" style="display: block; text-align: center;" href="${h.postUrl(post.id, post.id)}">
            #${g.OPT.secondaryIndex and post.secondaryIndex or post.id} (${ungettext('%d reply', '%d replies', post.replyCount) % post.replyCount})
        </a>
    </div>
    %endfor
</div>
</div>
%if c.userInst.useAjax:
    <script type="text/javascript">popup_posts({ajax: true});</script>
%endif

%endif