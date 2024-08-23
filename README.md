### Everything

Installation

Make sure you have at least python 3.10 installed.

pip install -r requirements.txt

create a .env file and add the following keys

You can get geocoding api key from this website (no payment is required): https://www.geoapify.com/reverse-geocoding-api/ but to make it easier the key i use can be found here: https://onetimesecret.com/secret/69f3px1of5qhz7qismem07w4acgon5b

You can get an anthropic api key by visiting console.anthropic.com

```
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_KEY
OPENAI_API_KEY=ADD_HERE # optional
GEOCODING_API_KEY=HERE
```

Once added, simply run the following command
```zsh
python main.py
```


### How it works

The program functions as a proactive and independent personal assistant for a user based on their data. It has access to a suite of tools in order to properly do it's job. 

1. Once it is running the program will undergo what it believes the most proactive and helpful form of actions. 

2. At the end of every turn it will request input from the user. Here you can ask it for more information or undergo more actions. This will help it learn how to best help the user.

3. It is simulating a day in the life so only runs for 15 turns in total (but you can interrupt it at any point)


My approach is a combination of Tool calling and Chain of Thought.

I use tool calling in order for the AI to interact with the users data and make changes where it deems appropriate. In addition it allows the AI to get information from third parties (e.g getting up to date  location data for directions)

I used Chain of Thought in order for the tool to reason better with the data it is provided. I acheive this with a combination of prompt and recursive method calling.


### Drawbacks
You will need an Anthropic API key to use this tool. It uses Claude 3.5 Sonnet by default, but if you have low API Rate limits it will move to using Haiku.

### Testing
To run tests. Have pytest installed and run `pytest tests`




