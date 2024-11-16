# 👋 Introduction

Toolhouse is a platform that helps developers integrate tools in their projects, to build powerful AI agents. You can start this journey with only 3 lines of code in your app.

# ℹ️ Getting Started

This sample application is built with Flask and uses Anthropic and Toolhouse. Follow along to make changes to your copy of this repository! For ease of use, you only have to install the dependencies once.

## Requirements

- A [Toolhouse](https://toolhouse.ai) account. If you don't have one already, follow this [link](https://join.toolhouse.ai).
- An [Anthropic](https://www.anthropic.com/) account.

# 🛠️ Installation

To install, clone this repository.

``` bash
git clone https://github.com/toolhouse-community/sample-flask.git
cd sample-flask
```

Create a `.env` file and ensure that you have exported both Toolhouse and Anthropic API Keys in it.

```bash
ANTHROPIC_API_KEY='YOUR-ANTHROPIC-KEY'
TOOLHOUSE_API_KEY='YOUR-TOOLHOUSE-KEY'
```

## Install the Required Dependencies

### With Virtual Environment (Preferred)

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Without Virtual Environment

```bash
pip install -r requirements.txt
```

If you don't have Flask pre-installed, execute the following:

```bash
pip install Flask
```

# ⚒️ Setup Toolhouse

Head over to the [Toolstore](https://app.toolhouse.ai/) and install the tools you'd like the LLM to use.

Tools are serverless functions that run on the Toolhouse infrastructure, and empower LLMs with new functionalities like scraping the internet, a particular website, or sending emails.

Additionally, you can also create and use [Bundles](https://docs.toolhouse.ai/toolhouse/bundles) to reduce hallucinations and avoid unnecessary credit consumption. All you need to do is pass the Bundle name in Line 63 of `app.py`.

# 🏃 Run the Application

In your terminal, execute the following command to start the application.

```bash
flask run
```

By default, the Flask app runs on port=5000. Head over to the URL on your terminal and see the application in action.

# 💡 Make Changes

If you'd like to use the application out of the box with your own ideas, make changes to the `system_message` prompt, in Line 24 of `app.py`.

To make changes to the interface, edit `templates/index.html`.

# 📚 Learn More

To learn more about Toolhouse, [read our documentation](https://docs.toolhouse.ai/toolhouse)! We also have a thriving community on [Discord](https://discord.gg/xPvyBxhHtu) and would love to have you join us!