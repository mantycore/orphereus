<%page args="routeName, kwargDict={}"/>

%if c.pages and c.pages > 1:
<div id="paging">
    %if c.page > 0:
    <a rel="prev" href="${h.url_for(routeName, **(dict(kwargDict, **dict(page=c.page - 1))))}">←</a>
    %endif
    
    %if not c.showPagesPartial:
        %for pg in range(0, c.pages):
            <a href="${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}"
                %if pg == c.page:
                class="current"
                %endif
                >${pg}</a>
        %endfor
    %else:
        %for pg in range(0, 2):
            <a href="${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}"
                %if pg == c.page:
                class="current"
                %endif
                >${pg}</a>
        %endfor
        %if c.leftPage and c.leftPage > 2:
        ...
        %endif
        %if c.leftPage and c.rightPage:
            %for pg in range(c.leftPage, c.rightPage):
                <a href="${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}"
                    %if pg == c.page:
                    class="current"
                    %endif
                    >${pg}</a>
            %endfor
            %if c.rightPage < c.pages - 2:
                ...
            %endif
        %endif
        %for pg in range(c.pages - 2, c.pages):
            <a href="${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}"
                %if pg == c.page:
                class="current"
                %endif
                >${pg}</a>
        %endfor
    %endif
    %if c.page < c.pages-1:
        <a rel="next" href="${h.url_for(routeName, **(dict(kwargDict, **dict(page=c.page + 1))))}">→</a>
    %endif
</div>
%endif

