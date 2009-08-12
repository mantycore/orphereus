# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />
%if c.message:
<span class="theader">${c.message}</span>
%endif 
<br />
%if c.returnUrl:
<a href="${c.returnUrl}">${_('Back')}</span>
%endif 