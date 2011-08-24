# -*- coding: utf-8 -*-
<%def name="head_tags()">
</%def>
<%def name="menu()">
<ul id='menu'>
	<li><a href='/flickr/members' class='l50'>Member Info</a></li>
	<li><a href='/flickr/moderators' class='l50'>Moderator Info</a></li>
	<li><a href='/profile/bookmarklet'>Get the Bookmarklet</a></li>
	<li><a href='/ping/index'>Moderator's Ping Queue</a>
	<li><a href='/browse/index'>Moderator's Browse View</a>
	<li><a href='/ping/rss'>RSS Feed of Pings</a></li>
</ul>
</%def>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    ${self.head_tags()}
	<!-- Combo-handled YUI CSS files: --> 
	<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?2.7.0/build/reset-fonts-grids/reset-fonts-grids.css&2.7.0/build/base/base-min.css"> 
	<script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.3.1/jquery.min.js'></script>  
	<link rel='stylesheet' type='text/css' href='/site.css'> 
	</head>
  <body>
<div id="doc2" class="yui-t7">
   <div id="bd">
	<div class="yui-ge">
    <div class="yui-u first" id='hd'>
		<h1><a href='/'>Strobist RoboMod</a><h1>
	    </div>
    <div class="yui-u">
% if c.username:
Logged in as ${c.username}. <a href='/logout'>Logout</a>
% else:
 You're not logged in. <a href='/flickr/login_user'>Login ( as a user )</a> or 
 <a href='/flickr/login'>Login ( as a moderator )</a>.
% endif
	    </div>
</div>
<div>
	${self.menu()}
	<br clear='all' />
	${self.body()}
		</div>

	</div>
   <div id="ft">This site is a production of Eric Soroos, aka wiredfool. Site code copyright Eric Soroos, 2009.</div>
</div>

  </body>
</html>