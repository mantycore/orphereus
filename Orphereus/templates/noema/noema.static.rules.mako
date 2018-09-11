# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

<!-- ${_("Rules")} -->

%if h.templateExists(c.actuatorTest+'noema.rulesCont.mako'):
    <%include file="${c.actuator+'noema.rulesCont.mako'}" />
%endif
<hr />
