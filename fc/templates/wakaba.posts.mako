# -*- coding: utf-8 -*-
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
		%if t.OmittedPosts:
			<span class="omittedposts">${t.OmittedPosts}</span>
		%endif
		%for p in t.Replies:
			<table>
				<tbody>
					<tr>
						<td class="doubledash">&gt;&gt;</td>
						<td class="reply" id="reply${p.PostID}">
							<a name="${p.PostID}"></a>
							<label>
								<input type="checkbox" name="delete" value="${p.PostID}" />
								<span class="replytitle"></span>
								<span class="commentpostername"></span>
								${p.Date}
							</label>
							<span class="reflink">
								<a href="${p.PostID}#i${p.PostID}">${p.PostID}</a>
							</span>
							&nbsp;  
							<blockquote>
								${p.Message}
							</blockquote> 
						</td>
					</tr>
				</tbody>
			</table>
		%endfor
	</div>
%endfor
