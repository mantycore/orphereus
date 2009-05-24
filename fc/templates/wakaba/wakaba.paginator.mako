<%page args="routeName, kwargDict={}"/>

%if c.pages:
<table border="1"><tbody><tr><td>
%if c.page > 0:
    [<a href='${h.url_for(routeName, **(dict(kwargDict, **dict(page=c.page - 1))))}'>&lt;&lt;</a>]
%endif

%if not c.showPagesPartial:
    %for pg in range(0,c.pages):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}'>${pg}</a>]
        %endif
    %endfor
%else:
    %for pg in range(0,2):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}'>${pg}</a>]
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
                [<a href='${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}'>${pg}</a>]
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
            [<a href='${h.url_for(routeName, **(dict(kwargDict, **dict(page=pg))))}'>${pg}</a>]
        %endif
    %endfor
%endif
%if c.page < c.pages-1:
    [<a href='${h.url_for(routeName, **(dict(kwargDict, **dict(page=c.page + 1))))}'>&gt;&gt;</a>]
%endif
</td></tr></tbody></table>
%endif
