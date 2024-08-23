### Everything

Installation

Make sure you have at least python 3.10 installed.

pip install -r requirements.txt

create a .env file and add the following keys

You can get geocoding api key from this website (no payment is required): https://www.geoapify.com/reverse-geocoding-api/

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

The program functions as a proactive and independent personal assistant for a user based on their data. It has access to a suite of tools in order to properly do it's job. I used claude sonnet and haiku.


### Testing
To run tests. Have pytest installed and run `pytest tests`




