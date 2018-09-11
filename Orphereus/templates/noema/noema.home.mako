# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

%for template in c.hometemplates:
<%include file="${'noema.%s.mako' % template}" />
%endfor
