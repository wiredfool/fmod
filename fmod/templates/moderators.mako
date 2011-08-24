# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<%def name="head_tags()">
	<title>Moderators</title>
</%def>
<%def name="menu()">
</%def>

<div class="yui-ge">
    <div class="yui-u first">
		<div class="yui-gd">
    		<div class="yui-u first">
				
	    		</div>
    		<div class="yui-u">
			<h1>Moderators</h1>

<p>This site is designed to help the Strobist group moderators moderate the pool 
more effectively. We are doing this by using the biggest asset we have,
members. To do that, we ask that interested members of the group flag images
that are not following the group guidelines. They have been doing this with the 
no-strobist-info tag -- this is the next generation. 
</p>

<p><h2 class='inline'>Step 1</h2> is to <a href='/flickr/login_user'>authenticate</a> with flickr. 
This site uses the write permission level. We need this permission to add tags to images and 
to remove images from the group pool. (and in the future, comment and flickrmail the owners 
of the images that we bounce) We store the necessary authentication token in the session
information, and it is cleared when you log out. We do not store it in the database. 
</p>

<p><h2 class='inline'>Step 2</h2> is to visit the <a href='/ping/index'>moderator queue</a>. If you're really a moderator,
there's a line of options across the top of each image to evaluate. <ul>
<li>Keep in pool does nothing
to the image on flickr, it just clears the ping and marks the image as ok. </li>
<li>Not Strobist tags the image not-strobist and removed-from-strobist-group, then removes it 
from the group. Good for those random shots in ambient light. </li>
<li>No Strobist Info tags the image no-strobist-info and removed-from-strobist-group, then removes it 
from the group.  </li>
<li>NSFW tags the image NSFW and removed-from-strobist-group, then removes it 
from the group.  </li>
<li>Defer Decision removes the image from the page, but leaves it in the queue for the 
next time you or another moderator visits the moderation queue.</li>
</ul>
These options are done with your credentials, so people will see that you have added
tags to their images. 
</p>


<p><h2 class='inline'>Step 3</h2> (optional) is to install the <a href='/profile/bookmarklet'>bookmarklet</a> in your web browser. Bookmarklets are small snippets
of javascript that run when you trigger them like a bookmark (or favorite) and can perform a 
small action. This will let you experience the group member side of things.</p>

<p><h2 class='inline'>Step 4</h2> (optional) is to browse the Strobist flickr group. 
When you are on an image page and it needs to be flagged, trigger the bookmarklet. 
When triggered, The bookmarklet contacts this server with the image's id and 
along with your username and a signature of the request. Then you can go review the image,
or leave it for someone else. 
</p>

	    		</div>
			</div>

	    </div>
    <div class="yui-u">
		
	    </div>
</div>



