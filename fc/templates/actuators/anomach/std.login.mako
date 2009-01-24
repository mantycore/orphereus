# -*- coding: utf-8 -*-

<div style="position: relative; top: -40px; text-align: center;"><img src="${g.OPT.staticPathWeb}hello.png" alt="oh hi"/></div>

<div class="postarea">
    <form id="postform" action="${c.currentURL}authorize" method="post">
        <span class="postblock">
        ${_('Enter your security code')}
        </span>
        <p><input name="code" type="password" size=60 style="text-align: center"></p>
        %if c.showCaptcha:
            <p class="postblock">${_('Too many login attempts. Enter CAPTCHA please')}</p>
            <div><img src='/captcha/${c.captid}' style="border: #964600 2px solid;"></div>
            <p><input name="captcha" size=32 style="text-align: center"></p>
            <p><input name="captid" type="hidden" value="${c.captid}"></p>
        %endif
        <p><input type="submit" value="${_('OK')}"></p>
    </form>
</div>  