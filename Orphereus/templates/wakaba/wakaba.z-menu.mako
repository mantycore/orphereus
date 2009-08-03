<div id="boardlist_header">
<div id="overlay_menu" style="position: fixed; top: 0px;" class="reply" onmouseout="javascript:menu_show('');">
<script>var menu_current = '';</script>
[<a href="#" onmouseover="javascript:menu_show('menu_special');">${_('Special pages')}</a>]
%if c.boardlist:
    %for section in c.boardlist:
        %if section[1]:
        	[<a href="#" onmouseover="javascript:menu_show('menu_${h.sectionName(section[1])}');">${section[1]}</a>]
        %else:
        	[<a href="#" onmouseover="javascript:menu_show('menu_unnamed');">${_('Unnamed section')}</a>]
        %endif
    %endfor
[<a href="#" onmouseover="javascript:menu_show('menu_special2');">${_('User pages')}</a>]
%if len(c.menuLinks):
    [<a href="#" onmouseover="javascript:menu_show('menu_links');">${_('Links')}</a>]
%endif
%if not c.userInst.Anonymous and c.userInst.filters:
    [<a href="#" onmouseover="javascript:menu_show('menu_filters');">${_('Filters')}</a>]
%endif

      <div id="menu_special" style="display:none;" onmouseover="javascript:menu_show('menu_special');"  onmouseout="javascript:menu_show('');">
		    %if g.OPT.allowOverview:
		    <a href="${h.url_for('boardBase', board='~')}" title="/~/">${_('Overview')}</a><br />
		    %endif
		    %if not c.userInst.Anonymous:
		    <a href="${h.url_for('boardBase', board='@')}" title="/@/">${_('Related threads')}</a><br />
		    %endif
		    <a href="${h.url_for('boardBase', board='!')}" title="/!/">${_('Statistics')}</a>
      </div>

    %for section in c.boardlist:
      <div id="menu_${h.sectionName(section[1])}" style="display:none;" onmouseover="javascript:menu_show('menu_${h.sectionName(section[1])}');"  onmouseout="javascript:menu_show('');">
        %for board in section[0]:
		    <a href="${h.url_for('boardBase', board=board.tag)}" title="${board.comment}"><b>/${board.tag}/</b> &mdash; ${board.comment}</a><br />
        %endfor
      </div>
    %endfor
%endif

	<div id="menu_special2" style="display:none;" onmouseover="javascript:menu_show('menu_special2');"  onmouseout="javascript:menu_show('');">
		%if not c.userInst.Anonymous:
		    <a href="${h.url_for('userProfile')}">${_('Profile')}</a><br />
		%elif g.OPT.allowAnonProfile:
		    <a href="${h.url_for('userProfile')}">${_('Settings')}</a><br />
		%endif
		%if c.userInst.isAdmin():
		    <a href="${h.url_for('holySynod')}">${_('Holy Synod')}</a><br />
		%endif
		%if g.OPT.usersCanViewLogs:
		    <a href="${h.url_for('viewLogBase')}">${_('Logs')}</a><br />
		%endif
		
		%if not c.userInst.Anonymous:
		<a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Logout')}</a><br />
		%else:
		    %if g.OPT.allowLogin:
		        %if c.currentURL:
		            <a href="${h.url_for('authorizeToUrl', url=c.currentURL)}">${_('Login')}</a><br />
		        %else:
		            <a href="${h.url_for('authorize')}">${_('Login')}</a><br />
		        %endif
		    %endif
		    <a href="${h.url_for('logout')}" target="_top" onclick="parent.top.list.location.reload(true);">${_('Kill session')}</a><br />
		%if g.OPT.allowRegistration:
			<a href="${h.url_for('register', invite='register')}">${_('Register')}</a><br />
		%endif
		%endif		
    </div>

%if c.menuLinks:
	<div id="menu_links" style="display:none;" onmouseover="javascript:menu_show('menu_links');"  onmouseout="javascript:menu_show('');">
    %for link in c.menuLinks:
        % if isinstance(link, list) and len(link) == 2:
        <a href="${link[0]}">${link[1]}</a><br />
        %endif
    %endfor
    <a target="_blank" href="${h.url_for('static', page='donate')}">Donate</a><br />
    </div>
%endif

%if not c.userInst.Anonymous and c.userInst.filters:
	<div id="menu_filters" style="display:none;" onmouseover="javascript:menu_show('menu_filters');"  onmouseout="javascript:menu_show('');">
    %for f in c.userInst.filters:
        <a href="${h.url_for('boardBase', board=f.filter)}">/${f.filter}/</a><br />
    %endfor
    </div>
%endif
</div></div>
<br />