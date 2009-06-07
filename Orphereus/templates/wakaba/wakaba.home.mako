# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

%if h.templateExists(c.actuatorTest+'wakaba.homeTop.mako'):
    <%include file="${c.actuator+'wakaba.homeTop.mako'}" />
%endif

<hr style="clear: both;"/>

%if g.OPT.vitalSigns:

<%def name="vitalSigns()" cached=${g.OPT.statsCacheTime>0} cache_timeout=${g.OPT.statsCacheTime} cache_type="memory">
<div class="theader">
${_('Vital signs')}
<br/><br/>
<font size="-1">
${_("Unique users in last 1000 posts: %d") % c.last1KUsersCount}<br/>
${_("Unique users in previous 1000 posts: %d") % c.prev1KUsersCount}
</font>
<br/>
${_("Rate:")} <span style="color: ${c.last1KUsersCount / (c.prev1KUsersCount + 0.01) > 1.0 and "green" or "red"}">${'%.2f' % (c.last1KUsersCount / (c.prev1KUsersCount + 0.01))}</span>
<br/><br/>
<font size="-1">
${_("Posts during last week: %d") % c.lastWeekMessages}<br/>
${_("Posts during previous week: %d") % c.prevWeekMessages}
</font>
<br/>
${_("Rate:")} <span style="color: ${c.lastWeekMessages / (c.prevWeekMessages + 0.01) > 1.0 and "green" or "red"}">${'%.2f' % (c.lastWeekMessages / (c.prevWeekMessages + 0.01))}</span>
</div>
</%def>

${vitalSigns()}
%endif

<%def name="stats()" cached=${g.OPT.statsCacheTime>0} cache_timeout=${g.OPT.statsCacheTime} cache_type="memory">
<h3 class="theader"><a style="cursor:pointer; display: block;" onclick="toggle_div('boardsStatistics');">${_('Boards')}</a></h3>
<div id="boardsStatistics">
%if g.OPT.showShortStatistics and not c.userInst.Anonymous:
<span style="float: right;">
<i>${_("Total posts: %d; total users: %d (banned: %d, active: %d)") % (c.totalPostsCount, c.totalUsersCount, c.bannedUsersCount,  c.totalUsersCount - c.bannedUsersCount)} </i>
</span>
%endif

%if c.boards:
<i>${_('Let my BOARDS go!')}</i>
<%include file="wakaba.homeStatTable.mako" args="boards=c.boards,totalThreads=c.totalBoardsThreads,totalPosts=c.totalBoardsPosts"/>
%endif
</div>

%if c.stags:
<h3 class="theader"><a style="cursor:pointer; display: block;" onclick="toggle_div('specialTagsStatistics');">${_('Special tags')}</a></h3>
<div id="specialTagsStatistics">
<i>${_('Useful stuff is so useful')}</i>
<%include file="wakaba.homeStatTable.mako" args="boards=c.stags,totalThreads=c.totalSTagsThreads,totalPosts=c.totalSTagsPosts"/>
</div>
%endif

%if c.tags:
<h3 class="theader"><a style="cursor:pointer; display: block;" onclick="toggle_div('tagsStatistics');">${_('Tags')}</a></h3>
<div id="tagsStatistics"
%if c.userInst.useTitleCollapse:
style="display: none;"
%endif
>
<i>${_('Every small TAG has hidden powers. And it has everything to become a BOARD')}</i>
<%include file="wakaba.homeStatTable.mako" args="boards=c.tags,totalThreads=c.totalTagsThreads,totalPosts=c.totalTagsPosts"/>
</div>
%endif
<hr />
<br clear="all" />
</%def>

${stats()}
