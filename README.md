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

Create a github repo that you will use as your Maven repository.

```
Example: https://github.com/d5/mvn-repo
```

In `pom.xml` file of your your Java project that you want to deploy to github, add the following:


```
  <distributionManagement>
    <repository>
      <id>d5-repo</id>
      <url>https://github.com/d5/mvn-repo</url>
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
        <id>d5-repo</id>
        <url>https://github.com/d5/mvn-repo/raw/master</url>
    </repository>
</repositories>

<dependencies>
  <dependency>
    <groupId>gs.daniel.examples</groupId>
    <artifactId>helloworld</artifactId>
    <version>1.1</version>
  </dependency>
</dependencies>
```
