#!/usr/bin/env python3
# coding=utf-8
#
# <xbar.title>Service Monitor</xbar.title>
# <xbar.version>v0.1</xbar.version>
# <xbar.author>Cristian</xbar.author>
# <xbar.author.github>cmaluend</xbar.author.github>
# <xbar.desc>Ping the services and create a dropdown report</xbar.desc>
# <xbar.image>https://cmaluend.github.io/images/xbar/servicemonitor.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>
#
# by Cristian
import subprocess
import sys
from multiprocessing import Pool

try:
	import requests
except:
	subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

TITLE = "My Services"
'''
SERVICES = {
	"tier: [
		{
			"name": "Service name",
			"endpoint": "https://httpstat.us/200",
			"headers": {}							#optional
			"method": "GET",						#optional
			"body": {} 								#optional 
			"status_code": 200
		}
	]
}
'''
SERVICES = {
	"dev": [
		{ 
			"name": "service 1",
			"endpoint": "https://httpstat.us/200",
			"headers": {
				"Content-type": "text/html"
			},
			"status_code": 200
		},
		{ 
			"name": "service 2",
			"endpoint": "https://httpstat.us/400",
			"status_code": 200
		},
	],
	"uat": [
		{ 
			"name": "service 1",
			"endpoint": "https://httpstat.us/200",
			"status_code": 200
		},
	]
}
# green: \x1b[42m
# red: \x1b[41m
# blue: \x1b[44m
HEALTHY='\x1b[42m'
UNHEALTHY='\x1b[41m'
NC='\x1b[0m'

def process_environments():
	envs = SERVICES.keys()
	result = {}
	for env in envs:
		result[env] = process_services(SERVICES[env])
	return result

def process_services(services):
	servicesnames = [ x["name"] for x in services]
	with Pool() as pool:
		result = pool.map(call_service, services)
	return dict(zip(servicesnames, result))

def call_service(service):
	method =  service["method"] if "method" in service.keys() else "GET"
	data = service["body"] if "body" in service.keys() else None
	headers = {"user-agent":"xbar"}
	if "headers" in service.keys():
		headers.update(service["headers"])
	
	healthy = False
	try:
		response = requests.request(method=method, url=service["endpoint"], headers=headers, data=data, timeout=10)
		if response.status_code == service["status_code"]:
			healthy = True
	except Exception as err:
		pass
	return { 'healthy': healthy }

def create_dropdown_report(values):
	summary = ""
	menu = "\n---"
	for env in values.keys():
		healthy = True
		envmenu = ""
		servicemenu = ""
		for servicename in values[env].keys():
			service = values[env][servicename]
			if not service["healthy"]:
				healthy = False
			servicemenu += f'\n--{get_icon(healthy)} {servicename}'
		envmenu = f'\n{get_icon(healthy)} {env}{servicemenu}'
		menu+= envmenu
		summary += get_env_colored(env, healthy)

	return f'{summary}{menu}'
	
def get_icon(healthy):
	return "🟢" if healthy else "🔴"

def get_env_colored(env, healthy):
	color = HEALTHY if healthy else UNHEALTHY
	return f'{color} {env} {NC}'

def main():
	servicesStatus = process_environments()
	report = create_dropdown_report(servicesStatus)
	print(f'{TITLE}: {report}')

if __name__ == "__main__":
	main()
