import sys
import time
import method

cloudflare = method.Cloudflare()
github = method.Github()

sub_domain = sys.argv[1]
repo_name = sys.argv[2]

if repo_name is not None:
    github.repo_name = repo_name

add_CNAME_record_response = cloudflare.add_CNAME_record(sub_domain)

if add_CNAME_record_response.status_code == 200:
    print(f"Successfully added CNAME record for {sub_domain}.{github.root_domain}")
else:
    print(f"Failed to add CNAME record for {sub_domain}.{github.root_domain}")
    print("Error: " + add_CNAME_record_response(sub_domain).text)


enable_github_pages_response = github.enable_github_pages()
if enable_github_pages_response.status_code == 201:
    print("Successfully enabled GitHub Pages")
else:
    print("Failed to enable GitHub Pages")
    print("Error: " + enable_github_pages_response.text)


set_custom_domain_response = github.set_custom_domain(sub_domain)
if set_custom_domain_response.status_code == 204:
    print(f"Successfully set custom domain to {sub_domain}.{github.root_domain}")
else:
    print(f"Failed to set custom domain to {sub_domain}.{github.root_domain}")
    print("Error: " + set_custom_domain_response.text)

dns_status_response = github.check_DNS_status().json()

number_of_checks_dns = 0
while not dns_status_response["domain"]["dns_resolves"]:
    if number_of_checks_dns == 20:
        print("DNS propagation failed, please try again later")
        sys.exit(1)
    print("Waiting for DNS propagation...")
    time.sleep(10)
    dns_status_response = github.check_DNS_status().json()
    number_of_checks_dns += 1

print("DNS propagation successful")

workflow_run_status_response = github.get_workflow_run_status()
while workflow_run_status_response != "completed":
    print("Waiting for GitHub Pages build...(Actual status: " + workflow_run_status_response + ")")
    time.sleep(10)
    workflow_run_status_response = github.get_workflow_run_status()

print("GitHub Pages build successful")
print(f"Your website is available at http://{sub_domain}.{github.root_domain}")
print("TLS certificate is being provisioned. This may take up to 15 minutes to complete.")

number_of_checks_https = 0
while not dns_status_response["domain"]["responds_to_https"]:
    if number_of_checks_https == 40:
        print("TLS certificate generation failed, please try again later")
        sys.exit(1)
    print("Waiting for TLS certificate generation...")
    time.sleep(10)
    dns_status_response = github.check_DNS_status().json()
    number_of_checks_https += 1

print("TLS certificate generation successful")
print(f"Your website is available at https://{sub_domain}.{github.root_domain}")
print("Let's Enforce HTTPS !")

enforce_https_response = github.enforce_HTTPS()
if enforce_https_response.status_code == 204:
    print("Successfully enforce HTTPS")
else:
    print("Failed to enable HTTPS")
    print("Error: " + enforce_https_response.text)
    print("Response status code: " + str(enforce_https_response.status_code))

print("Enjoy your website !")
sys.exit(0)