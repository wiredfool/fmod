# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
	<atom:link href="http://fmod.wiredfool.com/ping/rss" rel="self" type="application/rss+xml" />
    <title>Pinged Images</title>
    <link>http://fmod.wiredfool.com/ping/index</link>
    <description>Pings from the strobist group</description>
    <pubDate>${c.fmtTime()}</pubDate>
    <generator>http://fmod.wiredfool.com/</generator>
    <language>en</language>
% for (ping,img) in c.items: 
<item>
    <title>${img.atts['title']}</title>
    <link>http://www.flickr.com/photos/${ping.owner}/${ping.image}/in/pool-strobist</link>
    <pubDate>${c.fmtTime(ping.dt)}</pubDate>
    <guid isPermaLink="false">${ping.owner}/${ping.image}/${ping.id}</guid>
    <description>
	${img.atts['username']} uploaded a photo: &lt;img src="${img.atts['img_url']}" /&gt;
	</description>
	<content:encoded><![CDATA[	
	Reported by: ${ping.username}<br />
${img.atts['username']} uploaded a photo:
<a href="${img.atts['photo_url']}"><img src="${img.atts['img_url']}" align='right' /></a>
${img.atts['description']}<br />
--<br />
<%
if len(img.atts['tags']): 
	context.write('<b>Tags:</b> %s<br />' % (', '.join(img.atts['tags']))) 
if len(img.atts['notes']): 
	context.write('<b>Notes:</b> %s<br />' % (', '.join([s.strip() for s in img.atts['notes']]))) 
if len(img.atts['comments']): 
	context.write('<b>Owner Comments:</b><br />%s<br />' % ('<br /> '.join(img.atts['comments']))) 
%>]]></content:encoded>
    </item>	
%endfor 
</channel>
</rss>