# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<%def name="menu()">
</%def>
<%def name="head_tags()">
	<title>Profile Page</title>
</%def>

<p>
You're logged in as ${c.session['user']} 
</p>

<ul>
<li><a href='/profile/bookmarklet'>Get the Bookmarklet</a></li>
<li><a href='/ping/index'>See Recent Pings</a></li>
<li><a href='/ping/rss'>RSS Feed of Pings</a></li>
<li><a href='/logout'>Logout</a></li>
</ul>