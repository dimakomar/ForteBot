 # ForteBot
 Internal ForteGroup slack bot for Ternopil branch office
 
<img src="https://i.imgur.com/QjbPpNc.png">

## Made with
 * Python 3.6.2
 * Django 1.11.6
 
## Installation

Assuming you have a [Python](https://www.python.org) and [pip](https://pip.pypa.io/en/stable/installing/) installed
```bash
 pip install -r requirements.txt
```

```bash
 python manage.py runserver
```
## Features
>`/anon_msg`  *your_msg* - Use it to send anonymus feedback

>`/anon_msg_random`  *your_msg* - Use it to send anonymus message to *#random*, channel

>`/start_temperature_vote` - Use it to start default temperature vote 

>`/start_question_vote` *your_msg* - Use it to start question vote 

>`/start_rating_vote` *your_msg* - Use it to start custom text vote with rating 

>`/get_results` - Use it to get results about last vote

>`/delivery` - Use it to get list of delivery links

>`/rate` *number* - Use it to answer the rating votes 


## TODOs

 * Add Unit tests
 * Update local delivery list
 * ~~Add schedule of duty~~
 * Any new ideas are wellcome 
