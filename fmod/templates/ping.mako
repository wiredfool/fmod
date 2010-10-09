<%inherit file="/base.mako" />
<%def name="head_tags()">
	<title>Pings</title>
</%def>
<%include file='ping.js' />
<div id='d_pings'>
%for ping in c.results: 
<% 
c.atts = ping.Image_fromPing().all_atts()
c.image = ping.image
c.ping = ping
%>
<%include file='one_ping.mako' />
%endfor
</div>

<div id='d_nopings'>
<p>There are no pings right now...</p>
</div>

<div id='d_addpings'>
<p><a onclick='onMorePings();return false;' title='Show 5 More Pings' href='#' class='a_more'>[+]</a></p>
</div>