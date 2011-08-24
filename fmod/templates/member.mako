# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<%def name="head_tags()">
	<title>Group Member Info</title>
</%def>
<%def name="menu()">
</%def>

<div class="yui-ge">
    <div class="yui-u first">
		<div class="yui-gd">
    		<div class="yui-u first">
				
	    		</div>
    		<div class="yui-u">
			<h1>Group Members</h1>

<p>This site is designed to help the Strobist group moderators moderate the pool 
more effectively. We are doing this by using the biggest asset we have,
members. To do that, we ask that interested members of the group flag images
that are not following the group guidelines. 
</p>

<p><h2 class='inline'>Step 1</h2> is to <a href='/flickr/login_user'>authenticate</a> with flickr. 
This site uses the lowest level of
permissions that flickr offers. For users, we do not store the 
authentication token that flickr returns. We do not access your account
for any reason other than to verify your flickr username and id. 
</p>

<p><h2 class='inline'>Step 2</h2> is to install the <a href='/profile/bookmarklet'>bookmarklet</a> in your web browser. Bookmarklets are small snippets
of javascript that run when you trigger them like a bookmark (or favorite) and can perform a 
small action. </p>

<p><h2 class='inline'>Step 3</h2> <img src='/flagged.jpg' width=210 height=68  style='display:block;right:30px;position:absolute;'>is to browse the Strobist flickr group. When you are on an image page and that image does not
have the necessary strobist information, is not safe for the pool, or does not use off camera flash,
trigger the bookmarklet. When triggered, the bookmarklet contacts this server with the image's id and 
along with your username and a signature of the request. You should see a confirmation that the image has been flagged. A moderator will review the image. 
</p>

<p>Remember that there are some images that don't need strobist info -- setup shots, diy mods
and other explanatory images are ok, even if it doesn't say how they were lit. </p>

	    		</div>
			</div>

	    </div>
    <div class="yui-u">
		
	    </div>
</div>



