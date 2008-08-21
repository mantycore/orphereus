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
      %if log.event != 0x00080001:
        <tr ${log.event < 0x10000 and "style='color:#F00;'" or ""}>
            <td>${log.date}</td>
            <td>${log.uidNumber}</td>
%if log.event>1:            
            <td>${log.event + c.userInst.secid()}</td>
%else:      
            <td>${log.event}</td>      
%endif
            <td>${log.entry}</td>
        </tr>
      %endif
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
