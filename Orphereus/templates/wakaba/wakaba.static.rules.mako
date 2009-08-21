# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<!-- ${_("Rules")} -->

%if h.templateExists(c.actuatorTest+'wakaba.rulesCont.mako'):
    <%include file="${c.actuator+'wakaba.rulesCont.mako'}" />
%endif
<hr />
