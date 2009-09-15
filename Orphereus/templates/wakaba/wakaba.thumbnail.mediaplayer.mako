<%page args="post"/>
</a>

<table class="thumb">
<tr><td>
<img src="${g.OPT.staticPathWeb +  h.modLink(post.file.thumpath, c.userInst.secid())}" width="${post.file.thwidth}" height="${post.file.thheight}" class="thumb"  alt="Preview" />

<br />
</td></tr><tr><td>
<object type="application/x-shockwave-flash"
        data="${g.OPT.staticPathWeb}player.swf?file=${g.OPT.filesPathWeb +  h.modLink(post.file.path, c.userInst.secid())}"
        width="150" height="15">
  <param name="movie" value="${g.OPT.staticPathWeb}player.swf?file=${g.OPT.filesPathWeb +  h.modLink(post.file.path, c.userInst.secid())}" />
</object>
</td></tr>
</table>

<a href="#" style="display: none">


