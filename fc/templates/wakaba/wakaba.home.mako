# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

%if h.templateExists(c.actuatorTest+'wakaba.homeTop.mako'):
    <%include file="${c.actuator+'wakaba.homeTop.mako'}" />
%endif

<hr style="clear: both;"/>

%if g.OPT.vitalSigns:

<%def name="vitalSigns()" cached=${g.OPT.statsCacheTime>0} cache_timeout=${g.OPT.statsCacheTime} cache_type="memory">
<div class="theader">
Vital signs
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

%if g.OPT.interestingNumbers:
<br/><br/>
SID: ${abs(c.userInst.secid()*c.userInst.secid() - c.userInst.secid()*c.totalPostsCount)}
%endif

</div>
</%def>

${vitalSigns()}
%endif

<%def name="stats()" cached=${g.OPT.statsCacheTime>0} cache_timeout=${g.OPT.statsCacheTime} cache_type="memory">
<h3>Boards</h3>
%if g.OPT.interestingNumbers and not c.userInst.Anonymous:
<span style="float: right;">
<i>Interesting numbers: ${c.totalPostsCount} [${abs(c.userInst.secid()*c.userInst.secid() - c.totalPostsCount*c.totalPostsCount)}]</i>
</span>
%endif

<i>Let my BOARDS go!</i>
<table width="100%" class="hlTable">
    <thead>
        <tr>
            <td style="width: 200px;">${_('Name')}</td>
            <td style="width: 40px;">${_('Threads')}</td>
            <td style="width: 40px;">${_('Posts')}</td>
            <td>${_('Description')}</td>
        </tr>
    </thead>
    <tbody>
%for b in c.boards:
        <tr>
            <td><a href="/${b.board.tag}/"><div class="hovblock">${b.board.tag}</div></a></td>
            <td>${b.count}</td>
            <td>${b.postsCount}</td>
            <td>
            %if b.board.options and b.board.options.comment:
                ${b.board.options.comment}
            %endif
            </td>  
        </tr>
%endfor 
        <tr>
            <td><div class="hovblock"><b>${_('Total')}</b></div></td>
            <td><div class="hovblock">${c.totalBoardsThreads}</div></td>
            <td><div class="hovblock">${c.totalBoardsPosts}</div></td>
            <td></td>  
        </tr>   
    </tbody>
</table>
<br/>

<h3>Tags</h3>
<i>Every small TAG has hidden powers. And it has everything to become a BOARD</i>
<table width="100%" class="hlTable">
    <thead>
        <tr>
            <td style="width: 200px;">${_('Name')}</td>
            <td style="width: 40px;">${_('Threads')}</td>
            <td style="width: 40px;">${_('Posts')}</td>
            <td>${_('Description')}</td>
        </tr>
    </thead>
    <tbody>
%for b in c.tags:
        <tr>
            <td><a href="/${b.board.tag}/"><div class="hovblock">${b.board.tag}</div></a></td>
            <td>${b.count}</td>     
            <td>${b.postsCount}</td>    
            <td>
            %if b.board.options and b.board.options.comment:
                ${b.board.options.comment}
            %endif
            </td>  
        </tr>
%endfor    
        <tr>
            <td><div class="hovblock"><b>${_('Total')}</b></div></td>
            <td><div class="hovblock">${c.totalTagsThreads}</div></td>
            <td><div class="hovblock">${c.totalTagsPosts}</div></td>
            <td></td>  
        </tr>   
    </tbody>
</table>

<hr />
<br clear="all" />
</%def>

${stats()}