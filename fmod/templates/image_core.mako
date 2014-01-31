# -*- coding: utf-8 -*-
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
	context.write('<b>Tags:</b> %s<br />' % (', '.join(s for s in c.atts['tags'] if s))) 
if len(c.atts['notes']): 
	context.write('<b>Notes:</b> %s<br />' % (', '.join([s.strip() for s in c.atts['notes'] if s]))) 
if len(c.atts['comments']): 
	context.write('<b>Owner Comments:</b><br />%s<br />' % ('<br /> '.join(s for s in c.atts['comments'] if s))) 
if (c.atts['ctHistory'] > 1):
	context.write("<br clear='all'>This image has been seen %s time(s) in the pool and moderated %s time(s).  " %
								   (c.atts['ctHistory'],c.atts['ctDecisions']))
arrMod = []
if c.atts['ctNsi']:
	arrMod.append('%s no strobist info' % c.atts['ctNsi'])
if c.atts['ctBump']:
	arrMod.append('%s for bumping' % c.atts['ctBump'])
if c.atts['ctOk']:
	arrMod.append('%s ok' % c.atts['ctOk'])
if len(arrMod):
   context.write(', '.join(arrMod))
if c.atts['history'] and c.atts['ctHistory'] > 1:
	context.write("<br />Bumps (GMT): "+', '.join([h for h in c.atts['history'] if h]))
%>
</div>
<br clear='all' />