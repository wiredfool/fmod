<a href="${c.atts['photo_url']}"><img src="${c.atts['img_url']}" align='right' /></a>
<div class='d_image_info'>
<h2 style='display:inline;'><a href="${c.atts['photo_url']}">${c.atts['title']} 
-- ${c.atts['username']}</a></h2> 
<a href='http://flickr.com/groups/${request.environ['pylons.pylons'].config['group_id']}/pool/${c.atts['owner']}/' title='View all from this user in the pool'>(view all)</a><br />
<br />
<% context.write(c.atts['description']) %>
<br />
--<br />
<% 
if len(c.atts['tags']): 
	context.write('<b>Tags:</b> %s<br />' % (', '.join(c.atts['tags']))) 
if len(c.atts['notes']): 
	context.write('<b>Notes:</b> %s<br />' % (', '.join([s.strip() for s in c.atts['notes']]))) 
if len(c.atts['comments']): 
	context.write('<b>Owner Comments:</b><br />%s<br />' % ('<br /> '.join(c.atts['comments']))) 
if (c.atts['ctHistory'] > 1):
	context.write("<br clear='all'>This image has been seen %s time(s) in the pool and moderated %s time(s)." %
					  			   (c.atts['ctHistory'],c.atts['ctDecisions']))
%>
</div>
<br clear='all' />