from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from . import DatabaseControler as dbClass
from .ErrorReporting import ausError as ERR
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.forms import ImageField

############################################################################################
#####     Navigation Methods
############################################################################################

def MainPage(request):

    ##### Show the Store Items

    # Session Check
    if 'username' in request.session:
        # Session is there

        r = GetFullStoreInfo()

        if type(r) is ERR:
            return render(request, 'Error.html', context={"Error_Message": r.func_PrintError()})
        else:
            # Data are OK
            if len(r):
                return render(request, 'mainPage.html', context={"ItemsList": r})
            else:
                # Store is Empty
                return render(request, 'mainPage.html',  context={"ItemsList": ['NO ITEMS']})

    else:
        # NO SESSION go login page
        return redirect(to='/')


def home(request):

    #####  Show the login Page

    # Logout of the system ( OPENING THIS WILL CAUSE THE SITE TO STOP )
    if 'ID' in request.session:
        request.session.clear()

    # Loign Page Open
    #return render(request, 'dd.html')
    return render(request, 'index.html')

    #from django.http import HttpResponse
    #return HttpResponse("Hello, World!")
def addItems(request):

    #### Show Add Item Page

    # Session Check
    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2):
        return render(request, 'addItems.html')
    else:
        # NO SESSION go login page
        return redirect(to='/')

def editUsers(request):

    #### Show users list

    # Session Check
    if 'username' in request.session and request.session['Privlage'] == 1:

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return render(request, 'Error.html', context={"Error_Message": db.func_PrintError()})

        # Preper the SQL
        TheSQL = "SELECT * FROM users WHERE ID != " + str(request.session['ID'])

        # Send the SQL
        r = dbClass.func_SendSQL(db, TheSQL)
        dbClass.func_CloseConnection(db)

        # Check results
        if type(r) is ERR:
            return render(request, 'EditUsers.html', context={"lblResult": r.func_PrintError()})
        else:
            return render(request, 'EditUsers.html', context={"ItemsList": r})

    else:
        # NO SESSION go login page
        return redirect(to='/')

def about(request):

    #### Show About Page

    return render(request, 'About.html')

def editStore(request):

    #### Show Edit Items Page

    # Session Check

    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2):
        # get the store info
        r = GetFullStoreInfo()

        if type(r) is ERR:
            return render(request, 'Error.html', context={"Error_Message": r.func_PrintError()})
        elif len(r):
            return render(request, 'EditStore.html', context={"ItemsList": r})
        else:
            # Store is Empty
            return render(request, 'EditStore.html')
    else:
        # NO SESSION go login page
        return redirect(to='/')

############################################################################################
#####     WORKING FUNCIONT for POST requests
############################################################################################

def InsertNewItems(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: InsertNewItems/
    # HTML FILE: addItems.html

    # JOB: Insert a NEW item with picture to the database
    ###########################

    # Session Check
    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2):

        ImageData = (request.POST['imagePath'])

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return render(request, 'Error.html', context={"Error_Message": db.func_PrintError()})

        # Preper the SQL
        parameters = {"itemId": request.POST['itemId'], "itemname": request.POST['itemname'],
                      "shortname": request.POST['shortname'], "description": request.POST['description'],
                      "Quantity": request.POST['Quantity'], "orginalprice": request.POST['orginalprice'],
                      "sellingprice": request.POST['sellingprice'], "category": request.POST['category'],
                      "hight": request.POST['hight'], "width": request.POST['width'],
                      "length": request.POST['length'], "weight": request.POST['weight'],
                      "minplayer": request.POST['minplayer'], "maxplayer": request.POST['maxplayer'],
                      "playtime": request.POST['playtime'], "imagePath":ImageData }

        TheSQL = "INSERT INTO `items`(`itemId`, `itemname`, `shortname`, `description`, `Quantity`, `orginalprice`, " \
                 "`sellingprice`, `category`, `hight`, `width`, `length`, `weight`, `minplayer`, `maxplayer`, " \
                 "`playtime`, `image3`) VALUES (%(itemId)s, %(itemname)s, %(shortname)s, %(description)s, %(Quantity)s," \
                 " %(orginalprice)s, %(sellingprice)s, %(category)s," \
                 " %(hight)s, %(width)s, %(length)s, %(weight)s, %(minplayer)s, %(maxplayer)s, %(playtime)s, %(imagePath)s)"


        # Send the SQL
        r = dbClass.func_InsertSQL(db, TheSQL, parameters, returnID=True)

        dbClass.func_CloseConnection(db)



        # Check results
        if type(r) is ERR:
            return render(request, 'addItems.html', context={"lblResult": r.func_PrintError()})
        else:
            return render(request, 'addItems.html', context={"lblResult":"Item was added successfully! "})
    else:
        # NO SESSION go login page
        return redirect(to='/')

