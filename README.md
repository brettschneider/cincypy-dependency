![Title Image](./etc/title_img.png)
# CincyPy 3/27/2025 Presentation on Dependency Injection #
By: Steve Brettschneider - steve.brettschneider@pinnsg.com

This is the source code from the demonstration of the Oooze dependency
injector from the 3/27/2025 [CincyPy](https://cincypy.com) meeting.

The accompanying PowerPoint presentation can be found here: 
[etc/CincyPy Dependency Injection.pptx](./etc/CincyPy%20Dependency%20Injection.pptx)

## Scripts ##

There are three demo scripts in this project:

1. **chatbots_1.py** - Demonstrates the `ooze.resvole()` function to manually retrieve a
   dependency from Ooze's dependency graph.
2. **chatbots_2.py** - Demonstrates using the `@ooze.start` decorator along with the
   `ooze.run()` function to kick off your script.
3. **agent.py** - Demonstrates using the `@ooze.magic` decorator.

## Project Setup ##
These demo scripts talk to the `llama3.1` LLM via [Ollama](https://ollama.com), a nice tool
for running AI/LLMs locally on your comptuer.  You will want to install Ollama and then
pull down the `llama3.1` model with the following command before running any of these
scripts:

```bash
$ ollama pull llama3.1
```

I use [pyenv](https://github.com/pyenv/pyenv) to have multiple versions of Python installed
on my computer at once.  This particular demo was built in Python 3.12.5, but I don't think
any remotely contemporary version will have issues (3.6+ should be fine).

I also use [Pipenv](https://pypi.org/project/pipenv/) to dependent-package management.  Like
`poetry`, `uv` and others, Pipenv allows me to manage my packages with a .lock file that
prevents issues with transient dependencies _(The packages that you install with pip have
dependencies on other packages.  Sometimes those other packages run into version conflicts.
Lock files help tamp that down.)_  It also allows you to see what packages dependend on what -
easily with the following command: `$ pipenv graph`.

```text
ollama==0.4.7
├── httpx
│   ├── anyio
│   │   ├── idna
│   │   ├── sniffio
│   │   └── typing_extensions
│   ├── certifi
│   ├── httpcore
│   │   ├── certifi
│   │   └── h11
│   └── idna
└── pydantic
    ├── annotated-types
    ├── pydantic_core
    │   └── typing_extensions
    └── typing_extensions
ooze==1.0.1
└── PyYAML
requests==2.32.3
├── certifi
├── charset-normalizer
├── idna
└── urllib3
```

Here are some commands that I use to get my environment up:

```bash
$ cd {wherever this project dir is}
$ pyenv local 3.12.5
$ pipenv install
```

## Running the scripts ##
Once your virtualenv is set up can can execute the scripts by simply executing them:

```bash
$ pipenv shell   # Acitvates the virtualenv that pipenv created for you.
(dependency) $ python chatbots_1.py
Me day be goin' swell, thank ye for askin' matey!
Iay amway havingay an amazingday so faray!
(dependency) $
(dependency) $ python chatbots_2.py
Me hearty! Day be sailin' along just fine, thank ye!
Oday isay excellentway, thank yousay!
(dependency) $
(dependency) $ python agent.py what the latest scanal in the whitehouse right now
Running from /Users/steve/Development/personal/cincypy/depdendency
Prompt: what the latest scanal in the whitehouse right now
Search tool engaged with query: latest scandal in the White House
Response: The latest scandal in the White House is the "Signal leak scandal" where sensitive military plans involving top Cabinet officials, including President Trump, were leaked through a group chat on the messaging service Signal.
(dependency) $ deactivate
$
```

### Two Small Disclaimers ###
* The `agent.py` script makes an API call to server.dev to obtain Google search
  results.  You will need to sign up for a [serper.dev](https://serper.dev) account
  and generate an API-KEY to run it.  Last time I checked serper.dev gives you 2,500
  API searches for free with signup (no credit card needed).  If you don't want to do
  that you can convert the search tool to using DuckDuckGo-Search.  That's free, but
  you may be subject to throttling.
* This code is provided for demonstration purposes only and is provided with
  no warranty or guarantee.  Use it at your own peril.

