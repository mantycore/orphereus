<div class="adminbar">
    [ \
    %if g.OPT.allowOverview:
    <a href="${h.url_for('boardBase', board='~')}" title="${_('Overview')}">/~/</a> \
    %endif
    %if not c.userInst.Anonymous:
    <a href="${h.url_for('boardBase', board='@')}" title="${_('Related threads')}">/@/</a> \
    %endif
    <a href="${h.url_for('boardBase', board='!')}" title="${_('Home')}">/!/</a> \
    ]

%if c.boardlist:
%if g.OPT.spiderTrap:
<span style="display: none"><a href="${h.url_for('botTrap1', confirm=c.userInst.secid())}">...</a><a href="${h.url_for('botTrap2')}">.</a></span>
%endif
%if g.OPT.dvachStyleMenu:
	${h.boardMenu(c.boardlist)}
%else:
    %for section in c.boardlist:
        %if section[1]:
            <!-- ${section[1]} -->
        %else:
            <!-- ${_('Unnamed section')} -->
        %endif
        [ \
        %for board in section[0]:
            <a href="${h.url_for('boardBase', board=board.tag)}" title="${board.comment}"><b>/${board.tag}/</b></a> \
        %endfor
        ]
    %endfor
%endif
%endif

%if not c.userInst.Anonymous:
    [<a href="${h.url_for('userProfile')}">${_('Profile')}</a>]
%elif g.OPT.allowAnonProfile:
    [<a href="${h.url_for('userProfile')}">${_('Settings')}</a>]
%endif
%if c.userInst.isAdmin():
    [<a href="${h.url_for('holySynod')}">${_('Holy Synod')}</a>]
%endif
%if g.OPT.usersCanViewLogs:
    [<a href="${h.url_for('viewLogBase')}">${_('Logs')}</a>]
%endif
%if c.menuLinks:
    %for link in c.menuLinks:
        % if isinstance(link, list) and len(link) == 2:
        [<a href="${link[0]}">${link[1]}</a>]
        %endif
    %endfor
%endif

[<a target="_blank" href="${h.url_for('static', page='donate')}">Donate</a>]
%if not c.userInst.Anonymous:
[<a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Logout')}</a>]
%else:
    %if g.OPT.allowLogin:
        %if c.currentURL:
            [<a href="${h.url_for('authorizeToUrl', url=c.currentURL)}">${_('Login')}</a>]
        %else:
            [<a href="${h.url_for('authorize')}">${_('Login')}</a>]
        %endif
    %endif
    [<a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Kill session')}</a>]
%if g.OPT.allowRegistration:
[<a href="${h.url_for('register', invite='register')}">${_('Register')}</a>]
%endif
%endif
%if not c.userInst.Anonymous and c.userInst.filters:
    <br />
    [ \
    %for f in c.userInst.filters:
        <a href="${h.url_for('boardBase', board=f.filter)}">/${f.filter}/</a> \
    %endfor
    ]
%endif
</div>
