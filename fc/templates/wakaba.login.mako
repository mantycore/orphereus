# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="postarea">
	<form id="postform" action="${c.currentURL}/auth" method="post">
		<span class="postblock">Enter your security code:</span>
		<input name="code" type="password" size=60>
		<input type="submit" value="OK">
	</form>
</div>
