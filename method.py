import json
import requests
import config

class Cloudflare:
    def __init__(self):
        self.header = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + config.cloudflare_token
        }
        self.api_url = "https://api.cloudflare.com/client/v4"
        self.zone_id = "6ccce59a23211dfcd03e565be3362edf"
        self.record_content = "kangapi.github.io"
        self.record_comment = "Added with my python script"
        self.record_type = "CNAME"
        self.github_class = Github()

    def list_DNS_records(self):
        url = f"{self.api_url}/zones/{self.zone_id}/dns_records"
        payload = {}
        response = requests.request("GET", url, headers=self.header, data=payload)
        return response

    def add_CNAME_record(self, sub_domain):
        url = f"{self.api_url}/zones/{self.zone_id}/dns_records"
        payload = json.dumps({
            "content": self.record_content,
            "name": sub_domain,
            "proxied": False,
            "type": self.record_type,
            "comment": self.record_comment
        })
        response = requests.request("POST", url, headers=self.header, data=payload)
        return response

    def delete_CNAME_record(self, record_name):
        record_list = self.list_DNS_records().json()
        for record in record_list["result"]:
            if record["name"] == record_name + "." + self.github_class.root_domain:
                if record["type"] == "CNAME":
                    if record["content"] == self.record_content:
                        if record["comment"] == self.record_comment:
                            url = f"{self.api_url}/zones/{self.zone_id}/dns_records/{record['id']}"
                            payload = {}
                            response = requests.request("DELETE", url, headers=self.header, data=payload)
                            return response
                        else:
                            print("Comment is not " + self.record_comment)
                    else:
                        print("Content is not " + self.record_content)
                else:
                    print("Record type is not " + self.record_type)
        print("DNS record not found")
        return False


class Github:
    def __init__(self):
        self.header = {
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + config.github_token,
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json'
        }
        self.api_url = "https://api.github.com"
        self.repo_name = "memo"
        self.user_name = "kangapi"
        self.root_domain = "kangapi.fr"
        self.workflow_id = None
        self.workflow_run_id = None

    def enable_github_pages(self):
        url = f"{self.api_url}/repos/{self.user_name}/{self.repo_name}/pages"
        payload = json.dumps({
            "source": {
                "branch": "main",
                "path": "/"
            }
        })
        response = requests.request("POST", url, headers=self.header, data=payload)
        return response

    def disable_github_pages(self):
        url = f"{self.api_url}/repos/{self.user_name}/{self.repo_name}/pages"
        payload = {}
        response = requests.request("DELETE", url, headers=self.header, data=payload)
        return response

    def set_custom_domain(self, sub_domain):
        url = f"{self.api_url}/repos/{self.user_name}/{self.repo_name}/pages"
        payload = json.dumps({
            "cname": sub_domain + "." + self.root_domain
        })
        response = requests.request("PUT", url, headers=self.header, data=payload)
        return response

    def check_DNS_status(self):
        url = f"{self.api_url}/repos/{self.user_name}/{self.repo_name}/pages/health"
        payload = {}
        response = requests.request("GET", url, headers=self.header, data=payload)
        while response.json() == {}:
            response = requests.request("GET", url, headers=self.header, data=payload)
        return response

    def enforce_HTTPS(self):
        url = f"{self.api_url}/repos/{self.user_name}/{self.repo_name}/pages"
        payload = json.dumps({
            "https_enforced": True
        })
        response = requests.request("PUT", url, headers=self.header, data=payload)
        return response

    def get_workflow_run_status(self):
        # Get workflow id
        url = f"{self.api_url}/repos/{self.user_name}/{self.repo_name}/actions/workflows"
        payload = {}
        first_workflow = requests.request("GET", url, headers=self.header, data=payload).json()["workflows"][0]
        self.workflow_id = first_workflow["id"]
        # Get workflow run id
        url = f"{self.api_url}/repos/{self.user_name}/{self.repo_name}/actions/workflows/{self.workflow_id}/runs"
        payload = {}
        first_workflow_run = requests.request("GET", url, headers=self.header, data=payload).json()["workflow_runs"][0]
        return first_workflow_run["status"]