import base64

def upload(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: upload/
    # HTML FILE: uploadImage.html

    # JOB: Upload an image from the user desktop to the media folder of the serever
        # and return the file name connected to the media folder. This method is used as
        # part of other html file using {% include %}
    # NOW it works with edit store and add item to upload the user picture for the game

    ###########################
    try:
        if request.method == 'POST' and request.FILES['upload']  \
                and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2):
            # Push the file to the database

            file = request.FILES['upload']
            ImageData =  base64.b64encode( file.read() )

            c = dbClass.func_ConnectToDB()
            #if type(c) == ERR:
            #    return render(request, 'Error.html', context={"Error_Message": "Error loading the image. Please try again!"})
            #else:
            #    InsrtSQL = "INSERT INTO `itemsimage`(`theImage`) VALUES ( %(ImageData)s )"
            #    paramters = {'ImageData':ImageData}

            #    r = dbClass.func_InsertSQL(Conn=c, SQLStatment=InsrtSQL, parameters=paramters)
            #    if type(r) == ERR:
            #        print("Insertion of image feils", r.func_PrintError())
            #        return render(request, 'Error.html', context={"Error_Message": "Image can't be saved to the database!"})
            #    else:
            #        print("Image OK r=", r)

            if request.POST['TheSender'].__eq__("EDIT"):
                return render(request, 'EditStore.html', {'theImage':ImageData.decode('utf-8')})
            else:
                return render(request, 'addItems.html', {'theImage': ImageData.decode('utf-8')})

        return render(request, 'Error.html', context={"Error_Message": "Error loading the image. Please try again!"})

    except:
        return render(request, 'Error.html', context={"Error_Message": "Error loading the image. Please try again!"})

    # Orginal working code where the link to the file is saved
    #if request.method == 'POST' and request.FILES['upload']:
    #    upload = request.FILES['upload']
    #    fss = FileSystemStorage()
    #   file = fss.save(upload.name, upload)
    #    file_url = fss.url(file)
    #    if request.POST['TheSender'].__eq__("EDIT"):
    #        return render(request, 'EditStore.html', {'file_url': file_url})
    #    else:
    #        return render(request, 'addItems.html', {'file_url': file_url})
    #
    #return render(request, 'Error.html', context={"Error_Message": "Error loading the image. Please try again!"})

def GetFullStoreInfo():

    ###########################
    ## A FUNCION ###

    # Connected: show store / show store for edit

    # JOB: Get all store item from the database and return in a normal dict
    ###########################

    # Connect to database
    db = dbClass.func_ConnectToDB()
    if type(db) is ERR:
        return ERR

    r = dbClass.func_SendSQL(db, "SELECT * FROM items")
    dbClass.func_CloseConnection(db)

    if type(r) is ERR:
        return ERR
    else:
        result = []

        # SQL was OK -- decode the result to show the images
        for i in range(0, len(r)):
            result.append([])
            for u in range(0, len(r[i])):
                if u == 17 and r[i][17]:
                    result[i].append(r[i][u].decode('utf-8'))
                else:
                    result[i].append(r[i][u])

        return result

