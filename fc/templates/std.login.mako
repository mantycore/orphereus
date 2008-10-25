# -*- coding: utf-8 -*-
<%inherit file="std.main.mako" />

<div class="postarea">
	<form id="postform" action="${c.currentURL}authorize" method="post">
		<span class="postblock">${_('Enter your security code')}</span>
		<p><input name="code" type="password" size=60 style="text-align: center"></p>
        %if c.showCaptcha:
            <p class="postblock">${_('Too many login attempts. Enter CAPTCHA please')}</p>
            <div><img src='/captcha/${c.captid}' style="border: #964600 2px solid;"></div>
            <p><input name="captcha" size=32 style="text-align: center"></p>
            <p><input name="captid" type="hidden" value="${c.captid}"></p>
        %endif
		<p><input type="submit" value="${_('OK')}"></p>
	</form>
	<br/>
	<a href="http://arch.anoma.ch/"><strong>Archive of teh Internets</strong></a>	
</div>
