% if session.has_key('postbody'):
    ${session['postbody']}
% endif
<form name="test" method="POST" action="/${c.board}">
Post goes here: <input type="text" name="body" />
<input type="submit" "name="submit" value="Submit />
</form>