def updateAnItem(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: updateItem/
    # HTML FILE: editStore.html

    # JOB: Update the changes to an item when user click 'save' or 'delete' buttons  by
        # the user in the editStore.html file
    ###########################

    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2) :

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return ERR
        else:
            if request.POST['action'].__eq__("Save"):

                # Preper the SQL
                parameters = {"itemId": request.POST['itemId'], "itemname": request.POST['itemname'],
                              "shortname": request.POST['shortname'], "description": request.POST['description'],
                              "Quantity": request.POST['Quantity'], "orginalprice": request.POST['orginalprice'],
                              "sellingprice": request.POST['sellingprice'], "category": request.POST['category'],
                              "hight": request.POST['hight'], "width": request.POST['width'],
                              "length": request.POST['length'], "weight": request.POST['weight'],
                              "minplayer": request.POST['minplayer'], "maxplayer": request.POST['maxplayer'],
                              "playtime": request.POST['playtime'], "imagePath": request.POST['imagePath']}

                TheSQL = "UPDATE `items` SET `itemname`=%(itemname)s,`shortname`=%(shortname)s,`description`=%(description)s," \
                         "`Quantity`=%(Quantity)s,`orginalprice`=%(orginalprice)s, " \
                         "`sellingprice`=%(sellingprice)s,`hight`=%(hight)s,`width`=%(width)s,`length`=%(length)s, " \
                         "`weight`= %(weight)s,`minplayer`=%(minplayer)s,`maxplayer`=%(maxplayer)s," \
                         "`playtime`=%(playtime)s,`image1`=%(imagePath)s WHERE `itemId`=%(itemId)s "


            elif request.POST['action'].__eq__('Delete'):

                parameters = {"itemId": request.POST['itemId']}

                TheSQL = "DELETE FROM `items` WHERE `itemId`=%(itemId)s"


            r = dbClass.func_SendSQL(myDBin=db, SQLStatment=TheSQL, parameters=parameters, returnDate=False)

        dbClass.func_CloseConnection(db)

        if type(r) is ERR:
            request.session['FeedBackMsg'] = 'There was an error procssing the request. Please try again and make usre you enter the correct data.'
            return redirect(to='/editStore/')
        else:
            # SQL was OK
            request.session['FeedBackMsg'] = 'Update done succssfully!'
            return redirect(to='/editStore/')
    else:
        return render(request, 'Error.html', context={"Error_Message": "You do NOT have the Right to access this page. Please make sure you have the correct right or contact the website admin to grandt you the right."})

def updateUser(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: updateUser/
    # HTML FILE: editUsers.html

    # JOB: Update the status of the user by the admin when clicking 'Accept' or 'Promote'
        # buttons  by in the editUsers.html file
    ###########################

    if 'username' in request.session and request.session['Privlage'] == 1:

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return ERR
        else:
            if request.POST['action'].__eq__("Accept"):
                TheSQL = "UPDATE `users` SET `mainverification`=1 WHERE `ID`=%(userID)s"
                paratmer = {'userID': request.POST['userID']}
                dbClass.func_SendSQL(myDBin=db,SQLStatment=TheSQL, parameters=paratmer,returnDate=False)

            elif request.POST['action'].__eq__("Promote"):
                if int(request.POST['Privlage']) < 2:

                    paratmer = {'userID': request.POST['userID']}
                    TheSQL = "UPDATE `users` SET `PrivlageLevel`=`PrivlageLevel`+ 1 WHERE `ID`=%(userID)s"

                    u = dbClass.func_SendSQL(myDBin=db, SQLStatment=TheSQL, parameters=paratmer,returnDate=False)

                    if type(u)== ERR:
                        dbClass.func_CloseConnection(db)
                        return render(request, 'Error.html', context={"Error_Message": u.func_PrintError()})

            elif request.POST['action'].__eq__("DePromote"):
                if int(request.POST['Privlage']) > 0:

                    paratmer = {'userID': request.POST['userID']}
                    TheSQL = "UPDATE `users` SET `PrivlageLevel`=`PrivlageLevel`- 1 WHERE `ID`=%(userID)s"

                    u = dbClass.func_SendSQL(myDBin=db, SQLStatment=TheSQL, parameters=paratmer,returnDate=False)

                    if type(u)== ERR:
                        dbClass.func_CloseConnection(db)
                        return render(request, 'Error.html', context={"Error_Message": u.func_PrintError()})

            dbClass.func_CloseConnection(db)
            return redirect(to='/editUsers')
    else:
        # NO SESSION go login page
        return redirect(to='/')

##################

def setting(request):
    if 'username' in request.session and (request.session['Privlage'] == 1):
        return render(request, 'Settings.html')

def ResetDatabase(request):
    if 'username' in request.session and (request.session['Privlage'] == 1):
        if request.POST['deletepwd'].__eq__("AliBHP#2110"):

            r = dbClass.func_CreateDatabase()
            if type(r) == ERR:
                return render(request, 'Error.html', context={"Error_Message": "Something went wrong while doing that!"})
            else:
                return render(request, 'OK.html', context={"The_Message":"Restarting the database was done!"})
        else:
            return render(request, 'Error.html', context={"Error_Message": "Worng password. Only website creator knows the password!"})
