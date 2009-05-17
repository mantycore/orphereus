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
LKA: ${c.last1KUsersCount};
PKA: ${c.prev1KUsersCount}
</font>
<br/>
ADK: <span style="color: ${c.last1KUsersCount / (c.prev1KUsersCount + 0.01) > 1.0 and "green" or "red"}">${'%.2f' % (c.last1KUsersCount / (c.prev1KUsersCount + 0.01))}</span>
<br/><br/>
<font size="-1">
LWA: ${c.lastWeekMessages};
PWA: ${c.prevWeekMessages}
</font>
<br/>
ADW: <span style="color: ${c.lastWeekMessages / (c.prevWeekMessages + 0.01) > 1.0 and "green" or "red"}">${'%.2f' % (c.lastWeekMessages / (c.prevWeekMessages + 0.01))}</span>

%if g.OPT.interestingNumbers and not c.userInst.Anonymous:
<br/><br/>
SID: ${abs(c.userInst.secid()*c.userInst.secid() - c.userInst.secid()*c.totalPostsCount)}
%endif

</div>
</%def>

${vitalSigns()}
%endif

<%def name="stats()" cached=${g.OPT.statsCacheTime>0} cache_timeout=${g.OPT.statsCacheTime} cache_type="memory">
<h3>${_('Boards')}</h3>
%if g.OPT.interestingNumbers and not c.userInst.Anonymous:
<span style="float: right;">
<i>Interesting numbers: ${c.totalPostsCount} [${abs(c.userInst.secid()*c.userInst.secid() - c.totalPostsCount*c.totalPostsCount)}]</i>
</span>
%endif

%if c.boards:
<i>${_('Let my BOARDS go!')}</i>
<%include file="wakaba.homeStatTable.mako" args="boards=c.boards,totalThreads=c.totalBoardsThreads,totalPosts=c.totalBoardsPosts"/>
%endif

%if c.stags:
<h3>${_('Special tags')}</h3>
<i>${_('Useful stuff is so useful')}</i>
<%include file="wakaba.homeStatTable.mako" args="boards=c.stags,totalThreads=c.totalSTagsThreads,totalPosts=c.totalSTagsPosts"/>
%endif

%if c.tags:
<h3>${_('Tags')}</h3>

<i>${_('Every small TAG has hidden powers. And it has everything to become a BOARD')}</i>
<%include file="wakaba.homeStatTable.mako" args="boards=c.tags,totalThreads=c.totalTagsThreads,totalPosts=c.totalTagsPosts"/>
%endif

<hr />
<br clear="all" />
</%def>

${stats()}
