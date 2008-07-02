# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="errorMessage">
<h1>${_('You are banned!')}</h1>
${_('You are banned for %s days for following reason : %s') % (c.userInst.bantime(),c.userInst.banreason())}
</div>