# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

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
%if c.pages:
<table border="1"><tbody><tr><td>
    %for pg in range(0,c.pages):
        %if pg == c.page:
            [${pg}]
        %else:
            [<a href='/viewLog/${pg}'>${pg}</a>]
        %endif
    %endfor
</td></tr></tbody></table>
%endif
