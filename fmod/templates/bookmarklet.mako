# -*- coding: utf-8 -*-
<%inherit file="/base.mako" />
<%def name="head_tags()">
	<title>Bookmarklet</title>
</%def>
<p>Firefox/Safari users -- drag this link: <a class='bookmarklet' href="javascript:(function(){var d=document;var i=d.createElement('script'),nsid='${c.nsid}',s='${c.secret}',q,b='${c.url}?';if(window.page_p){p=page_p;q='nsid='+nsid+'&id='+p.id+'&own='+p.ownerNsid+'&sec='+p.secret+'&con='+nextprev_currentContextID;i.src=b+q+'&s='+md5_calcMD5(q+s);d.body.appendChild(i);}else{var f=FLICKR.photo;q='nsid='+nsid+'&id='+f.getId()+'&own='+f.getOwner()+'&v=2';YUI({modules:{'gallery-crypto-md5':{fullpath:'http://fmod.wiredfool.com/md5.js'}}}).use('gallery-crypto-md5',function(Y) {i.src=b+q+'&s='+Y.Crypto.MD5(q+s);d.body.appendChild(i);})}})();">Flag</a> to your bookmarks bar. IE users -- make it a favorite using the right click menu, Opera users can shift-drag it to the toolbar.
</p>

<p>
When you're viewing an image page on flickr (an individual image, not a pool or set) activating on this bookmarklet will send some info about the image to this server. If the image is in the strobist group, it will be flagged for review by the moderation team. You can activate a bookmarklet by choosing it from the bookmarks meny, clicking on the bookmarks bar, or in Safari, cmd-[1-9] if it's in one of the first 9 spots on the bookmarks bar. 
</p>

<p>
This is the bookmarklet code for the concerned or curious. It assembles some information from the page that flickr provides, adds your username, signs all that, then sends it to this server. The returned script then adds a (Flagged) notation on the group pool entry.
<pre>
javascript:(function(){
	var d=document;var i=d.createElement('script'),nsid='${c.nsid}',s='${c.secret}',q,b='${c.url}?';
	if(window.page_p){
		p=page_p;
		q='nsid='+nsid+'&id='+p.id+'&own='+p.ownerNsid+'&sec='+p.secret+'&con='+nextprev_currentContextID;
		i.src=b+q+'&s='+md5_calcMD5(q+s);
 		d.body.appendChild(i);
	}else{
		var f=FLICKR.photo;
		q='nsid='+nsid+'&id='+f.getId()+'&own='+f.getOwner()+'&v=2';
		YUI({modules:{'gallery-crypto-md5':{fullpath:'http://fmod.wiredfool.com/md5.js'}}}
		   ).use('gallery-crypto-md5',function(Y) {
			i.src=b+q+'&s='+Y.Crypto.MD5(q+s);
 			d.body.appendChild(i);
		})
	}})();
</pre>
</p>

