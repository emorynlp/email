# email-mining

# enron

This goal of this project is to convert the original [Enron Email Dataset](https://www.cs.cmu.edu/~./enron/) into json format.

# Environment Setup:

Python verison >= 3.6.0

```
git clone git@github.com:emorynlp/email-mining.git
cd enron-data-parser
pip install -r requirements.txt
```

# Data set

[Download data set (May 7, 2015 Version of dataset)](https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tgz) from [Enron Email Dataset](https://www.cs.cmu.edu/~./enron/).

Unzip the file and put it under `enron-data-parser/` directory. The folder name is `maildir`

# Usage:

- Create `data` forlder:

```
mkdir data
```

## Generate json with original content:

```
python enron2json.py maildir data/email.threads.json data/number.cs
```

