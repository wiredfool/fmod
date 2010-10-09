Hello World, the environ variable looks like: <br />

<br />
Globals:
<br />
${dir()}

<br />
Environment:
<br />

${request.environ}

<br />
Pylons:
<br />
${dir(request.environ['pylons.pylons'])}

<br />
Pylons.config:
<br />
${request.environ['pylons.pylons'].config}

<br />
uri
<br />
${request.environ['pylons.pylons'].config['base_uri']}<br />
${request.path.split('/')[1]}

<br />
Request:
<br />
${request}

<br />
Request:
<br />
${dir(request)}


<br />
Session
<br />
${c.session}
