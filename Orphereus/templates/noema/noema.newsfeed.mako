%if c.newsFeed:
<div class="news-feed">
    <h2>Новости</h2>
    %for post in c.newsFeed:
    <div class="post-wrapper">
        <div class="news-item">
            <div class="news-head">
                %if post.title:
                <h3>${post.title}</h3>
                %endif
                <div class="news-date">${h.tsFormat(post.date)}</div>
            </div>
            <%include file="noema.fileBlock.mako" args="post=post,opPost=True,searchMode=None,newsMode=True" />
            <div class="post-text">
                <div class="real-post-text">
                    ${post.message}
                </div>
                <br class="clearer">
            </div>
            <div class="news-foot">
                обсуждаем в <a href="${h.postUrl(post.id, post.id)}">треде #${g.OPT.secondaryIndex and post.secondaryIndex or post.id}</a>
            </div>
        </div>
    </div>
    %endfor
</div>
%endif
