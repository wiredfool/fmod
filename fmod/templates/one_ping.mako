<div id='d_ping_${c.ping.id}' class='d_ping_image'>
%if c.fl_mod:
	<%include file='decision.mako' />
%endif
	<%include file='image_core.mako' />
%if c.ping.username:
	 Reported by: ${c.ping.username} 
%endif
%if c.ping.reason == 'Bump':
	for bumping.
%endif
<p></p>
</div>
