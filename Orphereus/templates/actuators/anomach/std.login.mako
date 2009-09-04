# -*- coding: utf-8 -*-

<div class="postarea" style="">
    <!-- <img src="${g.OPT.staticPathWeb}ohhi.png" alt="oh hi"/> -->
    <object width="550" height="400">
	<param name="movie" value="${g.OPT.staticPathWeb}anomi.swf">
	<embed src="${g.OPT.staticPathWeb}anomi.swf" width="600" height="400">
	</embed>
	</object>

    <form id="postform" action="${h.url_for('authorizeToUrl', url=c.currentURL)}" method="post">
        <span class="postblock">
        ${_('Enter your security code')}
        </span>
        <p><input name="code" type="password" size="60"/></p>
        %if c.showCaptcha:
            <p class="postblock">${_('Too many login attempts. Enter CAPTCHA please')}</p>
            <div><img src="${h.url_for('captcha', cid=c.captcha.id)}" style="border: #964600 2px solid;" alt="Captcha"/></div>
            <p><input name="captcha" size="32" style="text-align: center"/></p>
            <p><input name="captid" type="hidden" value="${c.captcha.id}"/></p>
        %endif
        <p><input type="submit" value="${_('OK')}"/></p>
    </form>
</div>
