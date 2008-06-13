# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />

<div class="postarea">
	<form id="postform" action="/register/doesntmatteranymore" method="post">
		<span class="postblock">Enter your security code :</span>
		<input name="key" type="password" size=60>
                <br>
                <span class="postblock">Re-enter security code :</span>
                <input name="key2" type="password" size=60>
                <br>
                Should be at least 24 symbols
                <br>
		<input type="submit" value="OK">                
	</form>
</div>
