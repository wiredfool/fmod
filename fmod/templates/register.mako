<%inherit file="/base.mako" />
<%def name="head_tags()">
	<title>Register</title>
</%def>

<p>
${c.msg}
</p>
<p>
${h.form('/register/submit', method='post')}
Username: ${h.text('username')}<br />
Password: ${h.password('password')}<br />
And Again: ${h.password('password_2')}<br />
${h.submit('Submit', 'Submit')}
${h.end_form()}

</p>