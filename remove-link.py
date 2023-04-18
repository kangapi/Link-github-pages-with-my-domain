import sys
import method

sub_domain = sys.argv[1]
repo_name = sys.argv[2]

github = method.Github()
cloudflare = method.Cloudflare()

github.repo_name = repo_name

disable_github_pages_response = github.disable_github_pages()
if disable_github_pages_response.status_code == 204:
    print("Successfully disabled GitHub Pages")
else:
    print("Failed to disable GitHub Pages")
    print("Error: " + disable_github_pages_response.text)
    print("Error response status code: " + disable_github_pages_response.status_code)

delete_CNAME_record_response = cloudflare.delete_CNAME_record(sub_domain)
if delete_CNAME_record_response.status_code == 200:
    print(f"Successfully deleted CNAME record for {sub_domain}.{github.root_domain}")
else:
    print(f"Failed to delete CNAME record for {sub_domain}.{github.root_domain}")
    print("Error: " + delete_CNAME_record_response(sub_domain).text)
    print("Error response status code: " + delete_CNAME_record_response.status_code)