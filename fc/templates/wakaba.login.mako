# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="logo"><center>${c.title}</center></div>
<hr />

<div class="postarea">
	<form id="postform" action="${c.currentURL}authorize" method="post">    
		<span class="postblock">${_('Enter your security code')}</span>
		<p><input name="code" type="password" size=60></p>
		<p><input type="submit" value="${_('OK')}"></p>
	</form>
</div>
