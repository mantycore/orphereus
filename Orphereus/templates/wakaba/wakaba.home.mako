# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

%if h.templateExists(c.actuatorTest+'wakaba.homeTop.mako'):
    <%include file="${c.actuator+'wakaba.homeTop.mako'}" />
%endif

<hr style="clear: both;"/>

%for template in c.hometemplates:
    <%include file="${'wakaba.%s.mako' % template}" />
%endfor

<hr />
<br clear="all" />

