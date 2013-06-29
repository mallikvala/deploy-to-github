# Usage:
# 	python deploy.py target-project-dir
#
# Description:
# 	This script reads your pom.xml file in your 'target-project-dir' to locate
# 	proper github repository to deploy to.
#
# Requirements:
#	- python 2.x installed
# 	- git installed

import os,sys
from xml.etree import ElementTree

class pom_obj:
	def __init__(self, target_project_dir):
		import re

		pom_path = os.path.join(target_project_dir, "pom.xml")
		self.project = ElementTree.parse(pom_path).getroot()
		self.ns_prefix = re.search("{.+}", self.project.tag).group(0)

		self.group_id = self._find('groupId').text
		self.artifact_id = self._find('artifactId').text
		self.version = self._find('version').text
		self.is_snapshot = self.version.endswith('-SNAPSHOT')

		if self.is_snapshot and self._find('distributionManagement/snapshotRepository') is not None:
			self.repo_url = self._find('distributionManagement/snapshotRepository/url').text
			self.repo_id = self._find('distributionManagement/snapshotRepository/id').text
			self.repo_git_url = self._get_repo_git_url(self.repo_url)		
		else:
			self.repo_url = self._find('distributionManagement/repository/url').text
			self.repo_id = self._find('distributionManagement/repository/id').text
			self.repo_git_url = self._get_repo_git_url(self.repo_url)

	def _ns_path(self, xml_path):
		return '/'.join([self.ns_prefix + t for t in xml_path.split('/') if t != '.'])

	def _find(self, xml_path):
		return self.project.find(self._ns_path(xml_path))

	def _findall(self, xml_path):
		return self.project.findall(self._ns_path(xml_path))

	def _get_repo_git_url(self, repo_url):
		from urlparse import urlparse

		o = urlparse(self.repo_url)
		p = o.path.split('/')
		return o.scheme+"://"+o.netloc+"/"+p[1]+"/"+p[2]+".git"


def clone_temp_local_repo(pom):
	import random, string

	temp_local_dir = None
	for i in range(5):
		temp_dir = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
		if not os.path.exists(temp_dir):
			temp_local_dir = temp_dir
			break

	if not temp_local_dir:
		print "Failed to create a temporary local clone directory. Try again."
		return None

	if os.system("git clone -n "+pom.repo_git_url+" "+temp_local_dir):
		print "Failed to clone from the remote repository: " + pom.repo_git_url

	return temp_local_dir

def push_to_remote_repo(deploy_path, pom):
	os.chdir(deploy_path)

	files_to_add = []

	for root, dirs, files in os.walk(deploy_path):
		files_to_add.extend([os.path.join(root, f) for f in files])

	commit_msg = pom.group_id+":"+pom.artifact_id+":"+pom.version

	os.system("git add "+" ".join(files_to_add))
	os.system("git commit "+" ".join(files_to_add)+" -m '"+commit_msg+"'")
	os.system("git push origin master")

def deploy(target_project_dir):
	current_dir = os.getcwd()
	target_project_dir = os.path.abspath(target_project_dir)
	if not os.path.exists(target_project_dir) or not os.path.isdir(target_project_dir):
		print "Target directory does not eixst or is not a directory: " + target_project_dir
		return

	try:
		pom = pom_obj(target_project_dir)
	except:
		print "Failed to load pom.xml. Make sure the file exists and it contains all required info: groupId, artifactId, version, and, distributionManagement.repository."
		return

	temp_local_dir = clone_temp_local_repo(pom)
	if not temp_local_dir:
		return

	temp_local_dir = os.path.abspath(temp_local_dir)

	os.chdir(target_project_dir)

	deploy_path = os.path.join(temp_local_dir, "releases")
	update_release = "-DupdateReleaseInfo=true"
	if pom.is_snapshot:
		deploy_path = os.path.join(temp_local_dir, "snapshots")
		update_release = "-DupdateReleaseInfo=false"
	
	deploy_command_line = "mvn -DaltDeploymentRepository="+pom.repo_id+"::default::file:"+deploy_path+" "+update_release+" clean deploy"

	if os.system(deploy_command_line):
		print "Deploy failed."
		return

	push_to_remote_repo(deploy_path, pom)

	import shutil
	shutil.rmtree(temp_local_dir)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "usage: python "+os.path.basename(__file__)+" target-project-dir"
		exit(1)

	deploy(sys.argv[1])
