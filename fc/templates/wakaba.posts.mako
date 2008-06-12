<%inherit file="wakaba.base.mako" />

%for t in c.Threads:
	<div id="thread-${t.PostID}">
		<span class="filesize">
			<a target="_blank" href="${t.FileSrc}">${t.FileName}</a>
			(<em>${t.FileSize}, ${t.ImgDimensions}</em>)
		</span>
		<span class="thumbnailmsg"></span><br />
		<a target="_blank" href="${t.FileSrc}">
			<img src="${ThumbSrc}" class="thumb" />
		</a>
		<a name="${t.PostID}"></a>
		<label>
			<input type="checkbox" name="delete" value="${t.PostID}" />
			<span class="filetitle"></span>  
			<span class="postername"></span>
			${t.Date}
		</label>
		<span class="reflink">
			<a href="${t.PostID}#i${t.PostID}">${t.PostID}</a>
		</span>
		&nbsp;
		<span class="replytothread">
			[
			<a href="${t.PostID}#i${t.PostID}">
				${c.Strings.Reply}
			</a>
			]
		</span>
		<blockquote>
			${t.Message}
		</blockquote>
		<span class="omittedposts">  Пропущено 8 ответов. Нажмите "ответ", чтобы увидеть тред целиком. </span> 
		<table>
			<tbody>
				<tr>
					<td class="doubledash">&gt;&gt;</td>
					<td class="reply" id="reply2492740">
						<a name="2492740"></a>
						<label>
							<input type="checkbox" name="delete" value="2492740" />
							<span class="replytitle"></span>
							<span class="commentpostername"></span>
							Чтв 12 Июн 2008 05:19:59
						</label>
						<span class="reflink">
							<a href="/b/res/2492501.html#i2492740">.2492740</a>
						</span>
						&nbsp;  
						<blockquote>
							<p>я нихуя не понял</p>
						</blockquote> 
					</td>
				</tr>
			</tbody>
		</table>
	</div>
%endfor
