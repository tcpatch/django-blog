from django.shortcuts import render
from .models import Poop, Nap, Feed, Food
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import pytz
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import base64
import io 


# Create your views here.
@login_required
def index(request):
    eastern = pytz.timezone('US/Eastern')
    
    try:
        latest_poop = Poop.objects.all()[0]
    except IndexError:
        latest_poop = None
    try:
        latest_nap = Nap.objects.all()[0]
    except IndexError:
        latest_nap = None
    try:
        latest_feed = Feed.objects.all()[0]
    except IndexError:
        latest_feed = None
    try:
        latest_food = Food.objects.all()[0]
    except IndexError:
        latest_food = None
    
    if latest_poop and latest_poop.time:
        last_poop_time = latest_poop.time.astimezone(eastern).strftime('%m/%d %I:%M %p')
    else:
        last_poop_time = 'None'

    if latest_nap and latest_nap.endTime:
        last_nap_end_time = latest_nap.endTime.astimezone(eastern).strftime('%I:%M %p')
    else:
        last_nap_end_time = 'napping...'

    if latest_feed and latest_feed.time:
        last_feed_time = latest_feed.time.astimezone(eastern).strftime('%I:%M %p')
    else:
        last_feed_time = 'None'
    if latest_food:
        last_food =latest_food.food_name
    else:
        last_food = 'None'

    if not latest_nap:
        nap_mod = 'Start'
    elif latest_nap.endTime:
        nap_mod = 'Start'
    else:
        nap_mod = 'End'
    today = timezone.now().astimezone(eastern).strftime('%Y-%m-%d')
    display_day = today
    if request.method == 'POST':
        #TODO check if poop, nap, or feed pressed
        button_pressed = request.POST
        if 'poop' in request.POST:
            poop = Poop()
            poop.save()
            last_poop_time = poop.time.astimezone(eastern).strftime('%m/%d %I:%M %p')
        elif 'napStart' in request.POST:
            if nap_mod == 'Start':
                nap = Nap()
                nap.save()
                nap_mod = 'End'
                last_nap_end_time = 'napping...'
            else:
                latest_nap.endTime = timezone.now()
                latest_nap.save()
                nap_mod = 'Start'
                last_nap_end_time = latest_nap.endTime.astimezone(eastern).strftime('%I:%M %p')
        elif 'feed' in request.POST:
            feed = Feed()
            feed.save()
            last_feed_time = feed.time.astimezone(eastern).strftime('%I:%M %p')
        elif 'food' in request.POST and 'foodValue':
            food = Food()
            food.food_name = request.POST['foodValue']
            food.save()
            last_food = request.POST['foodValue'][0]
        display_day = request.POST['displayDay']

    try:
        poops = Poop.objects.all()
    except IndexError:
        poops = None
    try:
        naps = Nap.objects.all()
    except IndexError:
        naps = None
    try:
        feeds = Feed.objects.all()
    except IndexError:
        feeds = None
    try:
        foods = Food.objects.all()
    except IndexError:
        foods = None
    poops_list = [[i.time, 'poop'] for i in poops if i.time.strftime('%Y-%m-%d') == display_day]
    napstart_list = [[i.startTime, 'nap start'] for i in naps if i.startTime.strftime('%Y-%m-%d') == display_day]
    napend_list = [[i.endTime, 'nap end'] for i in naps if i.endTime and i.startTime.strftime('%Y-%m-%d') == display_day]
    feeds_list = [[i.time, 'feed'] for i in feeds if i.time.strftime('%Y-%m-%d') == display_day]
    food_list = [[i.time, i.food_name] for i in foods if i.time.strftime('%Y-%m-%d') == display_day]
    display_list = poops_list + napstart_list + napend_list + feeds_list + food_list
    display_list.sort()
    l = [[i[0].astimezone(eastern).strftime('%I:%M %p'), i[1]] for i in display_list]

    return render(request, 'tracking/index.html', {'napMod': nap_mod,
                                                   'lastPoop': last_poop_time,
                                                   'lastNap': last_nap_end_time,
                                                   'lastFeed': last_feed_time,
                                                   'lastFood': last_food,
                                                   'displayList': l,
                                                   'today': display_day})


def time_to_decimal(t):
    a, b = t.split(':')
    a = float(a)
    b = float(b) / 60.0
    return a + b


def graph(request):
    try:
        poops = Poop.objects.all()
    except IndexError:
        poops = None
    try:
        naps = Nap.objects.all()
    except IndexError:
        naps = None
    try:
        feeds = Feed.objects.all()
    except IndexError:
        feeds = None
    try:
        foods = Food.objects.all()
    except IndexError:
        foods = None

    poops_list = [[i.time.strftime('%Y-%m-%d'), i.time.strftime('%H:%M'), 'poop'] for i in poops]
    nap_list = list()
    for i in naps:
        if i.endTime:
            nap_list.append([i.startTime.strftime('%Y-%m-%d'), i.startTime.strftime('%H:%M'), i.endTime.strftime('%H:%M'), 'nap start'])
        else:
            nap_list.append([i.startTime.strftime('%Y-%m-%d'), i.startTime.strftime('%H:%M'), None, 'nap start'])
    feeds_list = [[i.time.strftime('%Y-%m-%d'), i.time.strftime('%H:%M'), 'feed'] for i in feeds]
    food_list = [[i.time.strftime('%Y-%m-%d'), i.time.strftime('%H:%M'), i.food_name] for i in foods]

    all_days = list()
    for l in [poops_list, nap_list, feeds_list, food_list]:
        for i in l:
            all_days.append(i[0])
    all_days = list(set(all_days))
    all_days.sort()

    color_dict = {0: 'brown', 1:'green', 2:'grey', 3:'orange'}
    for c, l in enumerate([poops_list, nap_list, feeds_list, food_list]):
        added = False
        for y, day in enumerate(all_days):
            if c == 1:
                for i in l:
                    if i[0] == day:
                        try:
                            x1 = time_to_decimal(i[1])
                            x2 = time_to_decimal(i[2])
                            plt.plot([x1, x2], [y, y], c=color_dict[c])
                        except:
                            x = time_to_decimal(i[1])
                            plt.scatter(x, y, c=color_dict[c])
            else:
                for i in l:
                    if i[0] == day:
                        x = time_to_decimal(i[1])
                        plt.scatter(x, y, c=color_dict[c])
    
    plt.yticks(range(0, len(all_days)), all_days)
    plt.xlim(-0.5, 24.5)
    plt.xticks(range(0, 24), ['12am', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', 
                              '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm'],
               rotation='45')
    poop_patch = mpatches.Patch(color='brown', label='poop')
    nap_patch = mpatches.Patch(color='green', label='nap')
    feed_patch = mpatches.Patch(color='grey', label='feed')
    food_patch = mpatches.Patch(color='orange', label='food')
    plt.legend(handles=[poop_patch, nap_patch, feed_patch, food_patch])
    plt.tight_layout()
    pic_IObytes = io.BytesIO()
    plt.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    image_string = str(pic_hash).replace("b'", '').replace("'", '')

    return render(request, 'tracking/graph.html', {'imageString': image_string})
