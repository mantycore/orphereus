function createElementEx(strTagName, arrAttrs, arrChildren)
{
	var objElement = document.createElement(strTagName);
	for (strIndex in arrAttrs)
	{
		objElement.setAttribute(strIndex, arrAttrs[strIndex]);
	}
	for (strIndex in arrChildren)
	{
		objElement.appendChild(arrChildren[strIndex]);
	}
	return objElement;
}
function getElementsByClass(searchClass, domNode, tagName)
{
	if (domNode == null)
		domNode = document;
	if (tagName == null)
		tagName = '*';
	var el = new Array();
	var tags = domNode.getElementsByTagName(tagName);
	var tcl = " "+searchClass+" ";
	for(i=0,j=0; i<tags.length; i++)
	{
		var test = " " + tags[i].className + " ";
		if (test.indexOf(tcl) != -1)
			el[j++] = tags[i];
	}
	return el;
}