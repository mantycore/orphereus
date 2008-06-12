<form name="test" method="POST" action="/${c.board}">
Post goes here: <textarea name="message" ></textarea>
<input type="submit" "name="submit" value="Submit />
</form>
% for post in c.posts:
<hr />
${post.message}
% endfor

