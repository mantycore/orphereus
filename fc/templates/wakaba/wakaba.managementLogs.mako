# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<%include file="wakaba.paginator.mako" args="baselink='hsViewLog'"/>

%if c.logs:
<table width="100%" class="hlTable">
    <thead>
        <tr>
            <td>Date</td>
            <td>UID</td>
            <td>Event</td>
            <td>Entry</td>
        </tr>
    </thead>
    <tbody>
    %for log in c.logs:
        <tr ${log.event < 0x10000 and "style='color:#F00;'" or ""}>
            <td>${log.date}</td>
            <td>${log.uidNumber}</td>
            <td>${log.event}</td>
            <td>${log.entry}</td>
        </tr>
    %endfor
    </tbody>
</table>
%endif

<%include file="wakaba.paginator.mako" args="baselink='hsViewLog'"/>
