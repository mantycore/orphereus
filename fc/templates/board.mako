<form name="test" method="POST" action="/${c.board}">
Post goes here: 
<br />
<textarea name="message" ></textarea>
<br />
<input type="submit" name="submit" value="Submit" />
</form>
<br />
% for post in c.posts:
<span style="background-color: wheat;">Post # ${post.id}</span>
${post.message}
<br />
% endfor

