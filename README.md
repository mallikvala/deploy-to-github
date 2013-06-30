deploy-to-github
================

Using `deploy.py` script, you can deploy your maven-based Java artifacts to the github. From other maven-based Java projects, your artifacts are accessible from the github.

This script is based on http://cemerick.com/2010/08/24/hosting-maven-repos-on-github/.

Requirements
------------

* You need a github account.
* You need `python` and `git` on your machine. 


Set up
------

Create a github repo that you will use as your Maven repository. Example:

```
https://github.com/d5/mvn-repo
```

In `pom.xml` file of your your Java project that you want to deploy to github, add the following:


```
  <distributionManagement>
    <repository>
      <id>my-repo</id>
      <url>https://github.com/your-github-account-name/your-repo-name</url>
    </repository>
  </distributionManagement>
```

Deploy
------

Run the following to deploy your artifacts to github.

```
python deploy.py path-to-your-project-dir
```

Then your artifact will be deployed to github and accessible from other Java project by adding the following to `pom.xml` file:

```
<repositories>
    <repository>
        <id>my-repo</id>
        <url>https://github.com/your-github-account-name/your-repo-name/raw/master</url>
    </repository>
</repositories>

<dependencies>
  <dependency>
    <groupId>your.artifact.group.id</groupId>
    <artifactId>your-artifact-id</artifactId>
    <version>your.artifact.version</version>
  </dependency>
</dependencies>
```

Example
-------

Under `example` directory, you can find 2 example projects:

* mathlib: example library project.
* helloworl: example application which has dependency on `mathlib` project.

Please refer to `pom.xml` file from these 2 projects to see how they're configured. 

These examples assume that GitHub repository is https://github.com/d5/mvn-repo. So, if you run:

```
python deploy.py example/mathlib
```

`mathlib` artifact will be built and deployed to https://github.com/d5/mvn-repo. (Of course, this will fail because you don't have my GitHub password; this is just an example.)

Then, when you build `helloworld` project, maven will download `mathlib` artifact from GitHub.
