# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<table class="category" width="100%" border="0" cellspacing="0" cellpadding="0">
<tbody>
    <tr>
        <td class="header">${_('Special pages')}</td>
    </tr>

    <tr>
        <td class="list">
            %if g.OPT.allowOverview:
            <div><a href="${h.url_for('boardBase', board='~')}" title="/~/" target="board">${_('Overview')}</a></div>
            %endif
            %if not c.userInst.Anonymous:
            <div><a href="${h.url_for('boardBase', board='@')}" title="/@/" target="board">${_('Related threads')}</a></div>
            %endif
            <div><a href="${h.url_for('boardBase', board='!')}" title="/!/" target="board">${_('Statistics')}</a></div>
        </td>
    </tr>
</tbody>
</table>

%if c.boardlist:
%if g.OPT.spiderTrap:
<span style="display: none"><a href="${h.url_for('botTrap1', confirm=c.userInst.secid())}">...</a><a href="${h.url_for('botTrap2')}">.</a></span>
%endif
%for section in c.boardlist:
    <table class="category" width="100%" border="0" cellspacing="0" cellpadding="0">
    <tbody>
        <tr>
            <td class="header">
                %if section[1]:
                    ${section[1]}
                %else:
                    ${_('Unnamed section')}
                %endif
            </td>
        </tr>

        <tr>
            <td class="list">
                %for board in section[0]:
                    <div>
                        <a href="${h.url_for('boardBase', board=board.tag)}" title="/${board.tag}/" target="board">
                            %if board.comment:
                                ${board.comment}
                            %else:
                                /${board.tag}/
                            %endif
                        </a></div>
                %endfor
            </td>
        </tr>
    </tbody>
    </table>
%endfor
%endif

<table class="category" width="100%" border="0" cellspacing="0" cellpadding="0">
<tbody>
    <tr>
        <td class="header">${_('Additional')}</td>
    </tr>

    <tr>
        <td class="list">
    %if not c.userInst.Anonymous:
        <div><a href="${h.url_for('userProfile')}" target="board">${_('Profile')}</a></div>
    %elif g.OPT.allowAnonProfile:
        <div><a href="${h.url_for('userProfile')}" target="board">${_('Settings')}</a></div>
    %endif
    %if c.userInst.isAdmin():
        <div><a href="${h.url_for('holySynod')}" target="board">${_('Holy Synod')}</a></div>
    %endif
    %if g.OPT.usersCanViewLogs:
        <div><a href="${h.url_for('viewLogBase')}" target="board">${_('Logs')}</a></div>
    %endif

    %if not c.userInst.Anonymous:
    <div><a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Logout')}</a></div>
    %else:
        %if g.OPT.allowLogin:
            <div><a href="${h.url_for('authorizeToUrl', url='!')}" target="board">${_('Login')}</a></div>
        %endif
        <div><a href="${h.url_for('logout')}" target="_top">${_('Kill session')}</a></div>
    %if g.OPT.allowRegistration:
    <div><a href="${h.url_for('register', invite='register')}" target="board" onclick="parent.top.list.location.reload(true);">${_('Register')}</a></div>
    %endif
    %endif
        </td>
    </tr>
</tbody>
</table>

<table class="category" width="100%" border="0" cellspacing="0" cellpadding="0">
<tbody>
    <tr>
        <td class="header">${_('Links')}</td>
    </tr>

    <tr>
        <td class="list">
    %if c.menuLinks:
        %for link in c.menuLinks:
            % if isinstance(link, list) and len(link) == 2:
            <div><a href="${link[0]}" target="board">${link[1]}</a></div>
            %endif
        %endfor
    %endif


    <div><a href="${h.url_for('static', page='donate')}" target="board">Donate</a></div>
        </td>
    </tr>
</tbody>
</table>

<table class="category" width="100%" border="0" cellspacing="0" cellpadding="0">
<tbody>
    <tr>
        <td class="header">${_('User filters')}</td>
    </tr>

    <tr>
        <td class="list">
%if not c.userInst.Anonymous and c.userInst.filters:
        %for f in c.userInst.filters:
            <div><a href="${h.url_for('boardBase', board=f.filter)}" target="board">/${f.filter}/</a><div>
        %endfor
%endif
		<div id="custFwdLink"><a onclick="javascript:toggle_div('custFwd');toggle_div('custFwdLink');">${_('Custom filter...')}</a></div>
        <div style="display:none" id="custFwd">
	        <form method="post" action="${h.url_for('makeFwdTo')}" target="board">
	        <input type="text" name="tags"/>
	        </form>
        </div>
        </td>
    </tr>
</tbody>
</table>