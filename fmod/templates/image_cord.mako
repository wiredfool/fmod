<%inherit file="/base.mako" />
<%def name="head_tags()">
	<title>Image View -- ${c.atts['title']}</title>
</%def>

<a href="${c.atts['photo_url']}"><img src="${c.atts['img_url']}" align='right' /></a>
<div><h2><a href="${c.atts['photo_url']}">${c.atts['title']}</a></h2>
${c.atts['description']}<br />
--<br />
<% 
if len(c.atts['tags']): 
	context.write('<b>Tags:</b> %s<br />' % (', '.join(c.atts['tags']))) 
if len(c.atts['notes']): 
	context.write('<b>Notes:</b> %s<br />' % (', '.join([s.strip() for s in c.atts['notes']]))) 
if len(c.atts['comments']): 
	context.write('<b>Owner Comments:</b><br />%s<br />' % ('<br /> '.join(c.atts['comments']))) 
%>
</div>
<br clear='all' />