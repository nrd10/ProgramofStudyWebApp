from shared import backends
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

import requests
import logging
import os
from shared.models import User as CustomUser
from shared.backends import PasswordlessAuthBackend
logger = logging.getLogger('shared/views.py')

# Create your views here.
def index(request):
    """
    View function for home page of site
    """
    return render(
        request,
        'index.html',
    )

def middle_request(request):
    """
    View function for getting access token
    from Duke OAuth Server
    """
    #Make request with token
    return render(request,'access_token.html')

def OIT_login(request):
    token = request.POST['token']
    url = "https://api.colab.duke.edu/identity/v1/"
    headers = {'Accept': 'application/json', 'x-api-key': 'grad-ops-ece'}
    headers['Authorization'] = 'Bearer ' + token
    res = requests.get(url, headers= headers)
    res_text = res.text
    # logger.error("Content is:")
    # logger.error(res_text)

    #Get Indices of "netid" and next key "lastName"
    netid_index = res_text.find("netid")
    lastname_index = res_text.find("lastName")
    # logger.error("Net ID index is:"+str(netid_index))
    # logger.error("Index of Last Name is:"+str(lastname_index))

    #Find ":" and "," between above two indices
    colon_index = res_text.find(":", netid_index, lastname_index)
    comma_index = res_text.find(",", netid_index, lastname_index)
    # logger.error("Colon index is:"+str(colon_index))
    # logger.error("Comma index is:"+str(comma_index))

    #Find starting quote and ending quote indices
    first_quote_index = res_text.find("\"", colon_index, comma_index-2)
    second_quote_index = res_text.find("\"", colon_index + 2, comma_index)
    # logger.error("First quote index is:"+str(first_quote_index))
    # logger.error("Second quote index is:"+str(second_quote_index))
    NETID = res_text[first_quote_index+1:second_quote_index]
    logger.error("Netid is:"+str(NETID))
    # myuser = CustomUser.objects.get(netid=NETID)
    # logger.error("Myuser is:"+str(myuser))
    # request.user = myuser

    user = authenticate(username=NETID)
    if user is not None:
        logger.error("WE AUTHENTICATED")
        login(request, user)


    return redirect('index')
