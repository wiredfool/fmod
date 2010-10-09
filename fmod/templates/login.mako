<%inherit file="/base.mako" />
<%def name="head_tags()">
	<title>Login</title>
</%def>
<p>
${c.msg}
</p>
<p>
${h.form('/login/submit', method='post')}
Username: ${h.text('username')}<br />
Password: ${h.password('password')}<br />
${h.submit('Login', 'Login')}
${h.end_form()}

</p>