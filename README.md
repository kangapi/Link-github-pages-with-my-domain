This small python script allow me to enable GitHub pages and set a custom domain.
It also adds a record on cloudflare to link with GitHub pages.
I use [typer](https://typer.tiangolo.com) to create a CLI.

To link a domain with GitHub pages the script make this actions :
* Add a CNAME record on Cloudflare dns zone
* Enable GitHub pages on the repo
* Set the custom domain on GitHub pages
* Check the dns propagation
* Check the workflow run status for GitHub pages
* Check is the HTTPS certificate is valid
* Enforce HTTPS on GitHub pages

Basic usage : `python main.py add <sub-domain> <repo-name>` and `python main.py remove <sub-domain> <repo-name>`
