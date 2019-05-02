# -*- coding: utf-8 -*-
from twisted.web import server, resource

from twisted.internet import reactor

import random, datetime, dateutil, shelve

food_choice = shelve.open('food_history')
housekeeping= shelve.open('lunch_housekeeping')

try:
  # see if it's our first run
  first = housekeeping['first']
except KeyError:
  #  yep, so let's load up our values...
  housekeeping['first'] = False
  housekeeping['last'] = None
  food_choice['Street Meat'] = None
  food_choice['White Castle'] = None
  food_choice['Five Guys'] = None
  food_choice['Chopt'] = None
  food_choice['Chipotle'] = None
  food_choice['Potbellies'] = None
  food_choice['Kortaco'] = None
  food_choice['Lennies'] = None
  food_choice['Buffalo Chicken Pizza'] = None
  food_choice['Sophies'] = None
  food_choice['Big Al\'s Chicken Calzone'] = None
  food_choice['Ho Yip'] = None
  food_choice['Shake Shack'] = None
  food_choice['Muscle Maker Grill'] = None
  food_choice['Katz'] = None
  food_choice['Carls Philly Cheesesteak'] = None
  food_choice['Taiwanese Burgers'] = None
  food_choice['Pita Press'] = None
  food_choice['Toasties'] = None
  food_choice['Indian Street Meat Khati Rolls'] = None
  food_choice['Shinjuku'] = None
  
  
"""  
food_dict = {
  'Street Meat': None,
  'White Castle': None,
  'Five Guys': None,
  'Chopt': None,
  'Chipotle': None,
  'Potbellies': None,
  'Bon Chon': None,
  'Kortaco': None,
  'Lennies': None,
  'Buffalo Chicken Pizza': None,
  'Sophies': None,
  'Big Al\'s Chicken Calzone': None,
  'Ho Yip': None,
  'Shake Shack': None,
  'Muscle Maker Grill': None,
  'Katz': None,
  'Carls Philly Cheesesteak': None,
  'Planet Gyro': None,
  'Pita Press': None,
  'Toasties': None,
  }
"""

"""
  make_decision:
    rules:
      check to make sure there is at least one item without a last eaten date
	if not reset all and continue
	if = 1: we eat that and reset all
      else:
	randomly select one from the set of those without a prior eaten date
"""
def make_decision():
  eaten = []
  uneaten = []
  for k,v in food_choice.items():
    if k == 'first':
      continue
    if v is None:
      uneaten.append(k)
    else:
      eaten.append(k)
  if len(uneaten) == 0:
    # we've completed a cycle, reset all food choices
    for k in eaten:
      food_choice[k] = None
  elif len(uneaten) == 1:
    # only one left, so set that as return and recycle all
    decision = uneaten[0]
    for k in eaten:
      food_choice[k] = None
    return decision, datetime.datetime.now()
  else:
    now = datetime.datetime.now()
    decision = uneaten[random.randint(0,int(len(uneaten)-1))]
    food_choice[decision] = now
    return decision, now
  #decision = food_dict.keys()[random.randint(0,int(len(food_dict.keys())-1))]
  



out_template = '<html> \
		<head> \
		<title>SO HUNGRY JEFF</title> \
		</head> \
		<body> \
		<font style="font-size:20px"><b>Lo! At {when}, I decree you shall eat:</b></font><br/> \
		<font style="font-size:180px"><b>{decision}</b></font> \
		<p>Your prior hungers were satisfied with...<br/> \
		{previous} \
		</p> \
		</body> \
		</html>' 


def show_previous():
  prev = '<ol>'
  prev_items = ''
  for k,v in food_choice.items():
    if k == 'first':
      continue
    if v is not None:
      prev_items = prev_items + '<li>{key} was eaten on {date}</li>'.format(key=k,date='%s/%s/%s' % (v.month, v.day, v.year))
  prev = prev + prev_items + '</ol>'
  return prev

def sanity_check_date():
  now = datetime.datetime.now()
  then = housekeeping['last']
  if then is None:
    # first run... 
    return True
  if now.day == then.day and now.month == then.month and now.year == then.year:
    print 'Trying to replay for todays lunch... UNACCEPTABLE'
    return False
  else:
    return True
  

class FeedMeResource(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
	print request.URLPath()
        request.setHeader("content-type", "text/html")
        if sanity_check_date() == False:
	  out = 'I have already proclaimed todays meal! Let me slumber till tomorrow!' + show_previous()
	  return out
	decision, when = make_decision()
        previous = show_previous()
        housekeeping['last'] = when
        out =  out_template.format(when=when.isoformat(),decision=decision, previous=previous)
        return out #just_today()




reactor.listenTCP(8099, server.Site(FeedMeResource()))
reactor.run()

