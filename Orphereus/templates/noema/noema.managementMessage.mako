# -*- coding: utf-8 -*-
<%inherit file="noema.management.mako" />
%if c.message:
<span class="theader">${c.message}</span>
%endif 
<br />
%if c.returnUrl:
<a href="${c.returnUrl}">${_('Back')}</span>
%else:
<a href="javascript:history.back();">${_('Back')}</span>
%endif 