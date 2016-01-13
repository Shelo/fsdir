File System Director
====================

The file system director is a system driven by the Structured File System Director Language (SFSDL). The main objective is to provide an easy to read syntax for file managment, trying to make it similar to an installation documentation.

As an example, consider creating an apache virtual host by a given template.conf:

```
# open the file in read-only mode.
READ '/etc/httpd/template.conf' COPYTO (/etc/httpd/conf.d/vh.conf)

# edit the file created before, find by regular expression 'template\.com' and set to 'somewebsite.com'
EDIT '/etc/httpd/conf.d/vh.conf' SETTO (template\.com) (somewebsite.com)
```

The features are:
- Run only when valid: all your code is pre-validated, no code will run until is fully valid.
- Sandbox: your code is first run into a sandbox that resembles your current file system.
- Apply the sandbox to the file system, no information is lost.
- Macros: (not used in the example).
- Search and replacement mechanics are regular expression driven (REGEX!).
- Export the code to an even easier to read documentation.
- Run bash commands from the script.
- Every feature is a plugin, extend the system to make it even more powerful.

This is a work in progress, an even more, an experimentation.
