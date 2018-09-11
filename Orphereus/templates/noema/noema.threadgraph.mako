# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

<form action="${h.url_for('graphForThread', post=c.postId)}" method="get">
<label><input type="checkbox" name="showThreadLines"/>${_('Show post order lines on graph')}</label><br/>
<label><input type="checkbox" name="showGreenLabels"/>${_('Show green prooflabels')}</label><br/>
<label><input type="checkbox" name="showRedLabels"/>${_('Show red prooflabels')}</label><br/>
<label><input type="checkbox" name="showYellowLabels"/>${_('Show yellow prooflabels')}</label><br/>

${_('Image format:')}
<select name="format">
  <option value="png" selected="selected">PNG</option>
  <option value="jpg">JPG</option>
  <option value="svg">SVG</option>
  <option value="gif">GIF</option>
</select>
<br/>
<input type="hidden" name="proceed" value="" />
<input type="submit" value="${_('Make graph!')}" />
</form>

<hr/>
