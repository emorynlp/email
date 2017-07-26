---
layout: default
title: ""
description: ""
---

# Email Mining

The goal of this project is to convert the original [Enron Email Dataset](https://www.cs.cmu.edu/~./enron/){:target="_blank"} into mordern format for investigation.


# Data set

- [May 7, 2015 Version of dataset](https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tgz){:target="_blank"} from [Enron Email Dataset](https://www.cs.cmu.edu/~./enron/){:target="_blank"}.

# Format Data

- [email.json](https://www.cs.cmu.edu/~./enron/){:target="_blank"}

This `enron.json` file contains all emails which are extracted from the dataset. The hierarchy of json is same as the original directory.  

- [email.all.json](https://www.cs.cmu.edu/~./enron/){:target="_blank"}

`email.all.json` is similiar with previous file, `enron.json`, but without the hierarchy. It only has an array of json. Inside the array, each json object is an email. 

- [email.all.json](https://www.cs.cmu.edu/~./enron/){:target="_blank"}

`email.threads.json` is like `email.all.json`, but only has emails containing threads. 

